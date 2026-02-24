from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.rag.vector_stores import get_chroma_client
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

test_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

def process_test_documents():
    documents = []
    current_doc = {}
    current_field = None
    logging.info(os.getcwd())

    with open('./app/rag/testing/documents.txt', 'r') as documents_file:
        for line in documents_file:
            line = line.rstrip()
            if line.startswith(".I"):
                if current_doc:
                    documents.append(current_doc)
                current_doc = {"id": line.split()[1]}
            elif line.startswith(".T"):
                current_field = "title"
                current_doc[current_field] = ""
            elif line.startswith(".A"):
                current_field = "author"
                current_doc[current_field] = ""
            elif line.startswith(".B"):
                current_field = "bibliography"
                current_doc[current_field] = ""
            elif line.startswith(".W"):
                current_field = "text"
                current_doc[current_field] = ""
            else:
                if current_field:
                    current_doc[current_field] += line + ' '

        
        if current_doc:
            documents.append(current_doc)
    

    chroma_db = get_chroma_client("test")
    for doc in documents:
        text = doc.get("text", "").strip()
        if not text:
            logging.info(doc.get("id", ""))
            continue
        chunks = test_splitter.split_text(text)
        if not chunks:
            logging.info(doc.get("id", ""))
            continue

        chroma_db.add_texts(
            texts=chunks,
            metadatas=[
                {   
                    "document_id": doc.get("id", ""),
                    "document_name": doc.get("title", ""),
                    "category_name": doc.get("id", ""),
                    "title": doc.get("title", ""),
                    "author": doc.get("author", ""),
                    "bibliography": doc.get("bibliography", ""),
                }
                for _ in chunks
            ]
        )

process_test_documents()