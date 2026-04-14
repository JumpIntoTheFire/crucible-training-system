import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, field_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.models import User, get_db
from backend.auth import hash_password, verify_password, create_access_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class RegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def username_valid(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if len(v) > 50:
            raise ValueError("Username must be 50 characters or fewer")
        return v

    @field_validator("password")
    @classmethod
    def password_strong(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=TokenOut,
    status_code=201,
    summary="Create a new account",
    description="Register with a unique username and email. Returns a JWT on success.",
)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already registered",
        )
    logger.info("New user registered (id=%s, username=%s)", user.id, user.username)
    token = create_access_token(user.id)
    return TokenOut(access_token=token, user_id=user.id, username=user.username)


@router.post(
    "/login",
    response_model=TokenOut,
    summary="Login",
    description=(
        "Authenticate with username (or email) and password. "
        "Returns a JWT valid for 24 hours."
    ),
)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Accept either username or email in the OAuth2 'username' field
    user = (
        db.query(User)
        .filter((User.username == form.username) | (User.email == form.username))
        .first()
    )
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    logger.info("User logged in (id=%s)", user.id)
    token = create_access_token(user.id)
    return TokenOut(access_token=token, user_id=user.id, username=user.username)
