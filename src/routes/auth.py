from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Request, File, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from src.services.redis_client import redis_client
import json

from src.database.models import User
from src.schemas.auth import (
    UserCreate,
    UserResponse,
    Token,
    RefreshTokenRequest,
    RequestPasswordReset,
    ResetPassword,
)
from src.conf.config import settings
from src.services.auth import (
    get_db,
    get_current_user,
    admin_required,
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    create_email_verification_token,
    decode_email_verification_token,
    create_password_reset_token,
    decode_password_reset_token,
)
from src.services.email import send_verification_email, send_password_reset_email
from src.services.cloudinary_service import upload_avatar
from src.services.limiter import limiter

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new user.

    Creates a new user in the database and sends an email verification link.

    Args:
        user (UserCreate): User registration data.
        background_tasks (BackgroundTasks): Background task manager.
        request (Request): HTTP request object.
        db (Session): Database session.

    Returns:
        UserResponse: The created user without password.
    """
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = get_password_hash(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed,
        confirmed=False,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_email_verification_token(new_user.email)
    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        new_user.username,
        token,
        str(request.base_url),
    )
    return new_user


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verify user's email using a token.

    Args:
        token (str): Token sent to the user's email.
        db (Session): Database session.

    Returns:
        dict: Confirmation message if successful.
    """
    try:
        email = decode_email_verification_token(token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.confirmed:
        raise HTTPException(status_code=400, detail="Email already verified")

    user.confirmed = True
    db.commit()
    return {"message": "Email verified successfully"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return access and refresh tokens.

    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials (username = email).
        db (Session): Database session.

    Returns:
        dict: Access token, refresh token, and token type.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    redis_client.set(
        user.email,
        json.dumps({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "confirmed": user.confirmed,
            "avatar": user.avatar,
            "role": user.role,
        }),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserResponse)
@limiter.limit("5/minute")
def read_users_me(request: Request, current_user: User = Depends(get_current_user)):
    """
    Get the current authenticated user's profile.

    Args:
        request (Request): HTTP request object.
        current_user (User): Authenticated user.

    Returns:
        UserResponse: User data.
    """
    return current_user


@router.patch("/avatar", response_model=UserResponse)
def update_avatar(file: UploadFile = File(...), current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Update avatar for the authenticated user.

    Args:
        file (UploadFile): Uploaded avatar image.
        current_user (User): Authenticated user.
        db (Session): Database session.

    Returns:
        UserResponse: Updated user with new avatar.
    """
    avatar_url = upload_avatar(
        file.file,
        public_id=f"avatars/{current_user.email}",
    )
    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user


@router.patch("/avatar/admin", response_model=UserResponse)
def update_avatar_admin(file: UploadFile = File(...), current_user: User = Depends(admin_required), db: Session = Depends(get_db)):
    """
    Update avatar for another user (admin only).

    Args:
        file (UploadFile): Uploaded avatar image.
        current_user (User): Authenticated admin user.
        db (Session): Database session.

    Returns:
        UserResponse: Updated user with new avatar.
    """
    avatar_url = upload_avatar(
        file.file,
        public_id=f"avatars/{current_user.email}",
    )
    current_user.avatar = avatar_url
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/request-reset-password")
def request_password_reset(data: RequestPasswordReset, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    Send password reset email to the user.

    Args:
        data (RequestPasswordReset): Email of the user requesting reset.
        background_tasks (BackgroundTasks): Background task manager.
        request (Request): HTTP request object.
        db (Session): Database session.

    Returns:
        dict: Confirmation message.
    """
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_password_reset_token(user.email)
    background_tasks.add_task(
        send_password_reset_email,
        user.email,
        user.username,
        token,
        str(request.base_url),
    )
    return {"message": "Password reset link sent to your email"}


@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    """
    Reset the user's password using a valid token.

    Args:
        data (ResetPassword): Token and new password.
        db (Session): Database session.

    Returns:
        dict: Success message.
    """
    try:
        email = decode_password_reset_token(data.token)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = get_password_hash(data.new_password)
    db.commit()
    return {"message": "Password has been reset successfully"}


@router.post("/refresh", response_model=Token)
def refresh_token(data: RefreshTokenRequest):
    """
    Generate a new access token using a valid refresh token.

    Args:
        data (RefreshTokenRequest): Refresh token.

    Returns:
        Token: New access token and the same refresh token.
    """
    try:
        payload = jwt.decode(
            data.refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    new_access_token = create_access_token(data={"sub": email})
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "refresh_token": data.refresh_token,
    }


@router.get("/admin-only")
def admin_only(current_user: User = Depends(admin_required)):
    """
    Endpoint accessible only by admin users.

    Args:
        current_user (User): Authenticated admin user.

    Returns:
        dict: Welcome message.
    """
    return {"message": "Welcome, admin!"}
