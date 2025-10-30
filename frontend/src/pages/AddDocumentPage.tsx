import { useState } from 'react'
import { useLocation, useNavigate} from 'react-router-dom';
import '@/styles/add-document.css'


interface DocumentType {
    id: number;
    name: string;
    description: string;
    category_id: number;
}

interface CategoryDictType{
    [category: string] : DocumentType[];
}

export default function AddDocumentPage(){
    const location = useLocation();
    const navigate = useNavigate();
    const state = location.state as { categories: CategoryDictType };
    const categories = state?.categories || {};

    const [documentDescription, setDocumentDescription] = useState<string>("");
    const [selectedCategory, setSelectedCategory] = useState<string>("");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    const uploadDocument = async () => {
        if (!selectedCategory){
            alert("Please enter a selected category");
            return;
        }
        if (!uploadedFile){
            alert("Please upload a PDF file");
            return;
        }
        const categoryId = categories[selectedCategory][0]?.category_id;
        if (!categoryId) {
            alert("Invalid category");
            return;
        }

        const newDocument = {
            name: uploadedFile.name,
            description: documentDescription,
            category_id: categoryId
        };
        
        try {
            const response = await fetch("http://127.0.0.1:8000/documents", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newDocument),
            });

            console.log(response)
            if (response.ok) {
                alert("Document Added")
                navigate("/");
            }

        } catch (error) {
            alert('Failed to upload document');
            throw error;
        }

    }

    return (
        <div className="add-document-page">
            <h2 style={{ textAlign: "center" }} className="add-document-title">Add Document</h2>
            <form 
                onSubmit={async () => {await uploadDocument()}}>
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
                <div className="feild upload-container">
                    <label htmlFor="file-upload" className="upload-label">
                        {uploadedFile ? (
                            <div className="file-name">{uploadedFile.name}</div>
                        ) : (
                            <div>
                                <p className="upload-icon">📄</p>
                                <p>Click to upload or drag and drop</p>
                                <p className="upload-text">PDF only</p>
                            </div>
                        )}
                        <input
                            id="file-upload"
                            type="file"
                            onChange={(e) => {
                                if (e.target.files) setUploadedFile(e.target.files[0]);
                            }}
                            className="file-input"
                        />
                    </label>
                </div>
                <button 
                    className="upload-document-button" 
                    type="submit"
                >
                    Add Document
                </button>
            </form>
        </div>
    )
}