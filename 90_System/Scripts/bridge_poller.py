import requests
import subprocess
import time
import json
import os

# --- ⚙️ CONFIGURATION ---
# Replace with your Vercel URL (e.g. https://kybernetes-relay.vercel.app)
RELAY_URL = "https://kybernetes.vercel.app"  
API_KEY = "kybernetes_secret_bridge_01" 
POLL_INTERVAL = 5 # Seconds

def execute_gemini(prompt):
    """Executes the Gemini CLI in headless mode."""
    print(f"🚀 Executing: {prompt}")
    
    # We use -y for YOLO mode (auto-approve) and --output-format json for parsing
    cmd = [
        "gemini", 
        "--prompt", prompt, 
        "-y", 
        "--output-format", "json"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            return f"❌ Error executing Gemini: {result.stderr}"
            
        # Parse the JSON output to extract the text response
        data = json.loads(result.stdout)
        # The CLI response structure usually contains the text in the last message
        return data.get("text", "No text response received.")
        
    except Exception as e:
        return f"❌ Bridge Exception: {str(e)}"

def main():
    print("🛰️ Kybernetes Bridge Poller Active...")
    print(f"Polling {RELAY_URL} every {POLL_INTERVAL}s")

    while True:
        try:
            response = requests.get(f"{RELAY_URL}/poll", params={"key": API_KEY})
            if response.status_code == 200:
                data = response.json()
                command = data.get("command")
                
                if command:
                    cmd_id = command["id"]
                    prompt = command["prompt"]
                    
                    # Execute locally
                    output = execute_gemini(prompt)
                    
                    # Send result back
                    requests.post(
                        f"{RELAY_URL}/result", 
                        params={"key": API_KEY},
                        json={"command_id": cmd_id, "output": output}
                    )
                    print(f"✅ Handled Command {cmd_id}")
                
            else:
                print(f"⚠️ Poll failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Poller Error: {e}")
            
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
