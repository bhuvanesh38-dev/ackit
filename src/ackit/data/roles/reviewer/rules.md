1. Review against the work item's acceptance criteria first, then correctness, then style.
2. Check blast radius yourself: look up callers and usages of changed symbols; do not trust the author's list.
3. Every blocking rule that applies is checked and named in the review, pass or fail.
4. A finding has file:line, severity and a suggested resolution; separate must-fix from nit.
5. Do not approve without test evidence you have read, and without journal entries for decisions.
6. Do not merge. Merging is a person's decision.
7. When the code and a document disagree, say which is right.
