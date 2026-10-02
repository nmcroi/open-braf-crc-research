# Independent review: co-mutation patient selection and assay coverage (issue 5)

Reviewer: Claude (Anthropic), working for the repository owner. Date of review and of all data retrieval: 2 October 2026.

Subject: the submitted analysis "MSK-IMPACT co-occurring alterations: what accompanies BRAF V600E in MSS colorectal cancer" on the public cBioPortal study `crc_msk_2026`.

Scope: public, de-identified data only. This review contains aggregate counts only. No patient or sample identifier, no row-level record, no survival field. The patient-level clinical endpoint (which holds survival fields) was never requested. Nothing here is treatment advice or a statement about prognosis.

## Summary of the verdict

| # | Submitted claim | Verdict |
|---|---|---|
| 1 | 7,237 samples, all profiled for mutations and copy number on four panel versions | Confirmed |
| 2 | 260 patients with BRAF V600E and microsatellite-stable disease | Confirmed |
| 3 | 5,345 microsatellite-stable patients "with no BRAF mutation of any kind" | Deviating: 5,342 under the stated definition |
| 4 | One patient has V600E in the primary and not in a later metastatic sample | Confirmed |
| 5 | 475 features tested, 26 at q < 0.05 (carrier rule); 24 under the first-sample rule | Confirmed as arithmetic of the submitted rule; the count depends on the test family (my family: 744 tested, 27 significant) |
| 6 | The ten rows of the effect table | Confirmed (differences of at most 0.1 percentage point, caused by claim 3) |
| 7 | Both KRAS-positive patients disappear under the first-sample rule; the KRAS mutation sits in a later metastatic sample | Confirmed |
| 8 | "Nineteen patients in this group have more than one sample", all nineteen differ between samples | Confirmed only for a restricted sample subset; 20 by all stable samples, 26 by all samples. "All differ" is uninformative: 85% of control pairs differ too |
| 9 | Every named gene is on all four panels | Confirmed for the panel gene lists |
| 10 | "An absent alteration is therefore an absent event and not an unmeasured one" | Deviating: not supported in this generality (AMER1 on IMPACT341; three significant features on genes missing from a panel; copy-number absence is not a call) |
| 11 | Panel version changes in 136 of 391 multi-sample patients | Confirmed |
| 12 | Lexicographic order equals specimen-number order in 391 of 391; no date is exposed | Confirmed, but true by construction and not evidence of chronology |
| 13 | Zero of 260 is an upper bound of roughly 1.1% at 95% confidence | Confirmed as a one-sided bound (1.15%); the two-sided exact bound is 1.41% |
| 14 | "If loss is as frequent as gain, the observation is noise" | Not supported as an inference; see section 5 |
| 15 | Data retrieved 11 September 2026 | Not testable by me; see "Not checked" |

## What was reviewed: exact source data and code version

**Source data.** cBioPortal public API, `https://www.cbioportal.org/api`, study `crc_msk_2026`. Portal version v7.1.2, backend commit `bbba61b2a45b3719187a310dcadaae75b9bef067`, study import date 2026-09-01 03:22:16. Retrieved 2026-10-02 between 20:10 and 20:23 UTC. 45 responses; endpoint, request body, byte count and SHA-256 of every raw response body are in `raw/fetch-manifest.json`. The main ones:

