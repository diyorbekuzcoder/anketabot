import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN")
WEB_APP_URL = os.getenv("WEB_APP_URL", "https://your-ngrok-url.ngrok-free.app")
