# Ops runbook — how we schedule live strategies

How the live FTMO forward tests are kept running on the Windows box. Written 2026-07-04 after the
daemon approach died three times. **The scripts live in `C:\Users\User\backtest_engine\backtest_engine2`,
not here** — this doc is just the method so we can repeat it for the next strategy.

## The principle: schedule, don't daemonize

A strategy that only *acts* at a few fixed times a day (enter/exit) does **not** need a 24/7 process.
A long-lived `while True: step(); sleep()` daemon is 23.9 hours of idle looping whose only job is to
expose you to crashes, sleep, and reboots. We learned this the hard way:

> The old model was a persistent daemon started **once, by an "At log on" scheduled task**. Any crash,
> reboot, or the PC going to **sleep** (`WakeToRun=False`) killed it, and nothing ever restarted it —
> it just went silently dead until the next interactive logon. Died ~3×; the overnight strat (acts
> 18:00 & 09:30 NY = middle of the night) was hit worst because the PC slept under it.

**Inversion that fixed it:** let Windows Task Scheduler own liveness. Run the strategy's existing
`step()` as a **one-shot "tick", fired every minute**. A crashed/missed tick just means next minute
reruns. No process to babysit.

## The moving parts

| File (`backtest_engine2`) | Role |
|---|---|
| `fx_seasonal_live.py`, `fx_seasonal_live_v2.py`, `overnight_live.py` | The strategies. Their tested `step()` / `resolve()` / helpers are reused **unchanged**. |
| `strat_tick.py` | Generic one-shot runner. Imports a strategy module, loads cross-call state from `data/<module>_tick_state.json`, connects to MT5, runs `step()` **once**, saves state, exits. |
| `setup_live_tasks.ps1` | Registers the 3 scheduled tasks. Non-elevated, re-runnable (unregisters + recreates). |

State (which session is open, entry fills) that used to live in the daemon's memory is persisted to a
tiny JSON sidecar per strat, so it survives between one-minute invocations.

## The exact task settings (why each matters)

Set in `setup_live_tasks.ps1` via `New-ScheduledTaskSettingsSet` / triggers:

