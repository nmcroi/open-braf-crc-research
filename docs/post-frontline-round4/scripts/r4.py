import json,time,urllib.request,urllib.parse,csv
def get(url):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'open-braf-check/1.0'}),timeout=40) as r: return r.read()
        except Exception as e: err=e; time.sleep(2+2*i)
    raise err
known={r['pmid'] for r in csv.DictReader(open('sources/catalog.csv')) if r['pmid']}
Q={
 'q1_ec_recent':'(encorafenib[tiab] AND cetuximab[tiab]) AND ("2026/08/15"[EDAT] : "2026/10/02"[EDAT])',
 'q2_braf_crc_recent':'(BRAF[tiab] AND V600E[tiab] AND colorectal[tiab]) AND ("2026/09/10"[EDAT] : "2026/10/02"[EDAT])',
 'q3_post_progression':'(encorafenib[tiab] AND colorectal[tiab] AND (("after progression"[tiab]) OR "subsequent"[tiab] OR "second-line"[tiab] OR "post-progression"[tiab] OR "beyond progression"[tiab] OR rechallenge[tiab] OR "later-line"[tiab])) AND ("2025/01/01"[EDAT] : "2026/10/02"[EDAT])',
 'q4_realworld_first_line':'(encorafenib[tiab] AND cetuximab[tiab] AND (FOLFOX[tiab] OR mFOLFOX6[tiab] OR chemotherapy[tiab]) AND ("real-world"[tiab] OR retrospective[tiab] OR cohort[tiab])) AND ("2025/06/01"[EDAT] : "2026/10/02"[EDAT])',
 'q5_breakwater':'BREAKWATER[tiab] AND colorectal[tiab] AND ("2026/06/01"[EDAT] : "2026/10/02"[EDAT])',
}
out={}
allids=set()
for k,q in Q.items():
    d=json.loads(get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmode=json&retmax=200&term='+urllib.parse.quote(q)))['esearchresult']
    out[k]={'query':q,'count':d['count'],'ids':d['idlist']}; allids|=set(d['idlist']); time.sleep(0.5)
ids=sorted(allids)
meta={}
for i in range(0,len(ids),100):
    d=json.loads(get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&id='+','.join(ids[i:i+100])))['result']
    for p in d['uids']: meta[p]={'title':d[p]['title'],'journal':d[p]['source'],'pubdate':d[p]['pubdate'],'types':d[p].get('pubtype',[])}
    time.sleep(0.5)
json.dump({'date':'2026-10-02','queries':out,'records':meta},open('pubmed-round4.json','w'),indent=1)
for k,v in out.items():
    print('==',k,v['count'])
    for p in v['ids']:
        m=meta[p]; print('  ','KNOWN' if p in known else 'new  ',p,'|',m['pubdate'],'|',m['journal'],'|',m['title'][:150])
