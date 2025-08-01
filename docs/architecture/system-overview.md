# System Architecture Overview

## High-Level Architecture

The Study Assistant is built as a microservices architecture with the following main components:

### Frontend (React SPA)
- **Technology**: React 19 + Vite 5 + Tailwind CSS
- **Responsibilities**: 
  - User authentication via Firebase
  - File upload interface
  - Real-time chat interface with WebSocket
  - Figure regeneration UI
  - Document export functionality

### Backend Gateway (FastAPI)
- **Technology**: FastAPI 0.111 + Uvicorn
- **Responsibilities**:
  - Authentication middleware
  - WebSocket management
  - Request routing
  - Rate limiting
  - Job queue management

### Core Services

#### OCR Service
- **Technology**: PaddleOCR ultra-lite
- **Purpose**: Extract text and diagrams from uploaded documents
- **Output**: JSON with text content and SVG representations

#### Chart OCR Service  
- **Technology**: chart-ocr 0.4
- **Purpose**: Extract data tables from charts
- **Requirements**: Optional GPU support

#### Retrieval Service (R2R-Light)
- **Technology**: R2R-Light 0.3.4
- **Features**:
  - Document chunking
  - Embedding generation (OpenAI ada-3 or Cohere)
  - Hybrid search (BM25 + vector)

#### Vector Database
- **Options**: pgvector 0.6 or Qdrant 1.9
- **Purpose**: Store and search document embeddings

#### LLM Integration
- **Models**: 
  - GPT-4o (primary)
  - Llama-3-8B via Ollama (fallback)
- **Functions**:
  - Generate chat responses
  - Create Napkin prompts
  - Extract alt-text for figures

#### Figure Rendering (Napkin API)
- **Purpose**: Convert prompts + data tables to branded SVG figures
- **SLA**: 95% of jobs complete in <10s

### Supporting Infrastructure

#### Task Queue
- **Technology**: Redis + RQ
- **Purpose**: Handle async OCR and Napkin polling

#### Authentication
- **Technology**: Firebase Auth
- **Features**: JWT-based authentication

#### Export Service
- **Technology**: python-docx + pdfkit
- **Output**: DOCX/PDF with regenerated content

## Data Flow

1. User uploads document → Frontend
2. Frontend sends to Backend Gateway
3. Gateway queues OCR job → Redis/RQ
4. OCR Service processes → Extract text/figures
5. ChartOCR extracts data from charts
6. R2R-Light chunks and embeds content
7. Embeddings stored in Vector DB
8. User asks question → WebSocket to Gateway
9. Gateway queries Vector DB + LLM
10. Streaming response back to Frontend
11. For figure regeneration:
    - Extract data table from ChartOCR
    - Generate Napkin prompt via LLM
    - Poll Napkin API for SVG
    - Cache and serve to Frontend

## Non-Functional Requirements

- **Performance**: P95 end-to-end latency <15s
- **Scale**: Support 1k concurrent WebSocket connections
- **Security**: HTTPS, OWASP top-10 compliance
- **Cost**: Stay within $50/month budget
- **Accessibility**: WCAG AA compliance