import html
import logging
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.schemas.application import AnketaFormModel
from backend.database.database import get_db
from backend.models.application import Application
from backend.models.branch import Branch
from backend.models.position import Position
from bot.setup import bot
from bot.config import BOT_TOKEN
from backend.utils.telegram import validate_telegram_data
from backend.services.s3_client import save_upload_file

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")

@router.get("/form", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@router.post("/submit_form")
async def submit_form(request: Request, db: Session = Depends(get_db)):
    try:
        form_data = await request.form()
        
        init_data = form_data.get("initData")
        if not init_data or not validate_telegram_data(init_data, BOT_TOKEN):
            return {"status": "error", "message": "Telegram avtorizatsiyasidan o'tilmadi (Security Check Failed)"}
            
        validated_data = AnketaFormModel(**form_data)
        
        rasm = form_data.get("rasm")
        pasport_fayl = form_data.get("pasport_fayl")
        
        # Use our new S3 / Local fallback uploader
        rasm_path = await save_upload_file(rasm, "uploads")
        pasport_path = await save_upload_file(pasport_fayl, "uploads")
        dynamic_lists_str = form_data.get("dynamic_lists", "{}")
        
        yangi_anketa = Application(
            telegram_user_id=validated_data.user_id,
            telegram_username=html.escape(str(validated_data.username)),
            first_name=html.escape(str(validated_data.ism)),
            last_name=html.escape(str(validated_data.familiya)),
            middle_name=html.escape(str(validated_data.otasining_ismi)),
            birth_date=html.escape(str(validated_data.tugilgan_sana)),
            gender=html.escape(str(validated_data.jins)),
            marital_status=html.escape(str(validated_data.oilaviy_holati)),
            education=html.escape(str(validated_data.malumoti)),
            speciality=html.escape(str(validated_data.talabami)),
            height=validated_data.boy,
            weight=validated_data.vazn,
            region=html.escape(str(validated_data.viloyat)),
            district=html.escape(str(validated_data.tuman)),
            address=html.escape(str(validated_data.manzil_toliq)),
            preferred_branch=html.escape(str(validated_data.filial)),
            previous_position=html.escape(str(validated_data.lavozim)),
            work_experience=html.escape(str(validated_data.avval_ishlagan)),
            citizenship=html.escape(str(validated_data.fuqaro)),
            driving_license=html.escape(str(validated_data.avto)),
            health_info=html.escape(str(validated_data.sogliq_ogir_narsa)),
            expected_salary=validated_data.xohlagan_maosh,
            criminal_record=html.escape(str(validated_data.sudlanganlik)),
            phone=html.escape(str(validated_data.qoshimcha_tel)),
            passport_photo=pasport_path,
            personal_photo=rasm_path,
            languages=dynamic_lists_str
        )
        
        db.add(yangi_anketa)
        db.commit()
        db.refresh(yangi_anketa)

        user_id = validated_data.user_id
        if user_id:
            try:
                await bot.send_message(chat_id=user_id, text="Sizning anketangiz muvaffaqiyatli qabul qilindi va HR bo'limiga yuborildi. Rahmat!")
            except Exception as e:
                logging.warning(f"Bot failed to send message to {user_id}: {e}")
            
        return {"status": "success"}
    except HTTPException as he:
        return {"status": "error", "message": he.detail}
    except Exception as e:
        logging.error(f"Form submission error: {e}", exc_info=True)
        return {"status": "error", "message": "Ichki server xatoligi yuz berdi. Iltimos, qayta urinib ko'ring."}

@router.get("/api/options")
async def get_options(db: Session = Depends(get_db)):
    branches = db.query(Branch).all()
    positions = db.query(Position).all()
    return {
        "branches": [b.name for b in branches],
        "positions": [p.name for p in positions]
    }
