# Implementation Backlog

## Phase 0 — Research

- [x] **RESEARCH-01 — Establish an evidence-bounded data foundation**
  - Outcome: maintainers can decide what the first trustworthy product may calculate/show.
  - Acceptance: primary-source inventory covers access, level, identity, cadence/history, reuse, missingness, caveats, ingestion; identity model and `score_v1` proposal are reproducible; unknowns stay explicit.
  - Verification: source links/tested API notes, `git diff --check`, placeholder/stale-name search.
  - Dependencies: none.
- [ ] **RESEARCH-02 — Run a reproducible national coverage audit**
  - Outcome: quantified joins/availability replace assumptions.
  - Acceptance: pin/checksum national artifacts; profile joins, years, suppression, samples, grade applicability, coverage; inspect a stratified mismatch sample; confirm commercial reuse terms.
  - Verification: tested audit script and dated generated summary; rerun is reproducible.
  - Dependencies: RESEARCH-01.
  - Status: technical audit complete in `docs/research/coverage-audit-2026-09-29.md`; verification remains incomplete until Skolenkäten commercial reuse terms and a supported bulk SALSA path (or an explicit decision to exclude it) are resolved.
- [ ] **RESEARCH-03 — Validate score fairness and comprehension**
  - Outcome: evidence supports publishing, revising, or withholding a composite score.
  - Acceptance: sensitivity covers weights/cohorts, small schools, missingness, with/without SALSA; fairness review measures rank movement; 5–8 parent sessions apply the `PRODUCT.md` threshold.
  - Verification: versioned analysis and anonymized study summary.
  - Dependencies: RESEARCH-02.
  - Status: quantitative diagnostic complete in `docs/research/score-sensitivity-2026-09-29.md`; it found material weight sensitivity, socioeconomic association, and uneven eligibility. Still incomplete pending statistician review, SALSA inclusion/exclusion sensitivity, and 5–8 parent sessions.

## Phase 1 — Data foundation

- [ ] **DATA-01 — Scaffold app and database**
  - Outcome: a fresh checkout installs, runs, builds, and tests with documented commands.
  - Acceptance: Next.js/TypeScript, PostgreSQL/PostGIS migrations, i18n skeleton, health check, CI, `.env.example`, exact command contract.
  - Dependencies: RESEARCH-01.
  - Status: Next.js 16/React 19/Material UI 9 shell, health endpoint, pinned pnpm lockfile, typecheck, lint, and production build are complete. Database/migrations, i18n, CI, environment contract, and automated browser coverage remain.
- [ ] **DATA-02 — Ingest Skolenhetsregistret v2**
  - Outcome: active grundskola directory with historical identity retained.
  - Acceptance: raw payloads; idempotent full/incremental import; active/ceased handling; organizer, address, coordinates, types, offered grades; schema drift and counters.
  - Dependencies: DATA-01.
- [ ] **DATA-03 — Ingest metrics and publish snapshots**
  - Outcome: school evidence and eligible `score_v1` snapshots reproduce from pinned artifacts.
  - Acceptance: results/staffing, SALSA, survey connectors; suppression/sample metadata; cohorts; coverage/confidence; ranking eligibility; no missing-to-zero behavior.
  - Dependencies: RESEARCH-02, RESEARCH-03, DATA-02.

## Later V1 slices

- [ ] **DISCOVERY-01** — Address, grade, accessible map/list, radius, filters, empty/error states.
- [ ] **PROFILE-01** — Stable route, evidence, trends, deterministic insights, sources, metadata.
- [ ] **COMPARE-01** — Compare up to four schools with expandable source measures.
- [ ] **RANK-01** — Municipality routes with eligibility disclosure.
- [ ] **FIT-01** — Local weights with Common Score and My Fit separate.

Later ideas stay in `docs/roadmap.md`.
