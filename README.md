#  Shopify Insights Scraper

This project is a Python-based FastAPI web application that extracts brand-related insights from Shopify-based e-commerce websites **without requiring Shopify's API**.

---

## Key Features

-  Scrape **product catalog**, **hero products**, **policies**, **FAQs**, and more
-  Extract **contact details**, **social media links**, and **about us**
-  Optionally uses **LLMs** to structure unstructured data
-  Competitor insight extraction via Google Search
-  PostgreSQL integration for persistent storage (optional)

---

##  Folder Structure
```bash
shopify_insights/
├── main.py # FastAPI application
├── scraper/
│ ├── init.py
│ ├── product.py
│ ├── homepage.py
│ ├── policies.py
│ ├── faqs.py
│ ├── contact.py
│ ├── social.py
│ └── utils.py
├── models/
│ └── schema.py # Pydantic models
├── requirements.txt
└── README.md

```

## ⚙ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/arthisri14/shopify-insights.git
cd shopify-insights
```

```bash
pip install -r requirements.txt
```
### Run the FastAPI App
```bash
Python run.app
```
### How to use the API
### POST /extract-insights
### Request Body:
```
{
  "website_url": "https://memy.co.in"
}
```



