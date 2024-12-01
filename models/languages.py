from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base_model import Base

class Languages(Base):
    __tablename__ = "languages"

    sales_id = Column(Integer, ForeignKey("sales.salesid"), nullable=False)
    supported_languages = Column(String)
    full_audio_languages = Column(String)
    id = Column(Integer, primary_key=True, autoincrement=True)
