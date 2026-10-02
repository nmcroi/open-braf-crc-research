#!/usr/bin/env python3
"""Re-implementation of the SUBMITTED selection rule on my own cached download.

Written only after my own numbers (analyze.py) were on disk and after reading
the submitted script comutations.py (SHA-256 4c3a94dc...c4bb). Purpose: explain
the differences between my recount and the submitted figures, feature by
feature. It re-states the submitted logic in my own code; it does not import or
execute the submitted script.

Submitted logic, as read:
  group A samples = Stable AND BRAF proteinChange starts with "V600E"
  group B samples = Stable AND no BRAF mutation record
  features        = any mutation record per gene, plus AMP (value 2) per gene
  carrier rule    = union of features over the patient's samples IN THAT GROUP'S SAMPLE LIST
  first_sample    = features of the lexicographically first sample IN THAT LIST
  a patient in both A and B is removed from B
  tested when carriers in A + B >= 15; denominators are always all patients

Optionally compares against the submitted result snapshot (aggregate JSON).

Usage:
    python replicate_submitted_rule.py [--cache DIR] [--submitted PATH/msk-comutations.json]
"""
import argparse
import collections
import gzip
import json
import os

from analyze import fisher_two_sided, bh

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "raw")
STUDY = "crc_msk_2026"


def load(cache, name):
    with gzip.open(os.path.join(cache, name + ".json.gz"), "rt") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(HERE, "cache"))
    ap.add_argument("--submitted", default=None)
    args = ap.parse_args()
    samples = load(args.cache, "samples")
    patient_of = {s["sampleId"]: s["patientId"] for s in samples}
    msi = {r["sampleId"]: r["value"] for r in load(args.cache, "clinical_sample") if r["clinicalAttributeId"] == "MSI_TYPE"}
    symbol, per_panel = {}, []
    for f in ("IMPACT341", "IMPACT410", "IMPACT468", "IMPACT505"):
        genes = load(args.cache, "gene_panel_" + f)["genes"]
        per_panel.append({g["hugoGeneSymbol"] for g in genes})
        for g in genes:
            symbol[g["entrezGeneId"]] = g["hugoGeneSymbol"]
    on_all = set.intersection(*per_panel)
    feat = collections.defaultdict(set)
    v600e, any_braf = set(), set()
    for m in load(args.cache, "mutations"):
        feat[m["sampleId"]].add(m["hugo"])
        if m["hugo"] == "BRAF":
            any_braf.add(m["sampleId"])
            if (m["proteinChange"] or "").startswith("V600E"):
                v600e.add(m["sampleId"])
    for s, g, a in load(args.cache, "cna_homdel_amp"):
        if a == 2:
            feat[s].add(symbol[g] + " amp")
    stable = {s for s, v in msi.items() if v == "Stable"}
    a_samples = sorted(stable & v600e)
    b_samples = sorted(stable - any_braf)

    out = {"a_samples": len(a_samples), "b_samples": len(b_samples)}
    for rule in ("carrier", "first_sample"):
        def collapse(ss):
            per, seen = collections.defaultdict(set), set()
            for s in ss:
                p = patient_of[s]
                if rule == "carrier":
                    per[p] |= feat.get(s, set()) - {"BRAF"}
                elif p not in seen:
                    seen.add(p)
                    per[p] = feat.get(s, set()) - {"BRAF"}
            return per
        A, B = collapse(a_samples), collapse(b_samples)
        overlap = len(set(A) & set(B))
        for p in set(A) & set(B):
            B.pop(p)
        nA, nB = len(A), len(B)
        cA = collections.Counter(f for v in A.values() for f in v)
        cB = collections.Counter(f for v in B.values() for f in v)
        rows = []
        for g in set(cA) | set(cB):
            a, b = cA[g], cB[g]
            if a + b < 15:
                continue
            rows.append({"feature": g, "a": a, "b": b, "p": fisher_two_sided(a, nA - a, b, nB - b)})
        for r, q in zip(rows, bh([r["p"] for r in rows])):
            r["q"] = q
        sig = sorted((r for r in rows if r["q"] < 0.05), key=lambda r: r["p"])
        partial = lambda f: f.replace(" amp", "") not in on_all
        res = {"n_A": nA, "n_B": nB, "patients_in_both_lists_removed_from_B": overlap,
               "A_patients_with_more_than_one_listed_sample": sum(
                   1 for n in collections.Counter(patient_of[s] for s in a_samples).values() if n > 1),
               "features_tested": len(rows), "significant": len(sig),
               "tested_features_on_genes_missing_from_at_least_one_panel": sum(1 for r in rows if partial(r["feature"])),
               "significant_features_on_genes_missing_from_at_least_one_panel": sorted(
                   r["feature"] for r in sig if partial(r["feature"])),
               "significant_features": [{"feature": r["feature"], "a": r["a"], "b": r["b"]} for r in sig]}
        if args.submitted:
            sub = json.load(open(args.submitted))["rules"][rule]
            theirs = {r["feature"]: (r["a"], r["b"]) for r in sub["significant_bh_0.05"]}
            mine = {r["feature"]: (r["a"], r["b"]) for r in sig}
            res["submitted"] = {"n_A": sub["n_braf_v600e_mss"], "n_B": sub["n_mss_braf_wt"],
                                "features_tested": sub["n_features_tested"], "significant": len(theirs)}
            res["significant_only_in_submitted"] = sorted(set(theirs) - set(mine))
            res["significant_only_in_replication"] = sorted(set(mine) - set(theirs))
            res["shared_significant_with_different_counts"] = {
                f: {"submitted": theirs[f], "replication": mine[f]} for f in set(theirs) & set(mine) if theirs[f] != mine[f]}
        out[rule] = res
    with open(os.path.join(RAW, "replication-of-submitted-rule.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
