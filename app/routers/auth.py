
# FastAPI utilities


# APIRouter → routes ko alag file me organize karne ke liye
# Depends → dependency injection (jaise DB session)
# HTTPException → error raise karne ke liye
# status → HTTP status codes (200, 400, 401, etc.)
from fastapi import APIRouter, Depends, HTTPException, status



# SQLAlchemy session & errors


# Session → database session ka type
from sqlalchemy.orm import Session

# IntegrityError → duplicate email jaise DB errors handle karne ke liye
from sqlalchemy.exc import IntegrityError


# datetime → OTP expiry check


# datetime.utcnow() use hota hai OTP expire hua ya nahi check karne ke liye
from datetime import datetime



# OAuth2 form (Swagger compatible login)

# OAuth2PasswordRequestForm →
# Swagger UI me username + password form auto create karta hai
from fastapi.security import OAuth2PasswordRequestForm



# Pydantic Schemas (Request / Response validation)


from ..schemas import (
    UserRegisterRequest,   # Register step-1 → name, email, password
    OTPVerifyRequest,      # Register step-2 → email + otp
    UserResponse,          # User ka response structure
    TokenSchema            # JWT token ka response format
)


# Database & Models


# SessionLocal → database session banane ke liye
from ..database import SessionLocal

# User → users table model
# EmailOTP → OTP store karne wali table
from ..models import User, EmailOTP


# Auth helper functions


from ..auth import (
    hash_password,         # plain password → hashed password
    verify_password,       # login ke time password match
    create_access_token,   # JWT token generate
    generate_otp,          # random 6-digit OTP
    get_otp_expiry_time    # OTP expire hone ka time
)


# Router initialization


# tags=["Auth"] → Swagger me "Auth" section ke andar APIs dikhengi
router = APIRouter(tags=["Auth"])



# Database session dependency

# Har request ke liye ek naya DB session create karta hai

def get_db():
    db = SessionLocal()     # DB session open
    try:
        yield db            # API function ko session provide
    finally:
        db.close()          # request complete hone ke baad session close



# REGISTER STEP-1 → SEND OTP
# API: POST /register/send-otp

@router.post("/register/send-otp", status_code=200)
def send_otp(
    user: UserRegisterRequest,      # frontend se: name, email, password
    db: Session = Depends(get_db)   # database session
):
    #  Check → email pehle se registered to nahi?
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 6-digit OTP generate
    otp_code = generate_otp()

    #  OTP ka expiry time calculate (ex: 5 min)
    expiry_time = get_otp_expiry_time()

    #  OTP ko database me save karna
    otp_entry = EmailOTP(
        email=user.email,
        otp_code=otp_code,
        expires_at=expiry_time,
        is_verified=0           # 0 = not verified
    )

    db.add(otp_entry)
    db.commit()

    #  DEMO PURPOSE ONLY
    # Production me OTP email / SMS pe bhejna chahiye
    return {
        "message": "OTP sent to email",
        "otp_demo": otp_code
    }




# REGISTER STEP-2 → VERIFY OTP & CREATE USER
# API: POST /register/verify-otp


@router.post(
    "/register/verify-otp",
    response_model=UserResponse,   # response ka structure
    status_code=201
)
def verify_otp_and_register(
    data: OTPVerifyRequest,        # email + otp
    db: Session = Depends(get_db)
):
    #  Latest unused OTP nikalna
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

    #  OTP galat hai
    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    #  OTP expire ho chuka hai
    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    #  User create karna
    new_user = User(
        name="Verified User",   # actual name frontend se aayega
        email=data.email,
        hashed_password=hash_password("default123")
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)   # DB se fresh data load
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User already exists")

    #  OTP ko verified mark karna
    otp_record.is_verified = 1
    db.commit()

    return new_user


# LOGIN API

# Ye API user ko login karwati hai
# Agar email + password sahi ho to JWT token return karti hai

@router.post(
    "/login",                      # API endpoint → /login
    response_model=TokenSchema     # Response ka format (access_token + token_type)
)
def login(
    # Swagger UI me jo "username" field hota hai,
    # usko hum EMAIL ke roop me use kar rahe hain
    form_data: OAuth2PasswordRequestForm = Depends(),

    # Database session (har request ke liye naya session)
    db: Session = Depends(get_db)
):
    # """
    # IMPORTANT NOTE:
    # Swagger ke OAuth2 login form me jo 'username' field hoti hai,
    # usme hum EMAIL pass kar rahe hain (username nahi).
    # """

   
    # STEP 1: Email se user fetch karna
    
    # Database me check karo ki ye email exist karti hai ya nahi
    db_user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )


    # STEP 2: User ya password invalid


    # Agar:
    # - user nahi mila
    # - ya password match nahi hua
    if not db_user or not verify_password(
        form_data.password,        # User ka entered password
        db_user.hashed_password    # Database me stored hashed password
    ):
        # Unauthorized error return karo
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

 
    # STEP 3: JWT token generate karna


    # User ke ID ke base par JWT access token banao
    token = create_access_token(
        {"user_id": db_user.id}
    )

    # STEP 4: Token response return
 

    return {
        "access_token": token,     # JWT token
        "token_type": "bearer"     # Token type (OAuth2 standard)
    }
