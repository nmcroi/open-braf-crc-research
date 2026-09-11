"""Prepare a source-pointer packet; no model calls and no inferred gene clustering."""
import csv,json,re,argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('uniprot_tsv',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
seeds=['BRAF','KRAS','PRDX1','WNT11','CD47','VEGFA','PTPN11','HIF1A'];hits={g:[] for g in seeds}
with a.uniprot_tsv.open() as f:
 for r in csv.DictReader(f,delimiter='\t'):
  for g in set(seeds)&set(r['gene_names'].split()):
   hits[g].append({'entry':r['entry'],'names':r['gene_names'],'url':r['link'],'pmids':sorted(set(re.findall(r'PubMed:(\d+)',r['function'])))})
a.out.write_text(json.dumps({'input_type':'Manually selected research seeds; not a measured co-cluster','gene_sources':hits,'missing':[g for g,h in hits.items() if not h],'ambiguous':[g for g,h in hits.items() if len(h)>1],'limitations':'Bundled annotations not refreshed against live UniProt. Alias matches are candidates, not formal identifier validation. Paper pointers are not claims of full-text review. All source families must be examined, not only top-k snippets.'},indent=2))
print('Packet built:',sum(bool(v) for v in hits.values()),'of',len(seeds),'genes mapped; no biological result claimed.')
