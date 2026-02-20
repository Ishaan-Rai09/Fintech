"""
Authentication API endpoints
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from backend.database.connection import get_db
from backend.models.user import User
from backend.schemas.auth import UserCreate, UserLogin, UserResponse, Token, APIResponse
from backend.middleware.security import hash_password, verify_password, create_access_token
from backend.middleware.auth_middleware import get_current_user
from backend.config import settings
import secrets

router = APIRouter(prefix="/auth", tags=["Authentication"])

# OAuth setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


@router.post("/register", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_pwd = hash_password(user_data.password)
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        password_hash=hashed_pwd,
        full_name=user_data.full_name,
        phone=user_data.phone
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return APIResponse(
        status="success",
        message="User registered successfully",
        data={"user_id": new_user.id, "username": new_user.username}
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Login and get JWT token
    """
    # Find user
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    """
    return {
        "success": True,
        "status": "success",
        "message": "User profile retrieved",
        "data": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "phone": current_user.phone,
            "is_active": current_user.is_active,
            "is_verified": current_user.is_verified,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None
        }
    }


@router.put("/me", response_model=APIResponse)
async def update_profile(
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile
    """
    if full_name:
        current_user.full_name = full_name
    if phone:
        current_user.phone = phone
    
    db.commit()
    db.refresh(current_user)
    
    return APIResponse(
        status="success",
        message="Profile updated successfully"
    )


@router.get("/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth login flow
    """
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle Google OAuth callback
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        # Check if user exists
        email = user_info.get('email')
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user from Google profile
            username = email.split('@')[0] + '_' + secrets.token_hex(4)
            user = User(
                email=email,
                username=username,
                full_name=user_info.get('name'),
                password_hash=hash_password(secrets.token_urlsafe(32)),  # Random password
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        # Redirect to frontend with token
        return RedirectResponse(url=f"/dashboard?token={access_token}")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}"
        )


@router.post("/google/token", response_model=Token)
async def google_token_login(id_token: str, db: Session = Depends(get_db)):
    """
    Login with Google ID token (for frontend client-side OAuth)
    """
    try:
        from google.oauth2 import id_token as google_id_token
        from google.auth.transport import requests
        
        # Verify token
        idinfo = google_id_token.verify_oauth2_token(
            id_token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )
        
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        
        # Get user info
        email = idinfo['email']
        name = idinfo.get('name', '')
        
        # Check if user exists
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            # Create new user
            username = email.split('@')[0] + '_' + secrets.token_hex(4)
            user = User(
                email=email,
                username=username,
                full_name=name,
                password_hash=hash_password(secrets.token_urlsafe(32)),
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": str(user.id)})
        
        return Token(access_token=access_token, token_type="bearer")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid Google token: {str(e)}"
        )
