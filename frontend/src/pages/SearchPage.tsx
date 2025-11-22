import {useState} from 'react'
import { useDocumentsAndCategories } from '@/components/FetchData'
import '@/styles/home.css'
import '@/styles/search.css'

export default function SearchPage(){
    const { 
        loading,
        error,
        categoryMap,
        // categoryDocumentMap,
    } = useDocumentsAndCategories();
    const [selectedCategory, setSelectedCategory] = useState("All");
    const [searchInput, setSearchInput] = useState("");
    // const [documentsSearchResult, setDocumentsSearchResult] = useState("");

    const handleSearch = () => {

        if (selectedCategory)
        alert("Searched for something");
    }

    if (loading) return <div></div>;
    if (error) return <div>Error loading documents</div>;

    return (
        
    <div>
        <div className='search-top'>
            {/* Title */}
            <h1 className='page-title'>Search</h1>
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
                    {Object.keys(categoryMap).map((cat) => (
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
                    🔍 Search
                </button>
            </div>
        </div>
    </div>)
}