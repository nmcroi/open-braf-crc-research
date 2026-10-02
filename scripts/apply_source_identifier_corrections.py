"""Apply reviewed identifier fixes to the imported public source catalog.

Run after importing the private library. This script contains only public IDs and
metadata; it deliberately does not ingest the private library or patient records.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "sources/catalog.csv"
ROWS = list(csv.DictReader(CSV.open(newline="", encoding="utf-8")))

PMIDS = {
    "S0290": "41648030", "S0292": "39145064", "S0295": "39255538",
    "S0296": "38777726", "S0297": "38833658", "S0299": "41648647",
    "S0300": "39620921", "S0302": "39153969", "S0311": "41165465",
    "S0321": "40025995", "S0322": "40616773", "S0323": "40676860",
    "S0328": "40739424", "S0331": "41647992", "S0333": "41115464",
    "S0340": "41768137", "S0347": "41566838",
}
DOI_URL_PREFIX = {"S0303", "S0309", "S0313", "S0328", "S0329", "S0340"}
DUPLICATES = {
    "S0301": "S0011", "S0313": "S0057", "S0320": "S0406",
    "S0326": "S0412", "S0335": "S0020", "S0344": "S0041",
    "S0348": "S0428", "S0353": "S0350",
}

by_id = {row["entry_id"]: row for row in ROWS}
assert len(ROWS) == 516 and len(by_id) == 516, "Unexpected import version"
assert len({r["pmid"] for r in ROWS if r["pmid"]}) == 297
assert len({r["nct"] for r in ROWS if r["nct"]}) == 149
assert all(not by_id[i]["pmid"] for i in PMIDS)
assert all(by_id[i]["doi"].startswith("https://doi.org/") for i in DOI_URL_PREFIX)
assert not by_id["S0352"]["source_url"] and not any(by_id["S0352"][k] for k in ("pmid", "doi", "nct"))

for entry_id, pmid in PMIDS.items():
    by_id[entry_id]["pmid"] = pmid
    by_id[entry_id]["source_url"] = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
for entry_id in DOI_URL_PREFIX:
    row = by_id[entry_id]
    row["doi"] = row["doi"].removeprefix("https://doi.org/")
    row["source_url"] = f"https://doi.org/{row['doi']}" if not row["pmid"] else row["source_url"]

# PubMed PMID 41648647 has the same DOI as the imported row but a more
# specific title: the BRAF (V600E) qualifier was omitted in the import.
by_id["S0299"]["title"] = (
    "Safety and efficacy of encorafenib-cetuximab combination in BRAF "
    "(V600E)-mutated metastatic colorectal cancer: real-world evidence "
    "from the CONFIDENCE Spanish multicenter study."
)

for entry_id, canonical_id in DUPLICATES.items():
    row, canonical = by_id[entry_id], by_id[canonical_id]
    if row["doi"] and canonical["doi"]:
        assert row["doi"].lower() == canonical["doi"].lower(), (entry_id, canonical_id)
    else:
        assert canonical["doi"].lower() in row["source_url"].lower(), (entry_id, canonical_id)

# S0352 is a note about a search, not a bibliographic source. Retain its ID
# in the audit history instead of silently reallocating subsequent IDs.
ROWS = [row for row in ROWS if row["entry_id"] != "S0352"]
assert len(ROWS) == 515
assert len({r["pmid"] for r in ROWS if r["pmid"]}) == 314
fields = list(ROWS[0])
with CSV.open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(ROWS)

with (ROOT / "sources/duplicate-links.csv").open("w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=["entry_id", "same_source_as"], lineterminator="\n")
    writer.writeheader()
    writer.writerows({"entry_id": key, "same_source_as": value} for key, value in DUPLICATES.items())

summary_file = ROOT / "sources/import-summary.json"
summary = json.loads(summary_file.read_text())
summary.update({
    "entries": len(ROWS),
    "with_source_link": sum(bool(row["source_url"]) for row in ROWS),
    "unique_pmids": len({row["pmid"] for row in ROWS if row["pmid"]}),
    "unique_ncts": len({row["nct"] for row in ROWS if row["nct"]}),
    "distinct_sources_after_duplicate_links": len(ROWS) - len(DUPLICATES),
    "removed_non_source_entry_ids": ["S0352"],
    "identifier_review_date": "2026-10-02",
})
summary_file.write_text(json.dumps(summary, indent=2) + "\n")

def catalog_line(row):
    marker = f" (same source as {DUPLICATES[row['entry_id']]})" if row["entry_id"] in DUPLICATES else ""
    if row["source_url"]:
        title = row["title"].replace("[", "(").replace("]", ")")
        return f"- **{row['entry_id']} — {row['category']}**: [{title}]({row['source_url']}){marker}"
    return f"- **{row['entry_id']}**: {row['title']} — source link pending{marker}"

header = (
    "# Source catalog\n\n"
    "Imported metadata with an identifier-level review on 2 October 2026; "
    "this is not a validated systematic review. Duplicate sources across "
    "categories are retained and linked. S0284 and S0288 remain unresolved. "
    "Use the CSV for filtering. Identifier agreement does not prove that an "
    "entry matches the intended private library note. No trial recruitment "
    "status is claimed.\n\n"
)
(ROOT / "sources/catalog.md").write_text(header + "\n".join(map(catalog_line, ROWS)) + "\n")
print(f"Corrected {len(ROWS)} rows; {summary['unique_pmids']} PMIDs, {summary['distinct_sources_after_duplicate_links']} distinct linked sources")
