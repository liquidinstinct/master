import os
from dotenv import load_dotenv

def setup_environment():
    # Load environment variables from the .env file
    env_loaded = load_dotenv()
    
    if not env_loaded:
        print("Error: .env file not found or failed to load.")
        return

    # Fetch the API key from the environment
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        print("Error: OPENAI_API_KEY is not set in the .env file.")
        return

    print("Environment variables loaded successfully.")
    print("OPENAI_API_KEY is set and ready to use.")

if __name__ == "__main__":
    setup_environment()
