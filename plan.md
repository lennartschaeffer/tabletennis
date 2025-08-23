# Table Tennis Gamified Practice App Plan

## Overview

This app allows users to select a table tennis skill to practice (forehand, backhand, alternation, rally longevity), upload a video, and receive feedback based on their chosen goal. The system uses ML models for ball/paddle detection, stroke classification, and table contour analysis.

---

## Features

- **Practice Modes:**

  - Forehand Practice
  - Backhand Practice
  - Alternation Challenge
  - Rally Longevity

- **Video Upload:** Users upload a video of their session.

- **Automated Evaluation:** ML models analyze the video and score performance based on the selected mode.

- **Feedback Dashboard:** Visualizes results, stats, and improvement suggestions.

---

## Frontend Implementation

### Tech Stack

- React (or Vue/Svelte)
- CSS/Styled Components
- Axios (for API calls)

### Key Components

1. **Practice Mode Selector**

   - Dropdown or buttons for mode selection.

2. **Video Upload**

   - File input for video.
   - Progress bar for upload.

3. **Results Dashboard**
   - Display stats (hits, forehands, backhands, alternations, rally streak).
   - Charts (e.g., bar chart for stroke counts).
   - Feedback messages.

### Example React Component Structure

```javascript
// PracticeApp.jsx
import React, { useState } from "react";
import axios from "axios";

function PracticeApp() {
  const [mode, setMode] = useState("forehand");
  const [video, setVideo] = useState(null);
  const [results, setResults] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("mode", mode);
    formData.append("video", video);

    const response = await axios.post("/api/evaluate", formData);
    setResults(response.data);
  };

  return (
    <div>
      <h1>Table Tennis Practice</h1>
      <select value={mode} onChange={(e) => setMode(e.target.value)}>
        <option value="forehand">Forehand Practice</option>
        <option value="backhand">Backhand Practice</option>
        <option value="alternation">Alternation Challenge</option>
        <option value="rally">Rally Longevity</option>
      </select>
      <input
        type="file"
        accept="video/*"
        onChange={(e) => setVideo(e.target.files[0])}
      />
      <button onClick={handleUpload}>Upload & Evaluate</button>
      {results && (
        <div>
          <h2>Results</h2>
          <pre>{JSON.stringify(results, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default PracticeApp;
```

---

## Backend Implementation

### Tech Stack

- FastAPI (Python) or Flask
- ML models (PyTorch, YOLO)
- Video processing (OpenCV)

### API Endpoints

- `POST /api/evaluate`
  - Accepts: `mode`, `video`
  - Returns: JSON with evaluation results

### Example FastAPI Endpoint

```python
# filepath: backend/main.py
from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import JSONResponse
import shutil
import os

app = FastAPI()

@app.post("/api/evaluate")
async def evaluate(mode: str = Form(...), video: UploadFile = Form(...)):
    video_path = f"temp/{video.filename}"
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # Call your ML evaluation function here
    results = evaluate_video(video_path, mode)

    os.remove(video_path)
    return JSONResponse(content=results)

def evaluate_video(video_path, mode):
    # Load models, process video, and return results based on mode
    # Example output:
    return {
        "mode": mode,
        "forehand_count": 12,
        "backhand_count": 8,
        "alternation_score": 6,
        "rally_streak": 14,
        "feedback": "Try to alternate more consistently!"
    }
```

---

## ML Evaluation Logic

- Use your existing code (`local_testing.py`) as the core evaluation logic.
- Refactor it into a function that accepts a video path and mode, and returns results.
- For each mode, tailor the scoring logic:
  - **Forehand:** Count forehand strokes.
  - **Backhand:** Count backhand strokes.
  - **Alternation:** Score correct alternations.
  - **Rally:** Track longest hit streak.

---

## Next Steps

1. Refactor your ML code into callable functions for backend integration.
2. Build the FastAPI backend and connect it to the frontend.
3. Implement the React frontend and connect to the backend API.
4. Test with sample videos and iterate on feedback logic.

---

## Optional Enhancements

- Add user authentication and leaderboards.
- Visualize stroke locations and rally heatmaps.
- Provide personalized improvement tips.

---
