import { useLocation } from 'react-router-dom';
import type { DocumentType } from "@/util/types"
import { useEffect, useState } from 'react';
import "@/styles/view-document.css"

export default function ViewDocumentPage() {
  const { state } = useLocation();
  const document : DocumentType = state.document;
  const category : string = state.category;
  const [downloadURL, setDownloadURL] = useState<string | null>(null)
  const [documentLoading, setDocumentLoading] = useState<boolean>(true)
  const [documentError, setDocumentError] = useState<boolean>(false);

  useEffect(() => {
    const fetchDocument = async() => {
      try {
        if (document.s3_document_key){
          const download_url_response = await fetch(
            `http://127.0.0.1:8000/download-url/${encodeURIComponent(document.s3_document_key)}?document_name=${encodeURIComponent(document.name)}`)
          if (!download_url_response.ok){
            throw new Error(`Error Status: ${download_url_response.status}`);
          }
          const { download_url } = await download_url_response.json()
          setDownloadURL(download_url)
        }
        else{
          setDocumentError(true)
        }
      } catch {
        setDocumentError(true)
      } finally {
        setDocumentLoading(false)
      }
    };
    fetchDocument()
  }, [document, documentError, documentLoading])

  return (
    <div className="view-document-page">
      <h1 className="document-name">{document.name}</h1>
      <h2 className="document-category">{category}</h2> 
      <p className="document-description">{document.description}</p> 
      <div className="document-file">
        {documentLoading ? (
          <></>
        ) : documentError ? (
          <div className="error-text">
            Document Not Found
          </div>
        ) : downloadURL ? (
          <iframe
            src={downloadURL}
            className="document-iframe"
            title="PDF Document"
          />
        ) : null}
      </div>
    </div>
  )
}