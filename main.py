from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = FastAPI()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # Verify token from .env

@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)  # Respond with the challenge token from Instagram
    else:
        raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def receive_update(request: Request):
    body = await request.json()

    # Process the incoming message
    if body.get("object") == "instagram":
        print("Received Instagram event:", body)
        return {"status": "received"}
    else:
        raise HTTPException(status_code=404, detail="Not an Instagram event")