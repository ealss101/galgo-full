import requests

API_URL = "http://127.0.0.1:8000/user"  # ✅ Use `/user` prefix

def fetch_admin_status(email):
    """Fetch admin status from FastAPI."""
    try:
        response = requests.get(f"{API_URL}/admin_status", params={"email": email})  # ✅ Use `params`
        if response.status_code == 200:
            return response.json().get("is_admin", False)
    except requests.RequestException:
        return False
    return False

def fetch_allowed_chatbots(email):
    """Fetch allowed chatbots from FastAPI."""
    try:
        response = requests.get(f"{API_URL}/chatbots", params={"email": email})  # ✅ Use `params`
        if response.status_code == 200:
            return response.json().get("chatbots", [])
    except requests.RequestException:
        return []
    return []
