# Sources: rig-veda

| ID | Name | URL | Edition | Script | Licence | Covers | Fetched how | Quality note | Role |
|---|---|---|---|---|---|---|---|---|---|
| S1 | DharmicData Rigveda JSON (from Vedic Heritage Portal) | https://github.com/bhavykhatri/DharmicData/tree/main/Rigveda | Śākala, accented | Devanagari | ODbL (repo LICENSE.txt) | maṇḍalas 1–10 | git clone (commit 96b3baf) | some suktas merged into one paragraph, some verse markers odd (see ISSUES.md); 10,490 verses extracted vs about 10,552 commonly cited; 8.66 missing; 31 suktas logged | primary candidate |
| S2 | GRETIL / Aufrecht | gretil.sub.uni-goettingen.de | Aufrecht | IAST | see site | all | blocked (403) from shell | not tested | cross-check, needs user download |
| S3 | Saswara Rigveda | https://github.com/daithal/saswara-rigveda | unstated | Devanagari/Kannada HTML | unstated | maṇḍalas 1–10 | not fetched | has padapāṭha | possible gap-filler |

Conversion: none needed (Devanagari already). Parser: tools/parse_dharmicdata.py, tools/build_text.py. Trailing verse numbers were removed and the closing double danda kept; Devanagari digits inside words are svara marks and were kept. The colophons "iti ... mandalam samaptam" at the end of mandalas 1 and 2 are not in the text files (logged).
Licence note: S1 repo LICENSE.txt is ODbL; the owner should confirm that suits their use.
