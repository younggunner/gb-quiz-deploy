# gb-quiz-deploy

GreaseBook quiz funnel — GitHub Pages. Serves `quiz.greasebook.com` (after DNS cutover; see
`Mission_Control/docs/Infrastructure/Hosting/quiz-instapage-exit-plan.md`).

The rules for this site, and the why behind each one, are in the GB Website Engine spec: https://github.com/GreaseBook/landing_pages/blob/main/gb-website-spec.md

- `/quiz` — Typeform sTbsRn (iframe embed) + attribution script ported VERBATIM from Instapage. ONE copy only (June 2026 incident: a duplicate blanked all quiz UTMs for a week).
- `/approved` — booking page (dual Calendly, pricing prep). Built + approved 2026-07-13.
- `/success` — post-booking confirmation (Calendly redirect target). "Tentatively scheduled" + videos + testimonials.

## Tests

`scripts/run-tests` runs the browser tests for `/approved` (Calendly is stubbed and every outside request is blocked).
One-time setup: `python3 -m pip install playwright && python3 -m playwright install chromium`.
