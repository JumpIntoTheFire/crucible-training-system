import logging
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.models import Base, Contact, engine, get_db
from backend.routes import auth, exercises, workouts

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# Log DB host only — never log credentials
_db_url = os.environ.get("DATABASE_URL", "")
_db_host = _db_url.split("@")[-1].split("/")[0] if "@" in _db_url else "localhost"
logger.info("Connecting to database at %s", _db_host)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Crucible Training System API",
    description="REST API for the CTS fitness coaching platform.",
    version="1.0.0",
)

# CORS — origins controlled by environment variable for easy production config
_raw_origins = os.environ.get("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174")
_allowed_origins = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

image_dir = os.path.join(os.path.dirname(__file__), "static", "images")
os.makedirs(image_dir, exist_ok=True)
app.mount("/images", StaticFiles(directory=image_dir), name="images")


# ── Schemas ──────────────────────────────────────────────────────────────────

class ContactIn(BaseModel):
    name: str
    email: EmailStr
    message: str

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name is required")
        if len(v) > 100:
            raise ValueError("Name must be 100 characters or fewer")
        return v

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message is required")
        if len(v) > 2000:
            raise ValueError("Message must be 2000 characters or fewer")
        return v


class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    message: str

    model_config = {"from_attributes": True}


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "service": "CTS API"}


@app.post("/contact", status_code=201, response_model=ContactOut, tags=["Contact"])
def submit_contact(payload: ContactIn, db: Session = Depends(get_db)):
    """Submit a contact form message."""
    entry = Contact(name=payload.name, email=payload.email, message=payload.message)
    db.add(entry)
    try:
        db.commit()
        db.refresh(entry)
        logger.info("Contact submission saved (id=%s)", entry.id)
        return entry
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Failed to save contact submission")
        raise HTTPException(status_code=500, detail="Could not save message. Please try again.")


@app.get("/contact", response_model=list[ContactOut], tags=["Contact"], include_in_schema=False)
def list_contacts(db: Session = Depends(get_db)):
    """Dev-only: list all contact submissions."""
    return db.query(Contact).order_by(Contact.id.desc()).all()


app.include_router(exercises.router)
app.include_router(auth.router)
app.include_router(workouts.router)
