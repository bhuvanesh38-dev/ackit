---
type: journal
title: 'Journal: Session heading shape rule'
status: draft
about: F-005
generated:
  by: ackit/1.3.0
  at: '2026-11-23T11:03:28Z'
---

<!-- ACF journal: Append-only record of decisions, corrections and findings for one feature or document set.
  writes: whoever made the decision | reviews: none | signs off: none
  update when: same turn as the decision or correction
  rules:
  - Entries: `## YYYY-MM-DD - kind: title`, kind is decision, correction, finding or note.
  - Newest first. Past entries are never edited; correct with a new entry.
  - Living docs state only current truth; history lives here.
-->

# Journal: Session heading shape rule

Append-only. Newest entry first. Never edit a past entry; correct it with a new one. Kinds: decision, correction, finding, note.

## 2026-11-23 - decision: ACF045 is a separate rule, not a tightening of ACF021

The owner asked why ACF021 is not simply tightened, since the kit is local with few adopters. Kept separate for three reasons: each rule has its own severity (the fields as errors and the heading as a warning are possible only as two rules); a new rule is a warning by default, so a bundle written before it does not fail on upgrade, while a tightened ACF021 would turn every entry without a sha into an error; and a new rule can later be promoted to an error by default, which a tightened old rule cannot be loosened from. The owner accepted this. Found while building: the kit's own first session entry carried `@ initial` as the sha and now says `@ none`. Not done, on purpose: checking that the day or week matches the date, or that the sha exists; both need a convention or a repository the rule should not assume.

## 2026-11-23 - note: journal started

Created for F-005.
