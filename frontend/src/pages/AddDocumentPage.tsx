import { useState } from 'react'

export default function AddDocumentPage(){
    const [documentName, setDocumentName] = useState<string>("");
    const [category, setCategory] = useState<string>("");
    // const [file, setFile] = useState<File | null>(null);

    const uploadDocument = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!documentName || !category){
            alert("Please enter all missing fields");
            return;
        }

        // if (!file){
        //     alert("Please select a file");
        // }

        alert("Document added (only frontend)")

    }

    return (
        <div className="add-document-page">
            <h2 style={{ textAlign: "center" }} className="add-document-title">Add Document</h2>
            <form onSubmit={uploadDocument}>
                <label>
                    Document Name: 
                     <input
                        type="text"
                        value={documentName}
                        onChange = {(e) => setDocumentName(e.target.value)}
                        style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem" }}
                    />
                </label>
                <label>
                    Category:
                    <input
                        type="text"
                        value={category}
                        onChange = {(e) => setCategory(e.target.value)}
                        style={{ width: "100%", padding: "0.5rem", marginTop: "0.3rem" }}
                    />
                </label>
                {/* <label>
                    Upload Document:
                    <input
                        type="file"
                        onChange = {(e) => setFile(e.target.files ? e.target.files[0] : null)}
                         style={{ width: "100%", marginTop: "0.3rem" }}
                    />
                </label> */}
                <button className="add-document-button" type="submit">
                    Add Document
                </button>
            </form>
        </div>
    )
}