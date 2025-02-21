import requests

API_URL = "http://127.0.0.1:8000/chat_history"

def fetch_chat_sessions(email, agent):
    """Fetch chat session history from FastAPI."""
    try:
        response = requests.get(f"{API_URL}/sessions", params={"email": email, "agent": agent})
        if response.status_code == 200:
            return response.json().get("sessions", [])
    except requests.RequestException:
        return []
    
    return []