| Response | Endpoint | Records | SHA-256 (first 16 hex) |
|---|---|---:|---|
| samples | `GET /studies/crc_msk_2026/samples?projection=DETAILED` | 7,237 | `52c4c1eee18103d5` |
| sample clinical data | `GET /studies/crc_msk_2026/clinical-data?clinicalDataType=SAMPLE` | 110,383 | `cb71c1cd74127f80` |
| mutations | `POST /molecular-profiles/crc_msk_2026_mutations/mutations/fetch?projection=DETAILED`, body `{"sampleListId":"crc_msk_2026_all"}` | 118,086 | `c2f795ae0a1498bf` |
| copy number, default events | `POST /molecular-profiles/crc_msk_2026_cna/discrete-copy-number/fetch?discreteCopyNumberEventType=HOMDEL_AND_AMP` | 12,657 | `b869c476648327ff` |
| copy number, all values | same endpoint with `discreteCopyNumberEventType=ALL`, 29 batches of 250 sorted sample IDs | 1,367,542 | per batch in manifest |
| gene panel assignment | `POST /molecular-profiles/{mutations,cna,structural_variants}/gene-panel-data/fetch` | 7,237 each | in manifest |
| gene panel content | `GET /gene-panels/IMPACT341`, `410`, `468`, `505` | 341, 410, 469, 505 genes | in manifest |
| stored copy-number values, targeted | `POST /molecular-profiles/crc_msk_2026_cna/molecular-data/fetch` | 24,949 | `2bf766b520252b0f` |

The samples and the default copy-number response were fetched a second time and gave byte-identical hashes. The other hashes were not re-tested for stability.

**Submitted material reviewed** (local copies in the private workspace; SHA-256):

- `findings-msk-comutations.md`: `b9edf8f4c44651bb163c421de66035160cb704e07b345da955c08e4f2c414d0e`
- `analyses/msk-comutations/comutations.py`: `4c3a94dc1e2ac848eeff024749b7abeeca34283388c8ac728dbf30342234c4bb`
- `results/msk-comutations.json`: `82e02a4800815b10cdc062097626ccb3fa0412674adc20a90ac3c4b533e2f18b`

None of these three files is present in the public repository at `origin/main` commit `e855da32b06bf990b155da4784e053190fdbf52d`; the only trace there is the record `REVIEW-MSK-SUBMISSION` in `reviews/records.json`. The hashes above are therefore the only version identifier.

**My code.** `scripts/fetch.py`, `scripts/analyze.py`, `scripts/replicate_submitted_rule.py`. Python 3.13, standard library only. SciPy 1.18.1 was used only to cross-check my Fisher exact test (1,470 tables, largest relative difference 1.9e-11). Hashes are in `raw/SHA256SUMS`.

## Order in which I read and did things

1. Read the workspace rules and `findings-msk-comutations.md` only.
2. Wrote `fetch.py` and `analyze.py` from scratch and ran them. While doing so I tried several group definitions and saw which ones give 260 and 5,345. My choice of "all Stable samples of a patient" as primary universe was made at this point, knowing the submitted totals but not the submitted code.
3. Saved a snapshot of my output. The selection flow and the named-feature table in `raw/` are byte-identical to that snapshot.
4. Only then opened `comutations.py`, `msk-comutations.json`, the earlier internal recount notes and the review record.
5. Wrote `replicate_submitted_rule.py`, which re-states the submitted rule in my own code on my own download. I did not execute the submitted script.
6. Added after step 4: the control prevalence by panel version, the panel dropout scan, the purity strata, the 20q co-occurrence count and the MSI mix. The patient-level direction count and the KRAS baseline comparison were planned before step 4 and coded after it.

## Comparison table

Carrier rule unless stated. "Mine" uses all Stable samples of a patient and the strict control definition.

