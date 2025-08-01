# Local Development Setup

## Prerequisites

- Node.js 20+
- Python 3.11+
- Docker & Docker Compose
- Firebase project (for authentication)
- OpenAI API key
- Napkin API key (request from Napkin.ai)

## Environment Variables

Create `.env` files in the root directory:

```bash
# .env
OPENAI_API_KEY=your_openai_key
NAPKIN_API_KEY=your_napkin_key
FIREBASE_CONFIG=your_firebase_config_json
```

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ejust-study-assistant
   ```

2. **Install dependencies**
   ```bash
   # Install root dependencies
   npm install

   # Install frontend dependencies
   cd frontend && npm install && cd ..

   # Install backend dependencies
   cd backend && pip install -r requirements.txt && cd ..
   ```

3. **Start infrastructure services**
   ```bash
   docker-compose up -d postgres redis pgvector
   ```

4. **Initialize database**
   ```bash
   cd backend
   python -m scripts.init_db
   ```

5. **Download Ollama model (optional)**
   ```bash
   docker-compose up -d ollama
   docker exec -it ejust-study-assistant-ollama-1 ollama pull llama3:8b-instruct
   ```

6. **Start development servers**
   ```bash
   # From root directory
   npm run dev
   ```

   This starts:
   - Frontend: http://localhost:5173
   - Backend: http://localhost:8000
   - API docs: http://localhost:8000/docs

## Individual Service Development

### Frontend Only
```bash
cd frontend
npm run dev
```

### Backend Only
```bash
cd backend
uvicorn main:app --reload
```

### OCR Service
```bash
cd services/ocr-service
python main.py
```

### Chart OCR Service
```bash
cd services/chart-ocr-service
python main.py
```

## Testing

### Run all tests
```bash
npm test
```

### Frontend tests
```bash
cd frontend && npm test
```

### Backend tests
```bash
cd backend && pytest
```

## Troubleshooting

### Port conflicts
If ports are already in use, modify the port mappings in:
- `docker-compose.yml`
- `frontend/vite.config.ts`
- `backend/main.py`

### Database connection issues
Ensure PostgreSQL is running:
```bash
docker-compose ps
docker-compose logs postgres
```

### OCR performance
For faster OCR on Mac M1/M2:
- Install PaddleOCR with MPS support
- Or use the lightweight CPU version

### Firebase authentication
1. Create a Firebase project
2. Enable Authentication
3. Add your domain to authorized domains
4. Download service account key
5. Set FIREBASE_CONFIG environment variable