from sqlalchemy import Column, Integer, String
from backend.database.database import Base

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
