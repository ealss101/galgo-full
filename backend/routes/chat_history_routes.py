from fastapi import APIRouter, HTTPException
from backend.services.chat_history_service import get_chat_sessions, save_chat_session
from pydantic import BaseModel
from typing import List, Dict

# ✅ Define Pydantic Model for Request
class ChatSessionRequest(BaseModel):
    user_id: str
    agent: str
    messages: List[Dict[str, str]]  # List of {role: str, content: str}
router = APIRouter()

@router.get("/sessions")
def fetch_chat_sessions(email: str, agent: str):
    """Fetches chat history for a user & agent."""
    sessions, error = get_chat_sessions(email, agent)
    if error:
        raise HTTPException(status_code=500, detail=error)
    
    return {"sessions": sessions}


@router.post("/save_chat_session")
def save_chat(request: ChatSessionRequest):
    """Saves a chat session in the database."""
    session_id = save_chat_session(request.user_id, request.messages, request.agent)

    if not session_id:
        raise HTTPException(status_code=500, detail="Failed to save chat session.")

    return {"message": "Chat session saved successfully", "session_id": session_id}
