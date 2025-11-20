import asyncio
import fitz
# from .celery import celery_client
from .database import AsyncSessionLocal
from .models import Document
from .s3 import s3_client, AWS_S3_BUCKET

# @celery_client.task
def extract_pdf_text(key):
    file = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=key)
    file_body = file["Body"].read()
    document = fitz.open(stream=file_body, filetype="pdf")
    extracted_text = ""
    for page in document:
        extracted_text += page.get_text()
    return extracted_text
