# National Coverage Audit

Generated: 2026-09-29T17:33:03.162405+00:00

## Scope

Active grundskola in daily register extract; selected PxWeb measures for 2022/23–2025/26; Skolenkäten 2026

## Measured results

- Active grundskola units: **4,624** with 100.0% complete visiting addresses.
- Coordinate sample: **120/120** (100.0%).
- Outcome + teaching + pupil-environment proxy intersection: **2,213** (47.9% of active units).
- This intersection is not score eligibility; SALSA, anchors, recency, confidence, and validation gates are not applied.

### Selected metric coverage

| Metric | Applicable | Latest available | Coverage | 3+ periods |
| --- | ---: | ---: | ---: | ---: |
| Elever: Antal elever | 4,624 | 4,507 | 97.5% | 4,282 |
| Elever: Andel (%) med utländsk bakgrund | 4,624 | 4,189 | 90.6% | 3,644 |
| Elever: Andel (%) med föräldrar med eftergymnasial utbildning | 4,624 | 4,427 | 95.7% | 4,150 |
| Personal: Lärare i ämnen/ämnesområden, andel (%) med behörighet (heltidstjänster) | 4,624 | 4,348 | 94.0% | 4,000 |
| Personal: Antal elever per lärare (heltidstjänster) | 4,624 | 4,481 | 96.9% | 4,161 |
| Delmål 1: Andel (%) elever som har lägst betyget E i samtliga ämnen efter årskurs 6 | 3,339 | 1,747 | 52.3% | 792 |
| Delmål 1: Andel (%) elever som har lägst betyget E i samtliga ämnen efter årskurs 9 | 1,776 | 1,274 | 71.7% | 889 |
| Delmål 1: Andel (%) elever som blir behöriga till ett nationellt program i gymnasieskolan | 1,776 | 1,148 | 64.6% | 576 |
| Delmål 2: Elevers upplevelse av trygghet i årskurs 5 (medelvärde)* | 3,392 | 3,097 | 91.3% | 0 |
| Delmål 2: Elevers upplevelse av trygghet i årskurs 8 (medelvärde)* | 1,777 | 1,573 | 88.5% | 0 |
| Delmål 2: Elevers upplevelse av studiero i årskurs 5 (medelvärde)* | 3,392 | 3,097 | 91.3% | 0 |
| Delmål 2: Elevers upplevelse av studiero i årskurs 8 (medelvärde)* | 1,777 | 1,573 | 88.5% | 0 |
| Delmål 2: Pedagogiska personalens uppfattning om trygghet (medelvärde)* | 4,624 | 4,005 | 86.6% | 0 |
| Delmål 2: Pedagogiska personalens uppfattning om studiero (medelvärde)* | 4,624 | 4,005 | 86.6% | 0 |
| Delmål 4: Vårdnadshavares uppfattning om deras barn får den hjälp som behövs för att klara skolarbetet (medelvärde)* | 4,624 | 4,260 | 92.1% | 0 |

### Skolenkäten 2026 joins

| Workbook | Unit codes | Joined active | Join rate | Active coverage | Unmatched | Unmatched current status |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| grade_5 | 1,640 | 1,612 | 98.3% | 34.9% | 28 | AKTIV: 11, UPPHORT: 6, VILANDE: 11 |
| grade_8 | 864 | 837 | 96.9% | 18.1% | 27 | AKTIV: 12, UPPHORT: 8, VILANDE: 7 |
| guardians | 2,256 | 2,204 | 97.7% | 47.7% | 52 | AKTIV: 11, UPPHORT: 13, VILANDE: 28 |
| teachers | 2,258 | 2,204 | 97.6% | 47.7% | 54 | AKTIV: 13, UPPHORT: 13, VILANDE: 28 |

## Known gaps

- No supported national bulk SALSA export was verified; only the public per-school SIRIS application and methodology were found.
- The daily register XLSX has complete visit addresses but no coordinates; coordinate coverage is estimated from a deterministic API detail sample.
- This audit profiles availability, not statistical validity, response bias, licence sufficiency, or parent comprehension.

## Source artifact hashes

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| school-units | 2,237,058 | `0392a9ecb0bca0638e368f63a60741108fab82d81f326edd5aaaaefb87f74038` |
| school-unit-index | 943,898 | `199c32e35a76aec3c6fe4e227a42445352602d86bf43ae3abfd29428186338d5` |
| grundskola-metrics | 4,919,156 | `0e292078e10822e5b7200f62062b14fba12731813fea4abe91e2440bccaf70d5` |
| survey-grade_5 | 5,177,311 | `7e4a81bb47eea1c6c00139db07d5d496e2fe6f785d950e4345b955d2c10cb220` |
| survey-grade_8 | 3,216,259 | `665723215042b7115e27992d21b5103832994159b4b4eaf60e1a066dd2e16301` |
| survey-guardians | 4,797,560 | `a77f82c8bf797c0b3678aee3b4550aa47250b860de3be41c94a411337516446f` |
| survey-teachers | 5,470,833 | `ee3a9e3857e511b12a3d926ba0656d51b47e10028ae7bacb6733981897516d3b` |
