# EJUST Study Assistant - Proof of Concept

A simple working prototype that transforms uploaded notes into a chat-enabled knowledge base with figure regeneration.

## What It Does

1. **Upload** - Drag & drop PDFs or images
2. **Chat** - Ask questions about your notes
3. **Regenerate** - Create clean versions of diagrams
4. **Export** - Download improved notes

## Simple Project Structure

```
ejust-study-assistant/
├── frontend/          # React app
│   ├── src/
│   │   ├── components/   # UI components
│   │   └── services/     # API calls
│   └── public/
├── backend/           # Python FastAPI server
│   ├── main.py          # Main server file
│   ├── ocr.py           # OCR processing
│   ├── chat.py          # Chat functionality
│   ├── uploads/         # Uploaded files
│   └── outputs/         # Generated files
├── docker-compose.yml    # Run everything with one command
└── README.md            # You are here!
```

## Quick Start

1. Clone the repo
2. Add your API keys to `.env`
3. Run `docker-compose up`
4. Open http://localhost:3000

That's it! 🚀