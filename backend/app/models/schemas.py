from pydantic import BaseModel
from typing import List, Optional, Dict

class BrandRequest(BaseModel):
    website_url: str

class Product(BaseModel):
    title: str
    price: Optional[str]
    url: Optional[str]

class FAQ(BaseModel):
    question: str
    answer: str

class BrandInsightsResponse(BaseModel):
    brand_name: Optional[str]
    product_catalog: List[Product]
    hero_products: List[Product]
    privacy_policy: Optional[str]
    refund_policy: Optional[str]
    faqs: List[FAQ]
    social_handles: Dict[str, str]
    contact_details: Dict[str, str]
    about_brand: Optional[str]
    important_links: Dict[str, str]
