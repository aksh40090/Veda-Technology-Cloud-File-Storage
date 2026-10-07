import os
from pathlib import Path
class StorageBackend:
 def __init__(self,root):
  self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
  self.bucket=os.getenv("S3_BUCKET"); self.mode="cloud" if self.bucket and os.getenv("S3_ACCESS_KEY_ID") and os.getenv("S3_SECRET_ACCESS_KEY") else "local"
  if self.mode=="cloud":
   import boto3
   self.client=boto3.client("s3",endpoint_url=os.getenv("S3_ENDPOINT") or None,region_name=os.getenv("S3_REGION","auto"),aws_access_key_id=os.getenv("S3_ACCESS_KEY_ID"),aws_secret_access_key=os.getenv("S3_SECRET_ACCESS_KEY"))
 def path(self,key):
  p=(self.root/key).resolve()
  if self.root.resolve() not in p.parents: raise ValueError("invalid key")
  return p
 def put(self,key,data,ctype):
  if self.mode=="cloud": self.client.put_object(Bucket=self.bucket,Key=key,Body=data,ContentType=ctype)
  else: self.path(key).parent.mkdir(parents=True,exist_ok=True); self.path(key).write_bytes(data)
 def get(self,key):
  return self.client.get_object(Bucket=self.bucket,Key=key)["Body"].read() if self.mode=="cloud" else self.path(key).read_bytes()
