1. Provisioning and deployment are idempotent: running them twice gives the same result.
2. Secrets live outside the repository (secret store or environment); never in code, images, CI logs or docs.
3. Every deployment has a rollback path that was written down, and tested where possible.
4. Least privilege: service accounts, tokens and network rules grant only what is needed.
5. Every change has a change record (what, why, when, who approved, how to roll back) before it touches a shared environment.
6. No direct writes to shared or production systems from an agent; produce the commands or the pipeline change for a person to run.
7. Each service has monitoring, alerts with owners, and a runbook; backups are defined and restore-tested.
