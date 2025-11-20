import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import '@/styles/home.css'
import type { CategoryType, DocumentType, CategoryMapType, CategoryDocumentsMapType} from '@/util/types';

export default function HomePage() {
  const [categoryDocumentMap, setCategoryDocumentMap] = useState<CategoryDocumentsMapType>({});
  const [categoryMap, setCategoryMap] = useState<CategoryMapType>({})
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState(false);

  const [showAddCategoryPopUp, setShowAddCategoryPopUp] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState<string>("");

  useEffect(() => {
    const fetchAll = async () => {
      try {
        // 1. Fetch all documents
        const document_response = await fetch("http://127.0.0.1:8000/documents");
        if (!document_response.ok) {
          throw new Error(`Error Status: ${document_response.status}`);
        }
        const document_data = await document_response.json();
        
        // 2. Fetch all categories
        const response = await fetch("http://127.0.0.1:8000/categories");
        if (!response.ok) {
          throw new Error(`Error Status: ${response.status}`);
        }
        const category_data = await response.json();
        
        // 3. Create category map
        const catMapNameToId : CategoryMapType = {};
        const catMapIdToName : Record<number, string> = {};
        category_data.forEach((cat : CategoryType) => {
          catMapNameToId[cat.name] = cat.id
          catMapIdToName[cat.id] = cat.name
        })
        setCategoryMap(catMapNameToId)

        // 4. Create category document map
        const catDocMap : CategoryDocumentsMapType = {}
        Object.keys(catMapNameToId).forEach((cat_name : string) => 
          catDocMap[cat_name] = []
        )
        document_data.forEach((doc : DocumentType) => {
          const cat_name : string = catMapIdToName[doc.category_id]
          if(cat_name){
            if (!catDocMap[cat_name]) {
              catDocMap[cat_name] = []
            }
            catDocMap[cat_name].push(doc)
          }
        })
        setCategoryDocumentMap(catDocMap)

      } catch {
        setError(true);
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  const toggleCategory = (category: string) => {
    setExpandedCategory(expandedCategory === category ? null : category);
  };

  const handleAddCategory = async () => {
    if (newCategoryName === ""){
      return alert("Enter a category name")
    }
    if (categoryDocumentMap[newCategoryName] || categoryMap[newCategoryName]) { 
      return alert("Category already exists");
    }

    try {
      const newCategory = {
        name: newCategoryName
      };
      const add_category_response = await fetch("http://127.0.0.1:8000/categories", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newCategory),
      });

      if(add_category_response.ok){
        const new_category_data : CategoryType = await add_category_response.json();
        setCategoryDocumentMap(prev => ({ ...prev, [new_category_data.name]: []}));
        setCategoryMap(prev => ({ ...prev, [new_category_data.name]: new_category_data.id}))

        setShowAddCategoryPopUp(false);
        setNewCategoryName("");

        alert(`Added Category: ${new_category_data.name}`)
      }

    } catch(error) {
      alert("Failed to add category")
      throw error
    }
  };

  const handleDeleteCategory = async(category: string) => {
    if (!confirm(`Confirm to delete ${category}\nNote: This will delete all documents under ${category}`)){
      return;
    }

    try {
      const category_id = categoryMap[category]
      const delete_category_response = await fetch(`http://127.0.0.1:8000/categories/${category_id}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if(delete_category_response.ok){
        const new_categoryMap = { ...categoryMap }
        delete new_categoryMap[category]
        setCategoryMap(new_categoryMap)

        const new_categoryDocumentMap = { ...categoryDocumentMap }
        delete new_categoryDocumentMap[category]
        setCategoryDocumentMap(new_categoryDocumentMap)

        alert(`Deleted Category: ${category}`)
      }

    } catch (error) {
      alert("Failed to delete category")
      throw error
    }
  }

  const handleDeleteDocument = async (category: string, document: DocumentType) => {
    if (!confirm(`Confirm to delete ${document.name} in ${category}`)){
      return;
    }

    try {
      const delete_document_response = await fetch(`http://127.0.0.1:8000/documents/${document.id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
      });

      if(delete_document_response.ok){
        setCategoryDocumentMap((prevCategories) => ({
          ...prevCategories,
          [category]: prevCategories[category].filter((doc : DocumentType) => doc.id !== document.id)
        }));
      }

    } catch (error) {
      alert("Failed to delete document")
      throw error
    }
  }

  const displayedCategories = selectedCategory === 'All' ? Object.keys(categoryDocumentMap) : [selectedCategory];

  if (loading) return <div></div>;
  if (error) return <div>Error loading documents</div>;

  return (
    <div>
      <div className='dashboard-top'>
        {/* Title */}
        <h1 className='dashboard-title'>Document Dashboard</h1>

        {/* Buttons container */}
        <div className='dashboard-buttons'>
          <button 
            className='dashboard-button add-category-button'
            onClick={() => setShowAddCategoryPopUp(true)}
          >
            Add Category</button>
          <Link to='/add-document'>
            <button className='dashboard-button add-document-button'>Add Document</button>
          </Link>
        </div>
      </div>

      {/* Category Filter Dropdown */}
      <div className='category-filter'>
        <label htmlFor="category">Filter by Category:</label>
        <select
          id="category"
          className="category-dropdown"
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
        >
          <option value="All">All</option>
          {Object.keys(categoryDocumentMap).map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {/* Documents by Category */}
      <div className='category-sections'>
        {displayedCategories.map((category) => (
          <div key={category} className='category-section'>
            <div
              className='category-header'
              onClick={() => toggleCategory(category)}
            >
              <h2>{category}</h2>
              <span>{expandedCategory === category ? '▲' : '▼'}</span>
            </div>
            
            {/* Document Table */}
            {expandedCategory === category && (
            <div>
              <table className='document-table'>
                <thead>
                  <tr>
                    <th>Document Name</th>
                    <th>Description</th>
                    <th>View</th>
                    <th>Delete</th>
                  </tr>
                </thead>
                <tbody>
                  {categoryDocumentMap[category].map((document, idx) => (
                    <tr key={idx}>
                      <td>{document.name}</td>
                      <td>{document.description}</td>
                      <td>
                        <Link
                          to={`/document/${document.id}`}
                          state={{document, category}}
                        >
                          <button 
                            className="document-button view-button"
                          >View</button>
                        </Link>
                      </td>
                      <td>
                        <button 
                          className="document-button delete-button"
                          onClick={() => handleDeleteDocument(category, document)}
                        >
                          Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className='delete-category-container'>
                <button 
                  className='delete-category' 
                  onClick={() => handleDeleteCategory(category)}
                >
                  Delete Category
                </button>
              </div>
            </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Add Category Pop Up */}
      {showAddCategoryPopUp && (
      <div className="popup-overlay">
        <div className="popup-content">
          <label>
            New Category:
            <input
              type="text"
              value={newCategoryName}
              onChange={(e) => setNewCategoryName(e.target.value)}
            />
          </label>

          <div className="popup-buttons">
            <button className="popup-add-category-button" onClick={handleAddCategory}>Add Category</button>
            <button className="popup-cancel-button" onClick={() => {
              setShowAddCategoryPopUp(false)
              setNewCategoryName("");
            }}>
              Cancel
            </button>
          </div>
        </div>
      </div>
    )}
    </div>
  );
}