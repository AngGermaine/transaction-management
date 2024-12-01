from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.base_model import Base

class ReviewData(Base):
    __tablename__ = "reviewdata"

    sales_id = Column(Integer, ForeignKey("sales.salesid"), nullable=False)
    reviews = Column(String)
    id = Column(Integer, primary_key=True, autoincrement=True)
