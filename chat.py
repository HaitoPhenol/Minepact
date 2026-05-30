import json
import requests
from config.config import API_KEY, BASE_URL, MODEL

# ==================== API configuration ====================

# API endpoint
url = BASE_URL

# HTTP headers for the request
headers = {
    "Authorization": API_KEY,  # your API key
    "Content-Type": "application/json"
}

# ==================== request payload ====================

# Construct the request payload for the API call
payload = {
    "model": MODEL,  # choose the model
    "messages": [
        {
            "role": "system", 
            "content": "You are Aliya. A Tsundere elf."  # System prompt: define the role of the AI assistant
        },
        {
            "role": "user", 
            "content": "早上好，今天你的耳朵也很毛茸茸呢！"  # User input
        }
    ]
}

# ==================== API call ====================

try:
    # Send POST request to API
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Check for HTTP errors
    
    # Parse response result
    result = response.json()
    
    # Output response and total tokens
    response_content = result["choices"][0]["message"]["content"]
    total_tokens = result.get("usage", {}).get("total_tokens", 0)
    
    print("================= response =================\n\n", response_content)
    print("\n================= total_tokens = ", total_tokens, "=================")
    
except requests.exceptions.RequestException as e:
    # Exception handling
    print(f"❌ Request failed: {e}")