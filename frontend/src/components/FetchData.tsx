import { useEffect, useState } from 'react'
import type { CategoryType, DocumentType, CategoryMapType, CategoryDocumentsMapType} from '@/util/types';

export function useDocumentsAndCategories(){
    const [categoryMap, setCategoryMap] = useState<CategoryMapType>({})
    const [categoryDocumentMap, setCategoryDocumentMap] = useState<CategoryDocumentsMapType>({});
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState(false);

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
                const catMapNametoId : CategoryMapType = {};
                const catMapIdToName : Record<number, string> = {};
                category_data.forEach((cat: CategoryType) => {
                    catMapNametoId[cat.name] = cat.id
                    catMapIdToName[cat.id] = cat.name
                })
                setCategoryMap(catMapNametoId)
        
                // 4. Create category document map
                const catDocMap: CategoryDocumentsMapType = Object.fromEntries(
                    Object.keys(catMapNametoId).map(name => [name, []])
                );
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
        }
        fetchAll();
    }, []);

    return {loading, error, categoryMap, categoryDocumentMap, setCategoryMap, setCategoryDocumentMap}
}