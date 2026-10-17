# AI proofreading result (proposals only; the text is unchanged)

- items packed: 822, answered: 822, not yet answered: 0
- proposals (error or unsure): 17 (proposals.tsv)
- sample of ordinary lines: 110 read, 5 with an error (4.5%)

An AI reading is a screen, not a proof. Verify proposals against the printed edition before any correction.

## Status after the parser fix (2026-10-17)
- 10 of the 17 proposals were defects of the extraction parser (dropped first word of verse 1, or a stray "॥" line). They are fixed by re-extracting from S1 with a corrected parser; the AI's suggested wording was not used. See proposals_status.tsv.
- All 5 sample errors (5 of 110, 4.5%) were of this kind. The sample lines were not re-read after the fix.
- 7 proposals remain open and need a printed edition: 010.184.3, 006.013.5a, 001.014.10, 001.120.4 (error) and 002.023.8a, 007.067.7b, 001.152.3a (unsure, accent questions).
- Read: 712 typo candidates (all flagged by a frequency heuristic; most were legitimate sandhi or inflected forms) + 110 sample lines. About 128,000 tokens in the text; lines outside these 822 were not read by the AI.
