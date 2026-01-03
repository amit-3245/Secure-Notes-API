# FastAPI ke tools import kiye gaye hain
# APIRouter → APIs ka group banane ke liye
# Depends → dependency injection ke liye
# HTTPException → error handle karne ke liye
from fastapi import APIRouter, Depends, HTTPException

# SQLAlchemy Session → database se communication ke liye
from sqlalchemy.orm import Session

#  Correct relative imports (.. ka matlab ek folder upar = app/)
from ..schemas import NoteCreate, NoteResponse   # note create & response schemas
from ..dependencies import get_current_user, get_db  # current user & db session
from ..models import Note   # Note model (notes table)

# Notes ke liye router banaya
# prefix="/notes" → saari APIs /notes se start hongi
# tags=["Notes"] → Swagger UI me grouping ke liye
router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)


# ---------------- CREATE NOTE API ----------------
# POST /notes
@router.post("/", response_model=NoteResponse)
def create_note(
    note: NoteCreate,                # Client se aane wala data (title, content)
    db: Session = Depends(get_db),    # Database connection
    user = Depends(get_current_user)  # JWT token se current logged-in user
):
    # Naya note object bana rahe hain
    # **note.dict() se title aur content aa raha hai
    # user_id=user.id se note ko logged-in user se jod rahe hain
    new_note = Note(
        title=note.title,
        content=note.content,
        user_id=user.id
    )

    # Note ko database session me add kar rahe hain
    db.add(new_note)

    # Database me note permanently save kar rahe hain
    db.commit()

    # Database se latest data (id ke saath) wapas le rahe hain
    db.refresh(new_note)

    # Client ko newly created note return
    return new_note


# ---------------- GET ALL NOTES API ----------------
# GET /notes
# Ye sirf logged-in user ke saare notes return karta hai
@router.get("/", response_model=list[NoteResponse])
def get_notes(
    db: Session = Depends(get_db),     # Database session
    user = Depends(get_current_user)   # JWT token se current user
):
    # Database se sirf current user ke notes fetch kar rahe hain
    return db.query(Note).filter(Note.user_id == user.id).all()
