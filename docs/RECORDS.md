# Inspectable research memory

Each records.json file is a list of objects with id, kind, title and depends_on. Source objects have url, version, cohort_id, reading and sharing. Dataset objects state access, unit and missingness. Claims identify unit, denominator, exact source locator and limitations. Hypotheses state support, counterevidence, a falsification test and clinical status. Analyses provide commands, outputs and actual execution status. Reviews state scope, unresolved points and status.

Stable IDs survive title changes. The original source catalog IDs S0001… remain unchanged; metadata-only catalog records are not promoted to verified claims. records.json is a curated graph for investigated sources and questions, not a claim to have read every catalog entry.

The graph validator rejects missing dependencies, duplicate IDs, cycles and hypothesis records without falsification tests. A baseline of source-record hashes lets the impact command mark changed sources and all dependent records for re-review. A changed record does not automatically change the scientific conclusion.

Run `python scripts/workspace.py validate`, `python scripts/workspace.py baseline --out /tmp/source-baseline.json`, `python scripts/workspace.py impact --baseline /tmp/source-baseline.json`, and `python scripts/workspace.py search chemokine`. SQLite search is rebuilt from public records, the source catalog and Markdown; it is a disposable index, not the canonical store. No personal directories are crawled.

Run `python scripts/sync_tasks.py --out /tmp/tasks.json` with an existing gh login to fetch Issue state; this is read-only on GitHub. Use `--vault /path/to/onderzoekswerkplaats` to refresh the local Dutch board. Failure preserves the previous snapshot and marks the board stale. The Issue remains authoritative.

Run `python3 scripts/workspace.py cohorts` to group papers by cohort. The mapping needs source review; this does not automatically detect undisclosed patient overlap.
