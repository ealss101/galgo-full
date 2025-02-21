from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr  # Enforces valid email format
    phone_number: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
