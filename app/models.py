
# SQLAlchemy ke columns aur data types

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text

# relationship → tables ke beech relation banane ke liye

from sqlalchemy.orm import relationship


# datetime → current time & expiry ke liye
from datetime import datetime


# Base class jisse saare ORM models inherit karte hain

from .database import Base



#                    USER MODEL

# Ye class "users" table ko represent karti hai
class User(Base):
    __tablename__ = "users"


    # Primary key (auto increment)

    id = Column(Integer, primary_key=True, index=True)

    # User ka naam
    # VARCHAR(100)

    name = Column(String(100), nullable=False)

    # User ka email (unique)
    # same email dobara register nahi ho sakta
  
    email = Column(String(150), unique=True, index=True, nullable=False)

    # Hashed password (bcrypt)
    # Plain password kabhi store nahi hota
   
    hashed_password = Column(String(255), nullable=False)


    # Account kab create hua
 
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: User → Notes (One-to-Many)
    # User delete hoga → uske notes bhi delete honge
  
    notes = relationship(
        "Note",
        back_populates="owner",
        cascade="all, delete"
    )

  
    # Relationship: User → OTPs (One-to-Many)
    # OTP verify hone ke baad user se link hota hai
 
    otps = relationship(
        "EmailOTP",
        back_populates="user",
        cascade="all, delete"
    )


#                    NOTE MODEL

# Ye class "notes" table ko represent karti hai
class Note(Base):
    __tablename__ = "notes"

    # Primary key
    
    id = Column(Integer, primary_key=True, index=True)

    # Note ka title
    # VARCHAR(200)
    title = Column(String(200), nullable=False)

    # Note ka content
    # TEXT → long content ke liye
  
    content = Column(Text, nullable=False)

  
    # Foreign key → kis user ka note hai

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Note creation time
    created_at = Column(DateTime, default=datetime.utcnow)


    # Relationship: Note → User

    owner = relationship(
        "User",
        back_populates="notes"
    )


#            EMAIL OTP MODEL 

"""
IMPORTANT DESIGN DECISION 

OTP user create hone se PEHLE generate hota hai.
Isliye OTP ko EMAIL ke base par store kiya jata hai,
na ki user_id ke base par.

OTP verify hone ke baad hi user create hota hai,
aur tab user_id link kiya jata hai.
"""
class EmailOTP(Base):
    __tablename__ = "email_otps"

    
    # Primary key
  
    id = Column(Integer, primary_key=True, index=True)


    # OTP kis email ke liye hai
    # User abhi exist na bhi kare tab bhi OTP aa sakta hai

    email = Column(String(150), index=True, nullable=False)



    # OTP verify hone ke baad user_id fill hota hai
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

   
    # 6 digit OTP cod
    otp_code = Column(String(6), nullable=False)

   
    # OTP expiry time
    # (Current time + 10 minutes)

    expires_at = Column(DateTime, nullable=False)


    # OTP verification status
    # 0 = not verified
    # 1 = verified
   
    is_verified = Column(Integer, default=0)

   
    # OTP generate hone ka time
   
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: OTP → User 
    
    user = relationship(
        "User",
        back_populates="otps"
    )
