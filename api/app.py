from flask import Flask, request, redirect, url_for, jsonify
import boto3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# AWS S3 Configuration via environment variables
# Define these in your deployment environment (e.g., Vercel Project Settings)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
S3_REGION = os.environ.get('S3_REGION', 'us-east-1')

missing = [
    name for name, val in [
        ('AWS_ACCESS_KEY_ID', AWS_ACCESS_KEY_ID),
        ('AWS_SECRET_ACCESS_KEY', AWS_SECRET_ACCESS_KEY),
        ('S3_BUCKET_NAME', S3_BUCKET_NAME),
    ] if not val
]
if missing:
    # Fail early with a helpful error if required env vars are missing
    raise RuntimeError(
        'Missing required environment variables: ' + ', '.join(missing)
    )

# Initialize boto3 S3 client
s3_client = boto3.client(
    's3',
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

@app.route('/')
def index():
    # Serve the HTML form
    return open('index.html').read()

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)

    # Optional: file size limit (e.g., 5MB)
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    max_size = 5 * 1024 * 1024  # 5 MB
    if file_length > max_size:
        return jsonify({'error': 'File too large'}), 400

    # Optional: file type check
    allowed_types = ['image/png', 'image/jpeg', 'text/plain']
    if file.mimetype not in allowed_types:
        return jsonify({'error': 'File type not allowed'}), 400

    # Upload file to S3
    try:
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=file,
            ContentType=file.mimetype
        )
        
        public_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{filename}"
        return jsonify({'url': public_url}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
