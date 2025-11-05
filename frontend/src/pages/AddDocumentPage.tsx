import { useEffect, useState } from 'react'
import { Link, useNavigate} from 'react-router-dom';
import '@/styles/add-document.css'

interface CategoryType{
  id: number;
  name: string;
}

export default function AddDocumentPage(){
    const navigate = useNavigate();
    const [categories, setCategories] = useState<CategoryType[]>([])

    const [documentDescription, setDocumentDescription] = useState<string>("");
    const [selectedCategory, setSelectedCategory] = useState<string>("");
    const [uploadedFile, setUploadedFile] = useState<File | null>(null);

    useEffect(() => {
        const fetchCategories = async () => {
            const category_response = await fetch ("http://127.0.0.1:8000/categories")
            if (!category_response.ok){
                throw new Error(`Error Status: ${category_response.status}`);
            }
            const response_data = await category_response.json()
            const category_data = response_data.map((category : CategoryType) => {
                return category
            });
            setCategories(category_data)

            if (category_data.length > 0){
                setSelectedCategory(category_data[0].name)
            }
        }
        fetchCategories();
    }, [])

    const uploadDocument = async () => {
        if (!uploadedFile){
            alert("Please upload a PDF file");
            return;
        }
        if (categories.length == 0){
            alert("No categories to select")
        }
        if (!selectedCategory){
            alert("Please select category");
            return;
        }
        const categoryObj = categories.find((cat : CategoryType) => cat.name == selectedCategory)
        if (!categoryObj) {
            alert("Invalid category");
            return;
        }

        const newDocument = {
            name: uploadedFile.name,
            description: documentDescription,
            category_id: categoryObj.id
        };
        
        try {
            const response = await fetch("http://127.0.0.1:8000/documents", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newDocument),
            });

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
            <form onSubmit={async (e) => {
                e.preventDefault();
                await uploadDocument();
            }}>
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
                <div className='feild'>
                    <label htmlFor="category">Select Category:</label>
                    <select
                        id="category"
                        className="category-dropdown"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="">-- Select a category --</option>
                        {categories.map((cat) => (
                            <option key={cat.name} value={cat.name}>
                                {cat.name}
                            </option>
                        ))}
                    </select>
                </div>
                <label className="feild">
                    Description: 
                    <textarea
                        value={documentDescription}
                        onChange={(e) => setDocumentDescription(e.target.value)}
                        style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem", backgroundColor: "#f0f4f8", fontSize: "large" }}
                        rows={4}
                    />
                </label>
                <div className='button-container'>
                    <Link to='/'>
                        <button 
                            className="buttons cancel-button" 
                        >
                            Cancel
                        </button>
                    </Link>
                    <button 
                        className="buttons upload-document-button" 
                        type="submit"
                    >
                        Add Document
                    </button>
                </div>
            </form>
        </div>
    )
}