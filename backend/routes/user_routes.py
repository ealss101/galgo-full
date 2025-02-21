from fastapi import APIRouter, HTTPException
from backend.services.user_service import get_allowed_chatbots, get_admin_status

router = APIRouter()

@router.get("/admin_status")
def fetch_admin_status(email: str):
    is_admin, error = get_admin_status(email)
    if error:
        return {"error": error}
    return {"is_admin": is_admin}

@router.get("/chatbots")
def fetch_chatbots(email: str):
    """Fetch allowed chatbots for a user."""
    chatbots, error = get_allowed_chatbots(email)
    if error:
        raise HTTPException(status_code=500, detail=error)
    return {"chatbots": chatbots}
