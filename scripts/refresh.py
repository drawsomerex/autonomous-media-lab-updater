"""Request an authenticated refresh of Autonomous Media Lab's public sources."""
import hashlib,hmac,json,os,sys,time,urllib.error,urllib.parse,urllib.request
TARGET='https://autonomousmedialab.com/internal/import/'
def request_parts(secret,body,now=None):
 stamp=str(int(time.time() if now is None else now))
 message='v1\n'+stamp+'\nPOST\n/internal/import/\n'+hashlib.sha256(body).hexdigest()
 signature=hmac.new(secret.encode(),message.encode(),hashlib.sha256).hexdigest()
 return {'Content-Type':'application/json','User-Agent':'AutonomousMediaLab-Actions/1.0','X-AML-Timestamp':stamp,'X-AML-Signature':signature}
def main():
 secret=os.environ.get('AML_UPDATE_SECRET','')
 if len(secret)<48:print('The AML_UPDATE_SECRET repository secret is missing or invalid.',file=sys.stderr);return 1
 repo=os.environ.get('GITHUB_REPOSITORY','drawsomerex/autonomous-media-lab-updater');run=os.environ.get('GITHUB_RUN_ID','')
 body=json.dumps({'run_url':f'https://github.com/{repo}/actions/runs/{run}','trigger':os.environ.get('GITHUB_EVENT_NAME','manual')},separators=(',',':')).encode()
 request=urllib.request.Request(TARGET,data=body,method='POST',headers=request_parts(secret,body))
 try:
  with urllib.request.urlopen(request,timeout=180) as response:raw=response.read(64000)
 except urllib.error.HTTPError as error:
  raw=error.read(64000);print('The import endpoint returned HTTP',error.code,file=sys.stderr)
 except (urllib.error.URLError,TimeoutError) as error:
  print('Could not reach the import endpoint:',str(error),file=sys.stderr);return 1
 try:result=json.loads(raw)
 except (ValueError,UnicodeError):print('The endpoint did not return an import result.',file=sys.stderr);return 1
 for source,status in result.get('sources',{}).items():
  print(source+':', 'OK' if status.get('ok') else 'FAILED',str(status.get('count',0))+' items;',status.get('message',''))
 if result.get('latest_youtube'):print('Latest video:',result['latest_youtube'].get('title',''))
 if result.get('skipped'):print(result['skipped'])
 if not result.get('ok'):print('One or more sources failed. Last good website content was retained.',file=sys.stderr);return 1
 return 0
if __name__=='__main__':sys.exit(main())
