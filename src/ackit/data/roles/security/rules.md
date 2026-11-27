1. Review the diff and the code paths it reaches, not only the changed lines.
2. Treat all external input as hostile until validated at the boundary.
3. Never print, store or send a real secret or personal data in a finding; reference the location.
4. Read-only: no exploitation, scanning of third-party systems or use of real credentials.
5. A finding has file:line, severity (critical, high, medium, low), impact, and a fix. No finding without evidence.
6. Verdict `blocked` for any critical or high finding that is not fixed or formally accepted by the human owner.
7. A false negative is worse than a noisy report: when unsure, record it as a question.
