"""Split an unbookmarked source into grepable per-section text + an INDEX.md.

For sources `index_corpus.py` cannot handle because the PDF has no embedded outline,
or because the text came from an .odg (LibreOffice Draw) export.

Usage:
    python split_corpus.py <file.odg|file.pdf> [--title "..."] [--min-chars N] [--dry]

Method, in order:
  1. .odg  -> text is extracted PER PAGE from the draw:page elements of content.xml,
              which restores real page numbers. Then headings are detected per page.
  2. .pdf  -> text per page from fitz, headings detected per page.
  Headings are matched against a set of chapter patterns (Chapter N, CHAPTER N, "N. Title",
  "PART N", roman numerals). A page qualifies only if the heading sits in the first few
  lines of the page, which is where chapter openers live.

Verification is printed and must be read: chapter count, monotonicity, and the largest
section. If detection fails, nothing is written and the caller should mark the source
NO-SECTION-INDEX rather than invent divisions.
"""
import os, re, io, sys, zipfile, argparse

HEAD_PATTERNS = [
    re.compile(r'^\s*CHAPTER\s+([0-9]{1,2}|[IVXL]{1,6})\b[.:\s]*(.{0,80})$', re.I),
    re.compile(r'^\s*(?:PART|SECTION)\s+([0-9]{1,2}|[IVXL]{1,6})\b[.:\s]*(.{0,80})$', re.I),
    re.compile(r'^\s*([0-9]{1,2})\.\s+([A-Z][A-Za-z0-9 ,:&\'\-/()]{4,80})\s*$'),
]
BOILER = re.compile(r'contents|copyright|index|bibliograph|acknowledg|about the author|disclosure',
                    re.I)


def odg_pages(path):
    """Text per book page, from the draw:page elements of an .odg."""
    z = zipfile.ZipFile(path)
    c = z.read('content.xml').decode('utf-8', 'replace')
    raw = re.split(r'<draw:page\b', c)[1:]
    pages = []
    for blk in raw:
        blk = blk[blk.find('>') + 1:] if '>' in blk[:400] else blk  # drop the element's own attributes
        blk = re.sub(r'</text:p>', '\n', blk)
        t = re.sub(r'<[^>]+>', '', blk)
        for a, b in (('&apos;', "'"), ('&quot;', '"'), ('&amp;', '&'),
                     ('&lt;', '<'), ('&gt;', '>'), ('&#10;', '\n')):
            t = t.replace(a, b)
        pages.append(re.sub(r'\n{3,}', '\n\n', t).strip())
    return pages


def pdf_pages(path):
    import fitz
    d = fitz.open(path)
    return [d[i].get_text() for i in range(d.page_count)]


TOC_ENTRY = re.compile(
    # an optional list number wraps the entry in some exports: "2. Chapter 3 Labeling"
    r'^\s*(?:[0-9]{1,2}\.\s*)?'
    r'((?:Chapter|Part|Appendix|Section)\s+(?:[0-9]{1,2}|[IVXL]{1,6}|[A-E])\b)\s*[-–—:.]?\s*(.{0,80})$',
    re.I)


def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def find_headings_via_toc(pages, scan=40, look=8):
    """Read the printed contents, then locate each entry's first appearance in the body.

    Far more reliable than pattern-matching the body directly: the contents page tells you
    exactly how many chapters there are and what they are called, so a missed or spurious
    match is visible instead of silent.
    """
    # 1. contents pages = early pages carrying several chapter-like entries
    toc_pages, entries = [], []
    for i in range(min(scan, len(pages))):
        lines = [l.strip() for l in pages[i].split('\n') if l.strip()]
        hits = [l for l in lines if TOC_ENTRY.match(l)]
        if len(hits) >= 3:
            toc_pages.append(i)
            entries.extend(hits)
    if not entries:
        return [], 0
    body_start = max(toc_pages) + 1

    # 2. dedupe, preserving order
    seen, ordered = set(), []
    for e in entries:
        k = norm(e)
        if k and k not in seen:
            seen.add(k)
            ordered.append(e)

    # 3. locate each in the body
    found = []
    cursor = body_start
    for e in ordered:
        m = TOC_ENTRY.match(e)
        key = norm(e)                       # "chapter 8 equity risk premium"
        label = norm(m.group(1))            # "chapter 8"
        title = norm(m.group(2))            # "equity risk premium"
        num = re.search(r'(\d+|[ivxl]+|[a-e])$', label)
        num = num.group(1) if num else ''
        for i in range(cursor, len(pages)):
            lines = [l.strip() for l in pages[i].split('\n') if l.strip()][:look]
            head = norm(" ".join(lines))
            ok = (key and key in head)
            # many books open a chapter with the number alone on one line and the title on
            # the next ("1" / "Introduction"), so the TOC string never appears verbatim
            if not ok and title and len(title) > 6 and title in head:
                first = norm(lines[0]) if lines else ''
                ok = (first == num) or head.startswith(title) or (num and head.startswith(num))
            if not ok and label and head.startswith(label):
                ok = True
            if ok:
                found.append((i, re.sub(r'\s+', ' ', e)[:90]))
                cursor = i + 1
                break
    return found, len(ordered)


