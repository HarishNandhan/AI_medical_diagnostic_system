
import os
from dotenv import load_dotenv
from euriai import EuriaiClient

# Load environment variables from .env file
load_dotenv()

# Initialize the EuriAI client
client = EuriaiClient(
    api_key=os.getenv("EURI_API_KEY"),
    model=os.getenv("EURI_DEFAULT_MODEL", "gpt-4.1-nano")
)

def generate_completion(messages, model=None, temperature=0.7, max_tokens=1000):
    """
    Generate completion using EuriAI client.
    
    Args:
        messages: List of message dictionaries or a single prompt string
        model: Model to use (optional, uses client default if not specified)
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens to generate
    
    Returns:
        Generated text response
    """
    # Handle both message format and simple prompt
    if isinstance(messages, str):
        prompt = messages
    elif isinstance(messages, list) and len(messages) > 0:
        # Extract the last user message as prompt
        prompt = messages[-1].get('content', '') if isinstance(messages[-1], dict) else str(messages[-1])
    else:
        raise ValueError("Messages must be a string or list of message dictionaries")
    
    # Use the specified model or fall back to client default
    if model:
        # Create a new client instance with the specified model
        temp_client = EuriaiClient(
            api_key=os.getenv("EURI_API_KEY"),
            model=model
        )
        return temp_client.generate_completion(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )
    else:
        return client.generate_completion(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens
        )

def generate_embedding(text):
    """
    Generate embeddings for the given text using EuriAI.
    
    Args:
        text: Text to embed
    
    Returns:
        Embedding vector
    """
    from euriai.embedding import EuriaiEmbeddingClient
    
    embedding_client = EuriaiEmbeddingClient(api_key=os.getenv("EURI_API_KEY"))
    return embedding_client.embed(text)