# Schools

Research-stage foundation for a transparent Swedish compulsory-school discovery and comparison product. Product intent lives in `PRODUCT.md`; the Phase 0 evidence base is in `docs/data-sources.md`, `docs/data-model.md`, `docs/scoring-methodology.md`, and `docs/research-findings.md`.

## Current Stage

Phase 0 source research, the technical national coverage audit, and the quantitative score sensitivity/fairness diagnostic are documented. RESEARCH-02 remains verification-incomplete for source rights and SALSA bulk access/exclusion. RESEARCH-03 still requires independent statistical review, SALSA resolution, and parent-comprehension sessions. Do not publish a composite score until the gates in `docs/scoring-methodology.md` pass.

## Repository Safety

The Git remote still targets the starter harness. Do not push until this product has its own confirmed repository remote.

## Documentation Map And Ownership

| File | Authoritative information | Read when |
| --- | --- | --- |
| `AGENTS.md` | Agent workflow, constraints, definition of done | Every task |
| `PRODUCT.md` | Product intent, V1 scope, success criteria, evidence | Every task |
| `PLANNER.md` | Active work and handoff | Every task |
| `ARCHITECTURE.md` | Platform, stack, state and integration decisions | Technical work |
| `docs/design.md` | UI foundation and visual/interaction direction | UI work |
| `docs/data-sources.md` | Source audit, access, reuse, cadence, caveats | Data work |
| `docs/data-model.md` | Entities, identity and import invariants | Data work |
| `docs/scoring-methodology.md` | Proposed scoring and validation gates | Scoring/ranking |
| `docs/research-findings.md` | Phase 0 conclusions | Planning |
| `TASKS.md` | Ordered backlog and task acceptance criteria | Planning or selecting work |
| `DECISIONS.md` | Product decision rationale and supersession history | Relevant decisions |
| `MEMORY.md` | Optional distinct collaboration preferences | When present/relevant |
| `docs/repo-setup.md` | PRD mapping and clone-to-product checklist | New product |
| `docs/agent-onboarding.md` | Resume and optional concurrent-agent protocol | Onboarding/handoff |
| `docs/prompts.md` | Copyable task prompts, including the startup prompt | As needed |
| `docs/release-checklist.md` | Stage-appropriate release checks | Sharing or releasing |
| `docs/roadmap.md` | Optional future possibilities, not committed scope | Future planning |

Change facts in their authoritative home; link to them elsewhere instead of duplicating them. Accepted decisions explain rationale; keep current product/architecture documents consistent when a decision changes.

## Command Contract

The Material UI Next.js application shell and server-side Geoapify address connector are scaffolded. DATA-01 still needs the database/migrations, CI, and integration tests. Nearby-school results remain gated on the national directory connector.

| Purpose | Exact command | Directory / prerequisites |
| --- | --- | --- |
| Setup / install | `pnpm install` | Node 24+; pnpm 12.8.1; copy `.env.example` to `.env.local` and set `GEOAPIFY_API_KEY` to enable address lookup |
| Run locally | `pnpm dev` | repository root |
| Build | `pnpm build` | repository root |
| Lint | `pnpm lint` | repository root |
| Type check | `pnpm typecheck` | repository root |
| Research unit tests | `python3 -m unittest tests/test_audit_school_data.py tests/test_score_sensitivity.py` | Python 3.11+; repository root |
| Coverage audit | `python3 scripts/audit_school_data.py --offline` | populated `.cache/research/school-data-2026`; omit `--offline` to fetch public sources |
| Score sensitivity diagnostic | `python3 scripts/analyze_score_sensitivity.py` | populated `.cache/research/school-data-2026`; research output only |
| Diff check | `git diff --check` | repository root |
| Documentation smoke check | `! rg -n '\[[^]]*(Product Name|fill|unresolved|task|addition|idea)[^]]*\]' PRODUCT.md ARCHITECTURE.md TASKS.md PLANNER.md docs/design.md docs/roadmap.md docs/PRD.md` | passes when no active template placeholders remain |

Document a short manual core-workflow check when automation is insufficient. Add reproducible scripts and CI once meaningful checks exist; avoid tool-specific verification as the only path.
