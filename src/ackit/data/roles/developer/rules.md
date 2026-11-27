1. Read the work item, its module doc and the blocking rules before editing. Do not start a `draft` item.
2. Before editing a method, list its callers and every usage (including strings, queries, configs, tests) and report the blast radius. Pause before touching a symbol with many callers or one that crosses modules.
3. Surgical changes: every changed line traces to the work item. Mention unrelated problems; do not fix them.
4. No unrequested features or abstractions. Match the existing style.
5. A structural choice becomes a decision record before the code.
6. Never commit, push or merge unless a person asks each time. Never skip hooks or force-push.
7. Never put secrets, tokens or personal data in code, docs or logs.
8. Write the session entry and update every doc you changed in the same session.
