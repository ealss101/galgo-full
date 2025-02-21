import requests

API_URL = "http://127.0.0.1:8000/admin"

def approve_users(user_ids):
    """Send approval request to FastAPI."""
    try:
        response = requests.post(f"{API_URL}/approve_users", json={"user_ids": user_ids})
        return response.status_code == 200
    except requests.RequestException:
        return False

def delete_users(user_ids):
    """Send delete request to FastAPI."""
    try:
        response = requests.post(f"{API_URL}/delete_users", json={"user_ids": user_ids})
        return response.status_code == 200
    except requests.RequestException:
        return False

def update_user_chatbots(email, chatbots):
    """Update chatbot access via FastAPI."""
    try:
        response = requests.post(f"{API_URL}/update_chatbots", json={"email": email, "chatbots": chatbots})
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_pending_users():
    """Fetch all pending users from the backend."""
    try:
        response = requests.get(f"{API_URL}/pending_users")
        print("DEBUG: API Response -", response.text)

        if response.status_code == 200:
            return response.json()

    except requests.RequestException as err:
        print(f"ERROR: {err}")

    return {"users": []}

def get_all_users():
    """Fetch all users from the backend."""
    try:
        response = requests.get(f"{API_URL}/all_users")
        print("DEBUG: API Response -", response.text)

        if response.status_code == 200:
            data = response.json()

            if isinstance(data, dict) and "users" in data:
                return data["users"]
            elif isinstance(data, list):
                return data  

    except requests.RequestException as err:
        print(f"ERROR: {err}")

    return []
