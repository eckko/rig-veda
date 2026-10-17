#!/usr/bin/env python3
"""Write toc.md, STATUS.md and ISSUES.md from build_result.json + headers."""
import json, re
from pathlib import Path

book = Path(__file__).resolve().parent.parent
res = json.load(open(book / 'tools' / 'build_result.json', encoding='utf8'))
layout = {int(k): v for k, v in res['layout'].items()}
counts = {tuple(map(int, k.split('.'))): n for k, n in res['counts'].items()}
hdr = {}
for line in open(book / 'headers.md', encoding='utf8'):
    m = re.match(r'\| (\d+) \| (\d+) \| (.*) \|$', line.rstrip('\n'))
    if m:
        hdr[(int(m.group(1)), int(m.group(2)))] = m.group(3)
DEV = str.maketrans('0123456789', '०१२३४५६७८९')
issue_kinds = {}
for sid, kind, what in res['issues']:
    issue_kinds.setdefault(sid, []).append((kind, what))

rows, status = [], []
for (m, c), n in sorted(counts.items()):
    f = f'text/p{m:03d}.md' if layout[m] == 'part' else f'text/ch{m:03d}.{c:03d}.md'
    purpose = (hdr.get((m, c), '')[:90] or 'see headers.md') + ' (source: S1 header)'
    purpose = purpose.replace('|', '/')
    rows.append(f'| {m:03d} | {c:03d} | सूक्त {str(c).translate(DEV)} | '
                f'Sukta {m}.{c} | {purpose} | {n} | unknown | {f} | extracted |')
    note = '; '.join(w for k, w in issue_kinds.get(f'{m:03d}.{c:03d}', []))[:80]
    status.append(f'| {m:03d} | {c:03d} | {n} | S1 | -- | -- | pass | {note} |')

total = sum(counts.values())
toc = f'''# Rigveda Samhita (ऋग्वेदसंहिता)

- Author / compiler: traditional rishi families, one per sukta; Shakala recension
- Subject and purpose of the book: collection of hymns (suktas) of rics to deities such as Agni and Indra (inferred; each sukta header in S1 names rishi, devata and chandas, see headers.md)
- Base edition: Shakala recension with Vedic accents, from the Vedic Heritage Portal via the DharmicData JSON (S1 in sources.md)
- Mapping: part = mandala (001-010), chapter = sukta, verse = ric. Widths are 3 digits everywhere.
- Totals: 10 parts, {len(counts)} chapters, {total} verses extracted (traditional: about 10,552 rics and 1,028 suktas, commonly cited, unverified here)

Layout: mandala 002 is one file (p002.md, under 1000 lines); all other mandalas have one file per sukta.
Sukta 8.66 is not in S1 (see ISSUES.md).

## Parts (suktas in S1, verses extracted)

''' + '\n'.join(
    f'- Part {m:03d} (mandala {m}): '
    f'{sum(1 for k in counts if k[0]==m)} suktas, '
    f'{sum(n for k, n in counts.items() if k[0]==m)} verses'
    for m in range(1, 11)) + '''

## Chapters

| Part | Chapter | Sanskrit name | English name | Purpose | Verses (extracted) | Verses (traditional) | File | Status |
|---|---|---|---|---|---|---|---|---|
''' + '\n'.join(rows) + '\n'
(book / 'toc.md').write_text(toc, encoding='utf8')

(book / 'STATUS.md').write_text(
    '# Status: rig-veda\n\nUpdated: 2026-10-17 on branch '
    'docs/2026-10-17/version-1. Base source: S1. Sanskrit only; no '
    'translations yet.\n\n| Part | Chapter | Sanskrit lines | Source | Hindi | '
    'English | Check | Notes |\n|---|---|---|---|---|---|---|---|\n'
    + '\n'.join(status) + '''

## Next
- Check S1 against a second source (GRETIL Aufrecht, blocked from the shell; needs a user download) to find dropped or merged verses.
- Translations (Hindi, English): not looked for yet.
''', encoding='utf8')

lines = ['# Issues: rig-veda', '',
         '| Line ID | Kind | What | Source(s) | Suggested check |',
         '|---|---|---|---|---|']
lines.append('| 008.066 | missing | S1 has 102 suktas in mandala 8 and skips number 66; '
             'the last verse number of S1 sukta 8.67 is 15 | S1 | check against print edition |')
lines.append('| all | count | S1 has %d verses; about 10,552 is the commonly '
             'cited total (unverified here) | S1 | compare per sukta with a '
             'second source |' % total)
for sid, kind, what in res['issues']:
    lines.append(f'| {sid} | {kind} | {what} | S1 | check against print edition |')
(book / 'ISSUES.md').write_text('\n'.join(lines) + '\n', encoding='utf8')
print(len(rows), 'rows', len(res['issues']), 'issues')
