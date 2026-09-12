"""Scoped processed-matrix QC; stdlib only. Does not validate biology or raw CELs."""
import argparse,csv,gzip,hashlib,json,math,statistics
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('matrix');p.add_argument('--out',required=True);a=p.parse_args()
b=Path(a.matrix).read_bytes();text=gzip.decompress(b).decode();meta={}
for line in text.splitlines():
 if line.startswith(('!Sample_title','!Sample_geo_accession')):
  row=next(csv.reader([line],delimiter='\t'));meta[row[0]]=row[1:]
lines=text.split('!series_matrix_table_begin')[1].split('!series_matrix_table_end')[0].strip().splitlines()
rows=list(csv.reader(lines,delimiter='\t'));header=rows.pop(0);ids=[x[0] for x in rows]
assert header[1:]==meta['!Sample_geo_accession']
assert all(len(x)==len(header) for x in rows)
x=[[float(v) for v in row[1:]] for row in rows];cols=list(zip(*x))
assert all(math.isfinite(v) for c in cols for v in c)
def q(c,f):
 s=sorted(c);k=(len(s)-1)*f;i=int(k);return s[i]+(s[min(i+1,len(s)-1)]-s[i])*(k-i)
def corr(x,y):
 mx=statistics.mean(x);my=statistics.mean(y)
 return sum((a-mx)*(b-my) for a,b in zip(x,y))/math.sqrt(sum((a-mx)**2 for a in x)*sum((b-my)**2 for b in y))
profiles=[{'sample':header[i+1],'title':meta['!Sample_title'][i],'min':min(c),'q25':q(c,.25),'median':q(c,.5),'q75':q(c,.75),'max':max(c),'zeros':c.count(0)} for i,c in enumerate(cols)]
pairs=[{'a':header[i+1],'b':header[j+1],'pearson':corr(cols[i],cols[j]),'identical':cols[i]==cols[j]} for i in range(len(cols)) for j in range(i)]
out={'sha256':hashlib.sha256(b).hexdigest(),'rows':len(x),'samples':len(cols),'duplicate_probe_ids':len(ids)-len(set(ids)),'nonfinite_values':0,'profiles':profiles,'pairs':pairs,'scope':'Processed matrix only; correlations cannot establish biological replicate independence'}
Path(a.out).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'rows':len(x),'samples':len(cols),'duplicate_probe_ids':out['duplicate_probe_ids'],'profiles':profiles,'correlation_range':[min(z['pearson'] for z in pairs),max(z['pearson'] for z in pairs)],'identical_pairs':sum(z['identical'] for z in pairs)},indent=2))
