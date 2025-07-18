# app/api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

router = APIRouter()

class WebsiteInput(BaseModel):
    website_url: str

@router.post("/extract_brand_insights")
def extract_brand_insights(payload: WebsiteInput):
    website_url = payload.website_url

    try:
        response = requests.get(website_url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Website not reachable")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    soup = BeautifulSoup(response.content, "html.parser")

    # Example extraction logic
    product_list = [tag.get_text(strip=True) for tag in soup.find_all("h2")]
    privacy_policy = soup.find("a", href=lambda x: x and "privacy" in x.lower())
    about_us = soup.find("a", href=lambda x: x and "about" in x.lower())

    return {
        "website_url": website_url,
        "brand_data": {
            "product_catalog": product_list,
            "privacy_policy_link": privacy_policy["href"] if privacy_policy else None,
            "about_us_link": about_us["href"] if about_us else None,
        }
    }
