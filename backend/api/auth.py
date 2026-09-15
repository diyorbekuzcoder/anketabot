from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from backend.database.database import get_db
from backend.models.admin import Admin
from backend.utils.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
import uuid

router = APIRouter()

# In-memory store for telegram authentication sessions
# Format: { "uuid_string": {"status": "pending" | "authenticated", "admin_username": "...", "admin_role": "..."} }
telegram_auth_sessions = {}

def get_current_admin(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        # Fallback to authorization header if we have one
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
    admin = db.query(Admin).filter(Admin.username == username, Admin.is_active == True).first()
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found")
        
    return admin

@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(
        (Admin.username == form_data.username) | (Admin.telegram_id == form_data.username)
    ).first()
    
    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
        
    if not admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.username, "role": admin.role}, expires_delta=access_token_expires
    )
    
    response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/telegram/start")
async def telegram_auth_start():
    token = str(uuid.uuid4())
    telegram_auth_sessions[token] = {"status": "pending"}
    # The bot username is Zeytun_HRbot
    bot_url = f"https://t.me/Zeytun_HRbot?start=auth_{token}"
    return {"bot_url": bot_url, "token": token}

@router.get("/telegram/status")
async def telegram_auth_status(token: str, response: Response):
    session_data = telegram_auth_sessions.get(token)
    if not session_data:
        raise HTTPException(status_code=404, detail="Auth token not found or expired")
        
    if session_data["status"] == "authenticated":
        # Create token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": session_data["admin_username"], "role": session_data["admin_role"]}, 
            expires_delta=access_token_expires
        )
        response.set_cookie(key="access_token", value=access_token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        
        # Clean up
        del telegram_auth_sessions[token]
        return {"status": "ok"}
        
    return {"status": "pending"}
