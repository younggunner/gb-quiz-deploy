# gb-quiz-deploy

GreaseBook quiz funnel — GitHub Pages. Serves `quiz.greasebook.com` (after DNS cutover; see
`Mission_Control/docs/Infrastructure/Hosting/quiz-instapage-exit-plan.md`).

- `/quiz` — Typeform sTbsRn (iframe embed) + attribution script ported VERBATIM from Instapage. ONE copy only (June 2026 incident: a duplicate blanked all quiz UTMs for a week).
- `/approved` — booking page (dual Calendly, pricing prep). Built + approved 2026-07-13.
- `/success` — post-booking confirmation (Calendly redirect target). "Tentatively scheduled" + videos + testimonials.
- NO CNAME file yet — added at DNS cutover so github.io preview URLs work first.
