import os,json,uuid
from pathlib import Path
from datetime import datetime,timezone
from flask import Flask,render_template,request,redirect,url_for,flash,send_file,jsonify
try:
 import boto3
 from botocore.exceptions import BotoCoreError,ClientError
except ImportError: boto3=None
BASE=Path(__file__).parent; UP=BASE/'uploads'; META=BASE/'metadata'; UP.mkdir(exist_ok=True); META.mkdir(exist_ok=True)
app=Flask(__name__,template_folder='templates',static_folder='static'); app.secret_key=os.getenv('FLASK_SECRET_KEY','veda-demo-secret'); app.config['MAX_CONTENT_LENGTH']=10*1024*1024
ALLOWED={'pdf','png','jpg','jpeg','gif','webp'}; CATS=['Documents','Images','Certificates','Projects','Other']
MODE=os.getenv('STORAGE_MODE','local').lower(); BUCKET=os.getenv('S3_BUCKET',''); REGION=os.getenv('S3_REGION','ap-south-1'); ENDPOINT=os.getenv('S3_ENDPOINT_URL',''); s3=None
if MODE=='s3' and boto3 and BUCKET:
 try: s3=boto3.client('s3',region_name=REGION,endpoint_url=ENDPOINT or None,aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
 except Exception: MODE='local'
def ep(n): return Path(n).suffix.lower().lstrip('.')
def mp(i): return META/f'{i}.json'
def _records(value):
 if isinstance(value, dict):
  return [value]
 if isinstance(value, list):
  return [item for item in value if isinstance(item, dict)]
 return []

def load(i):
 for p in META.glob('*.json'):
  try:
   data=json.loads(p.read_text(encoding='utf-8'))
   for record in _records(data):
    if str(record.get('id','')) == str(i):
     return record
  except (OSError,ValueError,TypeError):
   continue
 return None

def allfiles():
 records=[]
 for p in META.glob('*.json'):
  try:
   data=json.loads(p.read_text(encoding='utf-8'))
   records.extend(_records(data))
  except (OSError,ValueError,TypeError):
   continue
 return sorted(records,key=lambda x:x.get('uploaded_at',''),reverse=True)
def save(x):
 mp(x['id']).write_text(json.dumps(x,indent=2),encoding='utf-8')
def put(f,name):
 if MODE!='s3' or not s3:f.save(UP/name);return 'local'
 f.stream.seek(0);s3.upload_fileobj(f.stream,BUCKET,name,ExtraArgs={'ContentType':f.content_type or 'application/octet-stream'});return 's3'
def remove(x):
 try:
  if x['storage']=='s3' and s3:s3.delete_object(Bucket=BUCKET,Key=x['storage_name'])
  else:(UP/x['storage_name']).unlink(missing_ok=True)
  mp(x['id']).unlink(missing_ok=True);return True
 except:return False
@app.get('/')
def index():
 fs=allfiles(); total=sum(x.get('size_bytes',0) for x in fs); stats={'total':len(fs),'images':sum(x.get('category')=='Images' for x in fs),'documents':sum(x.get('category')=='Documents' for x in fs),'size_mb':round(total/1048576,2)}
 return render_template('index.html',files=fs,stats=stats,categories=CATS,storage_mode=MODE)
@app.post('/upload')
def upload():
 f=request.files.get('file');cat=request.form.get('category','Other')
 if not f or not f.filename:flash('Please select a file first.','error');return redirect(url_for('index'))
 if ep(f.filename) not in ALLOWED:flash('Only PDF and image files are allowed.','error');return redirect(url_for('index'))
 f.seek(0,2);size=f.tell();f.seek(0)
 if not size:flash('The selected file is empty.','error');return redirect(url_for('index'))
 if f.content_type and f.content_type not in {'application/pdf','image/png','image/jpeg','image/gif','image/webp'}:flash('Unsupported MIME type.','error');return redirect(url_for('index'))
 if cat not in CATS:cat='Other'
 i=uuid.uuid4().hex;name=f'{i}.{ep(f.filename)}'
 try:storage=put(f,name)
 except Exception as e:flash(f'Upload failed: {e}','error');return redirect(url_for('index'))
 x={'id':i,'original_name':Path(f.filename).name,'storage_name':name,'category':cat,'content_type':f.content_type or 'application/octet-stream','size_bytes':size,'size_mb':round(size/1048576,2),'storage':storage,'access':'Private','uploaded_at':datetime.now(timezone.utc).isoformat(timespec='seconds')};save(x);flash(f"{x['original_name']} uploaded successfully.",'success');return redirect(url_for('index'))
@app.get('/download/<i>')
def download(i):
 x=load(i)
 if not x:flash('File not found.','error');return redirect(url_for('index'))
 if x['storage']=='s3' and s3:
  try:
   o=s3.get_object(Bucket=BUCKET,Key=x['storage_name']);p=BASE/'.temp';p.mkdir(exist_ok=True);q=p/x['original_name'];q.write_bytes(o['Body'].read());return send_file(q,as_attachment=True,download_name=x['original_name'],mimetype=x['content_type'])
  except Exception as e:flash(str(e),'error');return redirect(url_for('index'))
 p=UP/x['storage_name']
 if not p.exists():flash('Stored file is missing.','error');return redirect(url_for('index'))
 return send_file(p,as_attachment=True,download_name=x['original_name'],mimetype=x['content_type'])
@app.post('/delete/<i>')
def delete(i):
 x=load(i)
 if x and remove(x):flash(f"{x['original_name']} deleted.",'success')
 else:flash('File not found or could not be deleted.','error')
 return redirect(url_for('index'))
@app.get('/api/files')
def api():return jsonify(success=True,storage=MODE,count=len(allfiles()),files=allfiles())
@app.get('/api/files/<i>')
def one(i):
 x=load(i);return (jsonify(success=True,file=x),200) if x else (jsonify(success=False,error='File not found'),404)
@app.get('/health')
def health():return jsonify(status='healthy',storage=MODE)
@app.errorhandler(413)
def too_large(e):flash('File is too large. Maximum size is 10 MB.','error');return redirect(url_for('index'))
if __name__=='__main__':app.run(host='0.0.0.0',port=5000,debug=True)
