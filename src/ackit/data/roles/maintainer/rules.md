1. `ackit validate` must pass before and after your change; fix errors, review warnings.
2. Never mark a document verified yourself; request human review. A changed document loses its `verified` entry.
3. Move history to the journal; living documents state current truth only.
4. Do not delete a signed-off or accepted document; deprecate it and link its replacement (supersedes).
5. Keep AGENTS.md under its size budget; move detail out, leave one row in the load-on-demand table.
6. Regenerate indexes with `ackit index --write`; do not hand-edit the generated sections.
