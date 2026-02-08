from fastapi import FastAPI, Request, Form, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import time

app = FastAPI(title="Kybernetes Cloud Relay")

# --- 🔒 SECURITY ---
# Change this to a strong secret key!
API_KEY = "kybernetes_secret_bridge_01" 
COMMAND_QUEUE = []
RESULTS = {}

class Command(BaseModel):
    id: str
    prompt: str
    sender: str
    timestamp: float

class Result(BaseModel):
    command_id: str
    output: str

# --- 📱 WHATSAPP ENDPOINT (Twilio Webhook) ---
@app.post("/whatsapp")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    """
    Entry point for WhatsApp. Twilio sends message in 'Body' 
    and sender in 'From'.
    """
    command_id = str(uuid.uuid4())
    new_cmd = {
        "id": command_id,
        "prompt": Body,
        "sender": From,
        "timestamp": time.time()
    }
    COMMAND_QUEUE.append(new_cmd)
    
    # Simple acknowledgment back to WhatsApp via Twilio XML response could be added here
    return {"status": "queued", "command_id": command_id, "message": "Command received by Kybernetes Relay."}

# --- 🛠️ LOCAL POLLER ENDPOINTS (Your PC hits these) ---
@app.get("/poll")
async def poll_commands(key: str):
    if key != API_KEY: 
        raise HTTPException(status_code=403, detail="Invalid API Key")
    if not COMMAND_QUEUE:
        return {"command": None}
    
    return {"command": COMMAND_QUEUE.pop(0)}

@app.post("/result")
async def post_result(result: Result, key: str):
    if key != API_KEY: 
        raise HTTPException(status_code=403, detail="Invalid API Key")
    RESULTS[result.command_id] = result.output
    print(f"Result received for {result.command_id}")
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
