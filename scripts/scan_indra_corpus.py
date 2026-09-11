"""Stream an INDRA JSON array; descriptive name matching, not biological validation."""
import argparse,gzip,json,collections,itertools
from pathlib import Path
SEEDS={'BRAF','KRAS','PRDX1','WNT11','CD47','VEGFA','PTPN11','HIF1A'}
def objects(f):
    decoder=json.JSONDecoder();buf='';started=False;eof=False
    while True:
        if not eof and len(buf)<65536:
            chunk=f.read(1048576);buf+=chunk;eof=not chunk
        buf=buf.lstrip()
        if not started:
            if not buf.startswith('['):raise ValueError('Expected JSON array')
            buf=buf[1:];started=True;continue
        buf=buf.lstrip()
        if buf.startswith(','):buf=buf[1:];continue
        if buf.startswith(']'):return
        try:obj,end=decoder.raw_decode(buf)
        except json.JSONDecodeError:
            if eof:raise
            chunk=f.read(1048576);buf+=chunk;eof=not chunk;continue
        yield obj;buf=buf[end:]
def names(x):
    found=set()
    if isinstance(x,dict):
        if 'name' in x and 'db_refs' in x:found.add(x['name'])
        for k,v in x.items():
            if k not in {'evidence','supports','supported_by'}:found|=names(v)
    elif isinstance(x,list):
        for v in x:found|=names(v)
    return found

def main():
    p=argparse.ArgumentParser();p.add_argument('corpus',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    count=0;hits=collections.Counter();pairs=collections.Counter();examples=[]
    with gzip.open(a.corpus,'rt') as f:
        for obj in objects(f):
            count+=1;selected=names(obj)&SEEDS;hits.update(selected)
            for pair in itertools.combinations(sorted(selected),2):pairs[' / '.join(pair)]+=1
            if len(selected)>1 and len(examples)<100:
                examples.append({'type':obj['type'],'seed_names':sorted(selected),'pmids':sorted({str(e['pmid']) for e in obj.get('evidence',[]) if e.get('pmid')}),'evidence_count':len(obj.get('evidence',[]))})
    result={'statements_parsed':count,'seed_matching':'Exact agent name, not exhaustive alias or context search','seed_statement_counts':dict(hits),'cooccurring_seed_pair_counts':dict(pairs),'first_100_pair_examples':examples,'limitations':'Counts are assembled statements, not patients, unique studies or validated CRC mechanisms. Co-occurrence is not necessarily a direct causal edge; names can occur in complexes or conditions. Tissue, genotype, evidence independence, direction and source correctness have not been reviewed.'}
    a.out.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='first_100_pair_examples'},indent=2))
if __name__=='__main__':main()
