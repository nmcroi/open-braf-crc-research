# TASK-0003 — independent normalization and rounding check

Public SCP2079 API re-fetched independently on 2026-09-11. Only aggregate output saved. Scope: five genes, 95,421 matched cell barcodes per gene, and public total_counts. This is a numerical transformation check, not a new biological result.

Hypothesis tested: y = round(log2(1 + count × 10,000 / total_counts), 3), with nonnegative integer count. Rather than accepting values within 0.05 of an integer, invert the actual rounding interval y ± 0.0005 and count feasible integers. Closed endpoints conservatively allow ties.

| Gene | Positive values | No integer fits single rounding | Fits wider ±0.00055 interval | Reproduced by Python round to 4 then 3 decimals |
|---|---:|---:|---:|---:|
| CXCL9 | 756 | 42 | 756 | 756 |
| CXCL10 | 1107 | 54 | 1107 | 1107 |
| CXCL11 | 1902 | 103 | 1902 | 1901 |
| CD47 | 53892 | 2627 | 53892 | 53889 |
| IDO1 | 676 | 48 | 676 | 676 |

All 58,333 positive values lie on the three-decimal grid. However, 2,874 cannot arise from the single-rounding model exactly. An additional rounding step is a strong candidate explanation: the wider interval admits integers for every positive value, and forward double rounding reproduces 58,329/58,333 values. The remaining four require inspecting tie/precision conventions or another processing detail. The exact author pipeline remains unverified.

This supports the proposed log2 / 10,000 / total_counts transformation much more strongly than a generic near-integer check, while qualifying the claim of exact raw-count recovery. Do not describe these inferred counts as the original deposited matrix, extend this to every gene without checking, or attribute this finding to the reviewer who first asked the question. The transform hypothesis came from Claude's review; this interval and double-rounding check was independently implemented here.

Zero check: maximum total_counts is 198,865. Under this model one count would produce at least 0.07078137, far above the zero-rounding interval. Thus rounding at these precisions alone would not hide a positive integer count as zero. This does not establish absence of expression biologically, exclude upstream filtering, or prove pipeline identity.

The patient's contribution to total inferred molecules and the unweighted patient-level direction statistic are different quantities. A large molecule share in one patient does not by itself turn a 16-patient direction analysis into a one-patient study. Small cell counts and leave-one-patient-out sensitivity still warrant explicit assessment.

Not rerun: depth adjustment, permutation tests, causal interpretation, protein function or matrix-file comparison. These remain outside this completed numerical check. Source URLs and hashes are in the accompanying result JSON; code makes no authenticated request.

Reproduce: `python3 scripts/audit_scp_rounding.py --out /tmp/scp-rounding.json`. [Recorded result](../results/scp-rounding-audit.json).
