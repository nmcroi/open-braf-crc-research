# BREAKWATER: a bounded request for post-maintenance outcomes

Prepared 13 September 2026, with ChatGPT assistance. **Unsent draft; no data access granted, no sponsor contacted.** This proposes a descriptive analysis, not a treatment recommendation or a claim of an effective salvage regimen.

## Verified access route

[Pfizer's official data-request page](https://www.pfizer.com/science/clinical-trials/trial-data-and-results/data-requests) directs researchers to [Pfizer's Vivli member page](https://vivli.org/ourmember/pfizer/). That page specifies a qualified research team including a biostatistician, proposal review and a data-use agreement. Approved analyses run in the secure Vivli environment. Its general timing rule is 18 months after study completion. Questions go to CTD@Pfizer.com. This is a route for enquiries, not confirmation that BREAKWATER is available today.

The [NCT04607421 record](https://clinicaltrials.gov/study/NCT04607421), checked 13 September (last posted update 11 June 2026), reports ACTIVE_NOT_RECRUITING; actual primary completion 1 March 2025 and estimated study completion 28 December 2027. The primary-completion date must not be substituted for study completion to calculate availability. The record says IPD sharing is planned subject to Pfizer's criteria. No immediate entitlement or earliest guaranteed release date is inferred.

**Practical first step:** ask whether the sponsor can supply an existing or newly prepared aggregate table for this specific subgroup, or confirm the appropriate route and timing. No participant-level records are requested in this initial enquiry. Any future restricted-data use requires a separately approved plan; a permission to access does not imply permission to send records to cloud AI systems.

## Draft enquiry

Subject: BREAKWATER NCT04607421 — availability of aggregate outcomes after progression during EC maintenance

Dear Clinical Trial Data Sharing team,

We are preparing a source-based research review of treatment sequencing after first-line encorafenib/cetuximab plus mFOLFOX6 in BRAF V600E metastatic colorectal cancer. The published supplementary Table S4 reports subsequent treatment use but not efficacy by subsequent regimen. The protocol permits continuation of fluorouracil plus EC or EC after discontinuation of oxaliplatin or mFOLFOX6.

Could you confirm whether an aggregate analysis is available for participants with first progression after oxaliplatin had been permanently discontinued, while encorafenib/cetuximab with or without fluorouracil remained ongoing? If available, we would be interested in the subgroup denominator, actual next systemic regimen, continued EC components, response-evaluable denominators, response and time-to-event outcomes measured from subsequent-treatment initiation, with follow-up and uncertainty.

If these outcomes have not been reported, could you advise whether an aggregate analysis or a formal proposal through Vivli would be the appropriate route, and whether this ongoing study is currently eligible for a request? We are not requesting patient-level data or implying that an eligible research team or data-use agreement has already been established.

Thank you.

[Sender to add their own name and affiliation accurately before sending.]

## Proposed cohort and data specification

1. Start with the randomized EC + mFOLFOX6 arm. State data cut-off, follow-up and all exclusions.
2. Reconstruct actual component exposure; distinguish permanent oxaliplatin withdrawal from a delayed/interrupted cycle. Record reason and time of withdrawal. Split EC + fluorouracil maintenance from EC-only maintenance. Do not define maintenance by subtracting median exposure durations.
3. Identify first documented progression while on maintenance. Define how dose gaps, scan dates, investigator versus central review and therapy beyond progression are handled. Show sensitivity to alternative gap definitions; do not choose a threshold after inspecting outcomes.
4. Produce a flow table: arm population → withdrew oxaliplatin before progression → maintenance type → progressed → received subsequent treatment / did not / unknown. Account for ongoing follow-up and death before subsequent treatment.
5. Define the **first** subsequent regimen from start dates and components. Distinguish FOLFIRI with antiangiogenic therapy, reintensification with oxaliplatin, continuation of EC with changed chemotherapy, other therapy and unknown. Keep later lines separate. Count unique patients; S4 categories are not a disjoint next-regimen classification.
6. For each adequately sized group, report treated, response-evaluable and missing counts, response definition, confidence intervals, progression/death events and follow-up. Subsequent PFS/OS starts at subsequent-treatment initiation; optionally report time from maintenance progression separately. Never call randomization-to-PFS2 a duration of benefit on the next regimen.
7. Record relevant baseline and decision-time confounders, including performance status, disease sites/burden, prior response, induction and maintenance duration, oxaliplatin-stop reason, neuropathy and local interventions. Small groups and suppressed cells remain explicitly unavailable.

## Interpretation limits and next milestone

This is an observational comparison among selected survivors reaching a subsequent line, not a randomized comparison of salvage choices. Confounding by indication, time-dependent selection and missing outcomes prevent a simple ranking of regimens. The first deliverable should be a feasibility/count table. An experienced oncology biostatistician should decide whether any adjusted comparison is supported. No raw records, authors' unpublished tables or restricted outputs should be posted without the applicable permission and disclosure review.

Primary context: [BREAKWATER publication, DOI 10.1056/NEJMoa2501912](https://doi.org/10.1056/NEJMoa2501912), original supplement S4; [protocol](https://cdn.clinicaltrials.gov/large-docs/21/NCT04607421/Prot_000.pdf), PDF pp.111 and 121; [our bounded source audit](breakwater-maintenance-context-20260913.md).
