# Issue 1 — source identifier corrections (2 October 2026)

AI-assisted check by Codex, independently recalculated from the public catalog after Claude's proposed corrections. Baseline: commit `1c3ef94`, 516 entries. No patient or restricted research data were used. This is an identifier audit, **not** a review of the scientific conclusions or a check that each identifier is the article intended by the original private library note.

## Checks and changes

| Check | Evidence and result | Change |
|---|---|---|
| Counts | Parsed all 516 rows independently: 297 unique PMIDs, 149 unique NCTs, 62 DOI-only rows, one entry without a link. | Post-correction: 515 rows, 314 unique PMIDs, 149 unique NCTs, 515 links and 507 distinct sources after eight same-source links. The 508 figure applies only if the non-source note S0352 is retained. |
| 17 missing PMIDs | Re-fetched the 17 proposed PMIDs in one batch from [PubMed ESummary](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=41648030,39145064,39255538,38777726,38833658,41648647,39620921,39153969,41165465,40025995,40616773,40676860,40739424,41647992,41115464,41768137,41566838&retmode=json). Each catalog DOI matches the corresponding PubMed DOI. Sixteen titles match after whitespace/punctuation normalization; S0299 has a more specific title in PubMed. | Added PMIDs and PubMed links; corrected S0299 to PubMed's title with “BRAF (V600E)”. The old “Conference abstracts” category is preserved pending a taxonomy cleanup; a PMID alone does not establish publication type. |
| Six malformed DOI URLs | For S0303, S0309, S0313, S0328, S0329 and S0340, the stored DOI began with `https://doi.org/`, and the source link repeated that prefix. | Normalized DOI and link. |
| Eight repeated sources | Seven pairs have identical normalized DOI; S0353's landing-page DOI equals S0350's DOI. | Kept both category rows and added [`sources/duplicate-links.csv`](../sources/duplicate-links.csv), so eight rows count once in source-level calculations. This does **not** mean eight independent studies were removed. |
| S0352 | Has no PMID, DOI, NCT or URL and describes a search note rather than an external source. | Removed from the bibliographic catalog. Its historical ID is not reassigned. |

The transformations are reproducible with [`scripts/apply_source_identifier_corrections.py`](../scripts/apply_source_identifier_corrections.py), run immediately after a fresh library import. [`scripts/validate.py`](../scripts/validate.py) now verifies counts, duplicate links and absence of doubled DOI URLs. The source graph under `sources/records.json` is a separate curated set and is unchanged; no downstream claim is automatically promoted by this catalog cleanup.

## Open discrepancies and limits

- S0284 is labeled CIViC but links to [PMID 31566309](https://pubmed.ncbi.nlm.nih.gov/31566309/), already S0001; the correct CIViC page has not been established. S0288 retains a placeholder title. They remain visibly unresolved, not silently repaired.
- PubMed title/DOI matching is partly circular because titles were imported from PubMed. A source-to-original-note comparison remains unperformed. No full articles were read for this identifier check.
- ClinicalTrials.gov and Crossref-wide baseline checks in Claude's proposal were not independently re-run here. The NCT count was recomputed from the catalog, not a fresh review of all registry records. Identifier-level review is therefore narrower than the issue's full acceptance criteria.
- No recruitment or patient-level eligibility decision is implied.