| Quantity | Submitted | Mine | Difference | Explanation |
|---|---:|---:|---:|---|
| Samples in study | 7,237 | 7,237 | 0 | |
| Patients in study | not stated | 6,789 | | |
| Patients with more than one sample | 391 | 391 | 0 | |
| Stable samples with V600E | not stated (283 in code) | 283 | 0 | |
| BRAF V600E MSS patients | 260 | 260 | 0 | |
| MSS patients without any BRAF mutation | 5,345 | 5,342 | 3 | Submitted rule keeps a patient who has at least one BRAF-free Stable sample; three of them carry a non-V600E BRAF mutation in another Stable sample |
| Same, before removing the V600E group | 5,346 | 5,346 under the submitted rule | 0 | Reproduced |
| Controls under a first-sample rule | 5,345 | 5,343 | 2 | Submitted "first" is the first BRAF-free Stable sample, not the patient's first Stable sample |
| BRAF group patients with more than one sample | 19 | 20 (Stable samples), 26 (any sample) | 1, 7 | Submitted count uses V600E-positive Stable samples only |
| Features tested, carrier | 475 | 744 | | Different family: submitted tests mutations and amplifications with at least 15 carriers, all denominators fixed. Mine adds deep deletions, threshold 5, coverage-aware denominators |
| Features q < 0.05, carrier | 26 | 27 | | 23 shared. Only submitted: KMT2C, CTNNB1, PTPRD (q 0.06 to 0.17 in my family). Only mine: INSR amp, PAX5 amp, RNF43 deletion, ZNRF3 deletion |
| Features tested and significant, first sample | 468 and 24 | 726 and 28 | | Same reason |
| Submitted rule re-implemented on my download | 475/26 and 468/24 | 475/26 and 468/24 | 0 | Identical feature lists and identical carrier counts for all 26 and 24 features |
| KRAS mutation | 2/260, 47.7% | 2/260, 2,544/5,342 = 47.6% | 0.1 pt | Control definition |
| NRAS mutation | 1/260, 4.2% | 1/260, 222/5,342 = 4.2% | 0 | |
| APC mutation | 31.2%, 79.9%, ratio 0.4 | 81/260 = 31.2%, 4,266/5,342 = 79.9%, ratio 0.39 | 0 | |
| AMER1 mutation | 1.2%, 5.6%, ratio 0.2 | 3/260 = 1.2%, 300/5,342 = 5.6%, ratio 0.21 | 0 | But see section 3: AMER1 is unreported on IMPACT341 |
| RNF43 mutation | 22.3%, 2.4%, ratio 9.3 | 58/260 = 22.3%, 127/5,342 = 2.4%, ratio 9.4 | 0.1 | Control definition (128/5,345 submitted) |
| AKT1 mutation | 5.8%, 0.8%, ratio 7.5 | 15/260, 41/5,342, ratio 7.5 | 0 | |
| TGFBR2 mutation | 5.8%, 1.4%, ratio 4.1 | 15/260, 75/5,342, ratio 4.1 | 0 | |
| SMAD4 mutation | 23.1%, 14.8%, ratio 1.6 | 60/260, 788/5,342 = 14.8%, ratio 1.6 | 0 | |
| MYC amplification | 10.8%, 5.1%, ratio 2.1 | 28/260, 271/5,342 = 5.1%, ratio 2.1 | 0 | |
| SRC amplification | 0%, 4.8% | 0/260, 258/5,342 = 4.8% | 0 | |
| ASXL1, DNMT3B, TOP1 amplification in BRAF group | 0 | 0, 0, 0 | 0 | Controls: 282, 261, 198 |
| KRAS carriers, first-sample rule | 0 | 0 | 0 | |
| Panel change among multi-sample patients | 136/391 | 136/391 | 0 | |
| Lexicographic order differs from specimen number | 0/391 | 0/391 | 0 | |
| Upper bound for 0/260 | about 1.1% | 1.15% one-sided, 1.41% two-sided | | |

95% intervals for the prevalence ratios (Katz log method) are in `raw/named-features.csv`, for example RNF43 9.4 (7.1 to 12.5), AKT1 7.5 (4.2 to 13.4), SMAD4 1.56 (1.24 to 1.97), MYC amplification 2.1 (1.5 to 3.1).

## 1. Patients against samples: selection flow and every denominator

From `raw/selection-flow.json`:

