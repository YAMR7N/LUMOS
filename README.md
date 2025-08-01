# EJUST Study Assistant

A graph-savvy study assistant that transforms user-uploaded notes (handwritten pages, PDFs, photos) into a chat-first knowledge base.

## Features

1. **Answer questions** with citations (RAG)
2. **Re-draw figures/graphs** in a clean, branded style via Napkin
3. **Export** regenerated notes as DOCX/PDF

## Architecture

- **Frontend**: React 19 + Vite 5 + Tailwind 3
- **Backend**: FastAPI with WebSocket support
- **OCR**: PaddleOCR ultra-lite + ChartOCR
- **Vector DB**: pgvector or Qdrant
- **LLM**: GPT-4o / Llama-3-8B
- **Task Queue**: Redis + RQ
- **Auth**: Firebase Auth

## Project Structure

```
├── frontend/               # React SPA
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API services
│   │   └── utils/        # Utilities
│   └── tests/
├── backend/               # FastAPI application
│   ├── api/              # API endpoints
│   ├── services/         # Business logic
│   ├── core/             # Core functionality
│   └── tests/
├── services/             # Microservices
│   ├── ocr-service/      # OCR processing
│   └── chart-ocr-service/# Chart recognition
├── infrastructure/       # Deployment configs
├── shared/              # Shared types/utils
└── docs/                # Documentation
```

## Getting Started

See [docs/deployment/local-setup.md](docs/deployment/local-setup.md) for development setup instructions.