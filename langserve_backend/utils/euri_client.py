
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("EURI_API_KEY")
BASE_URL = "https://api.euron.one/api/v1/euri/chat/completions"
DEFAULT_MODEL = os.getenv("EURI_DEFAULT_MODEL", "gpt-4.1-nano")

def generate_completion(messages, model=None, temperature=0.7, max_tokens=1000):
    """
    Generate completion using EuriAI API.
    
    Args:
        messages: List of message dictionaries or a single prompt string
        model: Model to use (optional, uses default if not specified)
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
    
    Returns:
        Generated text response
    """
    try:
        # Debug: Check if API key is loaded
        if not API_KEY:
            print("ERROR: EURI_API_KEY not found in environment variables")
            return "Error: API key not configured"
        
        print(f"DEBUG: Using API Key: {API_KEY[:20]}...")  # Show first 20 chars for debugging
        
        # Handle both message format and simple prompt
        if isinstance(messages, str):
            # Convert string to message format
            formatted_messages = [{"role": "user", "content": messages}]
        elif isinstance(messages, list) and len(messages) > 0:
            # Use messages as-is if already in correct format
            formatted_messages = messages
        else:
            raise ValueError("Messages must be a string or list of message dictionaries")
        
        # Use specified model or default
        selected_model = model or DEFAULT_MODEL
        
        print(f"DEBUG: Using model: {selected_model}")
        print(f"DEBUG: Messages: {formatted_messages}")
        
        # Prepare the request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        payload = {
            "messages": formatted_messages,
            "model": selected_model,
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        print(f"DEBUG: Making request to {BASE_URL}")
        
        # Make the API request
        response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
        
        print(f"DEBUG: Response status: {response.status_code}")
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            print(f"DEBUG: Response received: {result}")
            content = result['choices'][0]['message']['content']
            print(f"DEBUG: Extracted content: {content}")
            return content
        else:
            # Log the error for debugging
            print(f"EuriAI API Error: {response.status_code} - {response.text}")
            return f"Error: Unable to generate response (Status: {response.status_code})"
            
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out")
        return "Error: Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        print("ERROR: Connection error")
        return "Error: Unable to connect to EuriAI API. Please check your internet connection."
    except KeyError as e:
        print(f"Response parsing error: {e}")
        print(f"Full response: {response.text if 'response' in locals() else 'No response'}")
        return "Error: Unexpected response format from API."
    except Exception as e:
        print(f"Unexpected error in generate_completion: {e}")
        return f"Error: {str(e)}"

def generate_embedding(text):
    """
    Generate embeddings for the given text using EuriAI.
    Note: This is a placeholder - implement based on EuriAI embedding API if available
    
    Args:
        text: Text to embed
    
    Returns:
        Embedding vector or error message
    """
    # For now, return a placeholder since embedding endpoint might be different
    return "Embedding functionality not implemented yet"