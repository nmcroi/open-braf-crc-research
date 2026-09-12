# INDRA evidence and grounding review — 12 September 2026

Scope: three assembled statements, containing six evidence records, from the previously downloaded INDRA benchmark. These are not six independent experimental replications. Review of extraction and source identity, not clinical validation.

| Statement | Evidence PMIDs | Finding | Disposition |
|---|---|---|---|
| PTPN11 dephosphorylates PRDX1 | 23512980; 19540337; 15845350 | All three records ground the raw entity PAG to PRDX1/Q06830. The sentence attributed to 23512980 explicitly expands PAG to the protein named in UniProt Q9NWQ8 (PAG1). This is a demonstrable identity mismatch within the extracted evidence. The other two sentences mention PAG with Csk/Src, consistent with the same issue, but their full articles were not accessed. | Exclude this assembled edge as evidence for PRDX1; independently check remaining article contexts. |
| PRDX1 activates VEGFA | 27259998; 21343392 | Full XML of PMC5216922 does contain the expanded VEGF term. Its introduction cites prior work, including PMID 21343392 (reference 22), and PMID 24297309 (reference 23). The extracted target combines TLR4 with VEGF; the described endothelial processes depend on those pathways. | Do not count the two records as independent replication or as proof of direct activation of VEGFA. The corpus itself marks these records direct=false. |
| CD47 inhibits VEGFA | 27473366 | The extracted target is a VEGF pathway phrase, not an isolated protein measurement; the sentence concerns vascular smooth muscle. The corpus marks direct=false. | Retain only as a contextual literature lead. This extraction does not establish a direct protein interaction or colorectal treatment benefit. |

## What caused the identity mismatch?

[UniProt PRDX1/Q06830](https://www.uniprot.org/uniprotkb/Q06830/entry) lists PAG as an alternative protein name. [UniProt PAG1/Q9NWQ8](https://www.uniprot.org/uniprotkb/Q9NWQ8/entry) names the different protein matching the expansion in the extracted sentence. Both official JSON records were retrieved during this review. The observed raw entity is PAG, not PRX1. A possible PRX1/PRRX1 ambiguity elsewhere does not explain these selected records.

The assembled PTPN11 edge has a belief score of 0.905384136 despite this mismatch. That score does not substitute for checking protein identity and is not a clinical probability.

## Source access and reproducibility

- [INDRA benchmark, DOI 10.5281/zenodo.7559353](https://doi.org/10.5281/zenodo.7559353): original statements and evidence identifiers; the full corpus and extracted sentences are not redistributed here.
- [PMCID PMC5216922 full-text XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5216922/fullTextXML): introduction and references R22/R23 independently inspected. An abbreviation-only search misses the expanded term.
- [PMID 21343392](https://pubmed.ncbi.nlm.nih.gov/21343392/): cited primary prostate study; not a second independent result from the oral-cancer article.
- [PMID 23512980](https://pubmed.ncbi.nlm.nih.gov/23512980/): title/DOI/PMCID checked through Europe PMC metadata. Full-text XML retrieval for PMC3686999 returned 404 in this check; the identity mismatch above is established in the original corpus sentence, not claimed as a fresh full-article reading.
- [PMID 19540337](https://pubmed.ncbi.nlm.nih.gov/19540337/) and [PMID 15845350](https://pubmed.ncbi.nlm.nih.gov/15845350/): full articles not obtained. Absence of a gene name in an abstract is not a negative full-text result.
- [PMID 27473366](https://pubmed.ncbi.nlm.nih.gov/27473366/): current check inspected the corpus evidence, not a fresh full-article reading.

Machine-readable statement IDs and evidence hashes: [review record](../results/indra-grounding-review.json). Original seed counts remain historical retrieval results, not validated mechanistic evidence. TASK-0006 remains open for remaining source-context checks.
