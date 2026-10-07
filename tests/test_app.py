import io, pytest
from app import app
@pytest.fixture
def client(tmp_path,monkeypatch):
 app.config.update(TESTING=True);monkeypatch.setattr('app.UP',tmp_path/'uploads');monkeypatch.setattr('app.META',tmp_path/'metadata');(tmp_path/'uploads').mkdir();(tmp_path/'metadata').mkdir()
 with app.test_client() as c:yield c
def test_home(client):
 r=client.get('/');assert r.status_code==200;assert b'Cloud File Storage' in r.data
def test_health(client):
 r=client.get('/health');assert r.status_code==200;assert r.json['status']=='healthy'
def test_upload(client):
 r=client.post('/upload',data={'category':'Documents','file':(io.BytesIO(b'%PDF-demo'),'demo.pdf','application/pdf')},content_type='multipart/form-data',follow_redirects=True);assert r.status_code==200 and b'uploaded successfully' in r.data
def test_reject(client):
 r=client.post('/upload',data={'file':(io.BytesIO(b'x'),'a.txt','text/plain')},content_type='multipart/form-data',follow_redirects=True);assert b'Only PDF and image files are allowed' in r.data