| Step | Samples | Patients |
|---|---:|---:|
| Study | 7,237 | 6,789 |
| One sample per patient | | 6,398 |
| More than one sample (2, 3, 4, 5 samples: 345, 36, 9, 1) | | 391 |
| MSI_TYPE Stable | 6,114 | 5,764 with at least one Stable sample |
| MSI_TYPE Instable / Indeterminate / Do not report / missing | 770 / 281 / 52 / 20 | |
| Any BRAF mutation | 813 | 763 |
| BRAF V600E | 575 | 537 |
| V600E by MSI_TYPE: Stable / Instable / Indeterminate / Do not report / missing | 283 / 266 / 21 / 4 / 1 | |
| **BRAF group**: at least one Stable sample with V600E | 284 Stable samples | **260** |
| **Control, strict**: at least one Stable sample, no BRAF mutation in any Stable sample | 5,656 Stable samples | **5,342** |
| Control as submitted: at least one BRAF-free Stable sample, minus the BRAF group | | 5,345 |
| Stable patients in neither group (non-V600E BRAF mutation only) | | 162 |

Checks: 260 + 5,342 + 162 = 5,764. All sample IDs match the pattern `P-nnnnnnn-Tnn-IMn` and agree with the patient ID.

The sentence "5,345 microsatellite-stable patients with no BRAF mutation of any kind" is not accurate. The carrier rule was applied to V600E but not to "any BRAF mutation": three patients in the submitted control group have a non-V600E BRAF mutation in another Stable sample. The effect on every reported percentage is at most 0.1 point.

Six BRAF-group patients and 58 control patients also have a sample that is Indeterminate, "Do not report" or without MSI type. None has an Instable sample. Requiring all samples to be Stable gives 254 and 5,284.

## 2. Is the lexicographically first sample a justified choice?

As a way to count each patient once: yes. As a baseline or "earliest" sample: no. From `raw/sample-order.json`:

- Lexicographic order equals numeric specimen order in 391 of 391. This follows from the zero-padded two-digit number and tests nothing.
- The study exposes 23 clinical attributes. None is a collection or sequencing date. The only time-like field is a patient-level survival duration, which I did not fetch.
- Indirect support that the specimen number follows accession order: the panel size never decreases with rising specimen number (0 of 391 patients).
- Evidence that accession order is not biological order: 48 of 448 consecutive sample pairs go from a metastasis to a primary tumour. In the BRAF group 3 of 20 first-to-last pairs do.
- The first sample in the study is not always specimen T01: for 213 of 6,789 patients the lowest number is T02 or higher, and 93 of 391 multi-sample patients have a gap in their numbering. Specimens outside this study exist and are invisible here.
- In the submitted code "first" means the first sample within the already selected list (V600E-positive Stable, or BRAF-free Stable). For the BRAF group this happens to coincide with the first Stable sample in all 260 patients. For controls it does not, which is why the first-sample control count stays 5,345 instead of 5,343. Selecting on the outcome before taking "first" should be avoided.

Verdict: acceptable as a de-duplication sensitivity analysis, and the submitted text is right to say "lowest specimen number and nothing stronger". The effect table is stable under either rule except for KRAS and NRAS (2 to 0 and 1 to 0).

## 3. Panel, locus and copy-number coverage

**Panel level: confirmed.** All 7,237 samples are flagged as profiled for mutations, copy number and structural variants. Panels: IMPACT468 3,331, IMPACT505 2,789, IMPACT410 915, IMPACT341 202. The panel is the same across profiles and equals the GENE_PANEL attribute in all samples. 341 genes are on all four panels, 506 on at least one. KRAS, NRAS, APC, AMER1, RNF43, AKT1, TGFBR2, SMAD4, MYC, SRC, ASXL1, DNMT3B, TOP1 and BRAF are on all four lists.

**Being on the list is not the same as being reported.** I compared, for every gene and panel, the number of altered samples with the number expected from the other panels (4,137 combinations, `panel_dropout_scan` in `raw/coverage.json`). Two combinations pass a Bonferroni threshold:

- AMER1 mutations on IMPACT341: 0 of 202 samples, 15.8 expected (probability 7e-8). On the other three panels AMER1 is mutated in 7 to 8% of samples.
- BCOR amplification on IMPACT468: 0 of 3,331, 17.9 expected.

