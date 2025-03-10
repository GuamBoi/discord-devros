import aiohttp
import os
import logging
import requests

# Function to query OpenWebUI API
def query_openwebui(prompt):
    """Send the prompt to the OpenWebUI API and return the response."""
    # Fetching the OpenWebUI API URL and API key from environment variables
    api_url = os.getenv('OPENWEBUI_API_URL', 'http://localhost:5000/v1/query')  # Default URL if not provided
    api_key = os.getenv('OPENWEBUI_API_KEY', 'your_api_key_here')  # Default API key if not provided

    headers = {
        'Authorization': f'Bearer {api_key}',  # Authorization header
        'Content-Type': 'application/json',  # Content type as JSON
    }

    # Prepare the request payload
    payload = {
        "prompt": prompt,
        "max_tokens": 100,  # Adjust based on your needs
        "temperature": 0.7  # Adjust based on your needs
    }

    try:
        # Sending the POST request to the OpenWebUI API
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        return response.json()  # Return the response as JSON
    except requests.exceptions.RequestException as e:
        print(f"Error querying OpenWebUI: {e}")
        return {"error": "Failed to query the OpenWebUI API."}
