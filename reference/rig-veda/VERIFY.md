# VERIFY log: rig-veda

Dated log of the verify stage (skill /verify-vedic-book-reference). The Sanskrit in text/ is not changed by this stage.

## 2026-10-17 (branch docs/2026-10-17/version-1)
- Inventory: text/ = 985 files in the extraction format; the 3 latin-text files in tools/ are the parsers written for this book, and reference/tools/check_extraction.py is the extraction checker. Not source text; no question needed.
- Second edition: not available, skipped. Translations: none present.
- Structure: 10 parts, 1027 suktas, 10,490 verse numbers. Flags: 8.66 missing (already in ISSUES.md), 1.099 is short (1 verse). toc.md had a false alarm from a Parts table; replaced by a list. check_extraction.py: 0 errors, 0 warnings.
- Verse totals per mandala compared with figures I remember (not checked against a source): 1: 1993 (about 2006), 2: 429 (429), 3: 615 (617), 4: 589 (589), 5: 727 (727), 6: 765 (765), 7: 833 (841), 8: 1690 (about 1716), 9: 1097 (1108), 10: 1752 (1754). Treat as hints for where verses may be missing.
- Word checker: 128,427 tokens, 0 stray characters, 725 typo candidates (712 after packing). The metre check assumes anushtubh/upajati line lengths, which do not fit Vedic metres or this edition's line splits (9,463 flags), so metre.tsv was set aside as metre.tsv.skipped and not sent to the AI pass.
- AI proofreading: 14 packs (712 typo candidates + 110 sample lines).
