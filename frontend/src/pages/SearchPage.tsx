import {useState} from 'react'
import { useDocumentsAndCategories } from '@/components/FetchData'
import type { DocumentType } from '@/util/types';
import '@/styles/home.css'
import '@/styles/search.css'

export default function SearchPage(){
    const { 
        loading,
        error,
        categoryDocumentMap,
    } = useDocumentsAndCategories();
    const [selectedCategory, setSelectedCategory] = useState("All");
    const [searchInput, setSearchInput] = useState("");
    const [documentsSearchResult, setDocumentsSearchResult] = useState<DocumentType[] | null>(null)

    const handleSearch = () => {
        // 0. Check if text in search input
        if (searchInput === ""){
            return;
        }
        alert(searchInput)

        // 1. Select documents based on selected category
        let filteredDocuments : DocumentType[] = []
        if (selectedCategory === "All"){
            Object.keys(categoryDocumentMap).forEach((category : string) => {
                filteredDocuments.push(...categoryDocumentMap[category])
            })
        }
        else if(categoryDocumentMap[selectedCategory]){
            filteredDocuments = categoryDocumentMap[selectedCategory]
        }
        else{
            alert("Invalid category")
            return;
        }

        // 2. Perform search
        const search_result : DocumentType[] = filteredDocuments.filter((document : DocumentType) => 
            document.extracted_text && document.extracted_text.toLowerCase().includes(searchInput.toLowerCase())
        )
        setDocumentsSearchResult(search_result);
        alert("Searched for " + searchInput);
    }

    if (loading) return <div/>;
    if (error) return <div>Error loading documents</div>;

    return (    
        <div>
            <div className='search-top'>
                {/* Title */}
                <h1 className='page-title'>Document Search</h1>
            </div>

            <div className="search-controls">
                {/* Category Filters*/}
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

                {/* Search Bar*/}
                <div className="search-bar">
                    <input
                        type="search"
                        placeholder='Search Here'
                        onChange={(e) => setSearchInput(e.target.value)}
                        onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                        value={searchInput}
                    />
                    <button className="search-button" onClick={handleSearch}>
                        Search&nbsp; 🔍 
                    </button>
                </div>
            </div>
        </div>
    )
}