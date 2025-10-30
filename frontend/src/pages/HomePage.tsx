import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom';
import '@/styles/home.css'

interface DocumentType {
  id: number;
  name: string;
  description: string;
  category_id: number;
}

interface CategoryType{
  id: number;
  name: string;
}

interface CategoryDocumentsType {
  id: number;
  category: string;
  documents: DocumentType[];
}

interface CategoryDocumentsDictType{
  [category: string] : DocumentType[];
}

export default function HomePage() {
  const [categories, setCategories] = useState<CategoryDocumentsDictType>({});
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState(false);

  const [showAddCategoryPopUp, setshowAddCategoryPopUp] = useState<boolean>(false);
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

        // 3. Perform join on categories and documents
        const documentMap: Record<number, DocumentType[]> = {};
        document_data.forEach((doc : DocumentType) => {
          if(!documentMap[doc.category_id]){
            documentMap[doc.category_id] = []
          }
          documentMap[doc.category_id].push(doc);
        });
        const category_documents : CategoryDocumentsType[] = category_data.map((cat : CategoryType) => ({
          id: cat.id,
          category: cat.name,
          documents: documentMap[cat.id]
        }));
        const categoryDict: CategoryDocumentsDictType = {};
        category_documents.forEach((cat : CategoryDocumentsType) => {
          categoryDict[cat.category] = cat.documents;
        });
        
        setCategories(categoryDict);

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

  const handleAddCategory = () => {
    if (categories[newCategoryName]) { 
      return alert("Category already exists");
    }
    setCategories(prev => ({ ...prev, [newCategoryName]: [] }));
    setshowAddCategoryPopUp(false);
    setNewCategoryName("");
  };

  const handleDeleteDocument = (category: string, document: DocumentType) => {
    if (confirm("Are you sure you want to delete this document")){
      setCategories((prevCategories) => ({
        ...prevCategories,
        [category]: prevCategories[category].filter((doc : DocumentType) => doc.id !== document.id)
      }));
    }
  }

  const displayedCategories =
    selectedCategory === 'All' ? Object.keys(categories) : [selectedCategory];

  if (loading) return <div>Loading...</div>;
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
            onClick={() => setshowAddCategoryPopUp(true)}
          >
            Add Category</button>
          <Link 
            to='/add-document'
            state={{ categories: categories }}>
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
          {Object.keys(categories).map((cat) => (
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

            {expandedCategory === category && (
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
                  {categories[category]?.map((record, idx) => (
                    <tr key={idx}>
                      <td>{record.name}</td>
                      <td>{record.description}</td>
                      <td>
                        <button className="document-button view-button">View</button>
                      </td>
                      <td>
                        <button 
                          className="document-button delete-button"
                          onClick={() => handleDeleteDocument(category, record)}
                        >
                          Delete</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        ))}
      </div>

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
            <button className="popup-cancel-button" onClick={() => setshowAddCategoryPopUp(false)}>Cancel</button>
          </div>
        </div>
      </div>
    )}
    </div>
  );
}