from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import io
import os
import sys

# Ensure root directory is in sys.path for Vercel deployment
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scraper import scrape_website
from app.ai_helper import (
    calculate_metrics,
    analyze_financials_ai,
    analyze_website_ai,
    generate_combined_ai_report,
    chat_with_analyst
)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Company Profit & Loss Intelligence Hub")

# Enable CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Establish template directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Input models
class FinancialsInput(BaseModel):
    revenue: float
    cogs: float
    marketing: float
    rnd: float
    overhead: float
    apiKey: Optional[str] = None

class WebsiteInput(BaseModel):
    url: str
    apiKey: Optional[str] = None

class CombinedInput(BaseModel):
    financials: Dict[str, Any]
    website: Dict[str, Any]
    apiKey: Optional[str] = None

class ChatInput(BaseModel):
    history: List[Dict[str, str]]
    message: str
    financials: Dict[str, Any]
    website: Dict[str, Any]
    apiKey: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    """
    Renders the main dashboard webpage.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/analyze-financials")
async def analyze_financials_endpoint(data: FinancialsInput):
    """
    Computes key financial metrics and runs AI CFO evaluation.
    """
    raw_data = {
        "revenue": data.revenue,
        "cogs": data.cogs,
        "marketing": data.marketing,
        "rnd": data.rnd,
        "overhead": data.overhead
    }
    metrics = calculate_metrics(raw_data)
    ai_report = analyze_financials_ai(raw_data, user_key=data.apiKey)
    
    return {
        "metrics": metrics,
        "ai_report": ai_report
    }

@app.post("/api/connect-website")
async def connect_website_endpoint(data: WebsiteInput):
    """
    Scrapes the target business website and returns brand insights + AI SWOT analysis.
    """
    if not data.url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
        
    scrape_res = scrape_website(data.url)
    if not scrape_res["success"]:
        return {
            "success": False,
            "error": scrape_res["error"],
            "website_info": scrape_res,
            "ai_report": f"Could not analyze website due to scraping error: {scrape_res['error']}"
        }
        
    ai_report = analyze_website_ai(scrape_res, user_key=data.apiKey)
    
    return {
        "success": True,
        "website_info": scrape_res,
        "ai_report": ai_report
    }

@app.post("/api/combined-report")
async def combined_report_endpoint(data: CombinedInput):
    """
    Generates a combined financial and website strategic business growth report.
    """
    ai_report = generate_combined_ai_report(data.financials, data.website, user_key=data.apiKey)
    return {
        "ai_report": ai_report
    }

@app.post("/api/chat")
async def chat_endpoint(data: ChatInput):
    """
    Converses with the virtual CFO chatbot, context-aware of financials and web details.
    """
    response_text = chat_with_analyst(
        history=data.history,
        user_message=data.message,
        financials=data.financials,
        website_info=data.website,
        user_key=data.apiKey
    )
    return {
        "response": response_text
    }

@app.post("/api/upload-csv")
async def upload_csv_endpoint(file: UploadFile = File(...)):
    """
    Helper to parse financial records from an uploaded CSV file.
    Expects format: Key, Value
    e.g.,
    Revenue, 250000
    COGS, 80000
    Marketing, 30000
    R&D, 40000
    Overhead, 50000
    """
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents), header=None, names=["metric", "value"])
        
        # Normalize keys
        metrics_dict = {}
        for _, row in df.iterrows():
            metric_name = str(row["metric"]).strip().lower()
            try:
                val = float(str(row["value"]).replace(",", "").strip())
            except ValueError:
                continue
                
            if "revenue" in metric_name or "sales" in metric_name:
                metrics_dict["revenue"] = val
            elif "cogs" in metric_name or "cost of goods" in metric_name:
                metrics_dict["cogs"] = val
            elif "marketing" in metric_name or "advertising" in metric_name or "sales spend" in metric_name:
                metrics_dict["marketing"] = val
            elif "r&d" in metric_name or "rnd" in metric_name or "research" in metric_name or "product" in metric_name:
                metrics_dict["rnd"] = val
            elif "overhead" in metric_name or "general" in metric_name or "rent" in metric_name or "admin" in metric_name:
                metrics_dict["overhead"] = val
                
        # Fill missing values
        for key in ["revenue", "cogs", "marketing", "rnd", "overhead"]:
            if key not in metrics_dict:
                metrics_dict[key] = 0.0
                
        return {
            "success": True,
            "financials": metrics_dict
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading CSV: {str(e)}")
