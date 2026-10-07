# Deployment Guide

1. Push the repository to GitHub.
2. Create a Python web service on a free/available hosting provider.
3. Build/install: `pip install -r requirements.txt`.
4. Start: `gunicorn app:app`.
5. Set `SECRET_KEY`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`.
6. Create Cloudflare R2 or AWS S3 storage if cloud mode is required.
7. Set the five S3 environment variables in the host.
8. Upload a PDF/image and verify it appears in object storage.
9. Verify download and `/api/files`.
10. Add a custom domain and enable HTTPS.
11. Capture real screenshots for submission.

Do not fabricate deployment screenshots or URLs.
