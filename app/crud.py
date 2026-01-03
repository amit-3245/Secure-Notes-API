# Session ka use database se communicate karne ke liye hota hai
from sqlalchemy.orm import Session

# Ye error tab aata hai jab database constraint break hoti hai
# jaise duplicate email insert karne par
from sqlalchemy.exc import IntegrityError

#  Correct relative import:
# User model ko import kiya hai jo "users" table ko represent karta hai
from .models import User

# Password ko hash karne wala function (auth.py se)
from .auth import hash_password


# ---------------- CREATE USER FUNCTION ----------------
def create_user(db: Session, user):
    # User ka naya object bana rahe hain
    new_user = User(
        name=user.name,
        email=user.email,
        # Plain password ko hash karke store kar rahe hain
        hashed_password=hash_password(user.password)
    )

    try:
        # Naya user database session me add kar rahe hain
        db.add(new_user)

        # Database me changes permanently save kar rahe hain
        db.commit()

        # Latest data (id etc.) wapas fetch kar rahe hain
        db.refresh(new_user)

        # Successfully create hua user return kar rahe hain
        return new_user

    except IntegrityError:
        # Agar koi error aaye (jaise duplicate email)
        # to database ke pending changes undo kar dete hain
        db.rollback()

        # Error ko aage throw kar rahe hain
        # Router isse HTTPException me convert karega
        raise
