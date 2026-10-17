# Rigveda Samhita: raw extracted source bank

Stage 1 (extraction) of a pipeline: verify, review, fix, proofread come next. This folder holds the raw text, not a finished edition. Nothing here has been proofread.

Read, in order: FORMAT.md (file and line format), toc.md (structure), STATUS.md (what is done), sources.md (where text came from), ISSUES.md (known doubts), headers.md (rishi/devata/chandas headers from the source).

Rules for anyone editing here:
- Text lines come only from sources listed in sources.md; never from memory.
- Do not rename files or change line IDs of finished chapters.
- Record every doubt in ISSUES.md; fix text only in a later, explicit proofreading stage.
- Run `python3 reference/tools/check_extraction.py reference/rig-veda` before every commit.
- Branch pattern: `docs/YYYY-MM-DD/version-N`; push new branches only; the owner merges.

Mapping: part = mandala, chapter = sukta, verse = ric. Widths are 3 digits. Mandala 002 is one file (`p002.md`); other mandalas are one file per sukta.

Rebuild from S1 (clone https://github.com/bhavykhatri/DharmicData first):
```
python3 -I tools/parse_dharmicdata.py <DharmicData>/Rigveda /tmp/rv_parsed.json
python3 -I tools/build_text.py /tmp/rv_parsed.json .
python3 -I tools/write_docs.py
```

How to continue: open STATUS.md "Next". Main open work: cross-check against a second source (GRETIL, blocked from the shell, needs a user download) and find translations.
