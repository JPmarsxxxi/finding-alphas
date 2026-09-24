"""Index a corpus PDF into grepable per-section text + an INDEX.md.

Usage:
    python index_corpus.py <pdf> [--level N] [--min-pages N] [--title "..."]

Splits on the PDF's embedded bookmarks at the given outline level (default: the
shallowest level present), writes one .txt per section into a folder named after
the PDF, and an INDEX.md listing section / pages / file.

Drop a new PDF beside its siblings and run this — nothing else needs redoing.
"""
import sys, os, re, io, argparse
import fitz


def slug(s, n=52):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:n] or "section"


def index(pdf, level=None, min_pages=1, title=None):
    d = fitz.open(pdf)
    toc = d.get_toc()
    if not toc:
        raise SystemExit(f"{os.path.basename(pdf)}: no embedded bookmarks — needs a manual page map")

    if level is None:
        level = min(l for l, _, _ in toc)
    BOILER = ("cover", "title page", "copyright", "contents", "front matter", "half title")
    marks = [(l, t.strip(), p) for l, t, p in toc if l == level and p > 0]
    marks = [m for m in marks if m[1].lower().strip(" .0123456789") not in BOILER]

    # several bookmarks can share a start page — collapse them into one section
    by_page = {}
    for l, t, p in sorted(marks, key=lambda m: m[2]):
        by_page.setdefault(p, []).append(t)
    merged = [(" / ".join(ts), p) for p, ts in sorted(by_page.items())]

    # end page = start of the next mark at this level or shallower
    starts = sorted({p for l, _, p in toc if l <= level and p > 0})
    secs = []
    for t, p in merged:
        nxt = next((s for s in starts if s > p), d.page_count + 1)
        if nxt - p >= min_pages:
            secs.append((t, p, nxt - 1))

    out = os.path.join(os.path.dirname(pdf), slug(os.path.splitext(os.path.basename(pdf))[0], 60))
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".txt"):
            os.remove(os.path.join(out, f))

    rows = []
    for i, (t, a, b) in enumerate(secs, 1):
        txt = "\n".join(d[p].get_text() for p in range(a - 1, b))
        fn = "%02d_%s.txt" % (i, slug(t))
        io.open(os.path.join(out, fn), "w", encoding="utf-8").write(txt)
        rows.append((i, t, a, b, fn, len(txt)))

    name = title or os.path.basename(pdf)
    L = [f"# {name}", "",
         f"Corpus index. {d.page_count}pp, {len(rows)} sections at outline level {level}.",
         "**Grep this index, then open ONLY the section you need.** Page numbers are PDF pages.",
         "", "| # | section | pages | file |", "|---:|---|---|---|"]
    for i, t, a, b, fn, n in rows:
        L.append(f"| {i} | {t} | {a}–{b} | `{fn}` |")
    io.open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    return out, rows, d.page_count


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--level", type=int, default=None)
    ap.add_argument("--min-pages", type=int, default=1)
    ap.add_argument("--title", default=None)
    a = ap.parse_args()
    out, rows, pages = index(a.pdf, a.level, a.min_pages, a.title)
    print(f"{os.path.basename(a.pdf)}: {pages}pp -> {len(rows)} sections in {os.path.basename(out)}/")
    for i, t, s, e, fn, n in rows:
        safe = t[:58].encode(sys.stdout.encoding or "ascii", "replace").decode(sys.stdout.encoding or "ascii")
        print("  %2d p%-4d-%-4d %-58s %8d chars" % (i, s, e, safe, n))
