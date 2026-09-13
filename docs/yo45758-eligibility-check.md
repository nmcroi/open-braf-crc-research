# YO45758: public eligibility clarification

> **13 September 2026 follow-up — registry display reconciled, site access still unconfirmed.** The rendered [CTIS Summary](https://euclinicaltrials.eu/ctis-public/view/2024-519622-20-00) was reopened and explicitly displays Netherlands “Authorised, recruiting”, France “Authorised, recruitment pending”, and 25/03/2026 in Denmark’s row. A separate reviewer’s API interpretation had assigned that recruitment date to France and could not establish the Dutch recruitment flag. Exact country IDs/JSON paths have been requested for reconciliation; an array-join error is a hypothesis, not an established explanation. Accessibility text does not preserve every blank date column, so the displayed Dutch 18/08/2026 date is not newly asserted as an independently verified API recruitmentStartDate. The public recruitment label confirms neither a vacant slot nor acceptance of acquired RAS alongside BRAF V600E. No site has been contacted.


13 September 2026 · TASK-0004 · Source review by ChatGPT/Codex; independent review pending.

**Outcome:** public summaries do not establish whether acquired RAS mutations coexisting with BRAF V600E after first-line encorafenib/cetuximab plus chemotherapy qualify. This remains a protocol/site question, not confirmed access. This addendum narrows the [round 3 lead](post-frontline-round3.md); it does not report treatment efficacy.

| Source and inspected surface | Observation | Limit |
|---|---|---|
| [ClinicalTrials.gov NCT06884618](https://clinicaltrials.gov/study/NCT06884618), full public API record fetched today; posted update 21 April 2026 | Requires confirmed RAS mutation(s). Describes monotherapy dose escalation/expansion; no documentSection was returned. | No explicit acquired-RAS/BRAF co-mutation rule, allele list, assay requirement or prior-EC cohort decision. No documentSection means no attached document in this response, not no protocol anywhere. |
| [Official CTIS 2024-519622-20-00](https://euclinicaltrials.eu/ctis-public/view/2024-519622-20-00), rendered Summary and Trial Documents tabs | Netherlands remains labelled authorised/recruiting. Protocol/synopsis section and each displayed country document section report no attached documents. | Country status is not site capacity. The displayed attachment absence limits this route to the full protocol. |
| [Yale investigator page](https://medicine.yale.edu/center-clinical-investigation/trial/a-phase-i-study-of-ro7673396-in-patients-with-advanced-solid-tumors/?tab=healthPro), Health Professionals tab opened in browser; page dated 24 June 2026 | Six inclusion bullets including RAS confirmation; nine exclusion bullets. The acid-reducing-agent exclusion present in CT.gov was not displayed here. | An institutional summary is not a complete substitute for the protocol. Missing exclusion text is not evidence that a restriction was removed. No acquired-RAS/BRAF answer. |
| [NYU KRAS trial list](https://nyulangone.org/care-services/kras-excellence-initiative/kras-clinical-trials), RO7673396 entry | Listed under KRAS G12V and marked pending. | This local listing may reflect a selected cohort, curation or stale information. It does not establish a worldwide G12V-only rule or the Dutch cohort criteria. |
| [Roche two-page summary](https://forpatients.roche.com/content/patient-platform/global/en/trials/cancer/tumor/a-study-to-evaluate-the-safety--tolerability--pharmacok-47960.pdf), both pages read | Identifies itself as information taken from public registries and gives summary eligibility. | A registry-derived summary, not an independently obtained full protocol. Counting it as another confirmation would overstate source independence. |

## Questions that would resolve the enrollment lead

1. Does the currently open cohort accept acquired RAS mutations in BRAF V600E CRC after EC plus chemotherapy? Which RAS alleles and prior treatments are permitted?
2. What molecular assay, specimen type, sampling date and detection threshold satisfy screening? Can existing results answer this before new sampling is considered?
3. Which CRC cohort is actually open locally: monotherapy or a named combination? Is there screening capacity and a potential place?
4. Which current protocol version governs eligibility, organ function and concomitant medications?

A protocol exclusion or lack of a matching open cohort would remove this specific enrollment route. No outreach, enrollment, treatment interruption or testing recommendation was made. These sources alone cannot determine individual eligibility or benefit.

## Bounded search and reproducibility

English web searches on 13 September: `"YO45758" "BRAF"`; `"RO7673396" "acquired" mutation`; `"YO45758" protocol filetype:pdf`; `"RO7673396" "G12V"`. Relevant primary results above were opened; no full protocol resolving the question was found. The Yale professional tab required browser interaction; web extraction of its parameterized URL failed, but the rendered tab was successfully read. No claim of worldwide absence is made.

Public metadata can be refreshed without credentials at `https://clinicaltrials.gov/api/v2/studies/NCT06884618`. The retrieval hash and structured observations are in [the audit record](../results/yo45758-eligibility-check.json). Original source files stay outside the public repository. This is document verification, not independent clinical validation.

**Next action:** obtain the exact cohort answer via an authorized clinical discussion or new public protocol. Do not repeat the same summaries as a new research result while those inputs are unchanged.
