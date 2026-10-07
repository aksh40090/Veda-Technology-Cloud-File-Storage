# Veda Technology Cloud File Storage & Document Management System

## Run
```powershell
python -m pip install -r requirements.txt
python run.py
```
Open http://127.0.0.1:5000

## Features
PDF/image upload, 10 MB validation, categories, search, listing, download, delete, separate JSON metadata, REST API, health endpoint, local storage and optional AWS S3/Cloudflare R2 compatible storage.

## API
- GET /api/files
- GET /api/files/<id>
- GET /health

## GitHub
```powershell
git init
git add .
git commit -m "Complete Veda cloud file storage project"
git branch -M main
git remote add origin YOUR_GITHUB_URL
git push -u origin main
```
Never commit cloud credentials.
