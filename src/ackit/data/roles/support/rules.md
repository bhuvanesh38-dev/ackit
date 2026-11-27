1. Fill only what the evidence supports; a missing fact becomes a question, never a placeholder or a guess.
2. Never write `verified` or `verified_at_commit`, and never set a page to `stable`. A person verifies with `ackit verify` and sets the commit.
3. Run only read-only queries. Never execute a data change (INSERT, UPDATE, DELETE, a migration), and never write one as a recipe for someone to run. Describe the finding and the change that was made, and by whom.
4. Use only registered `module`, `vendors` and `tenants` values; when none fits, ask.
5. Do not copy customer personal data, credentials or tokens into a page; describe them ("a 10-digit account number") and name where they are.
6. A type 1 (data fix) or type 5 (code fix) resolution needs an engineering work item (`work_item`) or a stated reason there is none.
7. Do not edit a page a person has verified. When a ticket is reopened or the cause turns out different, write a new page that names the earlier one, or put the change as a question for the person.
8. Relations between tickets stay in the tracker.
