import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom';
import '@/styles/add-document.css'


interface DocumentType {
  id: number;
  name: string;
  description: string;
  category: string;
}

interface CategoryDictType{
  [category: string] : DocumentType[];
}

export default function AddDocumentPage(){
    const location = useLocation();
    const state = location.state as { categories: CategoryDictType };
    const categories = state?.categories || {};

    const [documentName, setDocumentName] = useState<string>("");
    const [documentDescription, setDocumentDescription] = useState<string>("");
    const [selectedCategory, setSelectedCategory] = useState<string>("");

    const uploadDocument = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!documentName || !selectedCategory){
            alert("Please enter all missing fields");
            return;
        }
        const new_document : DocumentType = {
            id: 101,
            name: documentName,
            description: documentDescription,
            category: selectedCategory
        }
        categories[selectedCategory].push(new_document)
        alert("Document added (only frontend)")

    }

    return (
        <div className="add-document-page">
            <h2 style={{ textAlign: "center" }} className="add-document-title">Add Document</h2>
            <form onSubmit={uploadDocument}>
                <label className="feild">
                    Document Name: 
                     <input
                        type="text"
                        value={documentName}
                        onChange = {(e) => setDocumentName(e.target.value)}
                        style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem", backgroundColor: "#f0f4f8", fontSize: "large"}}
                    />
                </label>
                <label className="feild">
                    Description Name: 
                     <input
                        type="text"
                        value={documentDescription}
                        onChange = {(e) => setDocumentDescription(e.target.value)}
                        style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem", backgroundColor: "#f0f4f8", fontSize: "large"}}
                    />
                </label>
                <div className='feild'>
                    <label htmlFor="category">Select Category:</label>
                    <select
                        id="category"
                        className="category-dropdown"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                    {Object.keys(categories).map((cat) => (
                        <option key={cat} value={cat}>
                            {cat}
                        </option>
                    ))}
                    </select>
                </div>
                <Link to='/'>
                    <button className="upload-document-button" type="submit">
                        Upload Document
                    </button>
                </Link>
            </form>
        </div>
    )
}