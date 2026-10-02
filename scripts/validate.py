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
assert s['with_source_link']==sum(bool(r['source_url']) for r in rows)
assert s['unique_pmids']==len({r['pmid'] for r in rows if r['pmid']})
assert s['unique_ncts']==len({r['nct'] for r in rows if r['nct']})
duplicate_links=list(csv.DictReader((root/'sources/duplicate-links.csv').open()))
by_id={r['entry_id']:r for r in rows}
assert len({r['entry_id'] for r in duplicate_links})==len(duplicate_links)
for link in duplicate_links:
    duplicate,canonical=by_id[link['entry_id']],by_id[link['same_source_as']]
    assert duplicate['entry_id'] != canonical['entry_id']
    assert duplicate['doi'].lower() == canonical['doi'].lower() or canonical['doi'].lower() in duplicate['source_url'].lower()
assert s['distinct_sources_after_duplicate_links']==len(rows)-len(duplicate_links)
assert all('https://doi.org/https://doi.org/' not in r['source_url'] for r in rows)
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
