import fitz
import pymupdf4llm
from app.core.s3 import s3_client, AWS_S3_BUCKET

# @celery_client.task
def extract_pdf_text(key):
    file = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=key)
    file_bytes = file["Body"].read()

    pdf_doc = fitz.open(stream=file_bytes, filetype="pdf")
    markdown_text = pymupdf4llm.to_markdown(pdf_doc)

    return markdown_text
