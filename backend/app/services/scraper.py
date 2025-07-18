import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from app.models.schemas import BrandInsightsResponse, Product, FAQ
import re

class ShopifyScraper:
    def __init__(self, base_url: str):
        if not base_url.startswith("http"):
            base_url = "https://" + base_url
        self.base_url = base_url.rstrip('/')
        if not self._is_shopify_store():
            raise ValueError("Provided URL is not a valid Shopify store")

    def _is_shopify_store(self):
        try:
            r = requests.get(self.base_url, timeout=10)
            return "shopify" in r.text.lower()
        except:
            return False

    def scrape(self) -> BrandInsightsResponse:
        return BrandInsightsResponse(
            brand_name=self._get_brand_name(),
            product_catalog=self._get_products(),
            hero_products=self._get_hero_products(),
            privacy_policy=self._get_policy("/policies/privacy-policy"),
            refund_policy=self._get_policy("/policies/refund-policy"),
            faqs=self._get_faqs(),
            social_handles=self._get_socials(),
            contact_details=self._get_contacts(),
            about_brand=self._get_about(),
            important_links=self._get_links()
        )

    def _get_html(self, path=""):
        url = urljoin(self.base_url, path)
        r = requests.get(url)
        return BeautifulSoup(r.text, 'lxml')

    def _get_brand_name(self):
        soup = self._get_html()
        return soup.title.text.strip() if soup.title else ""

    def _get_products(self):
        try:
            r = requests.get(urljoin(self.base_url, "/products.json"))
            data = r.json().get("products", [])
            return [Product(title=p["title"], price=str(p["variants"][0]["price"]), url=self.base_url + "/products/" + p["handle"]) for p in data]
        except:
            return []

    def _get_hero_products(self):
        soup = self._get_html()
        products = []
        for tag in soup.find_all('a', href=re.compile("/products/")):
            title = tag.text.strip()
            link = urljoin(self.base_url, tag['href'])
            if title:
                products.append(Product(title=title, url=link))
        return products[:5]  # Limit to top hero products

    def _get_policy(self, path):
        soup = self._get_html(path)
        return soup.get_text(separator="\n").strip()

    def _get_faqs(self):
        faqs = []
        soup = self._get_html("/pages/faqs")  # Try typical FAQ URL
        qas = soup.find_all(['h3', 'h4', 'p', 'li'])
        q, a = "", ""
        for tag in qas:
            if "?" in tag.text:
                q = tag.text.strip()
            elif q:
                a = tag.text.strip()
                faqs.append(FAQ(question=q, answer=a))
                q = ""
        return faqs[:10]

    def _get_socials(self):
        soup = self._get_html()
        socials = {}
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "instagram.com" in href:
                socials['instagram'] = href
            elif "facebook.com" in href:
                socials['facebook'] = href
            elif "tiktok.com" in href:
                socials['tiktok'] = href
        return socials

    def _get_contacts(self):
        soup = self._get_html("/pages/contact")
        text = soup.get_text()
        email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
        phone = re.findall(r'\+?\d[\d\s\-\(\)]{7,}', text)
        return {
            "email": email[0] if email else "",
            "phone": phone[0] if phone else ""
        }

    def _get_about(self):
        soup = self._get_html("/pages/about-us")
        return soup.get_text(separator="\n").strip()

    def _get_links(self):
        soup = self._get_html()
        links = {}
        for a in soup.find_all("a", href=True):
            text = a.text.strip().lower()
            if "order" in text:
                links["order_tracking"] = urljoin(self.base_url, a['href'])
            elif "blog" in text:
                links["blogs"] = urljoin(self.base_url, a['href'])
            elif "contact" in text:
                links["contact_us"] = urljoin(self.base_url, a['href'])
        return links
