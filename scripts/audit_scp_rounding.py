import urllib.request,urllib.parse,json,csv,io,math,hashlib,argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
BASE='https://singlecell.broadinstitute.org/single_cell/api/v1/studies/SCP2079/'
def fetch(url):
 with urllib.request.urlopen(urllib.request.Request(url,headers={'Accept':'application/json'}),timeout=50) as r:b=r.read()
 return b,{'url':url,'sha256':hashlib.sha256(b).hexdigest()}
u=BASE+'annotations/total_counts/cell_values?annotation_type=numeric&annotation_scope=study'
b,log=fetch(u);depth={r['NAME']:float(r['total_counts']) for r in csv.DictReader(io.StringIO(b.decode()),delimiter='\t')};assert all(math.isfinite(n) and n>0 for n in depth.values())
def run(g):
 u=BASE+'expression/violin?'+urllib.parse.urlencode(dict(cluster='Epithelial Cells',genes=g,annotation_name='biosample_id',annotation_type='group',annotation_scope='study'))
 b,l=fetch(u);d=json.loads(b);out={'cells':0,'positive':0,'non_3decimal':0,'within_005_integer':0,'unique_feasible_integer':0,'no_feasible_integer':0,'multiple_feasible_integers':0,'zero_with_possible_positive_integer':0,'fits_wider_00055_interval':0,'forward_round4_then_round3':0};seen=set();errors=[]
 for s in d['values'].values():
  assert len(s['cells'])==len(s['y'])
  for c,y in zip(s['cells'],s['y']):
   assert c not in seen;seen.add(c);out['cells']+=1;n=depth[c]
   out['non_3decimal']+=abs(y-round(y,3))>1e-9
   # Closed interval is conservative at rounding ties: ties can only shrink it.
   low=max(0,math.expm1(max(0,y-0.0005)*math.log(2))*n/10000)
   high=math.expm1((y+0.0005)*math.log(2))*n/10000
   lo=math.ceil(low-1e-9);hi=math.floor(high+1e-9)
   if y>0:
    out['positive']+=1;c0=math.expm1(y*math.log(2))*n/10000
    out['within_005_integer']+=abs(c0-round(c0))<0.05
    low2=max(0,math.expm1(max(0,y-0.00055)*math.log(2))*n/10000);high2=math.expm1((y+0.00055)*math.log(2))*n/10000
    out['fits_wider_00055_interval']+=math.ceil(low2-1e-9)<=math.floor(high2+1e-9)
    forward=math.log2(1+round(c0)*10000/n)
    out['forward_round4_then_round3']+=abs(round(round(forward,4),3)-y)<1e-9
    feasible=max(0,hi-lo+1)
    out['unique_feasible_integer']+=feasible==1;out['no_feasible_integer']+=feasible==0;out['multiple_feasible_integers']+=feasible>1
   else:out['zero_with_possible_positive_integer']+=hi>=1
 assert seen==set(depth)
 out['source']=l;return g,out
with ThreadPoolExecutor(max_workers=3) as pool:r=dict(pool.map(run,['CXCL9','CXCL10','CXCL11','CD47','IDO1']))
out={'method':'Conditional inverse rounding interval test: y = round(log2(1+count*10000/total_counts),3). Closed endpoints conservatively admit ties. Not proof of author pipeline or raw-count identity. No individual cell data saved.','depth_source':log,'max_total_counts':max(depth.values()),'min_one_count_transformed':math.log2(1+10000/max(depth.values())),'genes':r}
args.out.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
