import os
import google.generativeai as genai
from typing import List, Dict, Any

def get_api_key(user_key: str = None) -> str:
    """
    Resolves the Gemini API Key.
    Prioritizes key supplied in request, then env vars.
    """
    if user_key and user_key.strip():
        return user_key.strip()
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""

def get_gemini_response(prompt: str, system_instruction: str = "", user_key: str = None) -> str:
    """
    Configures and queries the Gemini API with the given prompt and system instructions.
    """
    api_key = get_api_key(user_key)
    if not api_key:
        raise ValueError("No API Key configured.")
    
    genai.configure(api_key=api_key)
    
    # Using gemini-1.5-flash as it is fast and efficient for dashboard insights
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction if system_instruction else None
    )
    
    response = model.generate_content(prompt)
    return response.text

def calculate_metrics(financials: Dict[str, Any]) -> Dict[str, Any]:
    """
    Helper to calculate margins and summaries from raw financial values.
    """
    # Safeguard inputs
    rev = float(financials.get('revenue', 0))
    cogs = float(financials.get('cogs', 0))
    mkt = float(financials.get('marketing', 0))
    rnd = float(financials.get('rnd', 0))
    overhead = float(financials.get('overhead', 0))
    
    gross_profit = rev - cogs
    operating_expenses = mkt + rnd + overhead
    net_profit = gross_profit - operating_expenses
    
    gross_margin = (gross_profit / rev * 100) if rev > 0 else 0
    net_margin = (net_profit / rev * 100) if rev > 0 else 0
    
    return {
        "revenue": rev,
        "cogs": cogs,
        "marketing": mkt,
        "rnd": rnd,
        "overhead": overhead,
        "gross_profit": gross_profit,
        "operating_expenses": operating_expenses,
        "net_profit": net_profit,
        "gross_margin": round(gross_margin, 2),
        "net_margin": round(net_margin, 2)
    }

def get_local_fallback_financials(metrics: Dict[str, Any]) -> str:
    """
    Local rules-based analysis of financials if Gemini is unavailable.
    """
    net_profit = metrics['net_profit']
    net_margin = metrics['net_margin']
    gross_margin = metrics['gross_margin']
    
    # Financial state analysis
    health = "Stable"
    if net_profit < 0:
        health = "CRITICAL (Unprofitable)"
    elif net_margin > 25:
        health = "EXCELLENT (High Profitability)"
    elif net_margin > 10:
        health = "HEALTHY"
        
    analysis = f"""### 📊 Financial Health: **{health}** (Local Rule Engine Sandbox)

*Note: Please configure a **Gemini API Key** in the top navigation bar to unlock advanced AI forecasting, SWOT reviews, and tailored strategic modeling.*

#### Key Metric Analysis:
1. **Gross Margin ({gross_margin}%):**
   * {"Healthy baseline. Your production cost is under control." if gross_margin > 50 else "Sub-optimal gross margin. Suggest auditing raw materials, software costs, or direct labor tariffs to improve pricing leverage."}
2. **Net Margin ({net_margin}%):**
   * {"Excellent operational leverage. Profits are flowing efficiently to the bottom line." if net_margin > 15 else "Tight net margins. High operational overhead or marketing burn is diluting sales revenue."}

#### Recommended Action Items:
* **Overhead Reduction:** Your overhead expenses constitute {round(metrics['overhead'] / (metrics['operating_expenses'] or 1) * 100, 1)}% of your operational expenses. Audit non-essential subscription software and lease options.
* **Customer Acquisition Cost (CAC):** Marketing accounts for {round(metrics['marketing'] / (metrics['operating_expenses'] or 1) * 100, 1)}% of total operating spend. Ensure digital acquisition channels (SEO, PPC) yield positive lifetime value (LTV:CAC > 3x).
"""
    return analysis

def get_local_fallback_website(website_info: Dict[str, Any]) -> str:
    """
    Local rules-based synthesis of website data if Gemini is unavailable.
    """
    title = website_info.get('title', 'Unknown Title')
    desc = website_info.get('description', 'No description found')
    domain = website_info.get('domain', '')
    
    analysis = f"""### 🌐 Website Analysis Summary (Local Sandbox Engine)

*Note: Set your **Gemini API Key** in the menu to generate a complete AI-driven brand positioning strategy and deep competitor benchmarking.*

* **Scraped Domain:** `{domain}`
* **Extracted Brand Title:** "{title}"
* **Meta Summary:** "{desc}"

#### Structural Observations:
* **SEO Integrity:** The website {"contains a descriptive meta tag for search engines" if desc else "is missing proper meta descriptions. This degrades organic search click-through rates (CTR)"}.
* **Brand Focus:** Based on headers, the company focuses on digital capabilities.
* **Ad-hoc Recommendation:** Boost site speed and integrate clear call-to-actions (CTAs) above the fold to maximize website traffic.
"""
    return analysis

