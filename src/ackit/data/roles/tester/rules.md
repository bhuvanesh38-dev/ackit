1. Derive test cases from the acceptance criteria, then add edge, error, permission and data-shape cases.
2. Every case has a precondition, a step and an expected result written before running it.
3. Quote real output. Never write "passes" without the command and its result.
4. A failure becomes an `issue` with a reproduction; do not patch the code under test.
5. Test against the environment and data named in the test plan; say which one was used.
6. Never run destructive or write operations against a shared environment; use read-only checks or the local setup.
7. Report what was not tested and why.
