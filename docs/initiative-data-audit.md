# Public initiative data audit — 2026-09-11

We now hold selected local source files, not just links. No source archive is redistributed by this repository. See [download provenance](../sources/initiative-downloads.json) and [our count audit](../results/initiative-data-audit.json).

| Initiative | Retrieved and checked | Remaining limits |
|---|---|---|
| Stanford Virtual Lab | Pinned repository metadata, documentation/license, experimental platemap and one measurement file. Own platemap count: 96 distinct wells and names. | Partial selection, not full experimental replication. Virus nanobody work is a methodology example, not CRC treatment evidence. |
| INDRA, associated with the DARPA Big Mechanism research lineage | Software documentation/license; publication PMID list; curation JSON; complete Zenodo JSON-gzip benchmark, checksum verified. | The current project also includes later work. This is not every DARPA project's data or a clinical evidence database. |
| REACH | Repository inventory and licensing pointers. | Main PDF license not assessed; no installation or code republication. |
| Research Swarm | Rechecked GitHub API (404), website (503), search index and archive index. | No verified live data export or replacement. Exact-URL archive query returned no rows; this is a limited search, not proof of absence. |

Our PMID count is 567,506 unique numeric IDs, one fewer than the publication repository README's 567,507. Cause unresolved. Exact overlap with our current 297 unique catalog PMIDs is zero; this says nothing about conceptual overlap or all INDRA knowledge.

The curation file contains 6,022 annotation records attached to 1,800 distinct statement hashes. The statement/evidence JSON fields are empty. Thus labels alone cannot support a mechanism review. It is a selected benchmark, not an unbiased estimate of extraction error. Do not count annotations as independent studies. Raw curator identity fields stay out of this repository.

The complete benchmark comes from [Zenodo 7559353](https://zenodo.org/records/7559353), under CC BY-NC-SA 4.0, separately from INDRA's BSD-2-Clause software license. The downloaded compressed JSON is 460,045,058 bytes. Our repository license does not replace source licenses. No pickle file was loaded.

## First practical use

The accompanying streaming script matches exact agent names for eight exploratory seeds. Counts describe assembled statements and may include complex membership or agent conditions, not necessarily direct causal edges. They are not patient counts, independent publications, evidence of novelty or validated CRC mechanisms. Alias matching and tissue/genotype/treatment context need separate review.

The next useful test is to link statement hashes to source evidence, independently review a small held-out set before revealing human curation labels, and score relation direction, entity grounding and hypothesis-versus-observation errors. Split by statement and source family to avoid counting correlated examples as independent. An attractive pathway or agreement between models is insufficient validation.

Stanford's useful contribution here is a inspectable sequence of question, specialist critique, executable methods and experimental checks. Its biological results cannot simply be transferred to cancer.

## Original resources

- [Stanford Virtual Lab](https://github.com/zou-group/virtual-lab)
- [INDRA](https://github.com/gyorilab/indra)
- [INDRA publication code and data pointers](https://github.com/sorgerlab/indra_assembly_paper)
- [REACH](https://github.com/clulab/reach)
- [DARPA program](https://www.darpa.mil/research/programs/big-mechanism)

This audit has not contacted contributors, enrolled in any external service, run paid model calls, or independently replicated the papers.

## Executed corpus scan

The complete JSON array parsed successfully: **894,939 assembled statements**. Exact agent-name counts and bounded source pointers are in [our scan result](../results/indra-seed-scan.json). Run `python3 scripts/scan_indra_corpus.py /path/to/indra_benchmark_corpus.json.gz --out /tmp/seed-scan.json` to reproduce. No source sentences are included in that output. These seed matches have not been independently reviewed.
