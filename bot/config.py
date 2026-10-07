import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN or BOT_TOKEN == "YOUR_TOKEN":
    raise ValueError("BOT_TOKEN is missing in the environment variables.")
WEB_APP_URL = os.getenv("WEB_APP_URL")
if not WEB_APP_URL or WEB_APP_URL == "https://your-ngrok-url.ngrok-free.app":
    raise ValueError("WEB_APP_URL is missing in the environment variables.")
