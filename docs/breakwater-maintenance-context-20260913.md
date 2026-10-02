# Progression during maintenance: what BREAKWATER actually documents

13 September 2026 · TASK-0004 · AI-assisted source review by ChatGPT/Codex · **Independent review pending.**

**Finding:** the public BREAKWATER protocol explicitly accommodates treatment after chemotherapy-component withdrawal and selected continuation after progression. These provisions identify a clinically relevant subgroup to investigate; they do not demonstrate that reintensification or continuing EC improves its outcomes.

## Primary documents and verified provisions

[NCT04607421](https://clinicaltrials.gov/study/NCT04607421) provides protocol amendment 7, dated 31 May 2024, and statistical analysis plan (SAP) version 7, dated 7 May 2024. Both were publicly uploaded on 25 February 2026; the retrieved registry's last posted update is 11 June 2026. This review does not establish whether later unposted amendments exist.

| Document and location | What was verified | Limit on interpretation |
|---|---|---|
| [Protocol](https://cdn.clinicaltrials.gov/large-docs/21/NCT04607421/Prot_000.pdf), section 6.6.3, p111 | In phase 3 Arm B, 5-FU plus encorafenib/cetuximab could continue after permanent oxaliplatin discontinuation. EC could continue after all mFOLFOX6 was stopped. | A permitted dose-modification pathway, not a randomized comparison of maintenance strategies. |
| Same protocol, section 7.1, pp120–122 | Progression is a discontinuation criterion, but continuation was allowed for participants still deriving clinical benefit, with favorable risk/benefit and sponsor discussion. Continuing pending central confirmation is a separate provision. | Permission does not establish how many continued or their outcomes. It does not show that adding irinotecan or restarting oxaliplatin reverses resistance. |
| [SAP](https://cdn.clinicaltrials.gov/large-docs/21/NCT04607421/SAP_001.pdf), section 6.5.3, pp84–86 | Exposure duration uses first and last dose dates, with drug-specific dosing-period adjustments. Drug-level dose changes are summarized separately. | Calendar exposure is not uninterrupted dosing or an individual's maintenance duration. |
| Same SAP, sections 6.4 and 6.5.5, pp79–80 and 87–88 | Listed efficacy subsets concern baseline factors/countries; subsequent therapies are tabulated. | No planned post-maintenance progression subgroup was located in these sections. This does not prove no such analysis was ever performed. |

Protocol pp111 and 121 were checked visually as well as in extracted text. Selected relevant sections were read; this is not a complete protocol/SAP audit. All these documents describe **one trial**, not independent confirmation cohorts.

## Published exposure data support asking the more specific question

[BREAKWATER, NEJM 2025](https://doi.org/10.1056/NEJMoa2501912), PMID40444708 / PMC12197837, supplementary Table S6: phase 3 EC+mFOLFOX6 safety population, **232 participants**. These are author-reported descriptive statistics, not a new patient-level analysis.

| Drug | Median exposure, weeks | Exposure ≥6 months, n/N (%) |
|---|---:|---:|
| Encorafenib | 49.4 | 169/232 (72.8%) |
| Cetuximab | 49.1 | 168/232 (72.4%) |
| Fluorouracil | 37.5 | 152/232 (65.5%) |
| Oxaliplatin | 21.3 | 67/232 (28.9%) |

The drugs had different exposure distributions. Subtracting their medians would **not** estimate individual maintenance duration. The table neither identifies intentional maintenance nor links withdrawal, progression and subsequent outcome. No confidence intervals for these medians are supplied in S6.

Table S7 adds a coding trap: 48/232 (20.7%) represents adverse-event-related permanent discontinuation of **all drugs in the grouped other-intervention category**, not the number stopping oxaliplatin. Permanent cessation of some, but not all, grouped drugs is classified under interruption. This footnote prevents counting a maintenance subgroup from that percentage.

## Current European guidance is an important counterweight

[ESMO 2026, PMID41990853](https://pubmed.ncbi.nlm.nih.gov/41990853/), DOI10.1016/j.annonc.2026.03.005, explicitly discusses FOLFIRI plus an antiangiogenic after first-line FOLFOX–EC (p766). This adds a professional guidance source to the [TNCD sequence review](post-frontline-sequence-20260913.md), not a new exact-sequence trial result.

The maintenance section distinguishes bevacizumab-based pathways from FOLFOX–anti-EGFR pathways. For progression during anti-EGFR plus 5-FU maintenance, it favors a conventional second-line regimen and states that benefit from reintroducing the same chemotherapy–anti-EGFR regimen is unestablished (p765). That paragraph is not a dedicated EC-maintenance subgroup analysis; it nevertheless argues against assuming that maintenance progression automatically supports reintroduction.

Access: publisher full text returned 403 and its API returned metadata only. Relevant prose was subsequently read in a [coauthor-uploaded full-text rendering](https://www.researchgate.net/publication/403801014_Metastatic_colorectal_cancer_ESMO_Clinical_Practice_Guideline_for_diagnosis_treatment_and_follow-up), uploaded 25 June 2026. Title, DOI and authors match PubMed/publisher metadata. Figures were not visually verified. Publication-era regulatory statements were not treated as current access information.

## The analysis that could answer the missing question

Proposed analysis specification, **not an analysis already performed**:

1. Within the original first-line EC+mFOLFOX6 arm, identify progression while still on full treatment versus progression after documented oxaliplatin withdrawal while EC, with or without 5-FU, continued. Keep temporary delays, permanent withdrawal, unclear status and stop reasons separate. Use an explicit dosing window, not an assumption from the assigned arm.
2. For the maintenance-progression group, report subsequent choices separately: oxaliplatin reintroduction with EC; a chemotherapy switch while EC continues; a switch without EC; local treatment with EC continuation; other therapy; no further treatment. Count people and treatment sequences distinctly, with missingness and censoring visible.
3. Report evaluable response denominators and outcomes from **start of that subsequent strategy**, with follow-up, confidence intervals and toxicity. PFS2 from original randomization is not interchangeable with this endpoint. Include the interval from progression to the next strategy and those unable to start it.
4. Treat comparisons as observational: fitness, earlier response, withdrawal reason, neuropathy, time off oxaliplatin and extent of progression may determine selection. Baseline survival comparisons between eventual maintenance and non-maintenance groups risk immortal-time bias. A suitable landmark or time-varying design and statistical review are needed; small or incomparable groups may support description only.

The protocol/SAP document relevant categories of dosing, progression and follow-up collection. Their existence makes a sponsor-side feasibility assessment reasonable; **completeness, linkability and availability of these data have not been verified**. Start by requesting permitted aggregate tables, not restricted individual records. No external request was sent.

## Search boundary and unresolved sources

The [audit record](../results/breakwater-maintenance-context-20260913.json) records the search queries, versions and file hashes. No exact post-maintenance regimen-specific outcome cohort was located in this bounded search. The already reviewed ECLYpSe design concerns progression after second-line EC; first-line EC+FOLFIRI efficacy does not answer salvage after EC+FOLFOX maintenance.

The ESMO author-upload route recovered the relevant prose despite the publisher access failure. Its PDF download failed; no locally preserved full ESMO PDF or visual figure audit is claimed. No result was inferred solely from search snippets.

EMA assessment reports were downloaded and searched in selected treatment-modification sections, without an exact subgroup outcome located; they are regulatory views of the same trial. A local FDA review download returned 404, although indexed text was available. These checks are not exhaustive reviews of all regulatory attachments.

**Consequence:** explicitly distinguish progression during maintenance from progression during the full induction regimen when asking for evidence. Neither the protocol permission nor the exposure table establishes benefit from continuing or restarting a particular drug for an individual.
