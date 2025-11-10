import { useLocation } from 'react-router-dom';
import type { DocumentType } from "@/util/types"
import { useEffect, useState } from 'react';
import "@/styles/view-document.css"

export default function ViewDocumentPage() {
  const { state } = useLocation();
  const document : DocumentType = state.document;
  const category : string = state.category;
  const [downloadURL, setDownloadURL] = useState<string | null>(null)

  useEffect(() => {
    const fetchDocument = async() => {
      const download_url_response = await fetch(
        `http://127.0.0.1:8000/download-url/${encodeURIComponent(document.s3_document_key)}?document_name=${encodeURIComponent(document.name)}`)
      if (!download_url_response.ok){
        throw new Error(`Error Status: ${download_url_response.status}`);
      }
      const { download_url } = await download_url_response.json()
      setDownloadURL(download_url)
    };
    fetchDocument()
  }, [document])

  return (
    <div className="view-document-page">
      <h1 className="document-name">{document.name}</h1>
      <h2 className="document-category">{category}</h2> 
      <p className="document-description">{document.description}</p> 
      <div className="document-file">
        {downloadURL ? (
          <iframe
            src={downloadURL}
            className = "document-iframe"
          />
        ) : 
          <div style={{ textAlign: 'center', paddingTop: '50px' }}>
            Loading Document...
          </div>}
      </div>
    </div>
  )
}