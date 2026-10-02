# Maintainer assessment of the independent co-mutation review

2 October 2026 · Issue #5 · Codex/ChatGPT. This assessment concerns the separate Claude review in [review.md](review.md), not a clinical validation of the original co-mutation analysis. The contributor report and its aggregate outputs were copied unchanged; source-response data at the sample level were not published.

## Decision

**Accept the report as an independently implemented review submission; request changes to the original analysis before treating its biological claims as established.** The report addresses the issue's selection flow, denominator, sample-order, panel-coverage, carrier-rule, uncertainty and background-comparison requirements. Its `raw/fetch-manifest.json` records 45 public API responses with request parameters, byte lengths and SHA-256 hashes. All 16 supplied artifact hashes in `raw/SHA256SUMS` matched the published scripts and aggregate files on this review. The report identifies the submitted source files by hashes because they are not in this repository.

I checked the published package for patient or sample identifiers, personal paths and email addresses; none was found. The scripts explicitly keep downloaded row-level cBioPortal responses in a local ignored cache, and `fetch.py` does not call the patient-level clinical endpoint. Publication of this package does not publish that cache. This is a content scan and code inspection, not an audit of every possible privacy risk in the external data source.

## Independent spot-check of the key CNA objection

I queried the [public cBioPortal API](https://www.cbioportal.org/api) directly using a separately written [aggregate-only script](../../scripts/spotcheck_msk_cna.py). It takes the first 100 sorted sample IDs from study `crc_msk_2026`, fetches panel assignments and gene lists, then requests the CNA `ALL` and `HOMDEL_AND_AMP` views. IDs remain in memory and are neither printed nor saved. The [result snapshot](../../results/msk-cna-spotcheck-2026-10-02.json) uses portal v7.1.2, backend commit `bbba61b2a45b3719187a310dcadaae75b9bef067`.

| Subset of 100 samples | Direct API count |
|---|---:|
| `ALL` rows | 22,695 |
| Zero-valued `ALL` rows | 22,535 |
| Zero rows on a gene *outside* that sample's panel | 6,705 |
| Samples with no `ALL` rows | 52 |
| Samples with no `HOMDEL_AND_AMP` rows | 52 |

This reproduces a counterexample to “explicit zero means measured absence”: a gene not included in a sample's assay cannot have a measured normal-copy call for that assay, yet the API returns zero rows there. A no-row sample has no explicit negative call in this API response. cBioPortal's [file-format documentation](https://docs.cbioportal.org/file-formats/) defines a stored discrete CNA value of 0 as neutral/no change; the observed off-panel API rows show why that definition cannot simply be assigned to every zero returned by this endpoint in this study. The precise API materialization mechanism remains unverified.

The 100-sample check does **not** independently establish the contributor's full-study totals of 1,367,542 `ALL` rows, 4,319 no-row samples, 87,147 off-panel zeros, or 318 `-1.5` calls omitted by `ALL`. Those remain documented results of the independent Claude implementation, with code and hashes for reproduction. I did not execute its full downloader or re-run its Fisher/BH analysis. Scientific conclusions based on mutation/CNA absence remain conditional on panel membership, locus callability and sample quality; the public API does not provide every needed locus-level measurement.

## Required follow-up

The original submission should incorporate the review's corrections: its control definition (5,342 strictly BRAF-unmutated patients versus 5,345 under the looser rule), actual selected-sample carrier rule, panel-aware denominators, CNA “no call” wording, grouping of four 20q amplifications as one chromosomal signal, and the control background for gain/loss. A separate review of those revised claims is still needed. Issue #5 should remain open and in review; publication of this assessment is not acceptance of a new treatment direction.
