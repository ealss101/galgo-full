from fastapi import APIRouter, HTTPException
from backend.services.auth_service import authenticate_user, store_user_request
from backend.utils import clean_phone_number
from backend.models import SignupRequest, LoginRequest
from backend.init_database import get_connection

# ✅ Add a global prefix instead of manually adding "/admin" for each route
router = APIRouter()

@router.post("/signup")
def signup_user(request: SignupRequest):
    """Handles user signup and stores in MySQL"""
    cleaned_phone = clean_phone_number(request.phone_number)
    
    if not cleaned_phone:
        raise HTTPException(status_code=400, detail="Invalid phone number format")

    success, message = store_user_request(
        request.first_name, request.last_name, request.email, request.password, cleaned_phone
    )
    
    if not success:
        raise HTTPException(status_code=500, detail=message)

    return {"message": message}

@router.post("/login")
def login_user(request: LoginRequest):
    """Authenticates user login"""
    user, message = authenticate_user(request.email, request.password)

    if not user:
        raise HTTPException(status_code=401, detail=message)

    return {"message": message, "user": user}


