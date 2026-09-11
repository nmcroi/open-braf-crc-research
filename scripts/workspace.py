"""Validate and search the public research graph; no network or private crawl."""
import argparse,csv,hashlib,json,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FOLDERS=['sources','datasets','claims','hypotheses','analyses','reviews']
def records(root=ROOT):
    return [r for folder in FOLDERS for r in json.loads((root/folder/'records.json').read_text())]
def validate(rr):
    ids=[r['id'] for r in rr]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate IDs')
    by={r['id']:r for r in rr}
    for r in rr:
        if not all(k in r for k in ['id','kind','title','depends_on']):raise ValueError('Missing fields')
        for dep in r['depends_on']:
            if dep not in by:raise ValueError('Unknown dependency: '+dep)
        if r['kind']=='hypothesis' and not r.get('falsification'):raise ValueError('Missing falsification test')
        if r['kind']=='source' and not all(r.get(k) for k in ['url','version','cohort_id','reading','sharing']):raise ValueError('Incomplete provenance')
    active=set();done=set()
    def visit(i):
        if i in active:raise ValueError('Dependency cycle')
        if i in done:return
        active.add(i)
        for dep in by[i]['depends_on']:visit(dep)
        active.remove(i);done.add(i)
    for i in by:visit(i)
    return by

def baseline(rr):
    return {r['id']:hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest() for r in rr if r['kind']=='source'}
def impact(rr,old):
    new=baseline(rr);changed={i for i in set(old)|set(new) if old.get(i)!=new.get(i)}
    affected=set(changed)
    while True:
        additions={r['id'] for r in rr if set(r['depends_on'])&affected}-affected
        if not additions:break
        affected|=additions
    return {'changed_sources':sorted(changed),'requires_review':sorted(affected-changed)}
def cohorts(rr):
    groups={}
    for r in rr:
        if r["kind"]=="source":groups.setdefault(r["cohort_id"],[]).append(r["id"])
    return groups

def search(query,root=ROOT):
    db=sqlite3.connect(':memory:');db.execute('create virtual table docs using fts5(id, text)')
    for r in records(root):db.execute('insert into docs values (?,?)',(r['id'],json.dumps(r,ensure_ascii=False)))
    with (root/'sources/catalog.csv').open() as f:
        for r in csv.DictReader(f):db.execute('insert into docs values (?,?)',(r['entry_id'],json.dumps(r)))
    for folder in ['docs','reviews','hypotheses']:
        for p in (root/folder).glob('*.md'):db.execute('insert into docs values (?,?)',(str(p.relative_to(root)),p.read_text()))
    # Quote user terms: do not interpret arbitrary FTS syntax.
    terms=' AND '.join('"'+x.replace('"','""')+'"' for x in query.split())
    return list(db.execute('select id,snippet(docs,1,"[","]","…",22) from docs where docs match ? limit 20',(terms,))) if terms else []
def main():
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('cohorts');sub.add_parser('validate');s=sub.add_parser('search');s.add_argument('query')
    s=sub.add_parser('baseline');s.add_argument('--out',required=True,type=Path)
    s=sub.add_parser('impact');s.add_argument('--baseline',required=True,type=Path)
    args=ap.parse_args();rr=records();validate(rr)
    if args.cmd=='validate':print(f'Validated {len(rr)} linked records.')
    elif args.cmd=='cohorts':print(json.dumps(cohorts(rr),indent=2))
    elif args.cmd=='baseline':args.out.write_text(json.dumps(baseline(rr),indent=2)+'\n')
    elif args.cmd=='impact':print(json.dumps(impact(rr,json.loads(args.baseline.read_text())),indent=2))
    else:print(json.dumps(search(args.query),indent=2))
if __name__=='__main__':main()
