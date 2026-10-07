import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from backend.api import admin, auth, bot, forms

app = FastAPI()

allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = allowed_origins_str.split(",") if allowed_origins_str != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(forms.router, tags=["forms"])
app.include_router(bot.router, prefix="/api/bot", tags=["bot"])


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
async def root_redirect():
    return RedirectResponse(url="/form")


@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/admin", status_code=303)
    response.delete_cookie("access_token")
    return response
