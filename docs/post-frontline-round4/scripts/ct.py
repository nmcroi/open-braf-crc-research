import json,urllib.request,urllib.parse,time
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'open-braf-check/1.0'}),timeout=40) as r: return json.loads(r.read())
F='NCTId,BriefTitle,OverallStatus,LastUpdatePostDate,StudyFirstPostDate,HasResults,LocationCountry,Phase'
out={'date':'2026-10-02','tracked':{},'new_or_updated':[]}
for n in ['NCT06884618','NCT07178717','NCT06640166','NCT05355701','NCT05379985','NCT06445062','NCT06607185','NCT07150403','NCT04607421']:
    p=get('https://clinicaltrials.gov/api/v2/studies/'+n+'?fields='+F)
    ps=p['protocolSection']; s=ps['statusModule']
    c=sorted({l.get('country') for l in ps.get('contactsLocationsModule',{}).get('locations',[])})
    out['tracked'][n]={'title':ps['identificationModule']['briefTitle'],'status':s['overallStatus'],'updated':s['lastUpdatePostDateStruct']['date'],'results':p.get('hasResults'),'countries':c}
    print(n,s['overallStatus'],s['lastUpdatePostDateStruct']['date'],p.get('hasResults'),'|',ps['identificationModule']['briefTitle'][:70],'|',','.join(c)[:90]); time.sleep(0.2)
q={'query.cond':'colorectal','query.term':'BRAF AND AREA[LastUpdatePostDate]RANGE[2026-09-12,MAX]','pageSize':'100','fields':F}
d=get('https://clinicaltrials.gov/api/v2/studies?'+urllib.parse.urlencode(q))
print('--- updated since 12-09:',len(d['studies']))
for p in d['studies']:
    ps=p['protocolSection']; s=ps['statusModule']
    c=sorted({l.get('country') for l in ps.get('contactsLocationsModule',{}).get('locations',[])})
    row={'nct':ps['identificationModule']['nctId'],'title':ps['identificationModule']['briefTitle'],'status':s['overallStatus'],'first':s['studyFirstPostDateStruct']['date'],'updated':s['lastUpdatePostDateStruct']['date'],'countries':c}
    out['new_or_updated'].append(row)
    print(row['nct'],row['status'],'first',row['first'],'upd',row['updated'],'|',row['title'][:95],'|',','.join(c)[:60])
json.dump(out,open('ctgov-round4.json','w'),indent=1)
