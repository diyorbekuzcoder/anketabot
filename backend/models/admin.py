from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from backend.database.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    profile_picture = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    telegram_id = Column(String, nullable=True, unique=True)
    role = Column(String, default="HR Admin") # Super Admin, HR Admin, Viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
