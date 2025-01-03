from flask import Flask, jsonify
from google.cloud import storage
import datetime
from google.oauth2 import service_account
import os
from dotenv import load_dotenv

load_dotenv()
BUCKET_NAME = os.getenv("BUCKET_NAME")
BLOB_NAME=os.getenv("BLOB_NAME")
PATH_SA_KEY = os.getenv("PATH_SA_KEY")
PROJECT_ID= os.getenv("PROJECT_ID")

app = Flask(__name__)
storage_client = storage.Client(project=PROJECT_ID)

@app.route('/get-signed-url', methods=['GET'])
def get_signed_url():
    try:
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(BLOB_NAME)

        expiration = datetime.timedelta(minutes=5)

        google_credentials = service_account.Credentials.from_service_account_file(
            PATH_SA_KEY)

        url = blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="PUT",
            credentials = google_credentials
        )

        return jsonify({
                "signed_url": url,
                "expires_in":str(expiration)
        } ),200
    
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),500


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)