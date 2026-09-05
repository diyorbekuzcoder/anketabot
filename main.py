import os
import uvicorn
import logging
from contextlib import asynccontextmanager
from backend.app import app
from bot.setup import bot, dp
from bot.handlers import router

if router not in dp.sub_routers:
    dp.include_router(router)

WEBHOOK_URL = os.getenv("WEBHOOK_URL") # e.g. https://your-cloudflare-tunnel.trycloudflare.com/api/bot/webhook
WEBHOOK_PATH = "/api/bot/webhook"

@asynccontextmanager
async def lifespan(app):
    # Startup
    if WEBHOOK_URL:
        # If WEBHOOK_URL is set, we set the webhook
        url = f"{WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"
        await bot.set_webhook(url=url, drop_pending_updates=True)
        logging.info(f"Webhook set to {url}")
    else:
        # Fallback to polling for local development without tunnels
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("Starting bot in long-polling mode (Fallback)")
        import asyncio
        asyncio.create_task(dp.start_polling(bot))
    yield
    # Shutdown
    await bot.session.close()

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
