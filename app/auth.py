
# CryptContext → password ko securely hash & verify karne ke liye
# bcrypt industry-standard hashing algorithm hai

from passlib.context import CryptContext

# jose.jwt → JWT token generate & verify karne ke liye

from jose import jwt


# datetime → token expiry & OTP expiry calculate karne ke liye

from datetime import datetime, timedelta

# random → OTP generate karne ke liye
import random


# secrets → secure random token (password reset ke liye)

import secrets

#                    JWT CONFIG


# JWT sign karne ke liye secret key
#  Production me ENV file (.env) me rakhna chahiye
SECRET_KEY = "SECRET123"

# JWT encryption algorithm
ALGORITHM = "HS256"

# JWT token expiry (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30


#                 PASSWORD HASHING CONFIG


# CryptContext object
# bcrypt → slow & secure (brute-force se protection)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

#                 PASSWORD FUNCTIONS


def hash_password(password: str) -> str:
    """
    Plain password ko encrypted (hashed) password me convert karta hai
    Register / Reset / Change password me use hota hai
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Login ke time user ka password verify karta hai
    """
    return pwd_context.verify(plain_password, hashed_password)


#                 JWT TOKEN FUNCTION


def create_access_token(data: dict) -> str:
    """
    JWT access token generate karta hai
    Login ke baad client ko diya jata hai
    """
    to_encode = data.copy()  # original data safe rahe

    # Token expiry time calculate
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Payload me expiry add
    to_encode.update({"exp": expire})

    # JWT token encode
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#                     OTP CONFIG

# OTP expiry time (minutes)
OTP_EXPIRE_MINUTES = 10


#                     OTP FUNCTIONS


def generate_otp() -> str:
    """
    Random 6-digit OTP generate karta hai
    Example: 483920
    Register / Forgot password me use hota hai
    """
    return str(random.randint(100000, 999999))


def get_otp_expiry_time() -> datetime:
    """
    OTP ka expiry time return karta hai
    Current time + 10 minutes
    """
    return datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)


#           PASSWORD RESET TOKEN (FORGOT PASSWORD)


def generate_reset_token() -> str:
    """
    Secure random token generate karta hai
    Ye token email ke through user ko bheja jata hai
    """
    return secrets.token_urlsafe(32)


def get_reset_token_expiry() -> datetime:
    """
    Password reset token ka expiry time
    (Example: 15 minutes)
    """
    return datetime.utcnow() + timedelta(minutes=15)
