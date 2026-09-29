# Phase 0 Research Findings

Research snapshot: 2026-09-29.

## Measured national audit

The reproducible report is [`research/coverage-audit-2026-09-29.md`](research/coverage-audit-2026-09-29.md). It found 4,624 active grundskola units, complete visiting addresses in the daily extract, and coordinates in all 120 deterministically sampled detail records. Staffing coverage is high (94.0–96.9% for the two candidate measures), while outcome coverage is materially lower (52.3% for grade-6 all-subject attainment and 64.6–71.7% for the two grade-9 measures). The 2026 survey workbooks join cleanly to current identities after accounting for ceased/dormant/non-GR units, but each respondent/grade covers only its participating/applicable population.

Only 2,213 active units (47.9%) have the simple intersection of an outcome measure, both teaching measures, and a pupil safety/study-environment pair. This is before SALSA, confidence, recency, and score eligibility rules.

## Quantitative sensitivity and fairness diagnostic

The reproducible [`research/score-sensitivity-2026-09-29.md`](research/score-sensitivity-2026-09-29.md) analysis forms grade-aware academic, teaching, and pupil-environment components from latest available values strictly for research. It is not a score release. The complete-case population is 2,015 schools (43.6%); relaxing to any two components adds 1,653 schools but creates evidence-incomparable totals.

Broad ordering is correlated across tested weights, yet exact positions are not robust: median absolute movement is 53–155 places and P95 movement is 202–562 among 2,015 schools. The provisional score remains materially associated with pupil context (Spearman 0.544 with parental postsecondary education; -0.312 with foreign-background share). Eligibility is highly uneven: 6.7% in the smallest school-size quartile versus 72.4% in the largest, and 22.7% for independent versus 48.1% for municipal schools. Among eligible schools, top-quartile representation also differs sharply by context, size, organizer, and grade configuration. These descriptive results do not establish causality, but they make a precise national league table indefensible without deeper review.

## What can be built reliably

- A nationwide active grundskola directory with actual grades, organizer/type, address, and frequently coordinates from daily Skolenhetsregistret v2.
- School profiles that show dated raw results, staffing, survey evidence, and official SALSA where applicable, with source-level caveats.
- Location/grade discovery using the register as the identity spine and an external geocoder only for the parent’s transient address.
- Transparent missing/coverage states and evidence-first comparisons before a composite score exists.

## What is not yet supportable

- A defensible published overall score or national/city ordinal ranking; the first sensitivity analysis found material rank movement, socioeconomic association, and uneven eligibility.
- One context-adjusted measure for every grade configuration: SALSA applies to sufficiently large grade-9 cohorts and is explicitly not a standalone ranking tool.
- Annual environment evidence for every school: the survey covers half the country per year.
- Inspection-based scoring, municipality placement/admissions likelihood, or travel time.
- A claim that SCB municipality context describes the pupils at an individual school.

## Unexpected/material findings

- The canonical register already includes WGS84 coordinates and offered grades, reducing initial geocoding needs for schools.
- Skolenhetsregistret v2 supports ceased units, historical-date lookup, and modification filters, which enables a cleaner incremental/history strategy.
- Kolada has school-level V15 units, but a separate identifier means it is not a drop-in join and much content may duplicate upstream Skolverket data.
- The new Skolverket national quality-system PxWeb table combines useful measures but currently exposes a limited period and is labelled non-official; canonical historical bulk series still need selection.

## Primary risks

Identity changes/reorganizations; suppressed small cohorts; non-comparable grade configurations; survey nonresponse/cycles; definition changes; raw outcome socioeconomic confounding; over-trust in a 0–100 number; revision without source notification; and ambiguous reuse terms for some downloadable workbooks.

## Recommended first product evidence

Start with directory facts and source values. Candidate scoring inputs are grade-appropriate outcomes, official SALSA residuals only where eligible, qualified-teacher share/pupils per teacher, and current-cycle pupil safety/study environment. Treat trend as a small component only with comparable history. Exclude inspections, scraped school claims, inferred neighborhood context, and duplicate outcome measures from `score_v1`.

## Recommendation

Proceed with reversible directory/profile/comparison foundation work, but keep the overall score off. The quantitative portion of RESEARCH-03 strengthens the case for an evidence-led comparison prototype rather than a universal ranking; statistician review, SALSA access/exclusion, source rights, and parent comprehension remain unresolved.
