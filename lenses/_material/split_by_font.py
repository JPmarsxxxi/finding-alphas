"""Split a PDF into sections using TYPOGRAPHY rather than text patterns.

For books whose contents page cannot be matched to the body. A chapter opener is
identified by a span set noticeably larger than the book's body font, appearing near the
top of a page. This works where regex fails because it reads how the book was typeset
instead of guessing at its wording.

Usage:
    python split_by_font.py <pdf> [--title "..."] [--ratio 1.35] [--top 0.45] [--dry]

Prints the body-font estimate and every candidate so the split can be judged before it is
written. Same quality gate as split_corpus.py: reject rather than ship a bad split.
"""
import os, re, io, sys, argparse, collections
import fitz


def body_size(doc, sample=60):
    """Modal font size across a sample of pages = the body text size."""
    c = collections.Counter()
    step = max(1, doc.page_count // sample)
    for i in range(0, doc.page_count, step):
        for b in doc[i].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    t = s["text"].strip()
                    if len(t) > 20:                      # only prose lines vote
                        c[round(s["size"], 1)] += len(t)
    return c.most_common(1)[0][0] if c else 10.0


def candidates(doc, base, ratio, top):
    """(page, text, size) for large spans sitting in the upper part of a page."""
    out = []
    for i in range(doc.page_count):
        page = doc[i]
        H = page.rect.height
        best = None
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    t = " ".join(s["text"].split())
                    if not (2 < len(t) < 90):
                        continue
                    if s["size"] < base * ratio:
                        continue
                    if s["bbox"][1] > H * top:           # must sit near the top
                        continue
                    if best is None or s["size"] > best[2]:
                        best = (i, t, s["size"])
        if best:
            out.append(best)
    return out


def run(path, title=None, ratio=1.35, top=0.45, min_chars=3000, dry=False):
    doc = fitz.open(path)
    base = body_size(doc)
    cands = candidates(doc, base, ratio, top)
    print("%s: %d pages | body font %.1f | %d candidate openers"
          % (os.path.basename(path), doc.page_count, base, len(cands)))

    pages = [doc[i].get_text() for i in range(doc.page_count)]
    total = sum(len(p) for p in pages)

    # Some books set chapter titles in a decorative font whose glyphs do not extract as
    # readable text (they come back as replacement chars). The page boundary is still
    # correct, so keep it and take the title from the first legible line instead.
    def legible(s):
        letters = sum(ch.isalpha() and ord(ch) < 128 for ch in s)
        return len(s) > 3 and letters >= 0.6 * len(s.replace(' ', ''))

    fixed = []
    for i, t, sz in cands:
        if not legible(t):
            for ln in [x.strip() for x in pages[i].split('\n') if x.strip()]:
                if legible(ln) and 3 < len(ln) < 80:
                    t = " ".join(ln.split())
                    break
        fixed.append((i, t, sz))
    cands = fixed
    secs = []
    for n, (i, t, sz) in enumerate(cands):
        end = cands[n + 1][0] if n + 1 < len(cands) else doc.page_count
        body = "\n".join(pages[i:end])
        if len(body) >= min_chars:
            secs.append((t, sz, i + 1, end, body))
    if not secs:
        print("  ** no sections above %d chars -> NO-SECTION-INDEX **" % min_chars)
        return None

    cover = sum(len(s[4]) for s in secs) / total
    biggest = max(secs, key=lambda s: len(s[4]))
    big = len(biggest[4]) / total
    starts = [s[2] for s in secs]
    mono = all(b > a for a, b in zip(starts, starts[1:]))
    print("  kept %d | coverage %.0f%% | largest %s (%.0f%%) | monotonic %s"
          % (len(secs), cover * 100, biggest[0][:40], big * 100, mono))

    fails = []
    if len(secs) < 5:  fails.append("only %d sections" % len(secs))
    if big > 0.25:     fails.append("largest is %.0f%% of book" % (big * 100))
    if cover < 0.60:   fails.append("coverage %.0f%%" % (cover * 100))
    if not mono:       fails.append("not monotonic")
    if fails:
        print("  ** REJECTED: %s **" % "; ".join(fails))
        return None

    if dry:
        for t, sz, a, b, body in secs:
            safe = t[:56].encode(sys.stdout.encoding or 'ascii', 'replace').decode(sys.stdout.encoding or 'ascii')
            print("     p%-4d-%-4d %4.1fpt %-56s %7d" % (a, b, sz, safe, len(body)))
        return secs

    out = os.path.join(os.path.dirname(path),
                       re.sub(r'[^a-z0-9]+', '_', os.path.splitext(os.path.basename(path))[0].lower())[:60])
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith('.txt'):
            os.remove(os.path.join(out, f))
    rows = []
    for n, (t, sz, a, b, body) in enumerate(secs, 1):
        fn = "%02d_%s.txt" % (n, re.sub(r'[^a-z0-9]+', '_', t.lower()).strip('_')[:46] or 'section')
        io.open(os.path.join(out, fn), 'w', encoding='utf-8').write(body)
        rows.append((n, t, a, b, fn))
    L = ["# %s" % (title or os.path.basename(path)), "",
         "Corpus index. %d pages, %d sections, detected by **typography** — spans at least %.0f%% larger"
         " than the %.1fpt body font, in the top %.0f%% of a page. The contents page could not be matched"
         " to the body." % (doc.page_count, len(rows), (ratio - 1) * 100, base, top * 100),
         "", "**Grep this index, then open ONLY the section you need.**", "",
         "| # | section | pages | file |", "|---:|---|---|---|"]
    for n, t, a, b, fn in rows:
        L.append("| %d | %s | %d-%d | `%s` |" % (n, t, a, b, fn))
    io.open(os.path.join(out, 'INDEX.md'), 'w', encoding='utf-8').write("\n".join(L) + "\n")
    for n, t, a, b, fn in rows:
        safe = t[:56].encode(sys.stdout.encoding or 'ascii', 'replace').decode(sys.stdout.encoding or 'ascii')
        print("   %2d p%-4d-%-4d %s" % (n, a, b, safe))
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--title', default=None)
    ap.add_argument('--ratio', type=float, default=1.35)
    ap.add_argument('--top', type=float, default=0.45)
    ap.add_argument('--min-chars', type=int, default=3000)
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    run(a.pdf, a.title, a.ratio, a.top, a.min_chars, a.dry)
