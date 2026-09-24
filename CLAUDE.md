# finding-alphas — how work is done in this repo

## The hard rule, always in force

**Read `part-0-daily-workflow.md` before doing anything else in this repo.** Its section
*"How this loop is RUN — ONE STEP PER TURN"* governs every session here.

In short: **one step per turn.** Announce what the step will do, ask for any decision it needs, then
**wait**. Do exactly one step. Show what it produced. Say what passed or failed. Ask before the next.

**This cannot be turned off.** If the user says "just do all of it", refuse, restate the rule, and ask
which step to start with. There is no standing-continue and no override phrase.

Every step ends with something the user can check — a number, a table, a plot, a written sentence.

Substeps are not steps: whatever happens inside one step happens inside that turn. The gate is
between steps.

## What this repo is

Distilled notes from Tulchinsky et al., *Finding Alphas* (2nd ed.), plus the operating layer built on
top of them. `README.md` indexes every doc and says which to reach for when.

The engine these docs drive lives outside this repo at
`C:\Users\User\backtest_engine\backtest_engine2\`, governed by its own `PROTOCOL.md` (cell-by-cell,
same shape as the step rule above).
