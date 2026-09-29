# Design Principles

## UI Foundation

- Selected design system: Google Material Design.
- React implementation: Material UI v9 with Emotion.
- Design reference: <https://m3.material.io/>.
- Component reference: <https://mui.com/material-ui/getting-started/>.
- Version: Material UI v9.x; pin the exact version at scaffold time.

Material UI is an actively supported React implementation with official Next.js integration. Its current component baseline implements Material Design 2, not Material Design 3. Use Material 3 guidance for hierarchy, adaptive layout, accessibility, motion, and product tokens without claiming full M3 parity. Google’s official Material Web components are not selected because they are in maintenance mode and do not completely cover the current system.

## Product Theme

- Calm neutral surfaces, muted Nordic blue primary, restrained teal secondary.
- Tonal surface hierarchy instead of heavy borders or card grids.
- Roboto as default UI type, self-hosted when packaging/licensing is established.
- Small radii, moderate elevation, and strong type hierarchy.
- Material Symbols only when they improve recognition; label or hide them appropriately for assistive technology.

Color, typography, shape, spacing, elevation, state, and motion tokens live in `src/theme`; features do not scatter raw theme values.

## Component Posture

- Use Material UI for inputs, buttons, chips, dialogs, navigation, tooltips, tables, alerts, skeletons, and focus behavior.
- Reserve contained buttons for the primary action; use text/outlined secondary actions.
- Use filter chips for active compact filters, not decoration.
- Use dialogs only for short interruptive decisions; details use stable routes or non-modal surfaces.
- Use data tables for comparison with sticky row labels and a linear mobile alternative.
- Maps/charts consume Material tokens and provide equivalent text/list access.
- Do not use dashboard templates or “cards everywhere.” Prefer typography, spacing, and tonal grouping.

## Tone And Interaction

- Start with location and grade, not marketing.
- Show source values before progressively disclosed formulas.
- Keep map/list synchronized and keyboard usable.
- Keep Common Score distinct from My Fit.
- Never make missing data feel like school failure or a rank feel like a verdict.

## Score Presentation

- Show an integer 0–100 only when eligible; otherwise “Not enough current data.”
- Pair every score with coverage, evidence period, and “Why?”.
- Expose raw value, cohort, transformation, weight, and contribution.
- Rankings disclose eligible/total counts and never number an ineligible school.
- Color is secondary, never the only encoding or a red/green moral grade.

## Responsive Layout

- Compact: list-first discovery, explicit alternate map view, bottom comparison action.
- Medium/expanded: adaptive map/list split; a side sheet only when it preserves navigation.
- Profiles/comparisons use readable linear sections, not dashboard grids.
- Navigation follows Material adaptive patterns while preserving URLs and browser history.

## Motion And Accessibility

Motion is brief, functional, and tokenized; respect reduced motion and avoid animated score counting. Meet WCAG 2.2 AA with visible focus, semantic tables/headings, chart text equivalents, 44px targets, localized labels, accessible map alternatives, and explicit loading/empty/error/partial states.

Verify desktop/mobile, keyboard, landmarks, zoom/reflow, reduced motion, map failure, no results, incomplete metrics, and suppression. Material components provide a baseline, not proof of accessibility in the composed product.
