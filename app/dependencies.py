
# FastAPI dependencies & security utilities


# Depends → dependency injection ke liye
# HTTPException → error response bhejne ke liye
# status → HTTP status codes ke liye
from fastapi import Depends, HTTPException, status

# JWT tools (token decode & error handling)

# jwt → token decode karne ke liye
# JWTError → invalid / expired token error ke liye
from jose import jwt, JWTError


# SQLAlchemy session type

from sqlalchemy.orm import Session


# OAuth2PasswordBearer
# Authorization header se Bearer token nikalta hai

from fastapi.security import OAuth2PasswordBearer



# Local project imports

from .database import SessionLocal
from .models import User
from .auth import SECRET_KEY, ALGORITHM


# OAuth2 scheme configuration

# tokenUrl="login" → Swagger UI ko batata hai
# token /login endpoint se milega
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# DATABASE SESSION DEPENDENCY

def get_db():
    """
    Har request ke liye ek naya database session deta hai
    Request complete hone ke baad automatically close ho jata hai
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CURRENT USER DEPENDENCY (JWT Protected)

def get_current_user(
    token: str = Depends(oauth2_scheme),   # Authorization: Bearer <token>
    db: Session = Depends(get_db)           # Database session
):
    """
    Ye dependency:
    1️ JWT token verify karti hai
    2️ Token se user_id nikalti hai
    3️ Database se user fetch karti hai
    4️ Valid user return karti hai

    Agar kuch bhi galat hua → 401 Unauthorized
    """

    try:

        # JWT token decode
        # SECRET_KEY + ALGORITHM se verify hota hai
 
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Token payload se user_id nikalna
     
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

    except JWTError:
    
        # Token invalid ya expired hai

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    
    # Database se user fetch
   
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Sab kuch sahi → authenticated user return
  
    return user
