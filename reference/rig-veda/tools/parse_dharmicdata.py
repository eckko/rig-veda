#!/usr/bin/env python3
"""Parse DharmicData Rigveda JSON (S1) into per-sukta structures.

Usage: parse_dharmicdata.py SRC_DIR OUT_JSON
Reads rigveda_mandala_1..10.json, splits each sukta's text into header
paragraphs and verse paragraphs. No text is typed or corrected here.
"""
import json, re, sys, unicodedata
from pathlib import Path

DIG = str.maketrans('०१२३४५६७८९', '0123456789')
ACCENT = re.compile('[\u0951\u0952\u1cd0-\u1cff]')
# a verse-end marker anywhere in the text: ॥ N ॥  |  ॥N  |  ॥ N ॥ M (M = extra)
MARK = re.compile(r'॥\s*([०-९]+)\s*(?:॥){0,2}(?:[ \t]+([०-९]+)(?=\s|$))?')


def clean(text):
    return unicodedata.normalize('NFC', text.replace('\r', ''))


def split_sukta(text):
    """Return (header_paragraphs, verses, trailing_text).

    A verse is {marker, extra, lines}. Header = everything before the word
    that holds the first accent mark. Lines of a verse are the source's own
    paragraph breaks inside it."""
    text = clean(text)
    parts, pos, marks = [], 0, []
    for m in MARK.finditer(text):
        parts.append(text[pos:m.start()])
        marks.append((int(m.group(1).translate(DIG)), m.group(2)))
        pos = m.end()
    tail = text[pos:]
    # header: cut the first chunk before the word with the first accent
    first = parts[0] if parts else tail
    acc = ACCENT.search(first)
    if acc:
        # start of the line that holds the first accent; if that line also
        # holds the end of the header (a danda), cut after the last danda,
        # so unaccented first words of verse 1 stay with the verse
        line_start = first.rfind('\n', 0, acc.start()) + 1
        segment = first[line_start:acc.start()]
        last_danda = max(segment.rfind('।'), segment.rfind('॥'))
        cut = line_start + last_danda + 1 if last_danda >= 0 else line_start
    else:
        cut = 0
    header_text, first_body = first[:cut], first[cut:]
    if parts:
        parts[0] = first_body
    else:
        tail = first_body
    header = [re.sub(r'\s+', ' ', h).strip()
              for h in re.split(r'\n\s*\n', header_text) if h.strip()]
    verses = []
    for chunk, (marker, extra) in zip(parts, marks):
        lines = [re.sub(r'\s+', ' ', l).strip()
                 for l in re.split(r'\n\s*\n|\n', chunk) if l.strip()]
        if lines:
            lines[-1] += ' ॥'
        verses.append({'marker': marker, 'extra': extra, 'lines': lines})
    tail_lines = [re.sub(r'\s+', ' ', l).strip()
                  for l in re.split(r'\n\s*\n|\n', tail) if l.strip()]
    return header, verses, tail_lines


def main(src, out):
    result = []
    for m in range(1, 11):
        data = json.load(open(Path(src) / f'rigveda_mandala_{m}.json',
                              encoding='utf8'))
        for item in data:
            header, verses, tail = split_sukta(item['text'])
            result.append({'mandala': m, 'sukta': item['sukta'],
                           'header': header, 'verses': verses, 'tail': tail})
    json.dump(result, open(out, 'w', encoding='utf8'), ensure_ascii=False)
    print(len(result), 'suktas',
          sum(len(r['verses']) for r in result), 'verses')


if __name__ == '__main__':
    main(*sys.argv[1:3])
