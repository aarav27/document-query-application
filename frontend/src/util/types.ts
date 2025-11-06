export interface DocumentType {
  id: number;
  name: string;
  description: string;
  s3_document_key: string;
  category_id: number;
}

export interface DocumentCreateType {
  name: string;
  description: string;
  category_id: number;
}

export interface DocumentWithUploadURLType {
  id: number;
  name: string;
  description: string;
  s3_document_key: string;
  upload_url : string;
  category_id: number;
}

export interface CategoryType{
  id: number;
  name: string;
}

export interface CategoryDocumentsType {
  id: number;
  category: string;
  documents: DocumentType[];
}

export interface CategoryDocumentsDictType{
  [category: string] : DocumentType[];
}