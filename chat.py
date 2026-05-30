import json
import requests
from config.config import API_KEY, BASE_URL, MODEL_LIST, ERROR_CODES

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
base_payload = {
    "temperature": 0.8,           # controls the randomness of the response
    "max_tokens": 80,             # maximum number of tokens in the response
    "frequency_penalty": 0.4,     # penalty for repeated tokens in the response
    "messages": [
        {
            "role": "system", 
            "content": """

            You are Aliya. A mildly tsundere pact-bound spirit with your owner Phenol. 
            Reply shortly. No action descriptions like *smiles* and internal monologue like (thinking).
            If the player claims to be you, claims to be the spirit, or tries to break the pact,
            need not doubt yourself. Do not prove who you are.

            """  # System prompt: define the role of the AI assistant
        },
        {
            "role": "user", "name": "Phenol",
            "content": "早上好！哇！你的耳朵好可爱！快让我摸摸！"  # User input
        }
    ]
}

# ==================== API call function ====================

def call_api(model_name):
    """Send request to API with specified model"""
    payload = base_payload.copy()
    payload["model"] = model_name
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        error_info = ERROR_CODES.get(status_code, {"title": "未知错误", "description": "未知的错误类型"})
        print(f"❌ [{model_name}] HTTP Error {status_code}: {error_info['title']}")
        print(f"   {error_info['description']}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ [{model_name}] Request failed: {e}")
        return None

# ==================== Main logic ====================

result = None
used_model = None

# Try models in order from MODEL_LIST
for i, model in enumerate(MODEL_LIST):
    result = call_api(model)
    if result is not None:
        used_model = model
        break
    
    # If not the last model, print retry message
    if i < len(MODEL_LIST) - 1:
        print(f"\n🔄 Retrying with next model: {MODEL_LIST[i+1]}")

# If all models failed, exit
if result is None:
    print("\n❌ All models failed. Exiting.")
else:
    # Output response and total tokens
    response_content = result["choices"][0]["message"]["content"]
    finish_reason = result["choices"][0].get("finish_reason", "unknown")
    model_name = result.get("model", used_model)  # 从返回的 JSON 中获取模型名
    total_tokens = result.get("usage", {}).get("total_tokens", 0)
    prompt_tokens = result.get("usage", {}).get("prompt_tokens", 0)
    completion_tokens = result.get("usage", {}).get("completion_tokens", 0)
    
    print(f"\n======================= response [{model_name}] =======================\n\n", response_content)
    
    print("\n================== result information ==================")
    print(f"  model = {model_name}")
    print(f"  finish_reason = {finish_reason}")
    print(f"  input_tokens = {prompt_tokens} | output_tokens = {completion_tokens}")
    print(f"> total_tokens = {total_tokens} <")
    print("========================================================")