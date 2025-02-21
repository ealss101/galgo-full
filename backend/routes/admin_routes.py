from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from backend.services.admin_service import (
    get_pending_users, approve_users, get_all_users, delete_users, update_user_chatbots
)

# ✅ Add a global prefix instead of manually adding "/admin" for each route
router = APIRouter()

# Pydantic Models
class UserApprovalRequest(BaseModel):
    user_ids: List[int]

class UserDeletionRequest(BaseModel):
    user_ids: List[int]

class ChatbotUpdateRequest(BaseModel):
    email: str
    chatbots: List[str]

@router.get("/pending_users")
def fetch_pending_users():
    users = get_pending_users()
    return {"users": users}  # ✅ Fix format for frontend compatibility

# 🔹 Approve Selected Users
@router.post("/approve_users")
def approve_selected_users(request: UserApprovalRequest):
    if approve_users(request.user_ids):
        return {"message": "Users approved successfully"}
    raise HTTPException(status_code=500, detail="Failed to approve users")

@router.get("/all_users")
def fetch_all_users():
    users = get_all_users()
    return {"users": users}  # ✅ Ensure frontend expects the correct format

# 🔹 Delete Users
@router.post("/delete_users")
def delete_selected_users(request: UserDeletionRequest):
    if delete_users(request.user_ids):
        return {"message": "Users deleted successfully"}
    raise HTTPException(status_code=500, detail="Failed to delete users")

# 🔹 Update Chatbot Access
@router.post("/update_chatbots")
def modify_chatbot_access(request: ChatbotUpdateRequest):
    if update_user_chatbots(request.email, request.chatbots):
        return {"message": "Chatbot access updated successfully"}
    raise HTTPException(status_code=500, detail="Failed to update chatbots")
