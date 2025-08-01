# Simple Setup Guide

## What You Need First

1. **API Keys** (get these before starting):
   - OpenAI API Key: https://platform.openai.com/api-keys
   - Napkin API Key: Request from https://napkin.ai

2. **Software** (install these):
   - Python 3.8+ 
   - Node.js 16+
   - Docker (optional but recommended)

## Quick Start (Using Docker) - Easiest Way!

1. Create a `.env` file:
```bash
OPENAI_API_KEY=your_openai_key_here
NAPKIN_API_KEY=your_napkin_key_here
```

2. Run everything:
```bash
docker-compose up
```

3. Open http://localhost:3000

## Manual Setup (Without Docker)

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## How to Use

1. **Upload**: Drag a PDF or image to the upload area
2. **Wait**: The app will process it (takes 10-30 seconds)
3. **Chat**: Ask questions about your document
4. **Regenerate**: Click on any diagram to make it cleaner

## Common Issues

- **"API key not found"**: Make sure your `.env` file is in the root directory
- **"Cannot connect to backend"**: Make sure backend is running on port 8000
- **"Upload failed"**: Check that the file is PDF or image format

## Next Steps

After you get the basic version working, you can:
1. Add more OCR accuracy
2. Improve the chat responses
3. Add user accounts
4. Deploy to the cloud