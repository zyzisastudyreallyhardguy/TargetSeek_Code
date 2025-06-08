import os

def setup_api_keys():
    """
    Set up required API keys for the application.
    Users should replace the placeholder values with their own API keys.
    """
    # OpenAI API Key
    os.environ["OPENAI_API_KEY"] = "Please replace with your own API key"
    
    # Google Search API Keys
    os.environ["GOOGLE_CSE_ID"] = "Please replace with your own CSE ID"
    os.environ["GOOGLE_API_KEY"] = "Please replace with your own API key"