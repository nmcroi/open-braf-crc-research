# Open BRAF CRC Research

An open, patient-motivated research workspace starting with **BRAF V600E, microsatellite-stable colorectal cancer**. Researchers, patients, relatives and friends of other patients, programmers and people working with AI tools are welcome to contribute reproducible analyses, primary sources and critical reviews.

BRAF/MSS is our starting point, not a boundary. Questions about surgery, local treatment, immunotherapy, cancer-cell recognition and relevant mechanisms in other cancers are welcome. Each task defines its population and explains what can and cannot transfer to colorectal cancer. See [research scope and ways to join](docs/SCOPE-AND-PARTICIPATION.md).

Our aim is to identify useful research questions and test them against evidence. This is an early volunteer project, not a clinical service or a validated autonomous discovery system. There are no claimed institutional partnerships.

## Start here

- **[516 source entries](sources/catalog.md)** / [machine-readable CSV](sources/catalog.csv): publications, trial registrations, conference abstracts and resources across 15 categories. Imported metadata is explicitly **not yet independently verified**. Entries can duplicate a source across categories; 516 does not mean 516 unique studies.
- **[Current findings](docs/findings.md)**: what has actually been checked, what remains uncertain, and what it does not establish.
- **[Open research tasks](https://github.com/nmcroi/open-braf-crc-research/issues)**: bounded tasks with acceptance criteria.
- **[Contributing](CONTRIBUTING.md)**: how to work independently, report negative results and submit a reviewable contribution.
- **[Other initiatives](docs/other-initiatives.md)**: verified links and realistic routes to contributing elsewhere.

## Reproduce the initial analyses

Python 3.10 or newer is recommended. The metadata audit uses only the standard library. The supplement extraction needs openpyxl.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analyses/scp2079/audit.py
python analyses/tian-supplement/extract.py
python scripts/validate.py
```

The first script requests public Single Cell Portal cell annotations and writes aggregate counts. The second downloads a public supplementary archive into memory and extracts published aggregate gene statistics. **It does not independently recalculate those statistics from cells.** No credentials are needed. Remote services may change or be unavailable. Outputs are written next to the scripts and ignored by Git; reviewed snapshots are in `results/`.

## What is shared

Source identifiers and links, original research notes, analysis code and permitted aggregate outputs. This repository does not contain an individual's medical dossier, restricted-access sequencing records, downloaded article collections or private AI conversations. Public availability of an article does not automatically permit republication; full texts remain at their original sources.

## How people and AI can collaborate

Choose an issue and state what you will independently verify. You can use your existing AI subscription for a small task and return a source-backed report through an Issue; coding contributors can submit code and results through a pull request. No separate participation app or shared API key is required. Identify AI assistance and distinguish new calculations from copied author statistics. A second model agreeing is not independent biological validation.

GitHub coordinates work and review; it does not automatically run a worldwide network of agents. No autonomous paid jobs or external-agent access are enabled by this repository. Maintainers review contributions before merging. See [AGENTS.md](AGENTS.md) for the same research rules in an agent-readable form.

Initial release: 11 September 2026. The initial catalog covers material available in the source collection on that date, not an exhaustive worldwide search. Research findings are not individual treatment recommendations.

If the supplementary archive service is slow, download its original ZIP separately and run `python analyses/tian-supplement/extract.py --archive /path/to/supplements.zip`. The initial extraction was verified against the previously retrieved primary archive; the cohort audit was also rerun against the live public API. No recalculation of the authors' gene-level statistical tests is claimed.

## Shared research workspace

[Project structure](docs/STRUCTURE.md) · [Task and review workflow](docs/WORKFLOW.md) · [Research memory](docs/RECORDS.md) · [Join with any AI](docs/TASK-PACKET.md) · [Two-week pilot](docs/PILOT.md) · [Data policy](docs/DATA-POLICY.md).

Current expert-review capacity is unfilled. New exploratory records are not clinical validation. Ordinary contributors can use Issues and Discussions; a maintainer reviews changes before publication.
