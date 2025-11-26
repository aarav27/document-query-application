export interface DocumentType {
  id: number;
  name: string;
  description: string;
  s3_document_key: string;
  category_id: number;
  extracted_text: string;
}

export interface DocumentCreateType {
  name: string;
  description: string;
  s3_document_key: string;
  category_id: number;
}

export interface CategoryType{
  id: number;
  name: string;
}

export interface CategoryMapType{
  [category : string] : number
}

export interface CategoryDocumentsMapType{
  [category: string] : DocumentType[];
}