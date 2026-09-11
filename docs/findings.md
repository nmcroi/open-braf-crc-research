# Initial checked findings

Date: 2026-09-11. These are bounded checks, not a systematic review or a treatment recommendation.

## SCP2079: the accessible epithelial cohort differs from the whole-cell study

[Primary study](https://doi.org/10.1038/s41591-022-02181-8); [public portal](https://singlecell.broadinstitute.org/single_cell/study/SCP2079).

The article reports 23 patients with paired pretreatment/day-15 biopsies and 419,551 cells across cell types. Independently joining eight public annotation fields yields 95,421 epithelial cells, 27 patients and 46 biological specimens; 19 patients have both timepoints, including 16 MSS and 3 MSI. The public cluster and file descriptions identify this as an epithelial selection. The exact reasons for the difference from the article's 23 complete patients remain unverified.

| Minimum epithelial cells at each timepoint | All complete pairs | MSS pairs |
|---:|---:|---:|
| 1 | 19 | 16 |
| 10 | 15 | 13 |
| 20 | 15 | 13 |
| 50 | 13 | 12 |
| 100 | 11 | 10 |

Cell-count filters may select on treatment-induced tumor depletion. They are sensitivity analyses, not universal quality cutoffs. One public NR label coexists with PFS above six months; its reason is unresolved. RECIST is a separate field. Prior targeted therapy is not resolved by the inspected annotations. Raw expression has not yet been reanalyzed.

Reproduction: `python analyses/scp2079/audit.py`. Snapshot: `results/scp2079-metadata-audit.json`, including retrieval URLs and response hashes. Only aggregate results are committed.

## Tian supplementary gene statistics: a hypothesis, not a new mechanism

The two sheets of Supplementary Table 2 contain 36,601 non-empty gene rows each. We extracted 16 genes per sheet. In the longer-PFS group, published epithelial avg_log2FC values include CXCL9 1.273, CXCL10 4.604, CXCL11 2.565, CD47 0.395 and IDO1 1.603. These are author-provided group statistics, not independently recomputed patient effects. Positive group-level changes do not establish co-change within patients or cells.

Question: does within-patient chemokine induction coexist with CD47/IDO1 induction after accounting for sample coverage and MSI? This cannot establish clinical benefit from targeting those genes. Avoid validating a signature on the same outcome-selected genes used to construct it.

Reproduction: `python analyses/tian-supplement/extract.py`. Snapshot: `results/tian-selected-genes.csv`. Source: [public supplementary archive](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9941044/supplementaryFiles).

## BREAKWATER: subsequent-treatment denominators

[Primary article, DOI 10.1056/NEJMoa2501912](https://doi.org/10.1056/NEJMoa2501912).

At the reported January 6, 2025 cutoff, the EC+mFOLFOX6 arm had 236 randomized patients, 67 still on study treatment, and 169 who had discontinued. Of the 169, 108 received subsequent systemic treatment: 63.9% of discontinuers or 45.8% of the whole arm. Subtracting gives 61 discontinuers without recorded subsequent systemic therapy at that cutoff. This is not a lifetime probability of having no treatment options. Regimen-specific efficacy after first-line EC+chemotherapy is not established by those counts.