def analyze_financials_ai(financials: Dict[str, Any], user_key: str = None) -> str:
    """
    Performs AI financial analysis. Falls back to local calculations if API fails.
    """
    metrics = calculate_metrics(financials)
    api_key = get_api_key(user_key)
    
    if not api_key:
        return get_local_fallback_financials(metrics)
        
    prompt = f"""
    Perform a professional financial analysis on the following company metrics:
    - Revenue: ${metrics['revenue']:,}
    - Cost of Goods Sold (COGS): ${metrics['cogs']:,}
    - Gross Profit: ${metrics['gross_profit']:,} (Gross Margin: {metrics['gross_margin']}%)
    - Operating Expenses:
      - Marketing/Sales: ${metrics['marketing']:,}
      - R&D/Product: ${metrics['rnd']:,}
      - General Overhead/Admin: ${metrics['overhead']:,}
      - Total OpEx: ${metrics['operating_expenses']:,}
    - Net Profit: ${metrics['net_profit']:,} (Net Margin: {metrics['net_margin']}%)
    
    Please provide:
    1. A concise Executive Summary of their financial performance.
    2. Deep observations about expense patterns (R&D vs Marketing vs Overhead).
    3. Actionable expense reduction strategies.
    4. Strategic ideas to boost the net profit margin.
    
    Format the response cleanly in professional Markdown. Keep the tone sharp, analytical, and highly advisory (like a veteran CFO).
    """
    
    sys_instruction = "You are a world-class CFO and financial analyst. Your reports are concise, professional, and full of highly practical, actionable financial advice."
    
    try:
        return get_gemini_response(prompt, sys_instruction, user_key)
    except Exception as e:
        return f"AI analysis failed ({str(e)}). Displaying local evaluation:\n\n" + get_local_fallback_financials(metrics)

def analyze_website_ai(website_info: Dict[str, Any], user_key: str = None) -> str:
    """
    Performs AI website profile analysis. Falls back to local calculations if API fails.
    """
    api_key = get_api_key(user_key)
    if not api_key:
        return get_local_fallback_website(website_info)
        
    prompt = f"""
    Analyze the scraped website profile for a company:
    - URL: {website_info.get('url')}
    - Domain: {website_info.get('domain')}
    - Page Title: {website_info.get('title')}
    - Meta Description: {website_info.get('description')}
    - Headings Extracted: {website_info.get('headings')}
    - Content Snippet: {website_info.get('body_text')}
    
    Please provide:
    1. An estimation of the Business Type & Primary Services/Offerings.
    2. Core Value Proposition (USP).
    3. Core Target Audience analysis.
    4. A SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats) based on their website presentation, SEO keywords, and messaging.
    
    Format as beautiful Markdown with clean headings.
    """
    
    sys_instruction = "You are a professional growth marketer and SEO auditor. You can extract brand positioning and strategize on online marketing channels instantly from text snippets."
    
    try:
        return get_gemini_response(prompt, sys_instruction, user_key)
    except Exception as e:
        return f"AI analysis failed ({str(e)}). Displaying local evaluation:\n\n" + get_local_fallback_website(website_info)

def generate_combined_ai_report(financials: Dict[str, Any], website_info: Dict[str, Any], user_key: str = None) -> str:
    """
    Synthesizes financial data and website profile to provide a holistic executive report.
    """
    metrics = calculate_metrics(financials)
    api_key = get_api_key(user_key)
    
    if not api_key:
        # Custom local combined fallback
        return f"""### 🏢 Integrated AI Business Summary (Local Sandbox Engine)

*Connect a **Gemini API Key** to synthesize custom business metrics with live web insights.*

* **Brand Title:** "{website_info.get('title', 'Unknown Brand')}" (`{website_info.get('domain', 'No domain connected')}`)
* **Net Revenue:** ${metrics['revenue']:,} | **Net Profit:** ${metrics['net_profit']:,} (Margin: {metrics['net_margin']}%)

#### Marketing Alignment Check:
Your marketing spend represents {round(metrics['marketing'] / (metrics['revenue'] or 1) * 100, 1)}% of total revenue. For a company offering digital services, this indicates a moderate marketing strategy. Ensure customer acquisition is optimized for the value propositions identified on your homepage.
"""
        
    prompt = f"""
    Perform a combined strategic analysis for a company based on its financial performance and website profile.
    
    Financial Data:
    - Revenue: ${metrics['revenue']:,}
    - Gross Profit Margin: {metrics['gross_margin']}%
    - Marketing Spend: ${metrics['marketing']:,} ({round(metrics['marketing']/(metrics['revenue'] or 1)*100, 1)}% of Revenue)
    - R&D/Product Development: ${metrics['rnd']:,} ({round(metrics['rnd']/(metrics['revenue'] or 1)*100, 1)}% of Revenue)
    - Overhead: ${metrics['overhead']:,} ({round(metrics['overhead']/(metrics['revenue'] or 1)*100, 1)}% of Revenue)
    - Net Profit Margin: {metrics['net_margin']}%
    
    Website Profile:
    - Domain: {website_info.get('domain')}
    - Title: {website_info.get('title')}
    - Description: {website_info.get('description')}
    - Snippet: {website_info.get('body_text')[:1000]}
    
    Tasks:
    1. Cross-reference the financial indicators with the website profile. Is the marketing spend appropriate for the type of business described on the website?
    2. Does the allocation of R&D expenses align with the digital and product profile found on the homepage?
    3. Identify 3 specific Growth and Efficiency experiments this company can perform next quarter combining website branding opportunities and financial constraints. For example, if cash is tight, recommend low-cost SEO or pricing adjustments. If margins are high and marketing is low, recommend aggressive growth experiments.
    
    Provide a highly detailed, executive advisory report in markdown.
    """
    
    sys_instruction = "You are an elite Management Consultant and Business Advisor. You analyze operational numbers and product-market fit to produce powerful business solutions."
    
    try:
        return get_gemini_response(prompt, sys_instruction, user_key)
    except Exception as e:
        return f"AI combined synthesis failed ({str(e)})."

