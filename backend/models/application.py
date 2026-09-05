from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from backend.database.database import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    telegram_user_id = Column(Integer, index=True, nullable=True)
    telegram_username = Column(String, default="")
    
    # Qadam 1
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    gender = Column(String)
    birth_date = Column(String)
    marital_status = Column(String)
    children_count = Column(Integer, default=0)
    
    # Qadam 2
    education = Column(String)
    speciality = Column(String)
    languages = Column(Text, default="{}") # JSON
    
    # Qadam 3
    height = Column(Integer)
    weight = Column(Integer)
    region = Column(String)
    district = Column(String)
    address = Column(String)
    preferred_branch = Column(String)
    
    # Qadam 4
    work_experience = Column(String) # years or text
    previous_company = Column(String)
    previous_position = Column(String)
    citizenship = Column(String)
    driving_license = Column(String)
    
    # Qadam 5
    health_info = Column(String)
    expected_salary = Column(Integer)
    criminal_record = Column(String)
    
    # Qadam 6
    phone = Column(String)
    additional_phone = Column(String)
    passport_photo = Column(String, nullable=True) # file path
    personal_photo = Column(String, nullable=True) # file path
    
    # Meta
    status = Column(String, default="Yangi") # Yangi, Ko'rib chiqilmoqda, Suhbatga chaqirildi, Qabul qilindi, Rad etildi, Arxiv
    admin_comment = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
