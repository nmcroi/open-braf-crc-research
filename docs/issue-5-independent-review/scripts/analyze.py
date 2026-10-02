#!/usr/bin/env python3
"""Independent recount for issue 5: co-mutation patient selection and assay coverage.

Reads the local cache written by fetch.py and writes AGGREGATED output only
(counts and tables) to ../raw/. No patient or sample identifier is written.
Standard library only; SciPy, when installed, is used solely to cross-check
the home-made Fisher exact test.

Usage:
    python analyze.py [--cache DIR]
"""
import argparse
import collections
import csv
import glob
import gzip
import json
import math
import os
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "raw")
STUDY = "crc_msk_2026"
ID_RX = re.compile(r"^(P-\d{7})-T(\d{2})-IM(\d)$")
NAMED = ["KRAS", "NRAS", "APC", "AMER1", "RNF43", "AKT1", "TGFBR2", "SMAD4", "MYC", "SRC",
         "ASXL1", "DNMT3B", "TOP1", "BRAF"]
MIN_CARRIERS = 5  # a feature is tested when both groups together hold at least this many carriers


# ---------------------------------------------------------------- statistics
def log_choose(n, k):
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def fisher_two_sided(a, b, c, d):
    """Two-sided Fisher exact p for [[a, b], [c, d]]: sum of all tables with the
    same margins whose probability does not exceed that of the observed one."""
    r1, r2, c1, n = a + b, c + d, a + c, a + b + c + d
    lo, hi = max(0, c1 - r2), min(r1, c1)
    denom = log_choose(n, c1)

    def logp(x):
        return log_choose(r1, x) + log_choose(r2, c1 - x) - denom

    obs = logp(a)
    total = 0.0
    for x in range(lo, hi + 1):
        lp = logp(x)
        if lp <= obs + 1e-7:
            total += math.exp(lp)
    return min(1.0, total)


def bh(pvals):
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    q = [0.0] * m
    prev = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        prev = min(prev, pvals[i] * m / rank)
        q[i] = prev
    return q


def clopper_pearson(x, n, alpha=0.05):
    """Exact two-sided interval by bisection on the binomial tail."""
    def cdf(k, p):
        return sum(math.exp(log_choose(n, i) + i * math.log(p) + (n - i) * math.log(1 - p))
                   for i in range(0, k + 1)) if 0 < p < 1 else (1.0 if p == 0 else (1.0 if k >= n else 0.0))

    lower = 0.0 if x == 0 else _bisect_increasing(lambda p: 1 - cdf(x - 1, p), alpha / 2)
    upper = 1.0 if x == n else _bisect_decreasing(lambda p: cdf(x, p), alpha / 2)
    return lower, upper


def _bisect_increasing(f, target):
    lo, hi = 1e-12, 1 - 1e-12
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _bisect_decreasing(f, target):
    lo, hi = 1e-12, 1 - 1e-12
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) > target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def prevalence_ratio_ci(a, n1, c, n0):
    """Katz log interval; None when a cell is zero."""
    if a == 0 or c == 0:
        return None
    pr = (a / n1) / (c / n0)
    se = math.sqrt(1 / a - 1 / n1 + 1 / c - 1 / n0)
    return pr, pr * math.exp(-1.96 * se), pr * math.exp(1.96 * se)


def quantiles(vals):
    vals = sorted(vals)
    if not vals:
        return None
    q = statistics.quantiles(vals, n=4) if len(vals) > 1 else [vals[0]] * 3
    return {"n": len(vals), "q1": q[0], "median": q[1], "q3": q[2]}


