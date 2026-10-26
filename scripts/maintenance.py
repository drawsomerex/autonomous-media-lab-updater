"""Record the monthly scheduler health check so the public automation repository stays active."""
import base64,datetime,json,os,urllib.request,urllib.error
repo=os.environ['GITHUB_REPOSITORY'];token=os.environ['GITHUB_TOKEN']
url='https://api.github.com/repos/'+repo+'/contents/maintenance/last-checked.txt'
headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'AutonomousMediaLab-maintenance'}
sha=None
try:
 with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as r:sha=json.load(r)['sha']
except urllib.error.HTTPError as e:
 if e.code!=404:raise
content='Updater self-tests passed on '+datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')+' UTC.\n'
payload={'message':'Record monthly updater maintenance','content':base64.b64encode(content.encode()).decode()}
if sha:payload['sha']=sha
with urllib.request.urlopen(urllib.request.Request(url,data=json.dumps(payload).encode(),headers={**headers,'Content-Type':'application/json'},method='PUT'),timeout=30) as r:
 assert r.status in (200,201)
print('Monthly maintenance recorded. No import secret is used by this job.')
