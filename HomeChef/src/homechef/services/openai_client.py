import os
from openai import OpenAI  # We can still use the OpenAI library
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

# --- THIS IS THE CRITICAL CHANGE FOR GROQ ---
# 1. Initialize the client with the Groq API key and server URL.
# 2. Make sure your .env file has GROQ_API_KEY="gsk_..."
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

def chat_reply(system_prompt: str, user_prompt: str):
    """
    Sends a request to the Groq Chat API and gets a response.
    """
    if not client.api_key:
        return "ERROR: GROQ_API_KEY environment variable not set. Please update your .env file."

    try:
        print("Sending request to Groq API...")
        
        # This is the API call to the Groq model
        completion = client.chat.completions.create(
            # 3. Use a Groq model name. 'llama3-8b-8192' is a great, fast choice.
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            # 4. We still keep max_tokens to ensure full, untruncated recipes.
            max_tokens=2000, # Increased for potentially longer Groq responses
            temperature=0.7,
        )
        
        print("Response received from Groq API.")
        return completion.choices[0].message.content.strip()

    except Exception as e:
        print(f"An error occurred with the Groq API: {e}")
        # Return a user-friendly error message to the app window
        return f"Sorry, an error occurred while contacting the AI service.\n\nDetails: {e}"