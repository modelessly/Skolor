# Provisional Score Sensitivity and Fairness Diagnostic

Generated: 2026-09-29T17:33:03.855739+00:00

> Research diagnostic only. These calculations are not a production score or publishable ranking.

## Population and missingness

- Complete-case three-component population: **2,015** schools (43.6% of 4,624 active units).
- Allowing any two components raises the population to **3,668** (79.3%), adding 1,653 schools that are not directly comparable to complete cases.
- The two-of-three rule is a stress test, not a recommendation.

## Weight sensitivity

| Scheme | Academic / teaching / environment | Spearman vs baseline | Median rank move | P95 rank move | Top-quartile overlap |
| --- | --- | ---: | ---: | ---: | ---: |
| academic heavy | 60% / 20% / 20% | 0.938 | 123.0 | 421.0 | 82.3% |
| teaching heavy | 25% / 50% / 25% | 0.890 | 155.0 | 562.3 | 76.8% |
| environment heavy | 25% / 25% / 50% | 0.919 | 132.0 | 483.0 | 79.6% |
| near equal | 33% / 33% / 34% | 0.987 | 53.0 | 202.0 | 91.7% |

Material rank movement under plausible weights means a precise national ordinal ranking would overstate robustness even when broad ordering is correlated.

## Socioeconomic diagnostic

Context variables are **not** score inputs. They are used to test whether the provisional raw-evidence score remains associated with pupil context.

| Context measure | Schools | Score Pearson | Score Spearman | Academic Spearman |
| --- | ---: | ---: | ---: | ---: |
| parents postsecondary education | 2,014 | 0.534 | 0.544 | 0.653 |
| foreign background | 1,999 | -0.318 | -0.312 | -0.411 |

### Parent-education quartiles

| Group | Complete cases | Eligibility | Median score | Top-quartile share | Academic → baseline median rank shift |
| --- | ---: | ---: | ---: | ---: | ---: |
| Q1 (lowest) | 550 | 49.5% | 40.5 | 4.9% | -47.0 |
| Q2 | 563 | 50.7% | 46.2 | 15.3% | 20.0 |
| Q3 | 524 | 47.4% | 52.9 | 30.5% | 58.5 |
| Q4 (highest) | 377 | 34.2% | 62.1 | 61.0% | 2.0 |

Negative rank shift means the combined score ranks a school better than academic-only evidence.

## School-size diagnostic

| Pupil-count quartile | Active schools | Complete cases | Eligibility | Median score | Top-quartile share |
| --- | ---: | ---: | ---: | ---: | ---: |
| Q1 (lowest) | 1,128 | 76 | 6.7% | 62.7 | 53.9% |
| Q2 | 1,131 | 373 | 33.0% | 45.2 | 20.1% |
| Q3 | 1,129 | 756 | 67.0% | 48.6 | 22.4% |
| Q4 (highest) | 1,119 | 810 | 72.4% | 50.5 | 27.0% |

## Organizer type

| Group | Active schools | Complete cases | Eligibility | Median score | Top-quartile share |
| --- | ---: | ---: | ---: | ---: | ---: |
| Enskild | 820 | 186 | 22.7% | 53.6 | 37.1% |
| Kommunal | 3,803 | 1,829 | 48.1% | 48.7 | 23.8% |
| Region | 1 | 0 | 0.0% | — | — |

## Grade configuration

| Group | Active schools | Complete cases | Eligibility | Median score | Top-quartile share |
| --- | ---: | ---: | ---: | ---: | ---: |
| grades 1–6 | 2,825 | 1,019 | 36.1% | 50.9 | 29.9% |
| grades 1–9 | 872 | 384 | 44.0% | 49.3 | 21.9% |
| grades 7–9 | 568 | 429 | 75.5% | 46.9 | 17.9% |
| mixed/other | 359 | 183 | 51.0% | 48.3 | 20.8% |

## Interpretation

The diagnostic does not clear a composite score for publication. It demonstrates sensitivity to weighting and missingness and measures socioeconomic, size, organizer, and grade-configuration differences that require statistician review. SALSA sensitivity and parent comprehension remain open gates.

## Limitations

- This is an observational sensitivity diagnostic using latest available values, not the proposed multi-year score implementation.
- No SALSA bulk series was available, so with/without-SALSA sensitivity remains unresolved.
- Correlations do not establish causality or fairness; they flag where deeper review is required.
- Current offered grades may differ from the grades offered in an observation year.
- Suppression, response selection, cohort size, and uncertainty require further model-specific review.

## Input artifact hashes

| Artifact | SHA-256 |
| --- | --- |
| school-units.xlsx | `0392a9ecb0bca0638e368f63a60741108fab82d81f326edd5aaaaefb87f74038` |
| grundskola-metrics.json | `0e292078e10822e5b7200f62062b14fba12731813fea4abe91e2440bccaf70d5` |
