import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re

def scrape_website(url: str) -> dict:
    """
    Scrapes a website to extract key company profile information.
    Handles connection errors, timeouts, and HTML parsing.
    """
    url_to_fetch = url.strip()
    if not url_to_fetch.startswith(('http://', 'https://')):
        url_to_fetch = 'https://' + url_to_fetch
        
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # Fetching with a 10s timeout to prevent hanging
        response = requests.get(url_to_fetch, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to connect to {url_to_fetch}: {str(e)}",
            "url": url_to_fetch,
            "title": "",
            "description": "",
            "headings": [],
            "body_text": ""
        }
        
    try:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Preserve original soup for meta extraction, then decompose noise elements from working soup
        meta_soup = BeautifulSoup(html_content, 'html.parser')
        
        for element in soup(["script", "style", "noscript", "iframe", "svg", "header", "footer", "nav"]):
            element.decompose()
            
        title = meta_soup.title.string.strip() if meta_soup.title else ""
        
        # Extract meta description
        meta_desc = ""
        meta = meta_soup.find('meta', attrs={'name': re.compile(r'^description$', re.I)})
        if not meta:
            meta = meta_soup.find('meta', attrs={'property': re.compile(r'^og:description$', re.I)})
            
        if meta and meta.get('content'):
            meta_desc = meta.get('content').strip()
            
        # Extract headings
        headings = []
        for tag in ['h1', 'h2', 'h3']:
            for h in soup.find_all(tag):
                text = h.get_text().strip()
                # Clean multiple spaces/newlines
                text = re.sub(r'\s+', ' ', text)
                if text and len(text) > 3 and text not in headings:
                    headings.append(text)
                    
        # Extract paragraph body text
        paragraphs = []
        for p in soup.find_all(['p', 'span', 'li']):
            text = p.get_text().strip()
            text = re.sub(r'\s+', ' ', text)
            # Only count meaningful paragraphs
            if len(text) > 25 and text not in paragraphs:
                paragraphs.append(text)
                
        # Limit quantities to save context
        headings = headings[:20]
        paragraphs = paragraphs[:30]
        body_text = "\n".join(paragraphs)
        
        domain = urlparse(url_to_fetch).netloc
        
        return {
            "success": True,
            "url": url_to_fetch,
            "domain": domain,
            "title": title or domain,
            "description": meta_desc or (body_text[:150] + "..." if body_text else ""),
            "headings": headings,
            "body_text": body_text[:5000]  # Limit total chars to avoid LLM context blowup
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error parsing website content: {str(e)}",
            "url": url_to_fetch,
            "title": "",
            "description": "",
            "headings": [],
            "body_text": ""
        }
