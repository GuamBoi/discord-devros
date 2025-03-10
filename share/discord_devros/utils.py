import aiohttp
import os
import logging

# Open WebUI API Setup
OPEN_WEBUI_API_URL = os.getenv("OPEN_WEBUI_API_URL")
OPEN_WEBUI_API_KEY = os.getenv("OPEN_WEBUI_API_KEY")
MODEL_NAME = os.getenv("OPEN_WEBUI_MODEL_NAME")

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def query_openwebui(prompt):
    headers = {
        "Authorization": f"Bearer {OPEN_WEBUI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model": MODEL_NAME
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(OPEN_WEBUI_API_URL, json=payload, headers=headers) as response:
                # Log the status code and URL for debugging
                logger.info(f"API response status: {response.status} for {OPEN_WEBUI_API_URL}")
                
                response.raise_for_status()  # Raise error for bad responses
                data = await response.json()
                
                # Log the response for debugging
                logger.debug(f"API response: {data}")
                
                # Handle the API response format
                if "choices" in data and data["choices"]:
                    return data["choices"][0].get("message", {}).get("content", "No response.")
                else:
                    return "Model did not return a valid response."
    except aiohttp.ClientError as e:
        # Log client errors (e.g., network issues)
        logger.error(f"API request error: {e}")
        return "I'm having trouble connecting to the AI service right now."
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error: {e}")
        return "An unexpected error occurred."
