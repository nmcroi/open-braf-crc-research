#!/usr/bin/env python3
"""Independent fetch of the public cBioPortal study crc_msk_2026.

Written from scratch for the issue 5 review. Standard library only.

Everything that is downloaded is row-level public data and is written to a
local cache directory that must stay OUTSIDE the repository (default:
./cache next to this script, listed in .gitignore). Only the manifest
(endpoint, parameters, byte count, SHA-256 of the raw response body) is meant
to be published; it is written to ../raw/fetch-manifest.json.

Patient-level clinical data (which contains survival fields) is deliberately
never requested.

Usage:
    python fetch.py [--cache DIR]
"""
import argparse
import datetime
import gzip
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://www.cbioportal.org/api"
STUDY = "crc_msk_2026"
MUT_PROFILE = STUDY + "_mutations"
CNA_PROFILE = STUDY + "_cna"
SV_PROFILE = STUDY + "_structural_variants"
HERE = os.path.dirname(os.path.abspath(__file__))


def http(method, path, body=None, tries=6):
    url = API + path
    data = None
    headers = {"Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    last = None
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=600) as resp:
                return resp.read()
        except urllib.error.HTTPError as exc:
            if 400 <= exc.code < 500 and exc.code != 429:
                raise RuntimeError(f"{exc.code} for {url}: {exc.read()[:300]!r}")
            last = exc
            time.sleep(10 * (attempt + 1))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = exc
            wait = 10 * (attempt + 1)
            print(f"  retry {attempt + 1} after {wait}s: {exc}", file=sys.stderr)
            time.sleep(wait)
    raise RuntimeError(f"failed after {tries} tries: {url}: {last}")


class Cache:
    def __init__(self, directory):
        self.dir = directory
        os.makedirs(directory, exist_ok=True)
        self.manifest_path = os.path.join(directory, "manifest.json")
        self.manifest = {}
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path) as fh:
                self.manifest = json.load(fh)

    def get(self, name, method, path, body=None, body_note=None, compact=None):
        """Fetch once; store (optionally compacted) JSON gzip; hash raw bytes."""
        fpath = os.path.join(self.dir, name + ".json.gz")
        if name in self.manifest and os.path.exists(fpath):
            with gzip.open(fpath, "rt") as fh:
                return json.load(fh)
        print("fetch", name, file=sys.stderr)
        raw = http(method, path, body)
        parsed = json.loads(raw)
        stored = compact(parsed) if compact else parsed
        with gzip.open(fpath, "wt") as fh:
            json.dump(stored, fh)
        self.manifest[name] = {
            "method": method,
            "url": API + path,
            "request_body": body_note if body_note is not None else body,
            "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "response_bytes": len(raw),
            "response_sha256": hashlib.sha256(raw).hexdigest(),
            "records": len(parsed) if isinstance(parsed, list) else None,
        }
        with open(self.manifest_path, "w") as fh:
            json.dump(self.manifest, fh, indent=1, sort_keys=True)
        return stored


def compact_cna(rows):
    return [[r["sampleId"], r["entrezGeneId"], r["alteration"]] for r in rows]


