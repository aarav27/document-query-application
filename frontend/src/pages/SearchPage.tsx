import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { useDocumentsAndCategories } from "@/components/FetchData";
import type { DocumentType, SearchRequest } from "@/util/types";

import "@/styles/home.css";
import "@/styles/search.css";


export default function SearchPage() {
    const { loading, error, categoryMap, categoryDocumentMap } = useDocumentsAndCategories();
    const [selectedCategory, setSelectedCategory] = useState("All");
    const [searchInput, setSearchInput] = useState("");
    const [isSearching, setIsSearching] = useState(false);
    const [documentsSearchResult, setDocumentsSearchResult] = useState<DocumentType[] | null>(null);

    const hasSearched = documentsSearchResult !== null;
    const allResultsEmpty = hasSearched && documentsSearchResult.length == 0
    const categoryIdNameMap = Object.fromEntries(
        Object.entries(categoryMap).map(([categoryName, categoryID]) => [categoryID, categoryName])
    )

    useEffect(() => {
        if (searchInput !== "") {
            handleSearch();
        }
    }, [selectedCategory]);

    const handleSearch = async () => {
        if (searchInput === "") {
            setDocumentsSearchResult(null);
            return;
        }

        if (!categoryDocumentMap) {
            setDocumentsSearchResult(null);
            alert("No documents to search from!")
            return;
        }
        
        try {
            setIsSearching(true);

            const documentsToSearch : DocumentType[] = [];
            Object.entries(categoryDocumentMap).forEach(([category, documents]: [string, DocumentType[]]) => {
                if (selectedCategory !== "All" && selectedCategory !== category) return;
                documentsToSearch.push(...documents)
            })
            
            const categoryId = selectedCategory === "All" ? null : categoryMap[selectedCategory];

            const search_request: SearchRequest = {
                query: searchInput,
                category_ids: undefined
            };
            if (categoryId !== null) {
                search_request.category_ids = [categoryId];
            }

            const search_response = await fetch("http://127.0.0.1:8000/search", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(search_request)
            });

            if (!search_response.ok) throw new Error(`Error Status: ${search_response.status}`);
            const search_result : DocumentType[] = await search_response.json();
            setDocumentsSearchResult(search_result);

        } catch (err) {
            console.error(err);
            setDocumentsSearchResult([]);
        } finally {
            setIsSearching(false);
        }
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
                        onKeyDown={(e) => e.key === "Enter" && !isSearching && handleSearch()}
                        disabled={isSearching}
                    />
                    <button 
                        className="search-button"
                        onClick={handleSearch}
                        disabled={isSearching}
                    >
                        Search 🔍
                    </button>
                </div>
            </div>

            {/* Search Results */}
            <div className="category-sections">
                
                {/* 1. Has not searched yet */}
                {!hasSearched && <></>}
                
                {/* 2. Loading search */}
                {hasSearched && isSearching && (
                    <div className="search-loading">
                        Searching documents ...
                    </div>
                )}
                
                {/* 3. No matching results */}
                {hasSearched && !isSearching && allResultsEmpty && (
                    <div className="no-results">No results found</div>
                )}

                {/* 4. Matching Results */}
                {hasSearched && !isSearching && !allResultsEmpty && (
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
                                {documentsSearchResult.map((document : DocumentType, idx : number) => (
                                    <tr key={idx}>
                                        <td>{idx+1}</td>
                                        <td>{document.name}</td>
                                        <td>{categoryIdNameMap[document.category_id]}</td>
                                        <td>{document.description}</td>
                                        <td>
                                            <Link 
                                                to={`/document/${document.id}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
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