So for AMER1 the statement "absent means absent" does not hold on IMPACT341 (15 of 284 BRAF-group samples, 159 of 5,656 control samples). The AMER1 result itself survives: without IMPACT341 samples it is 3/251 (1.2%) against 300/5,191 (5.8%), p = 0.0006. For the other named features the control prevalence does not differ by panel version (`control_sample_prevalence_by_panel_version`, heterogeneity p from 0.08 to 0.99).

**Three of the 26 submitted significant features are on genes that are missing from a panel**: TCF7L2, PGR and MGA are not on IMPACT341. The submitted script divides by all 260 and 5,345 patients for every feature. In total 122 of its 475 tested features concern genes missing from at least one panel. With coverage-aware denominators the three results hold (TCF7L2 2/251 against 618/5,191; PGR 13/251 against 63/5,191; MGA 15/251 against 119/5,191), but the submitted percentages for them are slightly too low and the runtime coverage check does not cover them, because it only tests a fixed list of 14 genes.

**Copy number.** What the API actually returns:

- The discrete profile holds only the values 2, 0, -1.5 and -2. There are no low-level gains or single-copy losses.
- `HOMDEL_AND_AMP` returns 12,657 rows: 9,711 amplifications and 2,946 rows served as -2. Of those 2,946, 318 are stored as -1.5 (verified through the molecular-data endpoint) and 2,628 as -2.
- `ALL` returns 1,367,542 rows: the 9,711 amplifications, the 2,628 true -2 values and 1,355,203 zeros. It silently drops the 318 values of -1.5. Neither event type alone is complete.
- `ALL` returns rows only for the 2,918 samples that have at least one amplification or deletion call. The other 4,319 samples return no rows from any endpoint. The rows cover 40% of the sample by gene grid.
- 87,147 of the zeros in `ALL` are on genes that are not on that sample's panel. A zero is therefore matrix fill, not proof of a diploid call. No amplification or deletion call sits on a gene outside the sample's panel.
- Between 19 and 32 genes per panel never appear in the copy-number matrix at all (for example ALK, ATR, ERBB4, KMT2D, PTPN11, SETD2). All named genes do appear.
- 54 samples have no FRACTION_GENOME_ALTERED value; 29 of them still have calls.

Consequence: for a sample without any copy-number row, this source cannot distinguish "assessed, nothing found" from "could not be assessed". The share of samples with at least one call rises with tumour purity: 21.5% at purity 10 or lower, 28.3% at 20, 40.0% at 30 to 40, 53.9% at 50 or higher. An absent amplification in a low-purity sample is weak evidence of absence. This does not obviously bias the group comparison: purity (median 30 in both groups, 25% against 27% at 20 or lower), mean sample coverage (median 582 against 578) and panel mix are similar in the two groups. It does mean that amplification frequencies are lower bounds in both groups, and that "0% SRC amplification" is "no call in 260 patients", 49% of whose samples have no copy-number call at all (56% in controls).

The earlier internal note that about half of the gene by sample combinations are "explicitly called" under `ALL` should be read differently: the split is by sample (does it have any event), not by locus, so an explicit zero carries no extra assurance.

**The four absent amplifications are one event.** SRC, ASXL1, DNMT3B and TOP1 all lie on chromosome arm 20q. Of 335 control patients with at least one of the four, 278 have at least two and 167 have all four. The finding is "no 20q amplification call in 260 patients", once, not four independent results.

**Locus level: not verifiable.** Per-position or per-exon depth is not exposed. Only a mean coverage per sample is.

## 4. Is carrier status computed over all eligible samples?

No. In the submitted script the carrier rule pools only the samples that passed the group filter:

- BRAF group: only Stable samples that themselves carry V600E (283 samples). The one Stable sample without V600E, in the discordant patient, is left out, as are the non-Stable samples of six patients.
- Control group: only Stable samples without a BRAF mutation.

