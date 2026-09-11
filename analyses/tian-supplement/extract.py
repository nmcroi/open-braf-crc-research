from pathlib import Path
import openpyxl,json,hashlib,csv,urllib.request,zipfile,io,argparse
p=Path(__file__).parent
source='https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9941044/supplementaryFiles'
parser=argparse.ArgumentParser()
parser.add_argument('--archive',type=Path,help='Existing unmodified public supplementary ZIP, for offline use')
args=parser.parse_args()
if args.archive:
 archive=zipfile.ZipFile(args.archive)
else:
 with urllib.request.urlopen(source,timeout=30) as response: archive=zipfile.ZipFile(io.BytesIO(response.read()))
raw=archive.read('41591_2022_2181_MOESM3_ESM.xlsx')
w=openpyxl.load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
genes=['CXCL9','CXCL10','CXCL11','PRDX1','HIF1A','CD47','VEGFA','WNT11','PTPN11','DUSP6','ETV4','ETV5','SPRY4','CD274','IDO1','PTGS2']
out=[];counts={}
for s in w:
 count=0; missing=0;seen=set()
 for row in s.iter_rows(min_row=2,values_only=True):
  if row[0] is None:
   missing+=1
   if missing>=100:break
   continue
  missing=0;count+=1;seen.add(row[0])
  if row[0] in genes:out.append(dict(zip(['gene','avg_log2FC','pct_on','pct_pre','p_val','p_val_adj','neglog10pAdj','rank_score'],row),group=s.title))
 counts[s.title]={'nonempty_gene_rows':count,'unique_genes':len(seen),'selected_found':sum(x['group']==s.title for x in out)}
with (p/'geselecteerde-genen.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=list(out[0]));writer.writeheader();writer.writerows(out)
res={'source':'Tian et al, DOI 10.1038/s41591-022-02181-8, Supplementary Table 2','counts':counts,'sha256':{'41591_2022_2181_MOESM3_ESM.xlsx':hashlib.sha256(raw).hexdigest()},'rows':out,'note':'Published aggregate gene statistics extracted, not recalculated from cells. R/NR mean PFS above/below six months according to caption, not RECIST response. Stops after 100 blank gene rows because worksheets have padded dimensions.'}
(p/'supplement-controle.json').write_text(json.dumps(res,indent=2))
print(json.dumps(counts))
for x in out:print(x['group'],x['gene'],x['avg_log2FC'],x['p_val_adj'])
