import { useParams } from 'react-router-dom';
import type { DocumentType } from "@/util/types"
import { useEffect, useState } from 'react';
import "@/styles/view-document.css"

interface DocumentDownloadRequest {
  name: string,
  s3_document_key: string,

}
export default function ViewDocumentPage() {
  const { document_id } = useParams()
  const [document, setDocument] = useState<DocumentType | null>(null)
  const [downloadURL, setDownloadURL] = useState<string | null>(null)
  const [documentLoading, setDocumentLoading] = useState<boolean>(true)
  const [documentError, setDocumentError] = useState<boolean>(false);

  useEffect(() => {
    const fetchDocument = async() => {
      try {
        setDocumentLoading(true)
        
        const get_document_response = await fetch(`http://127.0.0.1:8000/documents/${document_id}`)
        if (!get_document_response.ok){
          throw new Error(`Error Status: ${get_document_response.status}`);
        }
        const doc : DocumentType = await get_document_response.json();
        setDocument(doc)

        const download_request : DocumentDownloadRequest = {
          name: doc.name,
          s3_document_key: doc.s3_document_key
        }
        const download_url_response = await fetch(`http://127.0.0.1:8000/documents/download-url`, {
          method: 'POST',
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(download_request)
        })
        if (!download_url_response.ok){
          throw new Error(`Error Status: ${download_url_response.status}`);
        }
        const download_url = await download_url_response.json()
        setDownloadURL(download_url)
        
      } catch {
        setDocumentError(true)
      } finally {
        setDocumentLoading(false)
      }
    };
    fetchDocument()
  }, [document_id])

  return (
    <div className="view-document-page">
      <h1 className="document-name">{document?.name}</h1>
      <h2 className="document-category">{document?.category}</h2> 
      <p className="document-description">
        {document?.description ? (document.description) : (<></>)}</p>
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