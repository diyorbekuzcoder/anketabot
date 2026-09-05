from fastapi import APIRouter, Request
from aiogram.types import Update
from bot.setup import bot, dp
from bot.config import WEB_APP_URL

router = APIRouter()

@router.post("/webhook")
async def bot_webhook(request: Request):
    update_data = await request.json()
    update = Update(**update_data)
    await dp.feed_update(bot=bot, update=update)
    return {"ok": True}