This is why the text says 19 multi-sample patients where the group has 20 with more than one Stable sample and 26 with more than one sample of any kind. For the named features the restriction changes nothing: my counts over all Stable samples are identical in the BRAF group. It should be stated explicitly, because the restricted rule removes exactly the discordant case that a reader of a multi-sample analysis wants to see. The earlier internal recount reached the same conclusion.

"In all nineteen the alteration profile differs between samples" is correct (20 of 20 in my universe) and carries little information: 234 of 276 control pairs (85%) and 339 of 391 pairs in the whole study also differ at variant level.

## 5. Gain and loss between samples: what can and cannot be concluded

The findings say: "If loss is as frequent as gain, the observation is noise." That inference is not valid in either direction. Symmetry would show that this dataset cannot separate acquisition from sampling; it would not show that no biology exists. And asymmetry would not show acquisition either, because the background in this cohort is itself asymmetric. First against last sample by specimen number, gene-level mutations on genes shared by both panels (`raw/paired-gain-loss.json`):

| Group | Pairs | Gains | Losses | Patients with more gains / more losses / equal | Patient-level sign test |
|---|---:|---:|---:|---|---:|
| BRAF group, Stable samples | 20 | 52 | 23 | 12 / 6 / 2 | p = 0.24 |
| Control, Stable samples | 276 | 547 | 312 | 136 / 71 / 69 | p = 7e-6 |
| Whole study, all samples | 391 | 1,193 | 780 | 212 / 93 / 86 | p = 8e-12 |

Later samples show more mutations than earlier ones in every group, including controls. Plausible non-biological reasons are visible in the data: the later sample has higher purity (median change plus 10 points in controls) and is more often a metastasis. Event-level tests would overstate this further because events cluster within patients; the patient-level test is the appropriate one.

For the specific observation:

- KRAS: 2 of 20 BRAF-group pairs gain a KRAS mutation (95% interval 1.2% to 31.7%), 0 of 20 lose one (0% to 16.8%). In both, the KRAS mutation is in a later metastatic sample that also carries V600E.
- Control baseline: 11 of 276 pairs gain KRAS and 3 lose it. 2/20 against 11/276 gives p = 0.22. Among control pairs with KRAS in either sample, 14 of 124 (11.3%, 6.3% to 18.2%) have it in only one of the two. A truncal driver is thus missed or absent in one of two samples about one time in nine, without any BRAF context.
- V600E itself: 1 of 35 multi-sample patients with V600E in any sample lacks it in another sample (0.07% to 14.9%).
- NRAS: 1 gain, 0 losses in the BRAF group.

Power and uncertainty for the main comparison (`raw/power.json`, 260 against 5,342, 80% power, at the p threshold that survived correction in my run, about 0.0017):

| Control prevalence | Smallest detectable enrichment | Largest detectable depletion |
|---:|---:|---:|
| 0.5% | 8 times | none, even total absence is not detectable |
| 1% | 5 times | none |
| 2% | 4 times | none |
| 5% | 2.5 times | 0.1 times |
| 10% | 2 times | 0.3 times |
| 20% | 1.75 times | 0.5 times |
| 50% | 1.3 times | 0.7 times |

A non-significant feature with a control prevalence below about 5% is therefore uninformative, not negative. Zero of 260 has a one-sided 95% upper bound of 1.15% and a two-sided exact bound of 1.41%.

Verdict: the two KRAS gains are a correct count. They are compatible with acquisition, with a subclone missed in the first sample, and with the general excess of gains seen in controls. Without dates and without treatment data this study cannot rank those explanations, whatever the gain to loss ratio turns out to be.

## 6. Reproducible aggregate checks

```
cd scripts
python fetch.py                       # downloads to scripts/cache/ (git-ignored), writes raw/fetch-manifest.json
python analyze.py                     # writes the aggregate files in raw/
python replicate_submitted_rule.py --submitted <path to msk-comutations.json>
```

Run time about two minutes for the download and under one minute for the analysis. The cache holds row-level public data and must not be committed. Files in `raw/`:

