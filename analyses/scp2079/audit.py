import urllib.request,urllib.parse,csv,io,json,hashlib
from pathlib import Path
from collections import Counter,defaultdict
from concurrent.futures import ThreadPoolExecutor
base='https://singlecell.broadinstitute.org/single_cell/api/v1/studies/SCP2079/annotations/'
fields={'patientID':'group','biosample_id':'group','treatment':'group','MMRstatus':'group','response':'group','RECIST':'group','PFSmo':'numeric','tissueSite':'group'}
def fetch(item):
 field,typ=item;u=base+field+'/cell_values?'+urllib.parse.urlencode({'annotation_type':typ,'annotation_scope':'study'})
 with urllib.request.urlopen(urllib.request.Request(u,headers={'Accept':'application/json'}),timeout=60) as r:b=r.read()
 rows=list(csv.DictReader(io.StringIO(b.decode()),delimiter='\t'))
 return field,{x['NAME']:x[field] for x in rows},{'url':u,'rows':len(rows),'unique_cells':len({x['NAME'] for x in rows}),'sha256':hashlib.sha256(b).hexdigest()}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,fields.items()))
data={k:v for k,v,_ in results};log={k:v for k,_,v in results}
common=set.intersection(*(set(v) for v in data.values()))
patients=defaultdict(lambda:defaultdict(set));cells=Counter()
for cell in common:
 pid=data['patientID'][cell]
 for f in fields:patients[pid][f].add(data[f][cell])
 cells[(pid,data['treatment'][cell])]+=1
complete=[p for p,d in patients.items() if d['treatment']=={'Pre','On'}]
def categories(field,selection):return dict(Counter('|'.join(sorted(patients[p][field])) for p in selection))
checks=Counter()
for p,d in patients.items():
 if len(d['PFSmo'])!=1 or len(d['response'])!=1:checks['nonconstant']+=1;continue
 try:
  pfs=float(next(iter(d['PFSmo'])));resp=next(iter(d['response']))
  checks['above6_R' if pfs>6 and resp=='R' else 'below6_NR' if pfs<6 and resp=='NR' else 'other']+=1
 except ValueError:checks['missing_PFS']+=1
out={'study':'SCP2079','source_log':log,'shared_cells':len(common),'patients':len(patients),'complete_pairs':len(complete),'biosamples':len(set(data['biosample_id'].values())),'complete_MMR':categories('MMRstatus',complete),'complete_response':categories('response',complete),'complete_RECIST':categories('RECIST',complete),'complete_sites':categories('tissueSite',complete),'all_MMR':categories('MMRstatus',patients),'response_PFS_check':dict(checks),'minimum_cells_per_complete_patient_time':min(cells[p,t] for p in complete for t in ['Pre','On']),'complete_MSS_response':categories('response',[p for p in complete if patients[p]['MMRstatus']=={'MSS'}]),'nonconstant_MMR':sum(len(d['MMRstatus'])!=1 for d in patients.values())}
out['cell_threshold_sensitivity']={}
for threshold in [1,10,20,50,100]:
 selected=[p for p in complete if all(cells[p,t]>=threshold for t in ['Pre','On'])]
 mss=[p for p in selected if patients[p]['MMRstatus']=={'MSS'}]
 out['cell_threshold_sensitivity'][str(threshold)]={'all_pairs':len(selected),'MSS_pairs':len(mss),'MSS_response':categories('response',mss)}
out['response_PFS_exceptions']=dict(Counter(('exactly_6' if float(next(iter(d['PFSmo'])))==6 else 'above_6_NR' if float(next(iter(d['PFSmo'])))>6 else 'below_6_R') for d in patients.values() if len(d['PFSmo'])==1 and len(d['response'])==1 and not ((float(next(iter(d['PFSmo'])))>6 and d['response']=={'R'}) or (float(next(iter(d['PFSmo'])))<6 and d['response']=={'NR'}))))
(Path(__file__).parent/'portal-cohort-samenvatting.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:v for k,v in out.items() if k!='source_log'},indent=2))
