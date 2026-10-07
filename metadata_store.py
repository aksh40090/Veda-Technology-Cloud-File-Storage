import json,uuid
from pathlib import Path
from datetime import datetime,timezone
class MetadataStore:
 def __init__(self,p):
  self.p=Path(p); self.p.parent.mkdir(parents=True,exist_ok=True)
  if not self.p.exists(): self.p.write_text("[]")
 def all(self): return json.loads(self.p.read_text())
 def get(self,i): return next((x for x in self.all() if x["id"]==i),None)
 def add(self,name,key,mime,size,cat):
  a=self.all(); r={"id":str(uuid.uuid4()),"filename":name,"object_key":key,"mime_type":mime,"size_bytes":size,"category":cat,"uploaded_at":datetime.now(timezone.utc).isoformat()}; a.insert(0,r); self.p.write_text(json.dumps(a,indent=2)); return r
