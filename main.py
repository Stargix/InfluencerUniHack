import sqlite3
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv
import os
import json
import requests
from typing import Dict, Any
from datetime import datetime
import database as db
import Classifier as ai

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Get configuration from environment variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GRAPH_ACCESS_TOKEN = os.getenv("GRAPH_ACCESS_TOKEN")
INSTAGRAM_GRAPH_URL = "https://graph.facebook.com/v21.0"

# Dictionary to track users who need to input their name
users_needing_name = {}

# Function to send message to a user
# Webhook verification endpoint
@app.get("/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return int(challenge)  # Return challenge token to verify webhook
        raise HTTPException(status_code=403, detail="Verification failed")
    raise HTTPException(status_code=400, detail="Missing parameters")

def get_all_messages():
    """Retrieve all messages from the 'business_prop' table in SQLite."""
    try:
        con = sqlite3.connect("jobOffers.db")
        cur = con.cursor()
        cur.execute("SELECT message_id, user_id, message FROM business_prop")
        rows = cur.fetchall()
        return [{"message_id": row[0], "user_id": row[1], "message": row[2]} for row in rows]
    finally:
        con.close()

@app.get("/messages")
async def read_messages():
    """API endpoint to retrieve all messages."""
    return get_all_messages()

# Webhook handler endpoint
@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print("Received JSON payload:", json.dumps(body, indent=2))

    db_to_create = True
    if db_to_create:
        db.generate_database()

    # Verify the webhook is from Instagram
    if body.get("object") != "instagram":
        raise HTTPException(status_code=404, detail="Not an Instagram event")

    try:
        # Extract message details
        entry = body.get("entry", [{}])[0]
        messaging = entry.get("messaging", [{}])[0]
        
        sender_id = messaging.get("sender", {}).get("id")
        recipient_id = messaging.get("recipient", {}).get("id")
        message = messaging.get("message", {})
        message_text = message.get("text", "")
        message_id = message.get("mid")

        # Validate message content
        if not sender_id or not message_text:
            return {"status": "no_valid_message"}
        
        print(f"Received message from {sender_id}: {message_text}")

        # Classify message
        is_business = ai.is_business_proposal(message_text)

        # Log the interaction
        print(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "sender_id": sender_id,
            "message_text": message_text,
            "is_business": is_business,
        }, indent=2))

        # Send reply

        # Store the message if it's a business proposal
        if is_business:
            db.insert_message(sender_id, message_text)
        db.print_database_contents()

        return {"status": "success", "is_business": is_business}

    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))




# class InstagramAPI:
#     """Class to handle Instagram API interactions"""
#     def __init__(self, access_token: str):
#         self.access_token = access_token
#         self.base_url = "https://graph.facebook.com/LATEST-API-VERSION"
#         self.max_message_length = 1000  # Instagram's message length limit

#     def send_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
#         """
#         Send a message to a user via Instagram API
#         Args:
#             recipient_id: The Instagram user ID to send message to
#             message_text: The message content
#         Returns:
#             Dict containing API response
#         """
#         # Truncate message if it exceeds maximum length
#         if len(message_text) > self.max_message_length:
#             message_text = message_text[:self.max_message_length]

#         endpoint = f"{self.base_url}/me/messages"
#         data = {
#             "recipient": {"id": recipient_id},
#             "message": {"text": message_text}
#         }
        
#         params = {"access_token": self.access_token}
#         response = requests.post(endpoint, json=data, params=params)
#         return response.json()

#     def send_reaction(self, recipient_id: str, message_id: str, reaction: str = "love") -> Dict[str, Any]:
#         """
#         Send a reaction to a message
#         Args:
#             recipient_id: The Instagram user ID
#             message_id: The ID of the message to react to
#             reaction: The type of reaction (default: "love")
#         Returns:
#             Dict containing API response
#         """
#         endpoint = f"{self.base_url}/me/messages"
#         data = {
#             "recipient": {"id": recipient_id},
#             "sender_action": "react",
#             "payload": {
#                 "message_id": message_id,
#                 "reaction": reaction
#             }
#         }
        
#         params = {"access_token": self.access_token}
#         response = requests.post(endpoint, json=data, params=params)
#         return response.json()

# class ResponseGenerator:
#     """Class to generate appropriate responses based on message type"""
#     def get_business_response(self) -> str:
#         """Generate response for business-related inquiries"""
#         return (
#             "Thank you for your business inquiry! I'll review your message and get back to you "
#             "within 24 hours. To help me assist you better, could you please provide:\n"
#             "1. Your preferred timeline\n"
#             "2. Project scope/requirements\n"
#             "3. Budget range (if applicable)"
#         )

#     def get_regular_response(self) -> str:
#         """Generate response for non-business messages"""
#         return "Thanks for your message! I'll get back to you soon. 👋"