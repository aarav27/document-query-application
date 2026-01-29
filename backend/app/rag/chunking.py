from langchain.text_splitter import RecursiveCharacterTextSplitter

def character_chunking(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_documents(documents)