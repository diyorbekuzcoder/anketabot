from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import WEB_APP_URL

router = Router()

from backend.database.database import get_db
from backend.models.admin import Admin
from backend.api.auth import telegram_auth_sessions

@router.message(CommandStart())
async def start_cmd(message: types.Message):
    parts = message.text.split()
    args = parts[1] if len(parts) > 1 else None
    if args and args.startswith("auth_"):
        token = args.split("_")[1]
        
        # Check if user is an admin
        from backend.database.database import SessionLocal
        db = SessionLocal()
        admin = db.query(Admin).filter(Admin.telegram_id == str(message.from_user.id), Admin.is_active == True).first()
        db.close()
        
        if admin:
            if token in telegram_auth_sessions:
                telegram_auth_sessions[token]["status"] = "authenticated"
                telegram_auth_sessions[token]["admin_username"] = admin.username
                telegram_auth_sessions[token]["admin_role"] = admin.role
                await message.answer("✅ Muvaffaqiyatli kirdingiz! Endi saytga qaytishingiz mumkin.")
            else:
                await message.answer("❌ Ulanish vaqti tugagan yoki xato. Iltimos saytdan qayta urinib ko'ring.")
        else:
            await message.answer("❌ Siz admin emassiz yoki telegram raqamingiz admin paneliga kiritilmagan.")
        return

    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Yo'riqnoma"), KeyboardButton(text="Anketa")]
        ],
        resize_keyboard=True
    )
    text = (
        "Salom 👋\n"
        "Bu yerda siz o'zingizning arizangizni 📄 to'ldirishingiz va bizning kompaniyamizdagi mavjud bo'sh ish o'rinlari haqida bilib olishingiz mumkin!\n\n"
        "Здравствуйте 👋\n"
        "Здесь Вы можете заполнить свою анкету 📄 и узнать о существующих вакансиях нашей Компании!"
    )
    await message.answer(text, reply_markup=markup)

@router.message(F.text.in_(["Yo'riqnoma", "Yordam"]))
async def yoriqnoma_cmd(message: types.Message):
    text = (
        "Foydalanish qoidalari:\n"
        "1. Siz barcha ma'lumotlarni to'liq kiritishingiz shart. Sizning kiritgan ma'lumotlaringiz xavfsizligi kafolatlanadi\n"
        "2. Ba'zi ma'lumotlarni botning o'zidagi tugmacha(knopka) orqali kiritishingiz kerak, masalan: filial, lavozim, ma'lumotingiz v.hkz shunga ahamiyat bering\n"
        "3. Ma'lumot kiritishda xato qilmaslikka harakat qiling\n"
        "4. Kiritgan ma'lumotlaringizni tasdiqlashdan oldin to'g'ri kiritganingizga ishonch hosil qilish uchun tekshirib chiqing\n"
        "5. Start tugmasini bosishingiz bilan bizga yuborgan malumotlaringizdan foydalanishga ruhsat bergan bo'lasiz. Biz shu ma'lumotlar orqali siz bilan bog'lanamiz\n"
        " Omadingizni bersin..."
    )
    await message.answer(text)

@router.message(F.text == "Anketa")
async def anketa_cmd(message: types.Message):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Anketani to'ldirish", web_app=WebAppInfo(url=f"{WEB_APP_URL}/form"))]
        ]
    )
    text = "📄 «Anketa to'ldirish» tugmasini bosish orqali siz anketa bo'limiga o'tqazilasiz. Anketa bo'limidagi barcha so'ralgan savollarga to'liq, aniq va xatolarsiz javob yozishingizni so'raymiz!"
    await message.answer(text, reply_markup=markup)
