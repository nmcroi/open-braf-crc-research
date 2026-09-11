"""Reproduce basic aggregate counts from the pinned initiative download manifest."""
import argparse,csv,json,collections
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('downloads',type=Path);a=p.parse_args()
r=a.downloads/'sorgerlab/indra_assembly_paper'
ids=(r/'run_assembly/pmids.txt').read_text().split();assert all(v.isdigit() for v in ids)
x=json.loads((r/'data/curation/indra_assembly_curations.json').read_text())
with (a.downloads/'zou-group/virtual-lab/nanobody_design/experimental_data/platemap.csv').open() as f:plate=list(csv.DictReader(f))
print(json.dumps({'pmids':len(ids),'unique_pmids':len(set(ids)),'curations':len(x),'unique_statement_hashes':len({v['pa_hash'] for v in x}),'tags':dict(collections.Counter(v['tag'] for v in x)),'plate_rows':len(plate),'unique_wells':len({v['Well Location'] for v in plate})},indent=2))
