import boto3
from botocore.config import Config
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
AWS_REGION_NAME = os.getenv("AWS_REGION_NAME")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION_NAME,
)
s3_client = session.client("s3", config=Config(signature_version="s3v4"))

def create_s3_document_key(document_id, document_name):
    datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    modified_document_name = document_name.replace(" ", "_")
    return f"{modified_document_name}-{document_id}-{datetime_string}"