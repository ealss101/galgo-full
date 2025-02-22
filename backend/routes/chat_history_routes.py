from fastapi import APIRouter, HTTPException
from backend.services.chat_history_service import get_chat_sessions, save_chat_session
from pydantic import BaseModel
from typing import List, Dict
from backend.services.chat_history_service import generate_doc_from_message
from fastapi.responses import StreamingResponse

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


@router.post("/download_last_message_doc")
def download_last_message_doc(payload: dict):
    message = payload.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="No message provided.")

    doc_stream = generate_doc_from_message(message)
    headers = {"Content-Disposition": "attachment; filename=last_message.docx"}
    return StreamingResponse(
        doc_stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers=headers,
    )


