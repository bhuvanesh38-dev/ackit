1. Read the architecture doc, the affected module docs and the blocking rules before proposing anything.
2. Respect the dependency and tier rules of the repository; never let a lower layer depend on a higher one.
3. Compute the blast radius: modules, public contracts (API, events, schema, config) and consumers touched.
4. Every structural choice becomes a decision record with at least two options and the deciding reason (Why).
5. State data and migration impact: new or changed schema, backfill, rollback, compatibility window.
6. Update the architecture, module and tech-stack docs in the same change; a design that leaves them stale is unfinished.
7. Designs are signed off by the human owner before implementation starts.
