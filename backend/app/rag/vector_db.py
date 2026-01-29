from langchain_community.vectorstores import Chroma

vectordb = Chroma.from_documents(
    persist_directory="./chroma_db"
)
vectordb.persist()