from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os
from mangum import Mangum

app = FastAPI()

# --- 🔗 SUPABASE CONFIG ---
# These should be set as Environment Variables in Vercel
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
API_KEY = os.environ.get("KYBERNETES_API_KEY", "kybernetes_secret_bridge_01")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- 📱 WHATSAPP ENDPOINT ---
@app.post("/whatsapp")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    data = {
        "prompt": Body,
        "sender": From,
        "status": "pending"
    }
    supabase.table("commands").insert(data).execute()
    return {"status": "queued"}

# --- 🛠️ LOCAL POLLER ENDPOINTS ---
@app.get("/poll")
async def poll_commands(key: str):
    if key != API_KEY: raise HTTPException(status_code=403)
    
    # Get the oldest pending command
    result = supabase.table("commands") 
        .select("*") 
        .eq("status", "pending") 
        .order("created_at") 
        .limit(1) 
        .execute()
    
    if not result.data:
        return {"command": None}
    
    cmd = result.data[0]
    # Mark as 'processing' so it doesn't get pulled again
    supabase.table("commands").update({"status": "processing"}).eq("id", cmd["id"]).execute()
    
    return {"command": {"id": str(cmd["id"]), "prompt": cmd["prompt"]}}

@app.post("/result")
async def post_result(command_id: str, output: str, key: str):
    if key != API_KEY: raise HTTPException(status_code=403)
    
    # Store result and mark as completed
    supabase.table("commands").update({
        "status": "completed",
        "result": output
    }).eq("id", command_id).execute()
    
    return {"status": "success"}

# Bridge FastAPI to Vercel
handler = Mangum(app)
