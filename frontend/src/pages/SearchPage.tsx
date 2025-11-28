import { useState } from "react";
import { Link } from "react-router-dom";

import { useDocumentsAndCategories } from "@/components/FetchData";
import type { DocumentType, CategoryDocumentsMapType } from "@/util/types";

import "@/styles/home.css";
import "@/styles/search.css";

export default function SearchPage() {
    const { loading, error, categoryDocumentMap } = useDocumentsAndCategories();
    const [selectedCategory, setSelectedCategory] = useState("All");
    const [searchInput, setSearchInput] = useState("");
    const [documentsSearchResult, setDocumentsSearchResult] = useState<CategoryDocumentsMapType | null>(null);

    const handleSearch = () => {
        if (searchInput === "") return;

        const searchResult: CategoryDocumentsMapType = {};
        Object.entries(categoryDocumentMap).forEach(([category, documents]: [string, DocumentType[]]) => {
            searchResult[category] = documents.filter((document) => 
                document.extracted_text && document.extracted_text.toLowerCase().includes(searchInput.toLowerCase())
            );
        })
        console.log(searchResult["Legal"])

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

                {/* Nothing searched yet */}
                {!documentsSearchResult ? (
                    <></>
                ) : selectedCategory === "All" ? (
                    Object.keys(documentsSearchResult).map((category) => (
                        (documentsSearchResult[category].length == 0) ? (<div></div>) : (
                            <div key={category} className="category-section">
                                <div className="category-header">
                                    <h2>{category}</h2>
                                </div>

                                {/* Document Table */}
                                <table className="document-table">
                                    <thead>
                                    <tr>
                                        <th>Document Name</th>
                                        <th>Description</th>
                                        <th>View</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                        {documentsSearchResult[category].map((document, idx) => (
                                            <tr key={idx}>
                                                <td>{document.name}</td>
                                                <td>{document.description}</td>
                                                <td>
                                                    <Link 
                                                        to={`/document/${document.id}`}
                                                        state={{ document, category, routeBack: "/search" }}
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
                        )
                    ))
                ) : (
                    <div/>
                )}
            </div>
        </div>
    );
}
