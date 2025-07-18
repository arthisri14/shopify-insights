from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.models.schemas import BrandRequest, BrandInsightsResponse, Product, FAQ
from app.db_models import BrandData
from app.database import SessionLocal, engine, Base

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List, Dict
import requests
import json
import webbrowser
import threading
import traceback
from fastapi.responses import JSONResponse

Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Shopify Brand Insights API",
    description="API that scrapes brand info from Shopify-based websites.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency: Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Global exception handler to capture unhandled errors
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Shopify Brand Insights API"}

# POST endpoint for brand insights
@app.post("/brand-insights", response_model=BrandInsightsResponse)
def get_brand_insights(request: BrandRequest, db: Session = Depends(get_db)):
    try:
        print("📥 Received website URL:", request.website_url)

        response = requests.get(request.website_url)
        print("🌐 Fetched URL with status code:", response.status_code)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch the website content.")

        soup = BeautifulSoup(response.text, "html.parser")

        brand_name = soup.title.string.strip() if soup.title else "Unknown Brand"
        print("🏷️ Brand Name:", brand_name)

        # Dummy product
        sample_product = Product(
            title="Sample Product",
            price="$19.99",
            url=urljoin(request.website_url, "/products/sample-product")
        )

        # Construct and return response
        return BrandInsightsResponse(
            brand_name=brand_name,
            product_catalog=[sample_product],
            hero_products=[sample_product],
            privacy_policy=urljoin(request.website_url, "/policies/privacy-policy"),
            refund_policy=urljoin(request.website_url, "/policies/refund-policy"),
            faqs=[
                FAQ(
                    question="What is the return policy?",
                    answer="Returns accepted within 30 days."
                )
            ],
            social_handles={
                "instagram": "https://instagram.com/example",
                "facebook": "https://facebook.com/example"
            },
            contact_details={"email": "support@example.com"},
            about_brand="This is a demo about section from the Shopify brand.",
            important_links={"home": request.website_url}
        )

    except Exception as e:
        print("❌ Error in /brand-insights:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
