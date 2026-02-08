from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from twilio.rest import Client as TwilioClient
import os
from mangum import Mangum

app = FastAPI()

# --- 🔗 CONFIGURATION ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
API_KEY = os.environ.get("KYBERNETES_API_KEY", "kybernetes_secret_bridge_01")

# Twilio Config
TWILIO_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER") # e.g. 'whatsapp:+14155238886'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
twilio_client = TwilioClient(TWILIO_SID, TWILIO_TOKEN) if TWILIO_SID else None

class ResultData(BaseModel):
    command_id: str
    output: str

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
    
    result = supabase.table("commands") \
        .select("*") \
        .eq("status", "pending") \
        .order("created_at", desc=False) \
        .limit(1) \
        .execute()
    
    if not result.data:
        return {"command": None}
    
    cmd = result.data[0]
    supabase.table("commands").update({"status": "processing"}).eq("id", cmd["id"]).execute()
    
    return {"command": {"id": str(cmd["id"]), "prompt": cmd["prompt"]}}

@app.post("/result")
async def post_result(result: ResultData, key: str):
    if key != API_KEY: raise HTTPException(status_code=403)
    
    # 1. Update DB
    db_res = supabase.table("commands").update({
        "status": "completed",
        "result": result.output
    }).eq("id", result.command_id).execute()
    
    if not db_res.data:
        return {"status": "error", "detail": "Command not found"}

    cmd_data = db_res.data[0]
    recipient = cmd_data["sender"]

    # 2. Reply to WhatsApp via Twilio
    if twilio_client and TWILIO_NUMBER:
        try:
            # We split the output if it's too long for a single WhatsApp message (1600 chars)
            message_body = result.output[:1500] 
            twilio_client.messages.create(
                body=message_body,
                from_=TWILIO_NUMBER,
                to=recipient
            )
        except Exception as e:
            print(f"Twilio Error: {e}")
    
    return {"status": "success"}

handler = Mangum(app)
