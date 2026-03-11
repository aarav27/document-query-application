# DocQuery
DocQuery is a application that lets you upload and interact with your PDFs. It has a hybrid search engine and Q&A agent powered by Retrieval-Augmented Generation (RAG) to search and retrieve information from PDF documents.


## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS%20S3-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-EF2D5E?style=for-the-badge&logo=qdrant&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white)


## Core Features

### 1. Document Handling
- Upload, view, and delete PDF documents
- Store and display document metadata
- Organize documents by custom categories for better management

### 2. Document Search
- Find relevant documents using combining keyword search (exact text matching) and semantic search (natural language and contextual meaning)

### 3. Q&A
- Ask questions about documents that synthesizes information across multiple documents
- Generates concise and accurate answers and cites relevant document sources in responses


## Usage

### Categories

1. Go to the "Home" section
2. Click "Add Category"
3. Enter a category name and click "Add Category"
4. Click the toggle for a category to see document information
5. Click "Delete Category" to delete category and all documents inside it
6. Select a category using the category dropdown

### Documents

1. Go to the "Home" section
2. Click the toggle for a category to see document information
3. Click "View" to view a document
4. Click "Delete" to delete a document

### Uploading Documents

1. Go to the "Home" section
2. Click "Add Document"
3. Select a PDF file
4. Enter a document description
5. Choose or create a category
6. Click "Upload"

### Document Search

1. Go to the "Search" section
2. Enter your search query
3. View results ranked by relevance
4. Click 'View' to view the document
5. Use filters to narrow results by category

### Q&A

1. Navigate to the "Q&A" section
2. Enter a query about the documents
3. View the LLM generated answer with cited sources
4. Continue the conversation


## Data Flow

### Document Ingestion
```
PDF Upload → Text Extraction → Chunking → Embedding Generation → Vector Store
```

### Document Search
```
User Query → Hybrid Search → Document Results
```

### Q&A
```
User Query → Processing -> Retrieval (Hybrid) → Augmentation -> LLM Generation → LLM Response
```


## Application Components

**Frontend (React + TypeScript)**
- Document Dashboard Page (Home)
    - Document and Category Management and View
    - Category Filter
    - Add/Remove Documents and Categories
- Add Document Page
- Search Page
- Q&A Page

**Backend (FastAPI + Python)**
- Endpoints
    - Documents
    - Categories
    - Search
    - Q&A
- Core Logic
    - Document Ingestion
    - Hybrid Search
    - RAG Pipeline

**Databases and Storage**
- **PostgreSQL**: Document metadata and categories
- **Qdrant**: Vector embeddings (dense and spare) for hybrid search
- **AWS S3**: PDF files and processed documents


## RAG Architecture
### Vector Database
- Qdrant stores dense and sparse embeddings to perform hybrid search
    - `sentence-transformers/all-MiniLM-L6-v2` to generate dense embeddings for semantic search 
    - `Qdrant/bm25` to generate sparse Embeddings for keyword search using BM25

### Semantic Search
- Computes cosine similarity to determine document relevance to a query (to capture similar contextual meaning)

### BM25 Search
- Ranking algorithm to determine document relevance to a query (for exact keyword matching)
- Calculates scores based on 
    - (1) term frequency (TF)
    - (2) inverse document frequency (IDF)
    - (3) document length normalization

### LLM Generation
- Model: `Qwen/Qwen2-1.5B-Instruct`
- Uses retrieved documents from hybrid search as context to augment response generation


## Installation & Setup

### 0. Prerequisites
- Node.js 16+ (for frontend development)
- Python 3.9+ (for backend)
- PostgreSQL 14+
- Docker (for containerized deployment)

### 1. Clone the Repository
```bash
git clone https://github.com/aarav27/document-query-application.git
cd document-query-application
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration:
# - DATABASE_URL=postgresql://user:password@localhost/docquery
# - AWS_S3_BUCKET="your_bucket_name"
# - AWS_REGION_NAME="region_name"
# - AWS_ACCESS_KEY_ID=your_access_key
# - AWS_SECRET_ACCESS_KEY=your_secret_key
# - QDRANT_URL=http://localhost:6333
# - QDRANT_API_KEY=your_api_key

# Start the backend server
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

Frontend will be available at `http://localhost:5173`

### 4. Database Setup

```bash
# Start PostgreSQL container
docker run -d \
  --name docquery-postgres \
  -e POSTGRES_DB=docquery \
  -e POSTGRES_USER=docuser \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:14

# Copy SQL initialization file into container
docker cp db-init/init.sql docquery-postgres:/init.sql

# Execute SQL inside container to create tables
docker exec -it docquery-postgres psql -U docuser -d docquery -f /init.sql
```

### 5. Vector Database Setup (Qdrant)

```bash
# Using Docker
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  qdrant/qdrant:latest
```

Qdrant dashboard will be available at `http://localhost:6333/dashboard`


## Project Structure Overview

```
docquery/
├── frontend/                    # React TypeScript application
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── styles/             # CSS/styling
│   │   ├── util/               # Types
│   │   ├── App.tsx             # Navigation and routes
│   │   └── main.tsx            # Application root
│   └── package.json
├── backend/                     # FastAPI application
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Configuration and utilities
│   │   ├── models/            # SQLAlchemy models
│   │   ├── rag/               # Document search and Q&A logic
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Document and category management logic
│   ├── main.py                # Backend startup
│   └── requirements.txt
└── db-init                    # Database setup
│   └── init.sql               # Application Schema
```


## API Endpoints

### Documents
- `GET /api/documents` - Retrieve all documents
- `GET /api/documents/{id}` - Retrieve a specific document
- `POST /api/documents` - Add a document
- `DELETE /api/documents/{id}` - Delete a document
- `POST /api/documents/download-url` - Generate download URL for document
- `POST /api/documents/upload-url` - Generate upload URL for document

### Categories
- `GET /api/categories` - Retrieve all categories
- `POST /api/categories` - Create a category
- `DELETE /api/categories/{id}` - Delete a category

### Search
- `POST /api/search` - Hybrid search across documents

### Q&A
- `POST /api/rag/qa` - Ask a question about documents and get an answer

