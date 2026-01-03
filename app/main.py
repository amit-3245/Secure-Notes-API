
# FastAPI core import

from fastapi import FastAPI

# Database related imports

from .database import engine
from .models import Base


# Routers import
from .routers import auth, notes, password



# FastAPI app instance

app = FastAPI(
    title="Secure Notes API",
    description="FastAPI project with JWT Auth, OTP verification & Password Management",
    version="1.0.0"
)


# DATABASE TABLE CREATE

# Ye line sabhi SQLAlchemy models ki tables create karegi
# (User, Notes, EmailOTP etc.)
# NOTE:
# Ye sirf first time ya new tables ke liye useful hoti hai
Base.metadata.create_all(bind=engine)


# ROUTERS REGISTER


#  Authentication & Registration APIs
# /register, /login, /register/send-otp, /register/verify-otp
app.include_router(auth.router)

#  Notes APIs (JWT protected)
# /notes/*
app.include_router(notes.router)

#  Password APIs
# /password/forgot
# /password/reset
# /password/change
app.include_router(password.router)


# ROOT TEST API

@app.get("/")
def root():
    return {
        "message": "Secure Notes API is running successfully "
    }
