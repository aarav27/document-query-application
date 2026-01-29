from langchain.schema import Document

def build_document(text: str):
    return [
        Document(
            page_content=text,
            metadata={
                "parser": "pymupdf4llm",
                # add more later
            }
        )
    ]