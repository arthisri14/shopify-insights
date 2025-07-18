from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class BrandData(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hero_product = Column(String)
    description = Column(Text)
    privacy_policy = Column(Text)
    return_policy = Column(Text)
    social_links = Column(Text)
    faqs = Column(Text)
    contact_info = Column(Text)