def compact_mut(rows):
    keep = ("sampleId", "patientId", "entrezGeneId", "proteinChange", "mutationType",
            "mutationStatus", "variantType", "chr", "startPosition", "endPosition",
            "referenceAllele", "variantAllele", "tumorAltCount", "tumorRefCount")
    out = []
    for r in rows:
        d = {k: r.get(k) for k in keep}
        d["hugo"] = (r.get("gene") or {}).get("hugoGeneSymbol")
        out.append(d)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(HERE, "cache"))
    args = ap.parse_args()
    c = Cache(args.cache)

    c.get("info", "GET", "/info")
    c.get("study", "GET", f"/studies/{STUDY}")
    c.get("molecular_profiles", "GET", f"/studies/{STUDY}/molecular-profiles")
    c.get("clinical_attributes", "GET", f"/studies/{STUDY}/clinical-attributes")
    samples = c.get("samples", "GET", f"/studies/{STUDY}/samples?projection=DETAILED&pageSize=100000")
    c.get("clinical_sample", "GET",
          f"/studies/{STUDY}/clinical-data?clinicalDataType=SAMPLE&projection=SUMMARY&pageSize=10000000")
    sample_ids = sorted(s["sampleId"] for s in samples)

    for prof in (MUT_PROFILE, CNA_PROFILE, SV_PROFILE):
        c.get("gene_panel_data_" + prof, "POST", f"/molecular-profiles/{prof}/gene-panel-data/fetch",
              {"sampleListId": STUDY + "_all"})
    panels = set()
    for prof in (MUT_PROFILE, CNA_PROFILE):
        rows = c.get("gene_panel_data_" + prof, "POST", f"/molecular-profiles/{prof}/gene-panel-data/fetch",
                     {"sampleListId": STUDY + "_all"})
        for row in rows:
            if row.get("genePanelId"):
                panels.add(row["genePanelId"])
    for p in sorted(panels):
        c.get("gene_panel_" + p, "GET", f"/gene-panels/{p}")

    # The GET variant of this endpoint insists on an entrezGeneId, so use the
    # POST fetch with the all-samples list to get every mutation in the study.
    c.get("mutations", "POST",
          f"/molecular-profiles/{MUT_PROFILE}/mutations/fetch?projection=DETAILED",
          {"sampleListId": STUDY + "_all"}, compact=compact_mut)

    # Discrete copy number. Default event type (HOMDEL_AND_AMP) in one call,
    # and the full matrix (ALL) in batches of sorted sample IDs.
    c.get("cna_homdel_amp", "POST",
          f"/molecular-profiles/{CNA_PROFILE}/discrete-copy-number/fetch?discreteCopyNumberEventType=HOMDEL_AND_AMP&projection=SUMMARY",
          {"sampleListId": STUDY + "_all"}, compact=compact_cna)
    batch = 250
    for i in range(0, len(sample_ids), batch):
        chunk = sample_ids[i:i + batch]
        c.get(f"cna_all_{i // batch:03d}", "POST",
              f"/molecular-profiles/{CNA_PROFILE}/discrete-copy-number/fetch?discreteCopyNumberEventType=ALL&projection=SUMMARY",
              {"sampleIds": chunk},
              body_note={"sampleIds": f"sorted sample IDs [{i}:{i + len(chunk)}] of the study sample list"},
              compact=compact_cna)

    # The ALL call silently drops some calls that HOMDEL_AND_AMP reports as -2.
    # Fetch the underlying stored values for exactly those sample and gene sets
    # from the generic molecular-data endpoint to see what they are.
    import glob
    seen = set()
    for f in sorted(glob.glob(os.path.join(args.cache, "cna_all_*.json.gz"))):
        with gzip.open(f, "rt") as fh:
            for s, g, _a in json.load(fh):
                seen.add((s, g))
    with gzip.open(os.path.join(args.cache, "cna_homdel_amp.json.gz"), "rt") as fh:
        missing = [(s, g) for s, g, _a in json.load(fh) if (s, g) not in seen]
    if missing:
        ms = sorted({s for s, _ in missing})
        mg = sorted({g for _, g in missing})
        c.get("cna_molecular_data_check", "POST",
              f"/molecular-profiles/{CNA_PROFILE}/molecular-data/fetch?projection=SUMMARY",
              {"sampleIds": ms, "entrezGeneIds": mg},
              body_note={"sampleIds": f"{len(ms)} samples that have a HOMDEL_AND_AMP call absent from the ALL response",
                         "entrezGeneIds": mg},
              compact=lambda rows: [[r["sampleId"], r["entrezGeneId"], r["value"]] for r in rows])

    # Publishable manifest (no row-level content).
    out = os.path.join(HERE, "..", "raw", "fetch-manifest.json")
    with open(out, "w") as fh:
        json.dump(c.manifest, fh, indent=1, sort_keys=True)
    print("manifest entries:", len(c.manifest))


if __name__ == "__main__":
    main()
