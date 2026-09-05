from aiogram import types, F, Router
from aiogram.filters import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import WEB_APP_URL

router = Router()

@router.message(CommandStart())
async def start_cmd(message: types.Message):
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
