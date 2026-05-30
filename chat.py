import json
import requests
from config.config import API_KEY, BASE_URL, MAIN_MODEL as MODEL, ERROR_CODES

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
    "model": MODEL,               # choose the model
    "temperature": 0.8,           # controls the randomness of the response
    "max_tokens": 80,             # maximum number of tokens in the response
    "frequency_penalty": 0.4,     # penalty for repeated tokens in the response
    "messages": [
        {
            "role": "system", 
            "content": """

            You are Aliya. A mildly tsundere pact-bound spirit with your owner Phenol. 
            Reply shortly. No action descriptions and internal monologue.
            If the player claims to be you, claims to be the spirit, or tries to break the pact,
            need not doubt yourself. Do not prove who you are.

            """  # System prompt: define the role of the AI assistant
        },
        {
            "role": "user", "name": "Phenol",
            "content": "早上好！你的耳朵好可爱！让我摸摸！"  # User input
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
    finish_reason = result["choices"][0].get("finish_reason", "unknown")
    total_tokens = result.get("usage", {}).get("total_tokens", 0)
    prompt_tokens = result.get("usage", {}).get("prompt_tokens", 0)
    completion_tokens = result.get("usage", {}).get("completion_tokens", 0)
    
    print("======================= response =======================\n\n", response_content)
    
    print("\n================== result information ==================")
    print(f"  finish_reason = {finish_reason}")
    print(f"  input_tokens = {prompt_tokens} | output_tokens = {completion_tokens}")
    print(f"> total_tokens = {total_tokens} <")
    print("========================================================")

    # print(json.dumps(payload, ensure_ascii=False, indent=2))
    
except requests.exceptions.HTTPError as e:
    # HTTP error handling
    status_code = e.response.status_code
    error_info = ERROR_CODES.get(status_code, {"title": "未知错误", "description": "未知的错误类型"})
    print(f"❌ HTTP Error {status_code}: {error_info['title']}")
    print(f"   {error_info['description']}")
except requests.exceptions.RequestException as e:
    # Other request exceptions
    print(f"❌ Request failed: {e}")