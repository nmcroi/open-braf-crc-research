"""Check catalog structure and aggregate result invariants; no network required."""
import csv,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((root/'sources/catalog.csv').open()))
assert len({r['entry_id'] for r in rows})==len(rows)
for r in rows:
    assert r['title'] and r['verification'] in {'imported_metadata_not_independently_verified','source_link_pending'}
    assert not r['pmid'] or re.fullmatch(r'\d+',r['pmid'])
    assert not r['nct'] or re.fullmatch(r'NCT\d{8}',r['nct'])
    assert not r['source_url'] or r['source_url'].startswith(('https://','http://'))
s=json.loads((root/'sources/import-summary.json').read_text())
assert s['entries']==len(rows)
a=json.loads((root/'results/scp2079-metadata-audit.json').read_text())
assert a['complete_pairs']==sum(a['complete_MMR'].values())
assert a['patients']>=a['complete_pairs']
assert a['shared_cells']==95421
assert all(v['rows']==v['unique_cells']==a['shared_cells'] for v in a['source_log'].values())
last=a['complete_pairs']
for n,d in sorted(a['cell_threshold_sensitivity'].items(),key=lambda x:int(x[0])):
    assert d['MSS_pairs']<=d['all_pairs']<=last
    assert sum(d['MSS_response'].values())==d['MSS_pairs']
    last=d['all_pairs']
print(f'Validated {len(rows)} catalog entries and cohort invariants.')
