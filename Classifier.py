from groq import Groq
import os
from dotenv import load_dotenv

def is_business_proposal(mensaje_usuario):
    print("AI working")  # Fixed typo in "working"
    
    # Load environment variables before accessing them
    load_dotenv()
    api_key = os.getenv("LLAMA_API_KEY")
    
    if not api_key:
        raise ValueError("API key not found. Make sure LLAMA_API_KEY is set in the .env file.")
    
    client = Groq(api_key=api_key)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""Given the following Instagram message, classify if it is business-related.
                        A business-related message includes any proposal, collaboration offer, sponsorship,
                        partnership request, or paid opportunity directed to an influencer. If the message is business-related,
                        return simply 'Yes'. If not, simply return 'No'. It is important to return exactly as told. 
                        Here is the message: {mensaje_usuario}"""
                }
            ],
            model="llama3-groq-70b-8192-tool-use-preview",
            temperature=0.5,
            max_tokens=1024,
            stream=False,
        )
        
        response = chat_completion.choices[0].message.content
        print("This is the response:", response)
        
        # Fixed the response checking logic
        if response.strip().lower() == "yes":
            return True
        return False
        
    except Exception as e:
        print(f"Error processing message: {e}")
        return False