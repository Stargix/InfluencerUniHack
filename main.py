
    # Import necessary libraries
from fastapi import FastAPI, Request, HTTPException  # Framework for building APIs
from dotenv import load_dotenv  # For loading environment variables
import os  # For accessing environment variables
import json  # For JSON operations
import requests  # For making HTTP requests
from typing import Dict, Any  # For type hints
from datetime import datetime  # For timestamp generation
import database as db

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Get configuration from environment variables
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")  # Token for webhook verification
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")  # Token for Instagram API access
INSTAGRAM_GRAPH_URL = "https://graph.facebook.com/v13.0"  # Base URL for Instagram Graph API

class MessageClassifier:
    """Class to classify incoming messages as business or non-business related"""
    def __init__(self):
        # Define keywords that indicate a business-related message
        self.business_keywords = {
            'price', 'cost', 'quote', 'service', 'business', 'project',
            'work', 'hire', 'contract', 'consultation', 'interested',
            'budget', 'proposal', 'inquiry', 'commission'
        }

    def is_business_opportunity(self, message: str) -> bool:
        """
        Check if message contains business-related keywords
        Args:
            message: The input message text
        Returns:
            bool: True if message contains business keywords, False otherwise
        """
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.business_keywords)

class InstagramAPI:
    """Class to handle Instagram API interactions"""
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://graph.facebook.com/LATEST-API-VERSION"
        self.max_message_length = 1000  # Instagram's message length limit

    def send_message(self, recipient_id: str, message_text: str) -> Dict[str, Any]:
        """
        Send a message to a user via Instagram API
        Args:
            recipient_id: The Instagram user ID to send message to
            message_text: The message content
        Returns:
            Dict containing API response
        """
        # Truncate message if it exceeds maximum length
        if len(message_text) > self.max_message_length:
            message_text = message_text[:self.max_message_length]

        endpoint = f"{self.base_url}/me/messages"
        data = {
            "recipient": {"id": recipient_id},
            "message": {"text": message_text}
        }
        
        params = {"access_token": self.access_token}
        response = requests.post(endpoint, json=data, params=params)
        return response.json()

    def send_reaction(self, recipient_id: str, message_id: str, reaction: str = "love") -> Dict[str, Any]:
        """
        Send a reaction to a message
        Args:
            recipient_id: The Instagram user ID
            message_id: The ID of the message to react to
            reaction: The type of reaction (default: "love")
        Returns:
            Dict containing API response
        """
        endpoint = f"{self.base_url}/me/messages"
        data = {
            "recipient": {"id": recipient_id},
            "sender_action": "react",
            "payload": {
                "message_id": message_id,
                "reaction": reaction
            }
        }
        
        params = {"access_token": self.access_token}
        response = requests.post(endpoint, json=data, params=params)
        return response.json()

class ResponseGenerator:
    """Class to generate appropriate responses based on message type"""
    def get_business_response(self) -> str:
        """Generate response for business-related inquiries"""
        return (
            "Thank you for your business inquiry! I'll review your message and get back to you "
            "within 24 hours. To help me assist you better, could you please provide:\n"
            "1. Your preferred timeline\n"
            "2. Project scope/requirements\n"
            "3. Budget range (if applicable)"
        )

    def get_regular_response(self) -> str:
        """Generate response for non-business messages"""
        return "Thanks for your message! I'll get back to you soon. 👋"

# Initialize necessary components
classifier = MessageClassifier()
instagram_api = InstagramAPI(PAGE_ACCESS_TOKEN)
response_generator = ResponseGenerator()

@app.get("/webhook")
async def verify_webhook(request: Request):
    """
    Handle webhook verification from Instagram
    Instagram sends a GET request with a challenge that must be echoed back
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return int(challenge)  # Return challenge token to verify webhook
        raise HTTPException(status_code=403, detail="Verification failed")
    raise HTTPException(status_code=400, detail="Missing parameters")

@app.post("/webhook")
async def webhook(request: Request):
    """
    Handle incoming webhook events from Instagram
    Process incoming messages and send appropriate responses
    """
    body = await request.json()
    db_to_create = True

    if db_to_create:
        db.generate_database()
        db_created = True

    # Verify the webhook is from Instagram
    if body.get("object") != "instagram":
        raise HTTPException(status_code=404, detail="Not an Instagram event")

    try:
        # Extract message details from the webhook payload
        entry = body.get("entry", [{}])[0]
        messaging = entry.get("messaging", [{}])[0]
        
        sender_id = messaging.get("sender", {}).get("id")
        message = messaging.get("message", {})
        message_text = message.get("text", "")
        message_id = message.get("mid")

        # Validate message content
        if not sender_id or not message_text:
            return {"status": "no_valid_message"}
        
        print(f"Received message from {sender_id}: {message_text}")

        # Classify message and generate appropriate response
        is_business = classifier.is_business_opportunity(message_text)
        # response_text = (response_generator.get_business_response() 
        #                 if is_business 
        #                 else response_generator.get_regular_response())

        # Send response back to user
        # response = instagram_api.send_message(sender_id, response_text)
        
        # Add a reaction to the original message
        instagram_api.send_reaction(sender_id, message_id)

        # Log the interaction for monitoring
        print(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "sender_id": sender_id,
            "message_text": message_text,
            "is_business": is_business,
            # "response": response_text,
            # "api_response": response
        }, indent=2))

        if is_business:
            db.insert_message(sender_id, message_text)
        db.print_database_contents()

        print(f"Processed message from {sender_id}")
        return {"status": "success", "is_business": is_business}

    except Exception as e:
        # Log any errors and return 500 status code
        print(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