def chat_with_analyst(history: List[Dict[str, str]], user_message: str, financials: Dict[str, Any], website_info: Dict[str, Any], user_key: str = None) -> str:
    """
    Drives a chat conversation with a virtual AI CFO.
    Maintains financial and website data as system context.
    """
    metrics = calculate_metrics(financials)
    api_key = get_api_key(user_key)
    
    # Financial context summary string
    context_summary = f"""
    The user's business context:
    - Revenue: ${metrics['revenue']:,}
    - COGS: ${metrics['cogs']:,}
    - Net Profit: ${metrics['net_profit']:,} (Margin: {metrics['net_margin']}%)
    - Operating Expenses: Marketing=${metrics['marketing']:,}, R&D=${metrics['rnd']:,}, Overhead=${metrics['overhead']:,}
    
    Website details:
    - Domain: {website_info.get('domain', 'Not connected')}
    - Title: {website_info.get('title', 'Not connected')}
    - Description: {website_info.get('description', 'Not connected')}
    """
    
    if not api_key:
        # Smart local rules chatbot responses
        msg_lower = user_message.lower()
        if "profit" in msg_lower or "net" in msg_lower or "revenue" in msg_lower:
            return f"Based on local metrics, your Revenue is **${metrics['revenue']:,}** with a Net Profit of **${metrics['net_profit']:,}** (Net Margin: **{metrics['net_margin']}%**). If you connect a Gemini API key, I can perform advanced forecasting or outline growth plans."
        elif "marketing" in msg_lower or "market" in msg_lower:
            return f"Your Marketing spend is **${metrics['marketing']:,}** ({round(metrics['marketing'] / (metrics['revenue'] or 1) * 100, 1)}% of Revenue). To review customer acquisition pathways and growth loops, please connect your Gemini API Key."
        elif "overhead" in msg_lower or "cost" in msg_lower or "expense" in msg_lower:
            return f"Operating expenses are **${metrics['operating_expenses']:,}** (COGS: ${metrics['cogs']:,}, Marketing: ${metrics['marketing']:,}, R&D: ${metrics['rnd']:,}, Overhead: ${metrics['overhead']:,}). I recommend auditing Overhead items if your margins need a boost."
        elif "website" in msg_lower or "site" in msg_lower:
            return f"Connected Website: **{website_info.get('domain', 'None')}**. Title: *\"{website_info.get('title', 'N/A')}\"*. Please connect a Gemini API Key to conduct search-intent alignment analyses."
        else:
            return f"Hello! I am your AI Business Analyst. I see your company has **${metrics['revenue']:,}** in revenue and **${metrics['net_profit']:,}** in net profits. Ask me about your expenses, margins, or connect a **Gemini API Key** in the top bar to activate full natural language answering!"

    # If api key is present, use Gemini API
    # Reconstruct history into Gemini structure or format a prompt with conversation history
    history_prompt = ""
    for msg in history[-10:]: # Keep last 10 turns to avoid context overflow
        role_label = "User" if msg['role'] == 'user' else "Assistant"
        history_prompt += f"\n{role_label}: {msg['content']}"
        
    history_prompt += f"\nUser: {user_message}"
    
    prompt = f"""
    You are chatting with a business owner.
    Here is their business context:
    {context_summary}
    
    Conversation History:
    {history_prompt}
    
    Assistant:
    """
    
    sys_instruction = "You are a professional Virtual CFO and AI Business Consultant. Use the user's financial details and scraped website profile to answer questions. Keep your answers concise, clear, and focused on profit expansion and business growth."
    
    try:
        return get_gemini_response(prompt, sys_instruction, user_key)
    except Exception as e:
        return f"AI Chat response failed due to API issue: {str(e)}. (Check your API key validity)"
