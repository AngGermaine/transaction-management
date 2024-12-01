from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.models.base_model import Base

class Sales(Base):
    __tablename__ = "sales"

    app_id = Column(Integer, ForeignKey("games.appid"), nullable=False)
    estimated_owners = Column(String)
    price = Column(Float, nullable=False)
    discount_dlc_count = Column(Integer)
    sales_id = Column(Integer, primary_key=True, autoincrement=True)
