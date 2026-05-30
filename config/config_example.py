# Add your API key and other configurations here
API_KEY = "your-api-key-here" 
BASE_URL = "https://www.xxx.cn/v1/chat/completions"  # endpoint

# Model list for fallback mechanism (tried in order)
MODEL_LIST = [
    "your-primary-model",     # Primary model
    "your-secondary-model",   # Secondary model
    "your-additional-model",  # Additional model
]

# Error code explanations for API responses
ERROR_CODES = {
    400: {
        "title": "Bad Request",
        "description": "Check request parameters. For example, o1 series models do not support system parameter."
    },
    401: {
        "title": "Unauthorized",
        "description": "Check if API key is correct. Try switching models to verify."
    },
    403: {
        "title": "Forbidden",
        "description": "Token group is disabled. Edit token to remove limit or create new token."
    },
    404: {
        "title": "Not Found",
        "description": "Check if Base URL is correct. Try adding /v1 or trailing slash."
    },
    413: {
        "title": "Request Too Large",
        "description": "Shorten the prompt content and retry."
    },
    429: {
        "title": "Rate Limited",
        "description": "Account is overloaded. Please retry later."
    },
    500: {
        "title": "Internal Server Error",
        "description": "If problem persists after multiple retries, please contact administrator."
    },
    503: {
        "title": "Service Unavailable",
        "description": "Current group has no channel for this model. Check model name for typos or extra spaces."
    },
    504: {
        "title": "Gateway Timeout",
        "description": "Upstream server did not respond in time. Please retry later."
    },
    524: {
        "title": "Connection Timeout",
        "description": "Channel is congested. Please wait and retry."
    }
}