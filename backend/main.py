from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the FastAPI app
app = FastAPI(title="Study Assistant API")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

# Create directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Study Assistant API is running!"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file uploads"""
    # Save the uploaded file
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # TODO: Process with OCR
    # TODO: Extract text and store in vector DB
    
    return {"filename": file.filename, "status": "uploaded"}


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """Handle chat conversations"""
    await websocket.accept()
    
    while True:
        # Receive message from frontend
        data = await websocket.receive_text()
        
        # TODO: Query vector DB
        # TODO: Generate response with GPT
        # TODO: Stream response back
        
        # For now, echo back
        await websocket.send_text(f"Echo: {data}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)