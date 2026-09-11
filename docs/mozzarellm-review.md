# MozzareLLM: scoped code review and offline test

Checked 2026-09-11 at upstream commit `a7aa28cbc1e76163301f8151fa168961d74965fa`, [Cheeseman lab repository](https://github.com/cheeseman-lab/mozzarellm). The code has an MIT license. 31 selected files were downloaded with hashes, including source, small example cluster lists and the bundled UniProt annotation table. The large supplementary Excel benchmark was not downloaded. This is not replication of a scientific benchmark.

## What it actually does

Given pre-existing gene clusters and optional experimental context, the analyzer asks an LLM to identify a dominant process, classify genes and prioritize follow-up. It is a cluster interpretation tool, not an automatic worldwide literature search. In `analyzer.py`, `use_retrieval` defaults to false. With retrieval enabled, `utils/retrieval.py` searches supplied annotations and local Markdown/text files. It does not fetch PubMed papers. Existing subscriptions can use a manual task packet; running the full upstream program requires provider API access. No API calls were made here.

## Executed checks

Only the inspected standard-library retrieval module was executed, not the analyzer or provider modules. Results are in mozzarellm-probe.json.

| Test | Result | Implication |
|---|---|---|
| Read bundled UniProt TSV | 20,461 rows, correct real-tab format | Input itself parses normally. |
| Reproduce example annotation lookup using full `gene_names` as key | 1/8 seed symbols found | Names such as `BRAF BRAF1 RAFB1` do not match the lookup key `BRAF`. This follows the example loader and analyzer's dictionary construction. |
| Explicitly match space-separated names, preserving accessions | 8/8 seeds, one candidate accession each | Our source packet repairs this handoff locally; live identifier validation remains separate. |
| Local notes without annotations | Three snippets | The bundled notes are a small knowledge selection, not comprehensive cancer coverage. |
| Eight mapped annotations plus notes, k=10 | Eight annotations, two notes | Additional evidence competes with annotations for limited slots. |
| Synthetic test with ten annotations and one conflicting note | Note found but omitted from all ten returned snippets | Fixed priority 100 for annotations versus at most 90 for notes can suppress additional evidence. This is a retrieval-capacity test, not a biological result. |

The metadata also reports an empty `genes_without_annotations` list when no annotation dictionary is supplied. Do not interpret an empty list in that situation as complete annotation coverage.

## Static findings requiring care

- `models.py` uses High/Medium/Low confidence and heuristic completeness/known-gene ratios. These are not calibrated probabilities or independent scientific validation.
- `analyzer.py` resumes results by cluster ID without checking an input/model/source hash at the skip point. Use a separate output directory for each versioned input/model/configuration; an unchanged ID need not mean unchanged research.
- Local citation objects identify files or annotation genes; they do not establish that a primary paper supports a generated claim.
- Our eight genes are manually selected research seeds, not an experimental co-cluster. Sending them as a discovered cluster would build the desired connection into the question.

## Usable result for this project

We prepared `mozzarellm-gene-sources.json`, an explicit source-pointer packet for BRAF, KRAS, PRDX1, WNT11, CD47, VEGFA, PTPN11 and HIF1A, retaining UniProt accessions/URLs and cited PMID pointers. It contains no model-generated claim or copied protein descriptions. Bundled annotation age and primary articles remain unverified. The companion packet-builder is standalone standard-library code and needs no API account.

Use this packet with TASK-0006's primary-paper checks. Require a claim-by-claim source table, counterevidence, cell/tissue/genotype context and an explicit novelty search. Keep curated descriptions, contrary evidence and unreviewed hypotheses in separate visible sections so a top-k ranking cannot silently hide a whole category. Document omissions. A second reviewer checks original papers rather than another model's summary.

Recommendation: adopt the scoped interpretation workflow and source packet now; do not activate the full autonomous pipeline or import its confidence labels as our evidence grades. Upstream files are unchanged. No external maintainer contacted, no paid runs started, and no new cancer finding claimed.

## Reproduction

Download `data/knowledge/uniprot_data.tsv` at the pinned upstream commit, then run:

`python3 scripts/build_mozzarellm_packet.py /path/to/uniprot_data.tsv --out /tmp/gene-sources.json`

The original retrieval probe was executed against the pinned source file; its code and downloaded originals are preserved in the separate local audit folder. The public manifest identifies the files and checksums.
