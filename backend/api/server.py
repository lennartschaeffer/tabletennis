from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import uuid

from backend.api.services.videoProcessingService import process_video

app = FastAPI(title="Table Tennis Analysis API")

# cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-video")
async def analyze_video(video: UploadFile = File(...)):
    # Create a temporary file to store the uploaded video
    temp_file = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.mp4")
    
    try:
        # Save uploaded file to temp location
        with open(temp_file, "wb") as buffer:
            buffer.write(await video.read())
        
        # Process the video and get results
        results = process_video(temp_file)
        
        return {
            "filename": video.filename,
            "forehand_count": results["forehand_count"],
            "backhand_count": results["backhand_count"],
            "total_hits": results["hit_count"],
            "status": "success"
        }
        
    finally:
        # Clean up the temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)