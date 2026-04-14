# backend/main.py

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import os

from backend.models import Contact, engine, Base
from backend.models import get_db

print(f"Connected to DB: {engine.url}")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CTS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/")
def read_root():
    return {"message": "CTS backend is live"}


@app.post("/contact", status_code=201, response_model=ContactOut)
def submit_contact(payload: ContactIn, db: Session = Depends(get_db)):
    entry = Contact(name=payload.name, email=payload.email, message=payload.message)
    db.add(entry)
    try:
        db.commit()
        db.refresh(entry)
        return entry
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Could not save message. Please try again.")


# Dev-only: list all contact submissions
@app.get("/contact", response_model=list[ContactOut])
def list_contacts(db: Session = Depends(get_db)):
    return db.query(Contact).order_by(Contact.id.desc()).all()


from backend.routes import exercises, auth, workouts
app.include_router(exercises.router)
app.include_router(auth.router)
app.include_router(workouts.router)
