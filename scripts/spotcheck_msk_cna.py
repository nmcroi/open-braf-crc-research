"""Independent aggregate-only cBioPortal CNA spot check; prints no sample IDs."""
import collections,json,urllib.request
BASE='https://www.cbioportal.org/api'; STUDY='crc_msk_2026'
def get(path):
    with urllib.request.urlopen(BASE+path,timeout=120) as f:return json.load(f)
def post(path,body):
    req=urllib.request.Request(BASE+path,data=json.dumps(body).encode(),headers={'Accept':'application/json','Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=120) as f:return json.load(f)
info=get('/info')
samples=get(f'/studies/{STUDY}/samples?projection=DETAILED')
ids=sorted(x['sampleId'] for x in samples)[:100]
assign=post(f'/molecular-profiles/{STUDY}_cna/gene-panel-data/fetch',{'sampleListId':STUDY+'_all'})
panel={x['sampleId']:x['genePanelId'] for x in assign}
used={panel[x] for x in ids}
content={name:{v['entrezGeneId'] for v in get('/gene-panels/'+name)['genes']} for name in used}
def fetch(kind):return post(f'/molecular-profiles/{STUDY}_cna/discrete-copy-number/fetch?discreteCopyNumberEventType={kind}&projection=SUMMARY',{'sampleIds':ids})
allrows=fetch('ALL');events=fetch('HOMDEL_AND_AMP')
with_rows={x['sampleId'] for x in allrows};event_samples={x['sampleId'] for x in events}
offpanel_zero=sum(x['alteration']==0 and x['entrezGeneId'] not in content[panel[x['sampleId']]] for x in allrows)
print(json.dumps({'portal_version':info.get('portalVersion'),'backend_commit':info.get('gitCommitId'),'retrieved_sample_count':len(samples),'deterministic_subset':'first 100 sorted public sample IDs; IDs not saved or printed','ALL_rows':len(allrows),'ALL_values':dict(collections.Counter(str(x['alteration']) for x in allrows)),'HOMDEL_AND_AMP_rows':len(events),'samples_with_no_ALL_rows':len(set(ids)-with_rows),'samples_with_no_event_rows':len(set(ids)-event_samples),'samples_in_ALL_without_event':len(with_rows-event_samples),'off_panel_zero_rows':offpanel_zero,'interpretation':'An ALL zero on an off-panel gene is not a measured normal-copy call; no-row samples have no explicit negatives.'},indent=2))
