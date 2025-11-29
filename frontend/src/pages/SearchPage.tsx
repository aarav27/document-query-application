import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { useDocumentsAndCategories } from "@/components/FetchData";
import type { DocumentType } from "@/util/types";

import "@/styles/home.css";
import "@/styles/search.css";

type SearchDocumentType = {
  id: number;
  name: string;
  description: string;
  s3_document_key: string;
  category: string;
  category_id: number;
  extracted_text: string;
}

export default function SearchPage() {
    const { loading, error, categoryDocumentMap } = useDocumentsAndCategories();
    const [selectedCategory, setSelectedCategory] = useState("All");
    const [searchInput, setSearchInput] = useState("");
    const [documentsSearchResult, setDocumentsSearchResult] = useState<SearchDocumentType[] | null>(null);

    const hasSearched = documentsSearchResult !== null;
    const allResultsEmpty = hasSearched && documentsSearchResult.length == 0

    useEffect(() => {
        if (searchInput !== "") {
            handleSearch();
        }
    }, [selectedCategory]);

    const handleSearch = () => {
        if (searchInput === "") {
            setDocumentsSearchResult(null);
            return;
        }

        if (!categoryDocumentMap) {
            setDocumentsSearchResult(null);
            alert("No documents to search from!")
            return;
        }

        const searchResult: SearchDocumentType[] = [];
        Object.entries(categoryDocumentMap).forEach(([category, documents]: [string, DocumentType[]]) => {
            if (selectedCategory !== "All" && selectedCategory !== category) return;

            const filteredDocuments : DocumentType[] = documents.filter((document : DocumentType) => 
                document.extracted_text && document.extracted_text.toLowerCase().includes(searchInput.toLowerCase())
            );
            
            filteredDocuments.forEach((document : DocumentType) => {
                const search_document : SearchDocumentType = {...document, category}
                searchResult.push(search_document)
            })
        })
        setDocumentsSearchResult(searchResult);
    };

    if (loading) return <div/>;
    if (error) return <div>Error loading documents</div>;

    return (
        <div>
            {/* Page Title */}
            <div className="search-top">
                <h1 className="page-title">Document Search</h1>
            </div>

            {/* Search Controls */}
            <div className="search-controls">

                {/* Category Filter */}
                <div className="category-filter">
                    <select
                        id="category"
                        className="category-dropdown"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="All">All Categories</option>
                        {Object.keys(categoryDocumentMap).map((cat) => (
                            <option key={cat} value={cat}>
                                {cat}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Search Bar */}
                <div className="search-bar">
                    <input
                        type="search"
                        placeholder="Search Here"
                        value={searchInput}
                        onChange={(e) => setSearchInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                    />

                    <button className="search-button" onClick={handleSearch}>
                        Search 🔍
                    </button>
                </div>
            </div>

            {/* Search Results */}
            <div className="category-sections">
                
                {/* 1. Has not searched yet */}
                {!hasSearched && <></>}
                
                {/* 2. No matching results */}
                {hasSearched && allResultsEmpty && (
                    <div className="no-results">No results found</div>
                )}

                {/* 3. Matching Results */}
                {hasSearched && !allResultsEmpty && (
                    <div className="results-section">
                        <div className="results-header">Top Results</div>
                        <table className="search-document-table">
                            <thead>
                            <tr>
                                <th>Rank</th>
                                <th>Document Name</th>
                                <th>Category</th>
                                <th>Description</th>
                                <th>View</th>
                            </tr>
                            </thead>
                            <tbody>
                                {documentsSearchResult.map((document : SearchDocumentType, idx : number) => (
                                    <tr key={idx}>
                                        <td>{idx+1}</td>
                                        <td>{document.name}</td>
                                        <td>{document.category}</td>
                                        <td>{document.description}</td>
                                        <td>
                                            <Link 
                                                to={`/document/${document.id}`}
                                                state={{ document, category: document.category, routeBack: "/search" }}
                                            >
                                                <button className="document-button view-button">
                                                    View
                                                </button>
                                            </Link>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </div>
        </div>
    );
}
