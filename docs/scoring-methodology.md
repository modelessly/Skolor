# Proposed Scoring Methodology

Status: research proposal only. `score_v1` must not be implemented/published until RESEARCH-02 and RESEARCH-03 pass. An independent analyst should be able to reproduce a released version from its eventual metric catalogue and code.

## Coverage audit consequence

The 2026-09-29 audit found that 2,213 of 4,624 active units (47.9%) have the simple intersection of an applicable outcome, both teaching measures, and a pupil safety/study-environment pair. This is an upper-bound proxy, not eligibility: it omits SALSA, anchor, recency, confidence, observation-year grade, and stability rules. A universal national Common Score would therefore exclude or differently model too many schools to publish responsibly today. Build evidence profiles and comparisons first; keep overall scoring disabled through RESEARCH-03.

## Sensitivity diagnostic consequence

The dated [`research/score-sensitivity-2026-09-29.md`](research/score-sensitivity-2026-09-29.md) diagnostic applied stricter grade-aware component rules to latest available values. Only 2,015 active units (43.6%) had all three provisional components. A two-of-three renormalization would raise nominal coverage to 79.3%, but would compare schools built from different evidence and is not recommended.

Plausible weight changes produced median absolute rank movements of 53–155 places among 2,015 complete cases; P95 movement reached 202–562 places. The provisional combined score also retained a 0.544 Spearman correlation with the share of pupils whose parents have postsecondary education (academic-only: 0.653). Complete-case eligibility was only 6.7% in the smallest pupil-count quartile and 22.7% for independent schools, versus 72.4% in the largest quartile and 48.1% for municipal schools. These results fail the robustness/equity bar for a precise national ordinal ranking. They do not prove bias or causality, but require statistician review, cohort redesign, SALSA analysis or explicit exclusion, and parent testing before any score is released.

## Principles

- Common School Score is fixed and comparable; My Fit is separate and user-weighted.
- Missing/suppressed/not-applicable never become zero.
- Applicability is grade-aware; do not judge F–6 schools on grade-9 outcomes or SALSA.
- Prefer multi-year robust evidence; expose actual values, periods, cohorts, coverage, and uncertainty.
- A score is descriptive decision support, not causal school quality or a guaranteed child outcome.

## Candidate `score_v1` components

Subject to national coverage audit:

| Component | Candidate evidence | Base weight |
| --- | --- | ---: |
| Academic outcomes | grade-appropriate attainment/eligibility/merit/national tests, avoiding duplicates | 30% |
| Context-adjusted performance | official SALSA actual-minus-model measures, grade 9 only | 25% |
| Teaching conditions | qualified-teacher share and pupils per teacher | 20% |
| School environment | current-cycle pupil safety/study environment plus carefully separated guardian/teacher evidence | 20% |
| Trend | robust multi-year slopes for non-overlapping core measures | 5% |

Weights are hypotheses. If a component is not applicable to a school type, publish grade-cohort component scores but do not silently claim one national overall scale until comparability analysis supports it.

## Metric transformation

For each metric/version/period/applicable cohort:

1. Validate unit/direction and preserve suppression.
2. Prefer a three-year weighted mean when comparable annual observations exist: latest 0.50, previous 0.30, third 0.20; otherwise use available years and disclose count. Survey cycles are not forward-filled as if current.
3. Winsorize only for benchmark calculation at predeclared 2.5th/97.5th percentiles; display the raw value unchanged.
4. Compute mid-rank empirical percentile among eligible comparable units: `p = (rank_mid - 0.5) / N`.
5. Convert to `metric_score = round(100 * p)`. Invert undesirable metrics before ranking.

Percentiles are chosen for interpretability and robustness, not because a 10-point score gap has a cardinal meaning. Minimum cohort `N=30`; otherwise no normalized score. Predeclare cohorts by school form, offered terminal grade/applicability, period, and metric—not neighborhood socioeconomic group.

## Aggregation and missingness

Within component `c`, use only available eligible metrics:

`C_c = sum(w_i * S_i) / sum(w_i available)`

Publish a component only when at least half its planned metric weight and its designated anchor metric are available. Overall score:

`Overall = sum(W_c * C_c) / sum(W_c eligible)`

Publish overall only when at least three substantive components are eligible, academic or context evidence is present where applicable, and available base component weight is at least 65%. Do not renormalize a school into ranking eligibility when its only evidence is one domain.

Coverage is evidence availability, not quality:

- High: ≥85% planned applicable weight, no stale core component.
- Medium: 70–<85%.
- Limited: 65–<70%; show score only outside ordinal rankings pending validation.
- Insufficient: <65% or eligibility rule failed; no overall/rank.

“Stale” is metric-specific and documented. Survey evidence is current for its two-year participation cycle, not just the latest calendar year.

## SALSA

Use official residuals only, never a home-grown socioeconomic regression in v1. Store actual, expected, residual, eligibility, and model year. Cap its influence as above; disclose that it applies only to grade 9, is not causal value-added, and Skolverket says it must not alone rank schools. Sensitivity analysis must show ranks with and without it.

## Trend

Require at least three comparable observations spanning at least three years. Fit a robust slope on raw or benchmark-relative values, shrink toward zero based on sample/years, cap contribution, and show “insufficient history” otherwise. Never infer trend across changed definitions/instruments.

## Confidence and ranking

Confidence is separate from score and combines coverage, recency, sample/denominator evidence, and stability. Do not invent sampling confidence intervals when source microdata/design does not support them.

Ranking requires Medium/High coverage, all category anchor rules, a cohort of at least 30, and no unresolved identity conflict. Display “Ranked schools with sufficient current data: X of Y.” Ties share rank; suppress ordinal claims when uncertainty/sensitivity makes ordering unstable. Profiles still show raw evidence for unranked schools.

## My Fit

Users set nonnegative component/proximity weights normalized to 100%. `My Fit` is recalculated from eligible common components plus proximity; missing preferences renormalize visibly. It never overwrites the Common Score or enters public rankings.

## Deterministic insights

Versioned rules may state a percentile band, material benchmark gap, multi-period direction, or missing/current survey fact. Each insight stores rule version and evidence references. No LLM generates factual claims.

## Validation gates

Before release: extend measured coverage by municipality and observation-year grade; resolve source rights and SALSA access/exclusion; independently review the measured weight/missingness/context/size/type sensitivity; compare outcome-only vs official context-informed ranks if SALSA becomes available; analyze suppression and cohort effects; have a statistician review; run the parent comprehension study; freeze code, catalogue, artifact hashes, and documentation as `score_v1`.
