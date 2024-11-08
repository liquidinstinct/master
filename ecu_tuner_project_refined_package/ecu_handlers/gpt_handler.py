import openai
import os
import logging
from dotenv import load_dotenv

# Load environment variables from a .env file (if not already loaded)
load_dotenv()

# Fetch OpenAI API key from environment variables for security
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure logging is set up for error tracking
logging.basicConfig(level=logging.INFO)

def analyze_fault_codes_with_gpt(codes):
    """
    Analyze vehicle fault codes using GPT-4 and return detailed recommendations.
    
    Parameters:
    - codes: str, comma-separated fault codes (e.g., "P0171, P0301")
    
    Returns:
    - analysis: str, GPT-generated analysis and recommendations for the fault codes.
    """
    if not openai.api_key:
        logging.error("OpenAI API key is not set. Please configure the API key in your environment.")
        return "API key error: Unable to connect to OpenAI."

    prompt = (
        f"You are an automotive diagnostic expert. Please analyze the following vehicle fault codes: {codes}. "
        "For each code, provide a detailed explanation including potential causes, suggested solutions, and any "
        "recommended troubleshooting steps. Indicate if any code is unrecognized and suggest a general diagnostic approach."
    )

    try:
        # Communicate with OpenAI API using the ChatCompletion endpoint for compatibility with GPT-4 models
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an automotive diagnostic expert."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.5
        )
        
        # Extract the analysis text from the response
        analysis = response.choices[0].message['content'].strip()
        logging.info("GPT-4 analysis completed successfully.")
        return analysis
    
    except openai.error.OpenAIError as api_error:
        logging.error(f"OpenAI API error: {api_error}")
        return "An error occurred while generating GPT analysis. Please try again later."
    
    except Exception as e:
        logging.error(f"Unexpected error during GPT-4 analysis: {e}")
        return "An unexpected error occurred. Please check the system logs for details."
