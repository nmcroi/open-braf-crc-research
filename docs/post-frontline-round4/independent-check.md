# Independent check of round 4 (2 October 2026)

Codex/ChatGPT checked selected claims in Claude's [round-4 report](post-frontline-round4.md). This is a bounded second reading, not an independent replication of the full PubMed search or a clinical recommendation.

## PC0428s opened and read

The owner-provided local PDF `PC0428s-Braftovi_Supplemental_Material.pdf` was opened and pages 14, 21–24 and 30–31 were checked against extracted text and rendered page images. It is 54 pages, authored by the Canadian Agency for Drugs and Technologies in Health, SHA-256 `a3c50332b6f08822aca8e9a9844c2cc6f62120e7fac72c44e01b9f3f4d670dec`. Its macOS download provenance points to the [official CDA-AMC supplemental PDF](https://www.cda-amc.ca/sites/default/files/DRR/2026/PC0428s-Braftovi_Supplemental_Material.pdf). Automated re-fetch returned HTTP 403 on this date; the local copy is not redistributed here. The [parent clinical review](https://www.ncbi.nlm.nih.gov/books/NBK622601/) references the same supplemental tables.

| Locator | Directly observed | Limit |
|---|---|---|
| Appendix 1, table 3, p. 14/54 | Consulted clinical experts state that treatment is not typically reintroduced in a later line after progression on it; discontinuation for another reason can permit downstream use. | This is expert input in a reimbursement review, not a trial result or a universal rule. |
| Appendix 4, table 9, pp. 21–22/54 | In the EC + mFOLFOX6 arm, 236 randomized, 169 discontinued, including 101 for progressive disease, at the 6 January 2025 cutoff. | Discontinuation and progression are different denominators. |
| Appendix 4, table 13, p. 24/54 | Among 236 randomized to EC + mFOLFOX6, 108 (45.8%) received any subsequent systemic treatment. FOLFIRI ± combination: 57 (24.2%); BRAF inhibitor ± combination: 19 (8.1%); single-agent chemotherapy ± combination: 17 (7.2%). | The percentages use all 236 randomized patients, not the 108 treated subsequently. Categories can overlap and are not outcomes of these regimens. |
| Appendix 4, table 18, pp. 30–31/54 | PFS2 median by randomized arm: 20.7 months (95% CI 19.0–23.9) vs 12.7 months (11.2–13.7). | Measured from initial randomization and pooled across later treatments; not second-line PFS or evidence that FOLFIRI or BRAF inhibitor retreatment works after EC + mFOLFOX6. PFS2 was assessed by investigators. |

The table does not break down outcomes by subsequent regimen. That supports the narrow negative conclusion in the round-4 report. It does not establish that no such data exist elsewhere or within the sponsor's unpublished records. The original study population and treatment line remain essential when comparing these figures with any later-line evidence.

## Registry checks

- The [ClinicalTrials.gov API record for NCT06884618](https://clinicaltrials.gov/api/v2/studies/NCT06884618), retrieved on 2 October 2026, shows a last-posted update of 28 September 2026, sites in Barcelona, Madrid, Pamplona, Birmingham and London, and no Netherlands site in that registry. The eligibility text mentions RAS mutations but does not explicitly settle coexistence with BRAF V600E after acquired resistance. This is not a determination of eligibility or available places; the separate CTIS Netherlands discrepancy remains open.
- The [ClinicalTrials.gov API record for NCT04607421](https://clinicaltrials.gov/api/v2/studies/NCT04607421) shows posted results and a PFS2 measure, but the public outcome module does not give subsequent-regimen efficacy tables. Its last posted update was 11 June 2026 at this check.

The five PubMed queries and nine tracked records in the contributor's snapshot are preserved alongside the original report. I did not independently rerun all five queries or read every newly returned abstract. The Canadian recommendation itself was checked through the supplemental material's expert-response table, while this review did not independently obtain the recommendation PDF.
