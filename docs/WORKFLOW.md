# Research workflow and ownership

GitHub Issues are authoritative for PUBLIC task status. Discussion threads and local mail are transport, not a second task database. The Obsidian board is a dated read-only projection; stale or offline snapshots must say so. Private tasks are separate and never imported to GitHub.

## State machine

Exactly one status label: `status:open`, `status:claimed`, `status:in-progress`, `status:submitted`, `status:in-review`, `status:done`, `status:blocked`.

Open → claimed → in-progress → submitted → in-review → done. Review may request changes and return to in-progress. Blocked tasks name the dependency and next check. Closing an issue with no acceptance evidence does not mark the research done. A submitted result is not an independently reviewed finding.

A contributor claims work by commenting with their handle, intended output and next update date. A maintainer assigns/labels it after checking existing claims. One primary executor per task; an explicitly independent replication is a separate role. If a promised update is >48 hours late, mark possible inactivity for human review; do not automatically revoke or duplicate work. No update deadline means freshness is unknown, not active.

## Roles and review

The owner sets priorities and approves external outreach and new spending. Maintainers check provenance, rights and completeness. The executor provides sources, code and limitations. An independent reviewer checks primary sources or independently runs/reimplements calculations and states exactly what was checked. A qualified scientific reviewer is needed before any clinical validation label; no such reviewer is currently appointed.

AI agreement is not biological validation. Public exploratory results are allowed when visibly labeled. Two papers using one cohort count as one cohort. A negative search records databases, queries, dates and inaccessible sources; it never proves global absence.

## Reconciliation

Source records, claims, analyses and reviews have stable IDs and explicit dependencies. New source versions do not overwrite the old version history. Run the graph audit after changing a source to identify dependent claims requiring review. A source mention is not evidence of full-text reading.

Task records use Issue URLs. Discussion and PR submissions reference the issue and artifact IDs. Source version changes are proposed in a PR; dependent review flags are generated before accepting the revision. Normalization, population, treatment, cell type, assay and timepoint must match before synthesizing patterns.

## Mail and automation

The existing local postbox remains separate from public GitHub. Each message refers to an Issue or private task ID and an artifact. Do not publish private messages or automatically copy local folders. Polling without work is not progress. Existing agents choose an executable task when no new message exists and record actual output or a blocking reason. Only the Codex scheduler is configured here; other agents must acknowledge their own setup.

No paid runners or automatic third-party model access are enabled. Ordinary chat users can download a task packet and return a completed form. Programmers submit a pull request. Do not execute untrusted submissions with credentials.
