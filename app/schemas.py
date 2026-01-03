
# Pydantic ka BaseModel import
# BaseModel ka use request & response data validate karne ke liye hota hai
# EmailStr automatically email format validate karta hai

from pydantic import BaseModel, EmailStr
from datetime import datetime


#                USER REGISTRATION (OTP BASED)


# -------- REGISTER STEP-1 : SEND OTP --------
# User jab register karega tab ye data aayega
# Is step me user DB me save nahi hota
class UserRegisterRequest(BaseModel):
    name: str                    # User ka naam
    email: EmailStr              # User ka email (auto validated)
    password: str                # Plain password (OTP verify ke baad hash hoga)


# -------- REGISTER STEP-2 : VERIFY OTP --------
# User OTP verify karega
class OTPVerifyRequest(BaseModel):
    email: EmailStr              # Jis email par OTP aaya
    otp: str                     # 6 digit OTP



#                LOGIN SCHEMA


# Login ke liye email + password
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#                USER RESPONSE


# User create hone ke baad response
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        # SQLAlchemy model → JSON
        from_attributes = True



#                JWT TOKEN RESPONSE


class TokenSchema(BaseModel):
    access_token: str            # JWT token
    token_type: str = "bearer"   # Bearer authentication


#                NOTES SCHEMAS


# Note create request
class NoteCreate(BaseModel):
    title: str
    content: str


# Note update request
class NoteUpdate(BaseModel):
    title: str
    content: str


# Note response
class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True



#           FORGOT / RESET / CHANGE PASSWORD


# -------- FORGOT PASSWORD (SEND OTP) --------
# User sirf email bhejega
class ForgotPasswordRequest(BaseModel):
    email: EmailStr


# -------- RESET PASSWORD (VERIFY OTP + NEW PASSWORD) --------
class ResetPasswordRequest(BaseModel):
    email: EmailStr              # User ka email
    otp: str                     # OTP jo email pe aaya
    new_password: str            # New password


# -------- CHANGE PASSWORD (LOGGED-IN USER) --------
class ChangePasswordRequest(BaseModel):
    old_password: str            # Purana password
    new_password: str            # Naya password
