# Reinduction after maintenance: testing whether adjacent evidence transfers

13 September 2026 · TASK-0004 · ChatGPT/Codex source review · **Independent review pending.**

**Result:** adjacent anti-EGFR studies support separating ongoing EGFR exposure from an EGFR-free interval. They do not establish the benefit or futility of reintensification after first-line EC-containing maintenance in BRAF V600E disease. This check follows the [BREAKWATER protocol and ESMO review](breakwater-maintenance-context-20260913.md).

## PanaMa: maintenance randomization is not salvage randomization

[Final PanaMa analysis](https://doi.org/10.1016/j.eclinm.2024.103004), PMID39802302 / PMC11719858, NCT01991873: RAS-wild-type mCRC, FOLFOX–panitumumab induction, then maintenance with 5-FU/folinic acid with or without panitumumab. No encorafenib was used.

| Prior maintenance | Received reinduction / maintenance population | Responses during reinduction |
|---|---:|---:|
| 5-FU/folinic acid + panitumumab | 50/125 | 4/50 (8.0%) |
| 5-FU/folinic acid | 78/123 | 28/78 (35.9%) |

Author-reported final-analysis counts (Table 2); reinduction was FOLFOX–panitumumab. Response denominators include non-evaluable participants. These are not individual response probabilities or a randomized comparison of reinduction against switching. Only 128/248 received reinduction, creating selection concerns. The trial's reinduction-PFS clock starts at progression during maintenance, not the first reinduction dose; do not mix it with differently defined endpoints.

The [initial report](https://doi.org/10.1200/JCO.21.01332), PMID34533973 / PMC8683209, explicitly says BRAF-mutated tumors were included and their subgroup data were not yet available. Calling the whole trial BRAF-wild-type would be inaccurate. No BRAF V600E/EC-specific salvage estimate was established here. Initial and final reports are the **same cohort** with updated counts.

## Valentino: a favorable result in selected patients is not evidence for BRAF V600E

[Valentino reinduction analysis](https://doi.org/10.1093/oncolo/oyab012), PMID35305093 / PMC8842305, NCT02476045: post-hoc analysis of 159 participants receiving post-progression therapy. Table 1 reports **0 BRAF-mutated tumors among 42 receiving anti-EGFR reinduction**, versus 5/117 in the alternative-treatment group. Subsequent matched comparison excludes BRAF-mutated cases.

Treatment choice was observational, associated with favorable clinical features. It cannot establish comparative salvage efficacy in BRAF V600E, and no EC-containing induction was studied. A separate internal table/prose discrepancy concerning the anti-EGFR-free interval was noticed; that interval was not used quantitatively in this review. Positive reinduction results should not be imported without their selection criteria.

## A 2026 pooled analysis still does not answer the EC question

[Anti-EGFR maintenance versus stop and go](https://doi.org/10.1016/j.esmoop.2026.107775), PMID42269232 / PMC13273794: selected **378** participants from PanaMa, Valentino, PRODIGE-28-TIME and IMPROVE. Eligibility explicitly excludes BRAF V600E and right-sided tumors; known MSI-H is excluded, which is not equivalent to confirming MSS in everyone.

It reuses patients from the earlier trials. It is not independent confirmation of PanaMa/Valentino and is not a new BRAF V600E cohort. Table 1 also shows different chemotherapy backgrounds: all 103 stop-and-go participants had irinotecan-based induction, while all 166 receiving 5-FU/anti-EGFR maintenance had oxaliplatin-based induction. This limits causal interpretation of a cross-trial strategy comparison even with adjustment. No pooled survival estimate is transferred to the EC population.

## What this changes

Retain the specific research question: **after oxaliplatin withdrawal, did progression occur during continued EC exposure, and what happened after each subsequent strategy?** Neither a favorable report from molecularly selected BRAF-wild-type patients nor poor aggregate reinduction outcomes without BRAF blockade settles that question.

The final PanaMa article gives a sponsor-mediated route for a scientifically sound data proposal. It is an accessible methodological comparison dataset, not a substitute for post-EC data. No data request or external contact was made, and no patient-level files were accessed. The useful next evidence would be a properly defined EC-maintenance subgroup or a prospective strategy comparison.

Full XML files were retrieved through Europe PMC; methods, relevant results/tables and limitations were checked, not all supplements. Source identities/hashes and checks are in the [audit record](../results/breakwater-maintenance-context-20260913.json). No newly calculated survival analysis is claimed.