- `selection-flow.json`, `sample-order.json`, `coverage.json`, `paired-gain-loss.json`, `power.json`
- `named-features.csv`: the thirteen named features under both rules, with counts, intervals, odds ratio, p and q
- `features-*.csv`: every feature with at least one carrier, group counts only
- `feature-summary.json`: test family sizes and significant lists for four rule and control combinations
- `replication-of-submitted-rule.json`: the submitted rule re-implemented, compared with the submitted snapshot
- `fetch-manifest.json`, `SHA256SUMS`

Feature definitions in my recount: a mutation is any record in the mutation profile for that gene; amplification is the value 2; deletion is -2 or -1.5; a patient is evaluable for a gene only through samples whose panel lists the gene; a feature is tested when both groups together have at least 5 carriers; Fisher exact two-sided; Benjamini-Hochberg over mutations, amplifications and deletions together.

## Not checked

- I did not execute the submitted script and did not re-test its Fisher and Benjamini-Hochberg helpers in isolation. The earlier review record states that 103 tables agreed with SciPy; I took that from the record. My re-implementation of the full submitted rule gives the same 26 and 24 features with the same counts, which is indirect support only.
- The claim that the submitted data was retrieved on 11 September 2026. My download is from 2 October 2026. The study import date (1 September 2026) precedes both, which suggests the same data version but does not prove it.
- Per-locus or per-exon sequencing depth, callability of specific hotspots, and detection limits. Not exposed by this source.
- Why AMER1 on IMPACT341 and BCOR amplification on IMPACT468 are empty. I established the pattern, not the cause.
- The meaning of the stored copy-number value -1.5. I did not find and did not look up the definition; I only showed that the API serves it as -2 in one event type and drops it in another.
- The behaviour of the `ALL` event type is inferred from the responses, not from cBioPortal documentation or source code.
- Whether a mutation is a driver or a passenger. No oncogenicity filter was applied by the submission or by me. The mutation profile includes 161 promoter (5'Flank) and 59 splice-region records.
- Structural variants (924 in the study) were not used by the submission or by me.
- The patient-level clinical data, any timeline endpoint and any survival field. Deliberately not requested.
- The earlier internal recount of the paired samples (allele fractions per variant). I read its conclusions after my own run and did not re-derive its per-variant figures for this public review.
- Whether MSI_TYPE "Stable" is a reliable label in low-purity samples.
- External validity: one institution, sequenced patients only.

## Where I doubt my own result

- My primary universe (all Stable samples of a patient) was chosen after I had seen that it reproduces 260. It is defensible, but it was not fixed in advance.
- The AMER1 finding is a statistical inference from a zero count, not a documented property of the panel.
- The claim that a zero under `ALL` is matrix fill rests on two observations (zeros on off-panel genes; rows only for samples with an event). It may be an artefact of how this portal version serves the profile rather than of the underlying data file.
- The gain and loss comparison uses first against last sample and gene-level presence. Other pairings (all consecutive pairs, variant level) would give somewhat different counts; I did not explore them.
- The power table fixes the control count at its expected value and is approximate.
- The sets of significant features (26, 27) differ because the test families differ; neither is "the" correct count.

## Requested changes to the submission

1. Replace "5,345 patients with no BRAF mutation of any kind" by the strict count (5,342), or describe the looser rule as it is.
2. State that the carrier rule pools only the selected samples, and report 20 (Stable) and 26 (all) next to 19.
3. Replace "an absent alteration is therefore an absent event" by a statement limited to panel membership, add the AMER1 exception, and use coverage-aware denominators for genes that are not on all four panels (TCF7L2, PGR, MGA among the significant ones).
4. Describe copy-number absence as "no call", note the purity dependence, and report the four 20q genes as one event.
5. Remove "if loss is as frequent as gain, the observation is noise" and replace it with the limited statement in section 5, including the control baseline.
6. Define "first sample" on the patient's samples before any outcome-based selection.
7. Publish the script and the result snapshot in the repository, so that a code version exists beyond a file hash.
