import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

app = Flask(__name__)
CORS(app)

# ODF S3 Configuration from environment variables
ODF_ENDPOINT = os.getenv('ODF_ENDPOINT')
ODF_ACCESS_KEY = os.getenv('ODF_ACCESS_KEY')
ODF_SECRET_KEY = os.getenv('ODF_SECRET_KEY')
ODF_BUCKET = os.getenv('ODF_BUCKET')
VERIFY_SSL = os.getenv('VERIFY_SSL', 'true').lower() == 'true'

# Initialize S3 client for ODF
s3 = boto3.client(
    's3',
    endpoint_url=f'https://{ODF_ENDPOINT}',
    aws_access_key_id=ODF_ACCESS_KEY,
    aws_secret_access_key=ODF_SECRET_KEY,
    config=Config(signature_version='s3v4'),
    verify=VERIFY_SSL
)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        try:
            s3.upload_fileobj(
                file,
                ODF_BUCKET,
                file.filename,
                ExtraArgs={'ACL': 'public-read'}
            )
            return jsonify({"message": f"File '{file.filename}' uploaded successfully."}), 201
        except ClientError as e:
            return jsonify({"error": str(e)}), 500

@app.route('/reports', methods=['GET'])
def list_reports():
    try:
        response = s3.list_objects_v2(Bucket=ODF_BUCKET)
        reports = []
        if 'Contents' in response:
            for obj in response['Contents']:
                url = s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': ODF_BUCKET, 'Key': obj['Key']},
                    ExpiresIn=3600 # URL expires in 1 hour
                )
                reports.append({"name": obj['Key'], "url": url})
        return jsonify(reports), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)