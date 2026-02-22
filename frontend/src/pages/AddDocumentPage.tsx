import { useEffect, useState } from 'react'
import { Link, useNavigate} from 'react-router-dom';
import '@/styles/add-document.css'
import type { CategoryType, DocumentCreateType } from '@/util/types';
import { useLoading } from '@/context/useLoading';

export default function AddDocumentPage(){
    const navigate = useNavigate();
    const [categories, setCategories] = useState<CategoryType[]>([])
    const { showLoader, hideLoader } = useLoading();


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
        }
        fetchCategories();
    }, [])

    const clearForm = () => {
        setDocumentDescription("")
        setSelectedCategory("")
        setUploadedFile(null)
    }

    const uploadDocument = async () => {
        if (!uploadedFile){
            alert("Please upload a PDF file");
            return;
        }
        if (categories.length == 0){
            alert("No categories to select from")
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

        try {
            showLoader();
            
            // 1. Generate an S3 presigned URL for uploading
            const upload_url_response = await fetch(`http://127.0.0.1:8000/documents/upload-url/${uploadedFile.name}`);
            if(!upload_url_response.ok){
                throw new Error(`Error Status: ${upload_url_response.status}`);
            }
            const {upload_url, s3_document_key} = await upload_url_response.json();

            // 2. Upload the document in S3 using the presigned URL
            const upload_document_response = await fetch(upload_url, {
                method: "PUT",
                body: uploadedFile,
                headers: {
                    "Content-Type": uploadedFile.type,
                },
            })
            if (!upload_document_response.ok){
                throw new Error(`Error Status: ${upload_document_response.status}`);
            }

            // 3. Add document record to database and generate upload URL
            const newDocument : DocumentCreateType = {
                name: uploadedFile.name,
                description: documentDescription,
                category_id: categoryObj.id,
                category_name: categoryObj.name,
                s3_document_key: s3_document_key,
            };
            const add_document_response = await fetch("http://127.0.0.1:8000/documents", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(newDocument),
            });
            if (!add_document_response.ok){
                throw new Error(`Error Status: ${upload_document_response.status}`);
            }
            
            navigate("/");

        } catch (error) {
            alert('Failed to upload document');
            throw error;
        } finally{
            hideLoader();
        }

    }

    return (
        <div className="add-document-page">
            <Link to='/'>
                <button className="buttons back-button">
                   &larr; Back
                </button>
            </Link>
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
                                <p>Click to upload</p>
                                <p className="upload-text">PDF only</p>
                            </div>
                        )}
                        <input
                            id="file-upload"
                            type="file"
                            accept='application/pdf'
                            onChange={(e) => {
                                const new_file = e.target.files?.[0]
                                if(new_file){
                                    if(new_file.type != 'application/pdf'){
                                        alert("Only PDF files are allowed!");
                                        return
                                    }
                                    setUploadedFile(new_file);
                                }
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
                    <button className="buttons clear-button" type="button" onClick={clearForm}>
                        Clear
                    </button>
                    <button className="buttons upload-document-button" type="submit">
                        Add Document
                    </button>
                </div>
            </form>
        </div>
    )
}