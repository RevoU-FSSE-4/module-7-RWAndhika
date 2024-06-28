from models.base import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Text, DateTime
from sqlalchemy.sql import func

class Review(Base):
    __tablename__ = 'review'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    email = mapped_column(String(100), nullable= False)
    rating = mapped_column(Integer, nullable=False)
    description = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())