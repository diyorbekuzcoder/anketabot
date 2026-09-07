from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
import json

from backend.database.database import get_db
from backend.models.application import Application
from backend.models.branch import Branch
from backend.models.position import Position
from backend.models.admin import Admin
from backend.utils.security import get_password_hash
from backend.api import auth
from starlette.concurrency import run_in_threadpool
import pandas as pd
import io
from fastapi.responses import StreamingResponse
from fastapi import UploadFile, File
from backend.services.s3_client import save_upload_file

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

def generate_excel(anketalar):
    data = []
    for a in anketalar:
        data.append({
            "ID": a.id,
            "Holati": a.status,
            "Ismi": a.first_name,
            "Familiyasi": a.last_name,
            "Otasining Ismi": a.middle_name,
            "Tug'ilgan sanasi": a.birth_date,
            "Jinsi": a.gender,
            "Tel": a.phone,
            "Suhbat vaqti / Izoh": a.admin_comment or "",
            "Yuborilgan sana": a.created_at.strftime("%Y-%m-%d %H:%M") if a.created_at else ""
        })
        
    df = pd.DataFrame(data)
    stream = io.BytesIO()
    with pd.ExcelWriter(stream, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Anketalar')
    
    stream.seek(0)
    return stream

@router.get("/export")
async def export_excel(request: Request, db: Session = Depends(get_db)):
    admin = auth.get_current_admin(request, db)
    anketalar = db.query(Application).order_by(Application.id.desc()).all()
    stream = await run_in_threadpool(generate_excel, anketalar)
    
    headers = {
        'Content-Disposition': 'attachment; filename="anketalar.xlsx"'
    }
    return StreamingResponse(stream, headers=headers, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@router.get("", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request, 
    status: Optional[str] = None,
    branch: Optional[str] = None,
    position: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        admin = auth.get_current_admin(request, db)
    except HTTPException:
        return templates.TemplateResponse(request=request, name="login.html")
        
    query = db.query(Application)
    if status:
        query = query.filter(Application.status == status)
    if branch:
        query = query.filter(Application.preferred_branch == branch)
    if position:
        query = query.filter(Application.previous_position == position)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Application.first_name.ilike(search_term)) | 
            (Application.last_name.ilike(search_term)) | 
            (Application.phone.ilike(search_term))
        )
        
    anketalar = query.order_by(Application.id.desc()).all()
    branches = db.query(Branch).order_by(Branch.id.desc()).all()
    positions = db.query(Position).order_by(Position.id.desc()).all()
    
    users = []
    if admin.role == "Super Admin":
        users = db.query(Admin).order_by(Admin.id.asc()).all()
    
    context = {
        "anketalar": anketalar, 
        "admin": admin, 
        "branches": branches, 
        "positions": positions,
        "users": users,
        "filters": {
            "status": status or "",
            "branch": branch or "",
            "position": position or "",
            "search": search or ""
        }
    }
    return templates.TemplateResponse(request=request, name="admin.html", context=context)

@router.get("/anketa/{anketa_id}", response_class=HTMLResponse)
async def admin_anketa_detail(request: Request, anketa_id: int, db: Session = Depends(get_db)):
    admin = auth.get_current_admin(request, db)
    anketa = db.query(Application).filter(Application.id == anketa_id).first()
    if not anketa:
        raise HTTPException(status_code=404, detail="Anketa topilmadi")
    
    try:
        dl = json.loads(anketa.languages)
        anketa.languages = json.dumps(dl, indent=2, ensure_ascii=False)
    except:
        pass
        
    return templates.TemplateResponse(request=request, name="admin_detail.html", context={"anketa": anketa, "admin": admin})

@router.post("/anketa/{anketa_id}/status")
async def update_anketa_status(request: Request, anketa_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    auth.get_current_admin(request, db)
    anketa = db.query(Application).filter(Application.id == anketa_id).first()
    if not anketa:
        raise HTTPException(status_code=404, detail="Anketa topilmadi")
    
    anketa.status = status
    db.commit()
    return RedirectResponse(url=f"/admin/anketa/{anketa_id}", status_code=303)

@router.post("/anketa/{anketa_id}/delete")
async def delete_anketa(request: Request, anketa_id: int, db: Session = Depends(get_db)):
    auth.get_current_admin(request, db)
    anketa = db.query(Application).filter(Application.id == anketa_id).first()
    if anketa:
        db.delete(anketa)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/branches")
async def add_branch(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    auth.get_current_admin(request, db)
    branch = Branch(name=name)
    db.add(branch)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/branches/{branch_id}/delete")
async def delete_branch(request: Request, branch_id: int, db: Session = Depends(get_db)):
    auth.get_current_admin(request, db)
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if branch:
        db.delete(branch)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/positions")
async def add_position(request: Request, name: str = Form(...), db: Session = Depends(get_db)):
    auth.get_current_admin(request, db)
    position = Position(name=name)
    db.add(position)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/positions/{position_id}/delete")
async def delete_position(request: Request, position_id: int, db: Session = Depends(get_db)):
    auth.get_current_admin(request, db)
    position = db.query(Position).filter(Position.id == position_id).first()
    if position:
        db.delete(position)
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# Admin Users Management

@router.post("/users")
async def add_admin_user(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form(...), full_name: str = Form(""), db: Session = Depends(get_db)):
    current_admin = auth.get_current_admin(request, db)
    if current_admin.role != "Super Admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    existing = db.query(Admin).filter(Admin.username == username).first()
    if existing:
        # Instead of failing silently, ideally we'd show an error, but let's just redirect for now
        return RedirectResponse(url="/admin#users", status_code=303)
        
    new_admin = Admin(
        username=username,
        password_hash=get_password_hash(password),
        full_name=full_name,
        role=role,
        is_active=True
    )
    db.add(new_admin)
    db.commit()
    return RedirectResponse(url="/admin#users", status_code=303)

@router.post("/users/{user_id}/update")
async def update_admin_user(request: Request, user_id: int, username: str = Form(...), password: str = Form(""), role: str = Form(...), full_name: str = Form(""), db: Session = Depends(get_db)):
    current_admin = auth.get_current_admin(request, db)
    if current_admin.role != "Super Admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    admin_user = db.query(Admin).filter(Admin.id == user_id).first()
    if not admin_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Check if new username conflicts
    if username != admin_user.username:
        existing = db.query(Admin).filter(Admin.username == username).first()
        if existing:
            return RedirectResponse(url="/admin#users", status_code=303)
            
    admin_user.username = username
    admin_user.full_name = full_name
    admin_user.role = role
    if password:
        admin_user.password_hash = get_password_hash(password)
        
    db.commit()
    return RedirectResponse(url="/admin#users", status_code=303)

@router.post("/users/{user_id}/delete")
async def delete_admin_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    current_admin = auth.get_current_admin(request, db)
    if current_admin.role != "Super Admin":
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Prevent deleting oneself
    if current_admin.id == user_id:
        return RedirectResponse(url="/admin#users", status_code=303)
        
    admin_user = db.query(Admin).filter(Admin.id == user_id).first()
    if admin_user:
        db.delete(admin_user)
        db.commit()
    return RedirectResponse(url="/admin#users", status_code=303)

@router.post("/profile/password")
async def update_profile_password(
    password: str = Form(...),
    current_user: Admin = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    current_user.password_hash = get_password_hash(password)
    db.commit()
    return {"status": "success", "message": "Password updated successfully"}

@router.post("/profile/update")
async def update_profile_details(
    phone_number: str = Form(None),
    telegram_id: str = Form(None),
    current_user: Admin = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    # Check if telegram_id is unique if it's changing
    if telegram_id and telegram_id != current_user.telegram_id:
        existing = db.query(Admin).filter(Admin.telegram_id == telegram_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Telegram ID already in use by another admin")
    
    current_user.phone_number = phone_number
    current_user.telegram_id = telegram_id
    db.commit()
    return {"status": "success", "message": "Profile updated successfully"}

@router.post("/profile/upload_picture")
async def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: Admin = Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    try:
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Faqat rasmlar yuklash mumkin")
            
        final_url = await save_upload_file(file)
        if not final_url:
            raise HTTPException(status_code=500, detail="Faylni yuklashda xatolik yuz berdi")
        
        current_user.profile_picture = final_url
        db.commit()
        return {"status": "success", "url": final_url}
    except Exception as e:
        print(f"Error uploading profile picture: {e}")
        raise HTTPException(status_code=500, detail="Error uploading file")
