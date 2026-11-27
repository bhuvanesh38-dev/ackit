---
type: test-evidence
title: 'Evidence for F-002: migration rehearsal on a copy of the first adopter store'
item: F-002
result: partial
status: final
generated:
  by: ackit-dev/agent
  at: '2026-11-23T09:00:00Z'
---

## Commands

```bash
# a throwaway copy outside every repository; the live store is only read; personal folders and tool folders are left out
cp -rL <store>/<project> /tmp/mig/src && rm -rf /tmp/mig/src/developers /tmp/mig/src/.git /tmp/mig/src/serena
.venv/bin/ackit import /tmp/mig/src --mapping <the adopter overlay's mapping.yaml> --dest /tmp/mig/bundle
.venv/bin/ackit validate /tmp/mig/bundle --json
```

## Results

First run: 327 files mapped, 100 errors and 922 warnings. Three kit-side causes were found and fixed: every file of a feature folder was imported as its own feature (99 file-name errors), feature files were not named after their id (3 errors), and relative links did not follow moved files. After the fixes: 327 files mapped, **1 error and 142 warnings**.

- The one error is ACF013: the entry file is 352 lines after import (324 in the store, plus section stubs the import adds) against the budget of 150. Cutting the entry file is a content change in the store, not a kit change.
- The 142 warnings are ACF008 links that point outside the imported folder (to other repository folders and scripts). The kit cannot repair those.
- Consumer paths: the entry file stays `AGENTS.md` and the rules folder `rules/` with the same nine file names (a listing of both sides is identical). The links under the code clones are unchanged by construction: `consumer_layout` names them and `ackit link --check` verifies them; the store's installer creates them.
- Not converted: a feature folder's stage files (analysis, frs, tdd, test-plan, implementation, journal) are imported as `reference` documents under `reference/features/`, not as a large feature with stage documents. The overlay's `stage-mapping.yaml` states the intended mapping; the conversion is not implemented.

## Coverage

Epic criteria after this run: validation clean on a migrated copy: **not met** (1 error, 142 warnings, for the reasons above); entry at 150 lines or fewer: **not met** (store content); characters loaded for a typical Java task against the 129k baseline: **not measured**; paths AX and Claude Code read unchanged: **met for the entry file and rules folder** (list identical), links verified by `link --check` on a real clone only when the store's installer has run. The orchestly pilot is with the orchestly session. Nothing in the live store, orchestly or any code repository was changed.
