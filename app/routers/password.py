
# FastAPI tools

from fastapi import APIRouter, Depends, HTTPException, status


# SQLAlchemy session

from sqlalchemy.orm import Session


# Datetime (OTP expiry check ke liye)

from datetime import datetime


# Schemas (request validation)

from ..schemas import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    ChangePasswordRequest
)
# Database & Models

from ..database import SessionLocal
from ..models import User, EmailOTP

# Auth utilities

from ..auth import (
    hash_password,
    verify_password,
    generate_otp,
    get_otp_expiry_time
)

# Current user dependency (JWT based)

from ..dependencies import get_current_user


# Router

router = APIRouter(
    prefix="/password",
    tags=["Password"]
)


# Database session dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#  FORGOT PASSWORD → SEND OTP
# POST /password/forgot

@router.post("/forgot", status_code=200)
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    #  Step 1: check user exists or not
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User with this email does not exist"
        )

    # 🔹 Step 2: generate OTP
    otp_code = generate_otp()
    expiry_time = get_otp_expiry_time()

    # 🔹 Step 3: save OTP in database
    otp_entry = EmailOTP(
        email=data.email,
        otp_code=otp_code,
        expires_at=expiry_time,
        is_verified=0
    )

    db.add(otp_entry)
    db.commit()

    #  DEMO PURPOSE ONLY
    # Production me OTP email pe jayega
    return {
        "message": "OTP sent to your email for password reset",
        "otp_demo": otp_code
    }


#  RESET PASSWORD → VERIFY OTP + SET NEW PASSWORD
# POST /password/reset

@router.post("/reset", status_code=200)
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    #  Step 1: valid OTP fetch (email + otp)
    otp_record = (
        db.query(EmailOTP)
        .filter(
            EmailOTP.email == data.email,
            EmailOTP.otp_code == data.otp,
            EmailOTP.is_verified == 0
        )
        .order_by(EmailOTP.created_at.desc())
        .first()
    )

    if not otp_record:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # 🔹 Step 2: expiry check
    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="OTP expired"
        )

    # 🔹 Step 3: user fetch
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 🔹 Step 4: update password (hash)
    user.hashed_password = hash_password(data.new_password)

    # 🔹 Step 5: mark OTP as used
    otp_record.is_verified = 1

    db.commit()

    return {
        "message": "Password reset successfully"
    }



# 3️ CHANGE PASSWORD (LOGGED-IN USER)
# POST /password/change

@router.post("/change", status_code=200)
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 🔹 Step 1: old password verify
    if not verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Old password is incorrect"
        )

    # 🔹 Step 2: new password hash & save
    current_user.hashed_password = hash_password(data.new_password)
    db.commit()

    return {
        "message": "Password changed successfully"
    }