def find_headings(pages, look=6):
    """(page_index, title) for pages whose opening lines look like a chapter opener."""
    hits = []
    for i, txt in enumerate(pages):
        lines = [l.strip() for l in txt.split('\n') if l.strip()][:look]
        for ln in lines:
            if len(ln) > 95:
                continue
            for pat in HEAD_PATTERNS:
                m = pat.match(ln)
                if not m:
                    continue
                tail = (m.group(2) or '').strip(' .:-')
                title = ln.strip() if tail else ln.strip()
                if BOILER.search(title):
                    break
                hits.append((i, re.sub(r'\s+', ' ', title)[:90]))
                break
            else:
                continue
            break
    # drop repeats of the same title (running headers)
    seen, out = {}, []
    for i, t in hits:
        k = t.lower()
        if k in seen and i - seen[k] < 3:
            continue
        seen[k] = i
        out.append((i, t))
    return out


def split(path, title=None, min_chars=1500, dry=False):
    ext = os.path.splitext(path)[1].lower()
    pages = odg_pages(path) if ext == '.odg' else pdf_pages(path)
    total = sum(len(p) for p in pages)

    hits, n_toc = find_headings_via_toc(pages)
    print("  method: contents page (%d entries, %d located)" % (n_toc, len(hits)))
    if len(hits) < 5:
        # The body-scan fallback was tried and removed: it matches numbered prose
        # ("4. Using the optimized code, what is the...") and produces a split that LOOKS
        # structured but is not, which is worse than none. Contents page or nothing.
        print("  ** NO USABLE CONTENTS PAGE -> mark NO-SECTION-INDEX **")
        return None

    # a heading that yields a tiny section is a false positive (running header, TOC line)
    secs = []
    for n, (i, t) in enumerate(hits):
        end = hits[n + 1][0] if n + 1 < len(hits) else len(pages)
        body = "\n".join(pages[i:end])
        if len(body) >= min_chars:
            secs.append((t, i + 1, end, body))

    print("%s: %d pages, %d chars" % (os.path.basename(path), len(pages), total))
    print("  headings matched: %d   sections kept (>=%d chars): %d"
          % (len(hits), min_chars, len(secs)))
    if not secs:
        print("  ** DETECTION FAILED — write nothing, mark NO-SECTION-INDEX **")
        return None
    starts = [s[1] for s in secs]
    mono = all(b > a for a, b in zip(starts, starts[1:]))
    biggest = max(secs, key=lambda s: len(s[3]))
    cover = sum(len(s[3]) for s in secs) / total
    big = len(biggest[3]) / total
    print("  monotonic: %s | coverage: %.0f%% | largest: %s (%d chars, %.0f%% of book)"
          % (mono, cover * 100, biggest[0][:44], len(biggest[3]), 100 * big))

    # quality gate — a split that leaves a third of the book in one section has not
    # found the chapters, it has found three arbitrary cuts. Reject rather than ship.
    fails = []
    if len(secs) < 5:   fails.append("only %d sections" % len(secs))
    if big > 0.25:      fails.append("largest section is %.0f%% of the book" % (big * 100))
    if cover < 0.60:    fails.append("coverage only %.0f%%" % (cover * 100))
    if not mono:        fails.append("section starts not monotonic")
    if fails:
        print("  ** REJECTED: %s -> mark NO-SECTION-INDEX **" % "; ".join(fails))
        return None

    if dry:
        for t, a, b, body in secs:
            print("     p%-4d-%-4d %-62s %8d" % (a, b, t[:62], len(body)))
        return secs

    out = os.path.join(os.path.dirname(path),
                       re.sub(r'[^a-z0-9]+', '_', os.path.splitext(os.path.basename(path))[0].lower())[:60])
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith('.txt'):
            os.remove(os.path.join(out, f))
    rows = []
    for n, (t, a, b, body) in enumerate(secs, 1):
        fn = "%02d_%s.txt" % (n, re.sub(r'[^a-z0-9]+', '_', t.lower()).strip('_')[:48] or 'section')
        io.open(os.path.join(out, fn), 'w', encoding='utf-8').write(body)
        rows.append((n, t, a, b, fn, len(body)))
    name = title or os.path.basename(path)
    L = ["# %s" % name, "",
         "Corpus index. %d pages, %d sections, detected from chapter headings"
         " (no embedded outline in the source)." % (len(pages), len(rows)),
         "**Grep this index, then open ONLY the section you need.**", "",
         "| # | section | pages | file |", "|---:|---|---|---|"]
    for n, t, a, b, fn, ln in rows:
        L.append("| %d | %s | %d-%d | `%s` |" % (n, t, a, b, fn))
    io.open(os.path.join(out, 'INDEX.md'), 'w', encoding='utf-8').write("\n".join(L) + "\n")
    for n, t, a, b, fn, ln in rows:
        safe = t[:60].encode(sys.stdout.encoding or 'ascii', 'replace').decode(sys.stdout.encoding or 'ascii')
        print("   %2d p%-4d-%-4d %-60s %8d" % (n, a, b, safe, ln))
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('path')
    ap.add_argument('--title', default=None)
    ap.add_argument('--min-chars', type=int, default=1500)
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    split(a.path, a.title, a.min_chars, a.dry)
