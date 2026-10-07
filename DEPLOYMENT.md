# Deployment

Local: `python -m pip install -r requirements.txt` then `python run.py`.

Production Linux: `gunicorn -w 2 -b 0.0.0.0:5000 app:app`.

For S3/R2 set STORAGE_MODE=s3, S3_BUCKET, S3_REGION, optional S3_ENDPOINT_URL, AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY. Keep credentials in environment variables.
