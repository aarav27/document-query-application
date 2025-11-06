import { useParams, useLocation } from 'react-router-dom';

interface DocumentType {
  id: number;
  name: string;
  description: string;
  category_id: number;
}

export default function ViewDocumentPage() {
    const { document_id } = useParams();
    const { state } = useLocation();
    const document : DocumentType = state.document;
    const category : string = state.category

    return (
        <div>
           <h1>{document.name}</h1>
           <h2>{document_id}</h2>
           <h2>{category}</h2>
           <div>{document.description}</div>
        </div>
    )
}