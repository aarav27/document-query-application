from langchain_community.vectorstores import Chroma

vectordb = Chroma(persist_directory="./chroma_db")