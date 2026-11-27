| Write or update | Type | Format |
|---|---|---|
| Ticket resolution | `ticket-resolution` | `resolution_type` (1 to 6), `tickets`; Quick summary / Symptom / Diagnosis / Root cause / Resolution / Verification / Follow-up; status `draft` |
| Issue pattern | `issue-pattern` | Problem / Signals / Cause / Resolution / Related resolutions; at least two resolutions behind it |
| Platform behaviour | `platform-behaviour` | Behaviour / Applies to / Evidence; status `draft` |
| Questions | under the section they belong to | one line per missing fact, starting with `Question:` |
| Engineering request | a work item (`issue` or `task`) | only for type 1 or 5, as the person asks; its id goes in `work_item` |

Never write `verified`; a person verifies.
