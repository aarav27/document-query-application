from PyPDF2 import PdfReader
from .s3 import s3_client, AWS_S3_BUCKET

def extract_pdf_text(s3_key):
    file = s3_client.get_object(Bucket=AWS_S3_BUCKET, Key=s3_key)
    reader = PdfReader(file["Body"])
    text = ''.join(page.extract_text() or '' for page in reader.pages)
    return text
