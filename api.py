from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import shutil
import os
from main import run_agent, FILENAME

app = FastAPI()

# In-memory session store (simple version)
sessions: dict[str, list] = {}

class QueryRequest(BaseModel):
    session_id: str
    query: str

@app.post("/query")
def query(request: QueryRequest):
    history = sessions.get(request.session_id, [])
    history = run_agent(request.query, messages=history)
    sessions[request.session_id] = history

    # Extract last assistant message as the response
    assistant_messages = [m for m in history if m["role"] == "assistant"]
    last_response = assistant_messages[-1]["content"] if assistant_messages else ""

    return {"response": last_response, "session_id": request.session_id}

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    dest = os.path.join("data", file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.get("/chart/{filename}")
def get_chart(filename: str):
    path = os.path.join("outputs", filename)
    if os.path.exists(path):
        return FileResponse(path, media_type="image/png")
    return {"error": "Chart not found"}