- **Trigger: 1-minute repetition, 10-yr duration** — fires forever, *not* logon-only (the original bug).
- **Trigger: AtLogOn** — re-arms immediately after a reboot / re-login.
- **`-WakeToRun`** — wakes the box for the tick (belt-and-suspenders vs sleep).
- **`powercfg /change standby-timeout-ac 0`** — the real sleep fix: the box never sleeps on AC.
- **`-StartWhenAvailable`** — catches up a missed run.
- **`-MultipleInstances IgnoreNew`** — a slow tick (v2 polls spread up to 90s) never stacks.
- **`-ExecutionTimeLimit 4min`** — kills a hung tick so it can't block the next.
- **`-RestartCount 3 -RestartInterval 1min`** — retries a failed launch.
- **Principal: `LogonType Interactive`, `RunLevel Limited`** — runs in *your* session (MT5's GUI
  terminal is only reachable from the interactive session; a "run whether logged on or not" task
  runs in session 0 and **can't** attach to MT5).

## No console flashing — use `pythonw.exe`

The task calls **`C:\ProgramData\anaconda3\pythonw.exe`** (the *windowless* Python), **not** `python.exe`
and **not** a `.bat`. Either of those pops a terminal window every minute. Because pythonw has no
console, `strat_tick.py` redirects its own stdout/stderr to `data/<module>_tick.out` (otherwise the
strategy's `print()`s crash on a `None` stdout).

## Deploy / redeploy / reset

```powershell
# (re)register all 3 tasks — safe to re-run anytime
powershell -ExecutionPolicy Bypass -File setup_live_tasks.ps1

# reset one strat's memory (forget open position / today's state)
del data\fx_seasonal_live_tick_state.json
```

## Add a NEW strategy

0. ⚠️ **Check hedging vs netting mode before writing the exit logic — see Gotchas, 2026-09-08.** On a
   hedging account, closing a position needs `position=<ticket>` on the order; a bare opposite-side
   order opens a second position instead of closing the first. Got this wrong once already.
1. Write it in the same shape as the others: module-level helpers + a `step(...)` + a `resolve()`.
2. Give it its **own MAGIC number** and own log/state paths (never share MAGIC — books collide).
3. Add a `run_<name>` variant to `strat_tick.py` if the `step()` signature differs (FX takes
   `(syms, state, openpos)`; overnight takes `(sym, st)`).
4. Add a row to the `$tasks` array in `setup_live_tasks.ps1` and re-run it.

## Health check ("is it alive?")

Read the status file — timestamp must be **< ~1 min old**; a fresh PID each tick is normal, not a
restart-loop:

```
data\overnight_status.txt        (#023 v1,  magic 160162)
data\overnight_v2_status.txt     (#023 v2,  magic 160164)
data\crypto_squeeze_status.txt   (#045 rule, magic 160165)   <- added 2026-09-02
```
The FX books (`daemon_status*.txt`, magics 160160/61) are DEAD — #016 v1/v2/v3 all unregistered by
2026-08-13. Their status files are stale by design; ignore them.

**`crypto_squeeze_status.txt` carries a `KILL=` line** if the pre-committed tripwire is breached
(kill lines live in `crypto_squeeze_live.py`'s docstring). Its absence is the all-clear.

### Watch for the silent death (learned the hard way, 2026-09-02)
An expired demo account does **not** stop the ticks — Task Scheduler keeps firing, the strategy keeps
writing `state=disconnected`, and nothing tells you. **#023 ran blind for 8 days** (2026-08-31 →
09-02) before anyone looked; MT5's own log showed `'1514206624': authorization on FTMO-Demo failed
(Invalid account)`. FTMO free-trial demos expire every ~2–3 weeks, so this recurs by design.
**Check `state=` in the status files, not just their timestamps** — a fresh timestamp with
`state=disconnected` looks alive and is not.

`data\<module>_tick.out` is **empty outside trade windows by design** (step() only prints on
enter/exit/skip). Round-trips land in `data\*_live_log*.parquet`; compare with `fx_seasonal_compare.py`.

## Gotchas

- **Check the account's margin mode (hedging vs netting) BEFORE writing exit logic — learned the
  hard way, 2026-09-08.** This account runs in **hedging** mode: sending an opposite-direction order
  with no position ticket does NOT close anything, it opens a second, independent position. `#045
  crypto_squeeze` was written assuming netting ("to exit, send the opposite side") and its very first
  live trade hit this exactly — the 12h exit sent a bare SELL, which opened a new short next to the
  still-open long instead of closing it. The code then believed itself flat while MT5 held both, and
  retried the same broken exit every minute for **3 days** (3,158 `not enough money` failures in
  `crypto_squeeze_live_tick.out`) as free margin got eaten down. Both stray positions closed by hand
  2026-09-08; the real trade, reconstructed from MT5's own fill prices (not the 0.00 the bug logged),
  was **-24.8 bp net** — the entry itself was fine, only the exit mechanism was broken.
  **The fix, now in `crypto_squeeze_live.py`'s `_order()`:** pass `position=<ticket>` on every closing
  order — MT5 requires it to know WHICH position to close on a hedging account. `mt5.positions_get()`
  tells you the mode implicitly (multiple entries per symbol/magic = hedging); check it once, in the
  platform settings or by watching for a stray duplicate, before the first live trade, not after.
  **Same root cause explains why `entry_fill`/`exit_fill` logged 0.00**, a separate but related bug:
  `order_send()`'s own `result.price` isn't reliably populated by this broker — read the real fill
  from `mt5.history_deals_get(ticket=r.deal)` instead, which is what `_fill_price()` now does.
- **Deleting old elevated tasks needs admin.** The original daemon tasks were registered elevated, so
  a non-elevated shell gets "Access denied". Delete them once from an **admin** cmd/PowerShell:
  `schtasks /delete /tn FX_Seasonal_016 /f` (+ `_v2`, + `US500_Overnight_023`). *(Done 2026-07-04.)*
- **The box must stay logged in with the MT5 terminal running** — that's the one liveness dependency
  this design can't remove, because the MT5 Python API attaches to the GUI terminal in your session.
- **Bulletproof upgrade:** if PC sleep/reboot ever recurs, move the *same* tick design to a cheap
  always-on Windows VPS. The PC being a personal daily-driver is the only remaining weak point.
