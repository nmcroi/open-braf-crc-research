"""Read GitHub task state; never mutate Issues. Local snapshot stays visibly dated."""
import argparse,datetime,json,subprocess
from pathlib import Path
REPO='nmcroi/open-braf-crc-research'
STATUSES={'open','claimed','in-progress','submitted','in-review','done','blocked'}
def normalize(issues):
    out=[]
    for i in issues:
        labels=[v['name'][7:] for v in i.get('labels',[]) if v['name'].startswith('status:')]
        status=labels[0] if len(labels)==1 and labels[0] in STATUSES else 'status-conflict'
        if i['state']=='CLOSED' and status!='done':status='closed-without-accepted-status'
        out.append(dict(id=f"TASK-{i['number']:04}",number=i['number'],title=i['title'],url=i['url'],status=status,updated_at=i['updatedAt'],assignees=[x['login'] for x in i.get('assignees',[])]))
    return out

def render(payload,stale=None):
    text='# Centrale openbare taken\n\nBron: GitHub Issues. Dit is een leesbare kopie, geen tweede werklijst.\n\n'
    text+='Laatste geslaagde synchronisatie (UTC): '+payload.get('synced_at','onbekend')+'\n\n'
    if stale:text+='**LET OP: synchronisatie mislukt; onderstaande informatie kan verouderd zijn.**\n\n'
    text+='| Taak | Status | Laatste GitHub-wijziging |\n|---|---|---|\n'
    for i in payload.get('tasks',[]):text+=f"| [{i['id']}: {i['title'].replace('|','/').replace(chr(10),' ')}]({i['url']}) | {i['status']} | {i['updated_at']} |\n"
    text+='\nEen recente wijziging is niet automatisch onderzoekswerk. Bekijk de gekoppelde resultaat- en reviewberichten. Een externe onderzoeker of model is pas actief bevestigd met een beschreven taak en updateafspraak.\n'
    return text

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--vault',type=Path);p.add_argument('--input',type=Path,help='Offline test fixture; never claim live freshness');a=p.parse_args()
    try:
        raw=json.loads(a.input.read_text()) if a.input else json.loads(subprocess.check_output(['gh','issue','list','--repo',REPO,'--state','all','--limit','1000','--json','number,title,state,updatedAt,url,assignees,labels'],stderr=subprocess.PIPE,timeout=40))
        if len(raw)>=1000:raise RuntimeError('Possible truncation; use paginated API before syncing')
        payload={'synced_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':'fixture' if a.input else 'live','tasks':normalize(raw)}
        a.out.parent.mkdir(parents=True,exist_ok=True);tmp=a.out.with_suffix('.tmp');tmp.write_text(json.dumps(payload,indent=2));tmp.replace(a.out)
        if a.vault:
            board=a.vault/'10-voortgang/GITHUB-TAKEN.md';board.parent.mkdir(parents=True,exist_ok=True);board.write_text(render(payload,stale=bool(a.input)))
        print(f"Read {len(raw)} tasks; source {payload['mode']}")
    except Exception:
        if a.vault:
            old=json.loads(a.out.read_text()) if a.out.exists() else {};board=a.vault/'10-voortgang/GITHUB-TAKEN.md';board.parent.mkdir(parents=True,exist_ok=True);board.write_text(render(old,stale=True))
        raise SystemExit('Task sync failed; previous snapshot preserved. Retry when GitHub is reachable.')
if __name__=='__main__':main()
