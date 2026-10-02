# Outcomes after first-line EC plus chemotherapy: round 4

2 October 2026 · TASK-0004 · Search and registry re-check by Claude (AI); independent review pending.

**Result:** no primary cohort reporting regimen-specific outcomes after first-line encorafenib + cetuximab + chemotherapy was found in this bounded search. Three things are new compared with rounds 1 to 3: a Canadian reimbursement recommendation and review that take an explicit position on what follows progression, an updated registry record for RO7673396, and posted BREAKWATER results on ClinicalTrials.gov. None of these is efficacy evidence for a second-line regimen.

## What was searched

Five PubMed queries on 2 October 2026 (entry dates up to that day; queries, counts and PMIDs in `raw/pubmed-round4.json`), 30 distinct records, 9 already in the catalog. Nine tracked registry records re-read through the ClinicalTrials.gov API v2, plus all colorectal records mentioning BRAF with an update posted since 12 September 2026 (`raw/ctgov-round4.json`). This is a bounded search, not a census; conference abstracts outside PubMed were not searched.

## Findings

| Source | What it is | What it adds, and what it does not |
|---|---|---|
| CDA-AMC reimbursement recommendation, encorafenib with cetuximab and mFOLFOX6, Canadian Journal of Health Technologies vol 6 issue 3, published 24 March 2026, report PC0428. PDF sha256 `c29f92ac…4978`, 15 pages, read in full text. | Health technology assessment, recommendation document. | The discontinuation condition states that patients who stop encorafenib or cetuximab for reasons other than progression may receive these drugs again later, and that patients whose disease progressed on them are not eligible for them in a subsequent line. The printed sentence is ambiguous on its own; this reading follows from the preceding sentence. The committee also records expert input that later-line options are limited, and that it could give no guidance on EC without chemotherapy for lack of evidence. This is a funding position based on absence of evidence, not a study result. |
| CDA-AMC reimbursement review, report PC0428r, April 2026, PMID 42190031, NCBI Bookshelf NBK622601. Retrieved from the Bookshelf open-access archive (`pub/litarch`, package sha256 `e118688d…13a5`), 51 pages, sections on subsequent treatment read in full. | Full clinical and economic review based on the clinical study report, interim analysis 2 (cut-off 6 January 2025). | Confirms the figures already extracted from the NEJM supplement: in the EC + mFOLFOX6 arm 45.8% received subsequent systemic therapy, most often FOLFIRI-based regimens (24.2%), BRAF-inhibitor-based regimens (8.1%) and single-agent chemotherapy (7.2%). The consulted clinical experts regard FOLFIRI-based chemotherapy as the expected next line after progression on EC + mFOLFOX6 and judged subsequent therapy in the trial representative of practice. The review reports PFS2 per arm only. **It contains no outcome per subsequent regimen**, nothing on continuing EC beyond progression and nothing on maintenance after stopping oxaliplatin. The Supplemental Material (report PC0428s, 54 pages, PDF sha256 `a3c50332…0dec`, obtained by the repository owner through a normal browser on 2 October 2026) was read for tables 3, 9, 13 and 18. Table 13 is identical to NEJM table S4: of 236 patients, 108 received subsequent systemic therapy, FOLFIRI-based 57, BRAF-inhibitor-based 19, single-agent chemotherapy 17, CAPIRI 11, FOLFOX 10, trifluridine/tipiracil 10, other categories 3 or fewer each. Table 9 gives disposition at the same cut-off: 169 discontinued, 101 of them for progression. Table 3 records the expert view that a treatment is not typically re-introduced in a later line after progression on it. Table 18 gives PFS2 per arm only; the PFS2 curve is redacted. |
| NCT06884618 (RO7673396, protocol YO45758) | Registry record, update posted 28 September 2026 (previous: 21 April 2026). | Country list now includes the United Kingdom (Birmingham, London); Spain lists Pamplona, Barcelona (VHIO) and Madrid; Denmark lists Copenhagen. The Netherlands is still absent from ClinicalTrials.gov, while CTIS named NKI/AVL in round 3. Eligibility text still only requires RAS mutation(s) and does not address BRAF V600E with acquired RAS alterations. The open question from round 3 stands. |
| NCT04607421 (BREAKWATER) | Results posted on ClinicalTrials.gov since 11 June 2026. | Contains the PFS2 definition (progression after start of the next anticancer therapy, by investigator) and outcome tables per arm. No table of subsequent regimens with outcomes. PFS2 is not second-line PFS. |
| NCT06640166 (ECLYpSe), NCT07178717 (rechallenge), NCT07150403 (ULYSSE), NCT05355701, NCT05379985, NCT06607185 | Registry records. | No status change and no posted results since round 3. NCT06445062 was updated on 22 September 2026, still United States only. |
| PMID 42791169, Clin Colorectal Cancer 2026 | Population-based cohort from Alberta, 43 patients on encorafenib plus panitumumab, 2018 to 2023. Abstract only. | Later-line doublet, before first-line use existed. Does not address the sequence. |
| PMID 41690877, Clin Colorectal Cancer 2026 | Single case from the AGMT registry: EC rechallenge combined with nivolumab in pMMR disease. Title and record only, no abstract. | One selected case; not the first-line sequence. Not in the catalog. |

## Reading

The evidence gap named in rounds 1 to 3 is unchanged on 2 October 2026 within this search. The Canadian recommendation shows how one national committee handled the same gap: without data, no funded continuation of the targeted pair after progression. That is consistent with, and does not add to, the French expert-opinion pathway found in the 13 September review. The first prospective result on EC beyond progression is still expected from ECLYpSe, which concerns patients who received EC in second line.

## Next step

The public documents on BREAKWATER are now exhausted for this question: 19 patients received a BRAF-inhibitor-based regimen after first-line EC + mFOLFOX6 and 57 a FOLFIRI-based regimen, but no outcome is reported for either group. Only the sponsor holds those data; see the earlier data-request proposal of 13 September. Re-run this search after the ESMO congress of October 2026.

## Limits

Abstract-level reading for the PubMed records. Registry status is not site capacity. No patient data used. No treatment recommendation is made or implied.