# ---------------------------------------------------------------- loading
def load(cache, name):
    with gzip.open(os.path.join(cache, name + ".json.gz"), "rt") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(HERE, "cache"))
    args = ap.parse_args()
    cache = args.cache
    os.makedirs(RAW, exist_ok=True)

    samples = load(cache, "samples")
    clin = load(cache, "clinical_sample")
    muts = load(cache, "mutations")
    cna_h = load(cache, "cna_homdel_amp")
    cna_all = []
    for f in sorted(glob.glob(os.path.join(cache, "cna_all_*.json.gz"))):
        with gzip.open(f, "rt") as fh:
            cna_all += json.load(fh)
    check = {(s, g): v for s, g, v in load(cache, "cna_molecular_data_check")}

    attr = collections.defaultdict(dict)
    for r in clin:
        attr[r["clinicalAttributeId"]][r["sampleId"]] = r["value"]
    msi = attr["MSI_TYPE"]

    def tnum(s):
        return int(ID_RX.match(s).group(2))

    bad_ids = sum(1 for s in samples if not ID_RX.match(s["sampleId"])
                  or ID_RX.match(s["sampleId"]).group(1) != s["patientId"])
    by_patient = collections.defaultdict(list)
    for s in samples:
        by_patient[s["patientId"]].append(s["sampleId"])
    lexi_vs_numeric_disagree = 0
    for p, ss in by_patient.items():
        if sorted(ss) != sorted(ss, key=tnum):
            lexi_vs_numeric_disagree += 1
        ss.sort(key=tnum)
    all_samples = [s["sampleId"] for s in samples]

    # panels
    panel = {}
    panel_profiled = {}
    for prof in ("mutations", "cna", "structural_variants"):
        rows = load(cache, f"gene_panel_data_{STUDY}_{prof}")
        panel_profiled[prof] = collections.Counter((r.get("genePanelId"), r["profiled"]) for r in rows)
        if prof == "mutations":
            panel = {r["sampleId"]: r["genePanelId"] for r in rows}
        elif prof == "cna":
            cna_panel = {r["sampleId"]: r["genePanelId"] for r in rows}
    panel_mismatch = sum(1 for s in all_samples if panel[s] != cna_panel[s] or panel[s] != attr["GENE_PANEL"].get(s))
    panel_names = sorted(set(panel.values()))
    panel_genes = {}
    symbol = {}
    for pn in panel_names:
        gp = load(cache, "gene_panel_" + pn)
        panel_genes[pn] = {g["entrezGeneId"] for g in gp["genes"]}
        for g in gp["genes"]:
            symbol[g["entrezGeneId"]] = g["hugoGeneSymbol"]
    entrez = {v: k for k, v in symbol.items()}
    on_all = set.intersection(*panel_genes.values())
    on_any = set.union(*panel_genes.values())

    def covered(s, g):
        return g in panel_genes[panel[s]]

    # alterations per sample
    mut_genes = collections.defaultdict(set)      # sample -> entrez set
    mut_variants = collections.defaultdict(set)   # sample -> variant keys
    braf_any, v600e = set(), set()
    braf_gene = entrez["BRAF"]
    off_panel_mut = 0
    for m in muts:
        s, g = m["sampleId"], m["entrezGeneId"]
        if g not in panel_genes[panel[s]]:
            off_panel_mut += 1
        mut_genes[s].add(g)
        mut_variants[s].add((g, m["chr"], m["startPosition"], m["endPosition"], m["referenceAllele"], m["variantAllele"]))
        if g == braf_gene:
            braf_any.add(s)
            if m["proteinChange"] == "V600E":
                v600e.add(s)

    all_seen = {(s, g): a for s, g, a in cna_all}
    amp = collections.defaultdict(set)
    homdel = collections.defaultdict(set)       # stored value -2
    deep15 = collections.defaultdict(set)       # stored value -1.5, served as -2 by HOMDEL_AND_AMP
    off_panel_cna = 0
    for s, g, a in cna_h:
        if g not in panel_genes[panel[s]]:
            off_panel_cna += 1
        if a == 2:
            amp[s].add(g)
        elif (s, g) in all_seen:
            homdel[s].add(g)
        else:
            assert check.get((s, g)) == -1.5, "unexplained call missing from ALL"
            deep15[s].add(g)

    # ------------------------------------------------ 1. selection flow
    stable = lambda s: msi.get(s) == "Stable"
    flow = collections.OrderedDict()
    flow["samples_in_study"] = len(samples)
    flow["patients_in_study"] = len(by_patient)
    flow["sample_ids_not_matching_pattern"] = bad_ids
    flow["samples_per_patient"] = dict(sorted(collections.Counter(len(v) for v in by_patient.values()).items()))
    flow["patients_with_more_than_one_sample"] = sum(len(v) > 1 for v in by_patient.values())
    flow["samples_by_MSI_TYPE"] = dict(collections.Counter(msi.get(s, "missing") for s in all_samples))
    flow["samples_with_any_BRAF_mutation"] = len(braf_any)
    flow["samples_with_BRAF_V600E"] = len(v600e)
    flow["V600E_samples_by_MSI_TYPE"] = dict(collections.Counter(msi.get(s, "missing") for s in v600e))
    flow["patients_with_V600E_in_any_sample"] = sum(any(s in v600e for s in ss) for ss in by_patient.values())
    flow["patients_with_any_BRAF_mutation_in_any_sample"] = sum(any(s in braf_any for s in ss) for ss in by_patient.values())

    st_by_patient = {p: [s for s in ss if stable(s)] for p, ss in by_patient.items() if any(stable(s) for s in ss)}
    flow["stable_samples"] = sum(len(v) for v in st_by_patient.values())
    flow["patients_with_at_least_one_stable_sample"] = len(st_by_patient)
    flow["patients_with_stable_and_nonstable_samples"] = sum(
        1 for p in st_by_patient if len(st_by_patient[p]) != len(by_patient[p]))
    flow["patients_with_more_than_one_stable_sample"] = sum(len(v) > 1 for v in st_by_patient.values())
    flow["stable_samples_with_V600E"] = sum(1 for s in v600e if stable(s))
    flow["stable_samples_without_any_BRAF_mutation"] = sum(1 for s in all_samples if stable(s) and s not in braf_any)

    grp_braf = {p for p, ss in st_by_patient.items() if any(s in v600e for s in ss)}
    ctrl_strict = {p for p, ss in st_by_patient.items() if not any(s in braf_any for s in ss)}
    ctrl_loose = {p for p, ss in st_by_patient.items() if any(s not in braf_any for s in ss)} - grp_braf
    ctrl_allsamples = {p for p in st_by_patient if not any(s in braf_any for s in by_patient[p])}
    flow["GROUP_braf_v600e_mss_patients (any stable sample with V600E)"] = len(grp_braf)
    flow["CONTROL_strict (>=1 stable sample, no BRAF mutation in ANY stable sample)"] = len(ctrl_strict)
    flow["CONTROL_strict_also_checking_nonstable_samples"] = len(ctrl_allsamples)
    flow["CONTROL_loose (>=1 stable sample WITHOUT BRAF mutation, minus V600E group)"] = len(ctrl_loose)
    flow["patients_with_a_BRAF_free_stable_sample_before_removing_V600E_group"] = len(ctrl_loose) + len(
        {p for p in grp_braf if any(s not in braf_any for s in st_by_patient[p])})
    flow["control_loose_patients_that_carry_a_nonV600E_BRAF_mutation_in_another_stable_sample"] = len(ctrl_loose - ctrl_strict)
    flow["stable_patients_in_neither_group (non-V600E BRAF only)"] = len(st_by_patient) - len(grp_braf) - len(ctrl_strict)
    flow["GROUP_alt_all_samples_stable"] = sum(1 for p in grp_braf if len(st_by_patient[p]) == len(by_patient[p]))
    flow["CONTROL_alt_all_samples_stable"] = sum(1 for p in ctrl_strict if len(st_by_patient[p]) == len(by_patient[p]))
    flow["GROUP_first_sample_overall_is_stable"] = sum(1 for p in grp_braf if stable(by_patient[p][0]))
    flow["braf_group_patients_with_more_than_one_stable_sample"] = sum(len(st_by_patient[p]) > 1 for p in grp_braf)
    flow["braf_group_patients_with_more_than_one_sample_of_any_MSI_type"] = sum(len(by_patient[p]) > 1 for p in grp_braf)
    flow["braf_group_patients_with_more_than_one_V600E_stable_sample"] = sum(
        sum(1 for s in st_by_patient[p] if s in v600e) > 1 for p in grp_braf)
    flow["braf_group_stable_samples"] = sum(len(st_by_patient[p]) for p in grp_braf)
    flow["braf_group_patients_V600E_discordant_between_stable_samples"] = sum(
        len({s in v600e for s in st_by_patient[p]}) > 1 for p in grp_braf)
    flow["braf_group_first_stable_sample_has_V600E"] = sum(st_by_patient[p][0] in v600e for p in grp_braf)
    flow["control_strict_stable_samples"] = sum(len(st_by_patient[p]) for p in ctrl_strict)
    flow["control_strict_patients_with_more_than_one_stable_sample"] = sum(len(st_by_patient[p]) > 1 for p in ctrl_strict)
    with open(os.path.join(RAW, "selection-flow.json"), "w") as fh:
        json.dump(flow, fh, indent=1)

    # ------------------------------------------------ 2. sample ordering
    order = collections.OrderedDict()
    multi = {p: ss for p, ss in by_patient.items() if len(ss) > 1}
    order["patients_with_more_than_one_sample"] = len(multi)
    order["lexicographic_order_differs_from_numeric_T_order"] = lexi_vs_numeric_disagree
    order["clinical_attributes_exposed_by_study"] = sorted(a["clinicalAttributeId"] for a in load(cache, "clinical_attributes"))
    order["date_like_attributes"] = [a for a in order["clinical_attributes_exposed_by_study"]
                                     if re.search(r"DATE|DAY|MONTH|YEAR|TIME|(^|_)AGE", a)]
    order["lowest_T_number_in_study_all_patients"] = dict(sorted(collections.Counter(
        tnum(ss[0]) for ss in by_patient.values()).items()))
    order["lowest_T_number_in_study_multi_sample_patients"] = dict(sorted(collections.Counter(
        tnum(ss[0]) for ss in multi.values()).items()))
    order["multi_sample_patients_with_gap_in_T_numbers"] = sum(
        1 for ss in multi.values() if [tnum(s) for s in ss] != list(range(tnum(ss[0]), tnum(ss[0]) + len(ss))))
    order["multi_sample_patients_panel_version_changes"] = sum(len({panel[s] for s in ss}) > 1 for ss in multi.values())
    pv = lambda s: int(panel[s].replace("IMPACT", ""))
    order["multi_sample_patients_panel_size_decreases_with_T_number"] = sum(
        any(pv(a) > pv(b) for a, b in zip(ss, ss[1:])) for ss in multi.values())
    st = attr["SAMPLE_TYPE"]
    order["consecutive_pairs_by_sample_type (lower T -> higher T)"] = dict(collections.Counter(
        f"{st.get(a)} -> {st.get(b)}" for ss in multi.values() for a, b in zip(ss, ss[1:])).most_common())
    order["first_in_study_sample_type_multi_sample_patients"] = dict(collections.Counter(
        st.get(ss[0]) for ss in multi.values()))
    order["first_in_study_sample_type_all_patients"] = dict(collections.Counter(
        st.get(ss[0]) for ss in by_patient.values()))
    order["braf_group_first_stable_sample_type"] = dict(collections.Counter(st.get(st_by_patient[p][0]) for p in grp_braf))
    order["control_strict_first_stable_sample_type"] = dict(collections.Counter(st.get(st_by_patient[p][0]) for p in ctrl_strict))
    order["braf_group_multi_stable: first stable sample is not the patient's first sample in the study"] = sum(
        1 for p in grp_braf if st_by_patient[p][0] != by_patient[p][0])
    with open(os.path.join(RAW, "sample-order.json"), "w") as fh:
        json.dump(order, fh, indent=1)

    # ------------------------------------------------ 3. coverage
    cov = collections.OrderedDict()
    cov["profiled_flags_by_profile_and_panel"] = {
        k: {f"{p}|profiled={b}": n for (p, b), n in v.items()} for k, v in panel_profiled.items()}
    cov["samples_where_panel_differs_between_profiles_or_clinical_attribute"] = panel_mismatch
    cov["panel_gene_counts"] = {p: len(g) for p, g in panel_genes.items()}
    cov["genes_on_all_four_panels"] = len(on_all)
    cov["genes_on_at_least_one_panel"] = len(on_any)
    cov["named_gene_panel_membership"] = {g: {p: entrez[g] in panel_genes[p] for p in panel_names} for g in NAMED}
    cov["mutation_records_total"] = len(muts)
    cov["mutation_types"] = dict(collections.Counter(m["mutationType"] for m in muts).most_common())
    cov["mutation_records_on_gene_outside_sample_panel"] = off_panel_mut
    cna_genes = {g for _, g, _ in cna_all}
    cov["cna_HOMDEL_AND_AMP_rows"] = len(cna_h)
    cov["cna_HOMDEL_AND_AMP_values_as_served"] = dict(collections.Counter(str(a) for _, _, a in cna_h))
    cov["cna_ALL_rows"] = len(cna_all)
    cov["cna_ALL_values"] = dict(collections.Counter(str(a) for _, _, a in cna_all))
    cov["cna_ALL_distinct_genes"] = len(cna_genes)
    cov["cna_ALL_distinct_samples"] = len({s for s, _, _ in cna_all})
    cov["samples_with_at_least_one_HOMDEL_AND_AMP_call"] = len({s for s, _, _ in cna_h})
    cov["samples_in_ALL_that_have_no_HOMDEL_AND_AMP_call"] = len({s for s, _, _ in cna_all} - {s for s, _, _ in cna_h})
    cov["samples_with_zero_rows_in_ALL"] = len(all_samples) - cov["cna_ALL_distinct_samples"]
    cov["cna_ALL_share_of_sample_x_gene_grid"] = round(len(cna_all) / (len(all_samples) * len(cna_genes)), 4)
    cov["cna_ALL_zero_rows_on_gene_outside_sample_panel"] = sum(
        1 for s, g, a in cna_all if g not in panel_genes[panel[s]])
    cov["cna_events_on_gene_outside_sample_panel"] = off_panel_cna
    cov["cna_HOMDEL_AND_AMP_calls_absent_from_ALL"] = sum(len(v) for v in deep15.values())
    cov["cna_stored_value_of_those_calls (molecular-data endpoint)"] = dict(collections.Counter(
        str(check[(s, g)]) for s in deep15 for g in deep15[s]))
    cov["panel_genes_never_in_cna_matrix"] = {p: len(panel_genes[p] - cna_genes) for p in panel_names}
    cov["named_genes_in_cna_matrix"] = {g: entrez[g] in cna_genes for g in NAMED}
    cov["samples_missing_FRACTION_GENOME_ALTERED"] = sum(1 for s in all_samples if s not in attr["FRACTION_GENOME_ALTERED"])
    cov["samples_missing_TUMOR_PURITY"] = sum(1 for s in all_samples if s not in attr["TUMOR_PURITY"])
    cov["samples_missing_MSI_TYPE"] = sum(1 for s in all_samples if s not in msi)

    def group_summary(patients):
        ss = [s for p in patients for s in st_by_patient[p]]
        def num(a):
            out = []
            for s in ss:
                try:
                    out.append(float(attr[a][s]))
                except (KeyError, ValueError):
                    pass
            return out
        return {
            "patients": len(patients), "stable_samples": len(ss),
            "panel": dict(sorted(collections.Counter(panel[s] for s in ss).items())),
            "sample_type": dict(collections.Counter(st.get(s) for s in ss)),
            "SAMPLE_COVERAGE": quantiles(num("SAMPLE_COVERAGE")),
            "TUMOR_PURITY": quantiles(num("TUMOR_PURITY")),
            "purity_missing": sum(1 for s in ss if s not in attr["TUMOR_PURITY"]),
            "purity_at_most_20": sum(1 for v in num("TUMOR_PURITY") if v <= 20),
            "FGA_missing": sum(1 for s in ss if s not in attr["FRACTION_GENOME_ALTERED"]),
            "samples_with_no_cna_call_at_all": sum(1 for s in ss if not amp[s] and not homdel[s] and not deep15[s]),
            "samples_with_no_mutation_record": sum(1 for s in ss if not mut_genes[s]),
        }
    def msi_mix(patients):
        out = collections.Counter()
        for p in patients:
            others = {msi.get(s, "missing") for s in by_patient[p]} - {"Stable"}
            out["all samples Stable"] += not others
            out["also an Instable sample"] += "Instable" in others
            out["also an Indeterminate / Do not report / missing sample"] += bool(others - {"Instable"})
        return dict(out)
    cov["msi_mix_braf_group"] = msi_mix(grp_braf)
    cov["msi_mix_control_strict"] = msi_mix(ctrl_strict)

    # does a missing copy-number call depend on tumour purity? (all samples in the study)
    strata = collections.OrderedDict()
    for label, lo, hi in (("purity <=10", 0, 10), ("purity 20", 11, 20), ("purity 30-40", 21, 40), ("purity >=50", 41, 100)):
        ss = [s for s in all_samples if s in attr["TUMOR_PURITY"] and lo <= float(attr["TUMOR_PURITY"][s]) <= hi]
        strata[label] = {"samples": len(ss),
                         "pct_with_at_least_one_amp_or_deletion_call": round(100 * sum(
                             1 for s in ss if amp[s] or homdel[s] or deep15[s]) / len(ss), 1) if ss else None}
    cov["cna_call_rate_by_purity_all_samples"] = strata
    no_fga = [s for s in all_samples if s not in attr["FRACTION_GENOME_ALTERED"]]
    cov["samples_missing_FGA_with_at_least_one_cna_call"] = sum(1 for s in no_fga if amp[s] or homdel[s] or deep15[s])

    # do the named features depend on panel version? control patients' stable samples, sample level
    def chi2_p_df3(x):
        return math.erfc(math.sqrt(x / 2)) + math.sqrt(2 * x / math.pi) * math.exp(-x / 2)
    ctrl_samples = [s for p in ctrl_strict for s in st_by_patient[p]]
    by_panel = collections.OrderedDict()
    for gname, kind in (("KRAS", "MUT"), ("NRAS", "MUT"), ("APC", "MUT"), ("AMER1", "MUT"), ("RNF43", "MUT"),
                        ("AKT1", "MUT"), ("TGFBR2", "MUT"), ("SMAD4", "MUT"), ("MYC", "AMP"), ("SRC", "AMP"),
                        ("ASXL1", "AMP"), ("DNMT3B", "AMP"), ("TOP1", "AMP")):
        g = entrez[gname]
        src = mut_genes if kind == "MUT" else amp
        obs = {pn: [sum(1 for s in ctrl_samples if panel[s] == pn and g in src[s]),
                    sum(1 for s in ctrl_samples if panel[s] == pn)] for pn in panel_names}
        tot_x, tot_n = sum(v[0] for v in obs.values()), sum(v[1] for v in obs.values())
        chi = 0.0
        for xk, nk in obs.values():
            for o, e in ((xk, nk * tot_x / tot_n), (nk - xk, nk * (tot_n - tot_x) / tot_n)):
                chi += (o - e) ** 2 / e
        by_panel[f"{gname}_{kind}"] = {**{pn: f"{v[0]}/{v[1]} ({100 * v[0] / v[1]:.1f}%)" for pn, v in obs.items()},
                                       "chi2_df3_p_heterogeneity": chi2_p_df3(chi)}
    cov["control_sample_prevalence_by_panel_version"] = by_panel

    # "on the panel list" versus "actually reported": for every gene x panel on
    # which the gene is listed, compare the observed number of altered samples with
    # the number expected from the other panels. Flag zero observed, >= 5 expected.
    n_panel = collections.Counter(panel.values())
    alt_sets = collections.defaultdict(set)
    for s in all_samples:
        for g in mut_genes[s]: alt_sets[(g, "MUT")].add(s)
        for g in amp[s]: alt_sets[(g, "AMP")].add(s)
        for g in homdel[s] | deep15[s]: alt_sets[(g, "HOMDEL_OR_DEEP")].add(s)
    flagged, scanned = [], 0
    for (g, kind), ss in sorted(alt_sets.items(), key=lambda kv: (symbol.get(kv[0][0], ""), kv[0][1])):
        pans = [pn for pn in panel_names if g in panel_genes[pn]]
        tot = sum(n_panel[pn] for pn in pans)
        for pn in pans:
            other = tot - n_panel[pn]
            if not other:
                continue
            scanned += 1
            obs = sum(1 for x in ss if panel[x] == pn)
            rate = (len(ss) - obs) / other
            if obs == 0 and rate * n_panel[pn] >= 5:
                flagged.append({"feature": f"{symbol[g]}_{kind}", "panel": pn, "samples_on_panel": n_panel[pn],
                                "observed": 0, "expected_from_other_panels": round(rate * n_panel[pn], 1),
                                "probability_of_zero": (1 - rate) ** n_panel[pn]})
    cov["panel_dropout_scan"] = {"gene_x_kind_x_panel_combinations_scanned": scanned,
                                 "bonferroni_threshold": 0.05 / scanned, "flagged": flagged}
    amer1 = entrez["AMER1"]
    def amer1_counts(patients):
        ss_ok = lambda p: [s for s in st_by_patient[p] if panel[s] != "IMPACT341"]
        ev = [p for p in patients if ss_ok(p)]
        return sum(any(amer1 in mut_genes[s] for s in ss_ok(p)) for p in ev), len(ev)
    xa, na = amer1_counts(grp_braf)
    xc, nc = amer1_counts(ctrl_strict)
    cov["AMER1_mutation_excluding_IMPACT341_samples"] = {
        "braf_group": f"{xa}/{na}", "control": f"{xc}/{nc}",
        "pct_braf": round(100 * xa / na, 2), "pct_control": round(100 * xc / nc, 2),
        "fisher_two_sided_p": fisher_two_sided(xa, na - xa, xc, nc - xc)}
    cov["mutation_records_on_gene_not_on_any_panel"] = sum(1 for m in muts if m["entrezGeneId"] not in on_any)

    # the four amplifications that are absent in the BRAF group all sit on chromosome arm 20q
    q20 = [entrez[g] for g in ("SRC", "ASXL1", "DNMT3B", "TOP1")]
    n_any = n_two = n_all = 0
    for p in ctrl_strict:
        k = sum(any(g in amp[s] for s in st_by_patient[p]) for g in q20)
        n_any += k >= 1; n_two += k >= 2; n_all += k == 4
    cov["control_patients_20q_cluster (SRC, ASXL1, DNMT3B, TOP1 amplification)"] = {
        "at_least_one": n_any, "at_least_two": n_two, "all_four": n_all}
    cov["braf_group_patients_with_any_of_the_four_20q_amplifications"] = sum(
        any(g in amp[s] for s in st_by_patient[p] for g in q20) for p in grp_braf)

    cov["braf_group"] = group_summary(grp_braf)
    cov["control_strict"] = group_summary(ctrl_strict)
    with open(os.path.join(RAW, "coverage.json"), "w") as fh:
        json.dump(cov, fh, indent=1)

    # ------------------------------------------------ feature tables
    def carriers(patients, sample_pick, gene, kind):
        """Returns (carriers, evaluable): evaluable = patients with at least one
        picked sample on a panel that contains the gene."""
        x = n = 0
        for p in patients:
            ss = [s for s in sample_pick(p) if covered(s, gene)]
            if not ss:
                continue
            n += 1
            if kind == "MUT":
                hit = any(gene in mut_genes[s] for s in ss)
            elif kind == "AMP":
                hit = any(gene in amp[s] for s in ss)
            elif kind == "HOMDEL":
                hit = any(gene in homdel[s] for s in ss)
            else:  # HOMDEL_OR_DEEP: -2 or -1.5, which is what HOMDEL_AND_AMP serves as -2
                hit = any(gene in homdel[s] or gene in deep15[s] for s in ss)
            x += hit
        return x, n

    def run(tag, grp, ctrl, pick):
        rows = []
        for g in sorted(on_any, key=lambda e: symbol[e]):
            if g == braf_gene:
                continue
            for kind in ("MUT", "AMP", "HOMDEL", "HOMDEL_OR_DEEP"):
                a, n1 = carriers(grp, pick, g, kind)
                c, n0 = carriers(ctrl, pick, g, kind)
                rows.append({"feature": f"{symbol[g]}_{kind}", "gene": symbol[g], "kind": kind,
                             "on_all_four_panels": g in on_all, "x_braf": a, "n_braf": n1, "x_ctrl": c, "n_ctrl": n0})
        # family for multiple testing: MUT, AMP and HOMDEL_OR_DEEP (strict HOMDEL is reported, not tested twice)
        tested = [r for r in rows if r["kind"] != "HOMDEL" and r["x_braf"] + r["x_ctrl"] >= MIN_CARRIERS
                  and r["n_braf"] > 0 and r["n_ctrl"] > 0]
        for r in tested:
            r["p"] = fisher_two_sided(r["x_braf"], r["n_braf"] - r["x_braf"], r["x_ctrl"], r["n_ctrl"] - r["x_ctrl"])
        for r, q in zip(tested, bh([r["p"] for r in tested])):
            r["q"] = q
        for r in rows:
            r["pct_braf"] = round(100 * r["x_braf"] / r["n_braf"], 2) if r["n_braf"] else None
            r["pct_ctrl"] = round(100 * r["x_ctrl"] / r["n_ctrl"], 2) if r["n_ctrl"] else None
            ci = prevalence_ratio_ci(r["x_braf"], r["n_braf"], r["x_ctrl"], r["n_ctrl"]) if r["n_braf"] and r["n_ctrl"] else None
            r["prev_ratio"], r["pr_lo"], r["pr_hi"] = (round(v, 3) for v in ci) if ci else (None, None, None)
            b, d = r["n_braf"] - r["x_braf"], r["n_ctrl"] - r["x_ctrl"]
            r["odds_ratio"] = round((r["x_braf"] * d) / (b * r["x_ctrl"]), 3) if b and r["x_ctrl"] else None
        cols = ["feature", "on_all_four_panels", "x_braf", "n_braf", "pct_braf", "x_ctrl", "n_ctrl", "pct_ctrl",
                "prev_ratio", "pr_lo", "pr_hi", "odds_ratio", "p", "q"]
        with open(os.path.join(RAW, f"features-{tag}.csv"), "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in sorted(rows, key=lambda r: (r.get("p", 2), r["feature"])):
                if r["x_braf"] + r["x_ctrl"] > 0:
                    w.writerow(r)
        summary = {
            "n_braf_patients": len(grp), "n_control_patients": len(ctrl),
            "features_with_any_carrier": sum(1 for r in rows if r["kind"] != "HOMDEL" and r["x_braf"] + r["x_ctrl"] > 0),
            "features_tested": len(tested),
            "features_q_below_0.05": sum(1 for r in tested if r["q"] < 0.05),
            "features_tested_by_kind": dict(collections.Counter(r["kind"] for r in tested)),
            "significant_by_kind": dict(collections.Counter(r["kind"] for r in tested if r["q"] < 0.05)),
            "significant_features": sorted(r["feature"] for r in tested if r["q"] < 0.05),
            "significant_not_on_all_four_panels": sorted(r["feature"] for r in tested if r["q"] < 0.05 and not r["on_all_four_panels"]),
            "largest_p_still_significant": max([r["p"] for r in tested if r["q"] < 0.05], default=None),
            "tested_count_at_other_thresholds": {
                str(k): sum(1 for r in rows if r["kind"] != "HOMDEL" and r["x_braf"] + r["x_ctrl"] >= k) for k in (1, 2, 3, 5, 10, 20)},
            "features_with_reduced_denominator": sum(1 for r in tested if r["n_braf"] < len(grp) or r["n_ctrl"] < len(ctrl)),
        }
        return rows, tested, summary

    pick_all_stable = lambda p: st_by_patient[p]
    pick_first_stable = lambda p: st_by_patient[p][:1]
    results = {}
    rows_c, tested_c, results["carrier_rule__control_strict"] = run("carrier-rule", grp_braf, ctrl_strict, pick_all_stable)
    _, _, results["carrier_rule__control_loose_as_submitted"] = run("carrier-rule-loose-control", grp_braf, ctrl_loose, pick_all_stable)
    grp_first = {p for p in st_by_patient if st_by_patient[p][0] in v600e}
    ctrl_first = {p for p in st_by_patient if st_by_patient[p][0] not in braf_any}
    rows_f, tested_f, results["first_sample_rule__groups_from_first_stable_sample"] = run(
        "first-sample-rule", grp_first, ctrl_first, pick_first_stable)
    _, _, results["first_sample_rule__carrier_groups_kept"] = run(
        "first-sample-rule-carrier-groups", grp_braf, ctrl_strict, pick_first_stable)

    # cross-check Fisher against SciPy when present
    try:
        from scipy.stats import fisher_exact
        worst = 0.0
        for r in tested_c + tested_f:
            ref = fisher_exact([[r["x_braf"], r["n_braf"] - r["x_braf"]], [r["x_ctrl"], r["n_ctrl"] - r["x_ctrl"]]])[1]
            worst = max(worst, abs(ref - r["p"]) / max(ref, 1e-300))
        results["fisher_crosscheck_scipy"] = {"tables": len(tested_c) + len(tested_f), "max_relative_difference": worst}
    except ImportError:
        results["fisher_crosscheck_scipy"] = "scipy not installed"
    with open(os.path.join(RAW, "feature-summary.json"), "w") as fh:
        json.dump(results, fh, indent=1)

    # named-feature table under both rules
    wanted = [("KRAS", "MUT"), ("NRAS", "MUT"), ("APC", "MUT"), ("AMER1", "MUT"), ("RNF43", "MUT"), ("AKT1", "MUT"),
              ("TGFBR2", "MUT"), ("SMAD4", "MUT"), ("MYC", "AMP"), ("SRC", "AMP"), ("ASXL1", "AMP"),
              ("DNMT3B", "AMP"), ("TOP1", "AMP")]
    idx_c = {r["feature"]: r for r in rows_c}
    idx_f = {r["feature"]: r for r in rows_f}
    with open(os.path.join(RAW, "named-features.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["feature", "rule", "x_braf", "n_braf", "pct_braf", "x_ctrl", "n_ctrl", "pct_ctrl",
                    "prev_ratio", "pr_lo", "pr_hi", "odds_ratio", "p", "q"])
        for g, k in wanted:
            for rule, idx in (("carrier", idx_c), ("first-sample", idx_f)):
                r = idx[f"{g}_{k}"]
                w.writerow([r["feature"], rule, r["x_braf"], r["n_braf"], r["pct_braf"], r["x_ctrl"], r["n_ctrl"],
                            r["pct_ctrl"], r["prev_ratio"], r["pr_lo"], r["pr_hi"], r["odds_ratio"],
                            r.get("p"), r.get("q")])

    # ------------------------------------------------ 4/5. paired samples: gain and loss
    def pair_stats(patients, sample_lists):
        """First versus last sample (by T number). Gene-level mutation presence,
        restricted to genes on both panels. Aggregates only."""
        out = collections.OrderedDict()
        pts = [p for p in patients if len(sample_lists[p]) > 1]
        out["patients_with_pair"] = len(pts)
        gained = lost = shared = 0
        any_gain = any_loss = identical = cna_differs = variant_differs = 0
        more_gain = more_loss = 0
        per_gene_gain, per_gene_loss = collections.Counter(), collections.Counter()
        purity_delta = []
        type_pairs = collections.Counter()
        panel_change = 0
        for p in pts:
            a, b = sample_lists[p][0], sample_lists[p][-1]
            common = panel_genes[panel[a]] & panel_genes[panel[b]]
            ga, gb = mut_genes[a] & common, mut_genes[b] & common
            g_gain, g_loss = gb - ga, ga - gb
            gained += len(g_gain); lost += len(g_loss); shared += len(ga & gb)
            any_gain += bool(g_gain); any_loss += bool(g_loss)
            more_gain += len(g_gain) > len(g_loss); more_loss += len(g_loss) > len(g_gain)
            for g in g_gain: per_gene_gain[symbol[g]] += 1
            for g in g_loss: per_gene_loss[symbol[g]] += 1
            va = {v for v in mut_variants[a] if v[0] in common}
            vb = {v for v in mut_variants[b] if v[0] in common}
            ca = {("amp", g) for g in amp[a] & common} | {("del", g) for g in (homdel[a] | deep15[a]) & common}
            cb = {("amp", g) for g in amp[b] & common} | {("del", g) for g in (homdel[b] | deep15[b]) & common}
            variant_differs += va != vb
            cna_differs += ca != cb
            identical += (va == vb and ca == cb)
            panel_change += panel[a] != panel[b]
            type_pairs[f"{st.get(a)} -> {st.get(b)}"] += 1
            try:
                purity_delta.append(float(attr["TUMOR_PURITY"][b]) - float(attr["TUMOR_PURITY"][a]))
            except (KeyError, ValueError):
                pass
        out["patients_more_gains_than_losses"] = more_gain
        out["patients_more_losses_than_gains"] = more_loss
        out["patients_gains_equal_losses"] = len(pts) - more_gain - more_loss
        k, n_dir = min(more_gain, more_loss), more_gain + more_loss
        out["patient_level_sign_test_two_sided_p"] = (
            min(1.0, 2 * sum(math.comb(n_dir, i) for i in range(0, k + 1)) / 2 ** n_dir) if n_dir else None)
        out["gene_level_mutations_shared"] = shared
        out["gene_level_mutations_gained_in_later_sample"] = gained
        out["gene_level_mutations_lost_in_later_sample"] = lost
        out["patients_with_any_gain"] = any_gain
        out["patients_with_any_loss"] = any_loss
        out["patients_with_different_variant_set"] = variant_differs
        out["patients_with_different_cna_call_set"] = cna_differs
        out["patients_with_identical_profile (variants and cna)"] = identical
        out["patients_with_panel_change_between_the_two_samples"] = panel_change
        out["sample_type_pairs"] = dict(type_pairs.most_common())
        out["purity_change_later_minus_earlier"] = quantiles(purity_delta)
        n = gained + lost
        if n:
            k = min(gained, lost)
            # events cluster within patients, so this event-level test overstates the evidence
            out["event_level_sign_test_two_sided_p (not independent, see patient-level test)"] = min(1.0, 2 * sum(math.comb(n, i) for i in range(0, k + 1)) / 2 ** n)
        for g in ("KRAS", "NRAS", "MAP2K1", "BRAF", "APC", "TP53"):
            out[f"{g}_gained"] = per_gene_gain.get(g, 0)
            out[f"{g}_lost"] = per_gene_loss.get(g, 0)
        return out

    pairs = collections.OrderedDict()
    pairs["braf_group__stable_samples"] = pair_stats(grp_braf, st_by_patient)
    pairs["control_strict__stable_samples"] = pair_stats(ctrl_strict, st_by_patient)
    v600_any = {p for p, ss in by_patient.items() if any(s in v600e for s in ss)}
    pairs["all_V600E_patients__all_samples_any_MSI"] = pair_stats(v600_any, by_patient)
    pairs["all_patients__all_samples_any_MSI"] = pair_stats(set(by_patient), by_patient)

    # all-samples view of the BRAF group: how many KRAS/NRAS carriers per rule
    kras, nras = entrez["KRAS"], entrez["NRAS"]
    pairs["braf_group_KRAS_carriers"] = {
        "any_stable_sample": sum(any(kras in mut_genes[s] for s in st_by_patient[p]) for p in grp_braf),
        "first_stable_sample": sum(kras in mut_genes[st_by_patient[p][0]] for p in grp_braf),
        "same_sample_as_V600E": sum(any(kras in mut_genes[s] and s in v600e for s in st_by_patient[p]) for p in grp_braf),
        "carriers_with_more_than_one_stable_sample": sum(
            len(st_by_patient[p]) > 1 for p in grp_braf if any(kras in mut_genes[s] for s in st_by_patient[p])),
    }
    pairs["braf_group_NRAS_carriers"] = {
        "any_stable_sample": sum(any(nras in mut_genes[s] for s in st_by_patient[p]) for p in grp_braf),
        "first_stable_sample": sum(nras in mut_genes[st_by_patient[p][0]] for p in grp_braf),
    }
    # calibration: how often does a truncal hotspot itself fail to reappear?
    n_pairs = n_disc = 0
    for p in v600_any:
        ss = by_patient[p]
        if len(ss) > 1:
            n_pairs += 1
            n_disc += len({s in v600e for s in ss}) > 1
    pairs["calibration_V600E_itself"] = {
        "multi_sample_patients_with_V600E_in_any_sample": n_pairs,
        "of_which_V600E_not_in_every_sample": n_disc,
        "interval_95": [round(v, 4) for v in clopper_pearson(n_disc, n_pairs)] if n_pairs else None,
    }
    x = pairs["braf_group__stable_samples"]
    n20 = x["patients_with_pair"]
    pairs["braf_group_uncertainty"] = {
        "KRAS_gain_per_paired_patient": f'{x["KRAS_gained"]}/{n20}',
        "interval_95": [round(v, 4) for v in clopper_pearson(x["KRAS_gained"], n20)],
        "KRAS_loss_per_paired_patient": f'{x["KRAS_lost"]}/{n20}',
        "loss_interval_95": [round(v, 4) for v in clopper_pearson(x["KRAS_lost"], n20)],
    }
    c = pairs["control_strict__stable_samples"]
    pairs["KRAS_gain_braf_group_vs_control_pairs"] = {
        "braf_group": f'{x["KRAS_gained"]}/{n20}', "control": f'{c["KRAS_gained"]}/{c["patients_with_pair"]}',
        "fisher_two_sided_p": fisher_two_sided(x["KRAS_gained"], n20 - x["KRAS_gained"], c["KRAS_gained"],
                                               c["patients_with_pair"] - c["KRAS_gained"]),
    }
    either = disc = 0
    for p in ctrl_strict:
        ss = st_by_patient[p]
        if len(ss) > 1:
            ka, kb = kras in mut_genes[ss[0]], kras in mut_genes[ss[-1]]
            either += ka or kb
            disc += ka != kb
    pairs["control_pairs_KRAS_discordance"] = {
        "pairs_with_KRAS_in_either_sample": either, "of_which_in_only_one_of_the_two": disc,
        "interval_95": [round(v, 4) for v in clopper_pearson(disc, either)]}
    with open(os.path.join(RAW, "paired-gain-loss.json"), "w") as fh:
        json.dump(pairs, fh, indent=1)

    # ------------------------------------------------ 5. power and bounds
    n1, n0 = len(grp_braf), len(ctrl_strict)
    power = collections.OrderedDict()
    power["zero_of_n_upper_bounds"] = {
        "n": n1,
        "one_sided_95": round(1 - 0.05 ** (1 / n1), 5),
        "two_sided_95_clopper_pearson": round(clopper_pearson(0, n1)[1], 5),
        "rule_of_three": round(3 / n1, 5),
    }
    sig_p = results["carrier_rule__control_strict"]["largest_p_still_significant"] or 0.05 / max(1, len(tested_c))
    power["alpha_used"] = {"nominal": 0.05, "bh_effective (largest p that still passed in my run)": sig_p}

    def pw(p0, p1, alpha):
        c = round(n0 * p0)
        tot = 0.0
        for a in range(0, n1 + 1):
            pa = math.exp(log_choose(n1, a) + (a * math.log(p1) if p1 > 0 else 0) + ((n1 - a) * math.log(1 - p1) if p1 < 1 else 0)) \
                if not (p1 == 0 and a > 0) else 0.0
            if pa < 1e-12:
                continue
            if fisher_two_sided(a, n1 - a, c, n0 - c) < alpha:
                tot += pa
        return tot

    grid = []
    for p0 in (0.005, 0.01, 0.02, 0.05, 0.10, 0.20, 0.50):
        row = {"control_prevalence": p0}
        for label, alpha in (("nominal", 0.05), ("bh_effective", sig_p)):
            # smallest enrichment ratio with >= 80% power
            up = None
            for ratio in [1.1, 1.2, 1.3, 1.4, 1.5, 1.75, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20]:
                if p0 * ratio < 1 and pw(p0, p0 * ratio, alpha) >= 0.8:
                    up = ratio
                    break
            down = None
            for ratio in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]:
                if pw(p0, p0 * ratio, alpha) >= 0.8:
                    down = ratio
                    break
            row[f"min_enrichment_ratio_80pct_power_{label}"] = up
            row[f"max_depletion_ratio_80pct_power_{label}"] = down
        grid.append(row)
    power["detectable_prevalence_ratio (n_braf=%d, n_ctrl=%d; control count fixed at expectation)" % (n1, n0)] = grid
    with open(os.path.join(RAW, "power.json"), "w") as fh:
        json.dump(power, fh, indent=1)

    print(json.dumps(flow, indent=1))
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
