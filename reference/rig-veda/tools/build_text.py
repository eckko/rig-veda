#!/usr/bin/env python3
"""Write text/ files, headers.md and issues.json from parse_dharmicdata output.

Usage: build_text.py PARSED_JSON BOOK_DIR
IDs: PPP.CCC.V[a-z]; part = mandala, chapter = sukta (3-digit widths).
Verse number V is the source's marker when a sukta's markers run 1..n;
otherwise V is the verse's position (1..n) and the source markers are
logged as a 'numbering' issue. Nothing is corrected.
"""
import json, re, sys, unicodedata
from pathlib import Path

ACCENT = re.compile('[॒॑᳐-᳿]')
LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def verse_lines(sid, number, lines):
    if len(lines) == 1:
        return [f'{sid}.{number} | {lines[0]}']
    return [f'{sid}.{number}{LETTERS[i]} | {l}' for i, l in enumerate(lines)]


def build_sukta(s):
    """Return (lines, issues) for one sukta."""
    m, c = s['mandala'], s['sukta']
    sid = f'{m:03d}.{c:03d}'
    issues = []
    verses = [dict(v) for v in s['verses']]
    # leftover text after the last marker
    for t in s['tail']:
        txt = t.strip()
        if ACCENT.search(txt):
            if not txt.endswith('॥'):
                txt += ' ॥'
            if verses and verses[-1].get('_open'):
                pass
            verses.append({'marker': None, 'extra': None, 'lines': [txt]})
            issues.append((sid, 'numbering', 'text after the last verse '
                           'marker kept as an unnumbered final verse'))
        elif 'समाप्त' in txt:
            issues.append((sid, 'other', f'colophon not in text: {txt}'))
        elif re.search(r'[०-९]', txt):
            issues.append((sid, 'numbering', f'stray marker text "{txt}" '
                           'left after the last verse'))
    markers = [v['marker'] for v in verses]
    clean = markers == list(range(1, len(markers) + 1))
    if not clean:
        issues.append((sid, 'numbering', 'source markers are not 1..n; IDs '
                       'use position: ' + ' '.join(
                           '-' if x is None else str(x) for x in markers)))
    out = []
    for index, v in enumerate(verses, start=1):
        number = v['marker'] if clean else index
        out.extend(verse_lines(sid, number, v['lines']))
    return out, issues


def main(parsed, book):
    book = Path(book)
    data = json.load(open(parsed, encoding='utf8'))
    (book / 'text').mkdir(exist_ok=True)
    per_mandala = {}
    issues, headers = [], []
    counts = {}
    for s in data:
        lines, iss = build_sukta(s)
        per_mandala.setdefault(s['mandala'], []).append((s['sukta'], lines))
        issues.extend(iss)
        counts[(s['mandala'], s['sukta'])] = len({
            re.match(r'(\S+?)[a-z]? \|', l).group(1) for l in lines})
        headers.append((s['mandala'], s['sukta'], ' / '.join(s['header'])))
    layout = {}
    for m, suks in sorted(per_mandala.items()):
        total = sum(len(l) for _, l in suks)
        if total < 1000:
            layout[m] = 'part'
            body = [x for _, l in suks for x in l]
            (book / 'text' / f'p{m:03d}.md').write_text(
                '\n'.join(body) + '\n', encoding='utf8')
        else:
            layout[m] = 'chapter'
            for c, l in suks:
                (book / 'text' / f'ch{m:03d}.{c:03d}.md').write_text(
                    '\n'.join(l) + '\n', encoding='utf8')
    with open(book / 'headers.md', 'w', encoding='utf8') as h:
        h.write('# Sukta headers as printed in S1 (rishi, devata, chandas)\n'
                '\nNot part of the text files. Source text, uncorrected.\n\n'
                '| Mandala | Sukta | Header |\n|---|---|---|\n')
        for m, c, t in headers:
            h.write(f'| {m} | {c} | {t.replace("|", "/")} |\n')
    json.dump({'layout': layout, 'counts': {f'{m}.{c}': n for (m, c), n
               in counts.items()}, 'issues': issues},
              open(book / 'tools' / 'build_result.json', 'w',
                   encoding='utf8'), ensure_ascii=False)
    print(layout, sum(counts.values()), 'verses', len(issues), 'issues')


if __name__ == '__main__':
    main(*sys.argv[1:3])
