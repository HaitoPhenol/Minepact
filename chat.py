import json
import requests
import time
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

def call_api(model_name, verbose=True):
    """Send request to API with specified model
    
    Returns:
        tuple: (result, response_time) where result is the API response or None,
               and response_time is the elapsed time in seconds
    """
    payload = base_payload.copy()
    payload["model"] = model_name
    
    start_time = time.time()
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_time = time.time() - start_time
        return response.json(), response_time
    except requests.exceptions.HTTPError as e:
        response_time = time.time() - start_time
        status_code = e.response.status_code
        error_info = ERROR_CODES.get(status_code, {"title": "Unknown Error", "description": "Unknown error type"})
        if verbose:
            print(f"❌ [{model_name}] HTTP Error {status_code}: {error_info['title']}")
            print(f"   {error_info['description']}")
            print(f"   Response time: {response_time:.2f}s")
        return None, response_time
    except requests.exceptions.RequestException as e:
        response_time = time.time() - start_time
        if verbose:
            print(f"❌ [{model_name}] Request failed: {e}")
            print(f"   Response time: {response_time:.2f}s")
        return None, response_time


def stress_test(max_consecutive_failures=3, delay=1):
    """
    Stress test function: continuously send requests until max_consecutive_failures reached.
    Statistics: model usage, token consumption per model, total tokens.
    
    Args:
        max_consecutive_failures: Stop after this many consecutive failures (default: 3)
        delay: Seconds to wait between requests (default: 1)
    """
    print("\n🚀 Starting stress test...")
    print(f"   Max consecutive failures: {max_consecutive_failures}")
    print(f"   Delay between requests: {delay}s\n")
    
    # Statistics tracking
    stats = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "consecutive_failures": 0,
        "model_tokens": {},  # {model_name: {prompt_tokens, completion_tokens, total_tokens}}
        "model_requests": {},  # {model_name: count}
        "model_response_times": {},  # {model_name: [response_times]}
        "total_prompt_tokens": 0,
        "total_completion_tokens": 0,
        "total_tokens": 0,
        "total_response_time": 0.0,
        "min_response_time": float('inf'),
        "max_response_time": 0.0
    }
    
    request_count = 0
    
    while stats["consecutive_failures"] < max_consecutive_failures:
        request_count += 1
        print(f"\n--- Request #{request_count} ---")
        
        result = None
        used_model = None
        
        # Try models in order
        for i, model in enumerate(MODEL_LIST):
            result, response_time = call_api(model, verbose=True)
            if result is not None:
                used_model = model
                stats["consecutive_failures"] = 0  # Reset failure counter
                break
            
            if i < len(MODEL_LIST) - 1:
                print(f"🔄 Retrying with next model: {MODEL_LIST[i+1]}")
        
        if result is not None:
            # Update success statistics
            stats["total_requests"] += 1
            stats["successful_requests"] += 1
            
            model_name = result.get("model", used_model)
            prompt_tokens = result.get("usage", {}).get("prompt_tokens", 0)
            completion_tokens = result.get("usage", {}).get("completion_tokens", 0)
            total_tokens = result.get("usage", {}).get("total_tokens", 0)
            
            # Initialize model stats if not exists
            if model_name not in stats["model_tokens"]:
                stats["model_tokens"][model_name] = {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
                stats["model_requests"][model_name] = 0
            
            # Update model stats
            stats["model_tokens"][model_name]["prompt_tokens"] += prompt_tokens
            stats["model_tokens"][model_name]["completion_tokens"] += completion_tokens
            stats["model_tokens"][model_name]["total_tokens"] += total_tokens
            stats["model_requests"][model_name] += 1
            
            # Update total stats
            stats["total_prompt_tokens"] += prompt_tokens
            stats["total_completion_tokens"] += completion_tokens
            stats["total_tokens"] += total_tokens
            
            # Update response time stats
            stats["total_response_time"] += response_time
            stats["min_response_time"] = min(stats["min_response_time"], response_time)
            stats["max_response_time"] = max(stats["max_response_time"], response_time)
            
            # Update model response times
            if model_name not in stats["model_response_times"]:
                stats["model_response_times"][model_name] = []
            stats["model_response_times"][model_name].append(response_time)
            
            # Print brief result
            response_content = result["choices"][0]["message"]["content"]
            print(f"✅ [{model_name}] Success - {len(response_content)} chars, {total_tokens} tokens, {response_time:.2f}s")
            
        else:
            # Update failure statistics
            stats["total_requests"] += 1
            stats["failed_requests"] += 1
            stats["consecutive_failures"] += 1
            print(f"❌ All models failed. Consecutive failures: {stats['consecutive_failures']}/{max_consecutive_failures}")
        
        # Add delay between requests
        if stats["consecutive_failures"] < max_consecutive_failures:
            time.sleep(delay)
    
    # Print final statistics
    print("\n" + "="*60)
    print("📊 Stress Test Results")
    print("="*60)
    print(f"Total requests: {stats['total_requests']}")
    print(f"Successful requests: {stats['successful_requests']}")
    print(f"Failed requests: {stats['failed_requests']}")
    print(f"Success rate: {stats['successful_requests']/stats['total_requests']*100:.1f}%")
    print(f"\n--- Response Time Statistics ---")
    avg_response_time = stats["total_response_time"] / stats["successful_requests"] if stats["successful_requests"] > 0 else 0
    print(f"  Total response time: {stats['total_response_time']:.2f}s")
    print(f"  Average response time: {avg_response_time:.2f}s")
    print(f"  Min response time: {stats['min_response_time']:.2f}s")
    print(f"  Max response time: {stats['max_response_time']:.2f}s")
    print("\n--- Token Usage by Model ---")
    for model_name, tokens in stats["model_tokens"].items():
        print(f"  {model_name}:")
        print(f"    Requests: {stats['model_requests'][model_name]}")
        print(f"    Prompt tokens: {tokens['prompt_tokens']}")
        print(f"    Completion tokens: {tokens['completion_tokens']}")
        print(f"    Total tokens: {tokens['total_tokens']}")
        # Model response time stats
        times = stats["model_response_times"].get(model_name, [])
        if times:
            avg_time = sum(times) / len(times)
            print(f"    Avg response time: {avg_time:.2f}s")
    print("\n--- Total Token Usage ---")
    print(f"  Prompt tokens: {stats['total_prompt_tokens']}")
    print(f"  Completion tokens: {stats['total_completion_tokens']}")
    print(f"  Total tokens: {stats['total_tokens']}")
    print("="*60)
    
    return stats

# ==================== Main logic ====================

def single_chat_request(user_input=None):
    """
    Perform a single chat request, trying models in order from MODEL_LIST.
    
    Args:
        user_input (str, optional): User input message. If None, prompts user for input.
    
    Returns:
        dict or None: The API response if successful, None otherwise
    """
    # Get user input from keyboard if not provided
    if user_input is None:
        user_input = input("请输入消息: ")
    
    # Update the user message in base_payload
    base_payload["messages"][1]["content"] = user_input
    
    # Normal single request mode
    result = None
    used_model = None

    # Try models in order from MODEL_LIST
    response_time = 0.0
    for i, model in enumerate(MODEL_LIST):
        result, resp_time = call_api(model)
        response_time += resp_time  # Accumulate response time across retries
        if result is not None:
            used_model = model
            break
        
        # If not the last model, print retry message
        if i < len(MODEL_LIST) - 1:
            print(f"\n🔄 Retrying with next model: {MODEL_LIST[i+1]}")

    # If all models failed, exit
    if result is None:
        print("\n❌ All models failed. Exiting.")
        return None
    else:
        # Output response and total tokens
        response_content = result["choices"][0]["message"]["content"]
        finish_reason = result["choices"][0].get("finish_reason", "unknown")
        model_name = result.get("model", used_model)  # Get model name from returned JSON
        total_tokens = result.get("usage", {}).get("total_tokens", 0)
        prompt_tokens = result.get("usage", {}).get("prompt_tokens", 0)
        completion_tokens = result.get("usage", {}).get("completion_tokens", 0)
        
        print(f"\n======================= response [{model_name}] =======================\n\n", response_content)
        
        print("\n================== result information ==================")
        print(f"  model = {model_name}")
        print(f"  finish_reason = {finish_reason}")
        print(f"  response_time = {response_time:.2f}s")
        print(f"  input_tokens = {prompt_tokens} | output_tokens = {completion_tokens}")
        print(f"> total_tokens = {total_tokens} <")
        print("========================================================")
        return result


# Uncomment the line below to run single chat request directly
# single_chat_request()

# Uncomment the line below to run stress test
# stress_test(max_consecutive_failures=3, delay=1)