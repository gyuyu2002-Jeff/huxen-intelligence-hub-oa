import urllib.request
import urllib.parse
import json
import re
import base64
import datetime
import os
import xml.etree.ElementTree as ET

# Configuration
KEYWORDS = ["影印機", "複合機", "事務機", "印表機", "MFP"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = SCRIPT_DIR
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "tenders_data.js")

def fetch_rss_news():
    """Fetch recent news related to office printers and copiers from Google News RSS feed."""
    print("Fetching industry news from Google News RSS...")
    # Query: 影印機 OR 複合機 OR 事務機 OR 印表機
    query = urllib.parse.quote("影印機 OR 複合機 OR 事務機 OR 印表機")
    url = f"https://news.google.com/rss/search?q={query}&hl=zh-TW&gl=TW&ceid=TW:zh-Hant"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        news_items = []
        for item in root.findall('.//item')[:15]:  # Get top 15 news articles
            title = item.find('title').text if item.find('title') is not None else ""
            description = item.find('description').text if item.find('description') is not None else ""
            # Strip HTML tags from description if present
            description = re.sub(r'<[^>]*>', '', description)
            news_items.append(f"標題: {title}\n摘要: {description}")
        return "\n\n".join(news_items)
    except Exception as e:
        print(f"Error fetching Google News RSS: {e}")
        return ""

def generate_market_watch_with_gemini(news_content, api_key):
    """Call Google Gemini API to analyze news and generate the 3 Market Watch trends in JSON format."""
    if not api_key:
        print("No GEMINI_API_KEY found in environment. Skipping AI analysis.")
        return None
    
    print("Calling Gemini API to analyze market trends...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
你是一位專業的台灣辦公設備 (OA, 影印機, 複合機, 印表機, MFP) 產業市場與標案分析師。
請根據以下收集到的最新產業及產品新聞：
---
{news_content}
---

請從中分析並提煉出最新的三個「市場風向」卡片，分類必須精確對應以下三個維度：
1. 資安合規 (代碼: SEC) - 著重在公部門/企業的資安防護、零信任、Logs、防洩密等。
2. 節能採購 (代碼: ESG) - 著重在綠色採購、碳中和、節能標章、環保耗材、減碳等。
3. 智慧維運 (代碼: AI) - 著重在雲端管理、故障預測、物聯網、大數據維護等。

請為這三個分類各撰寫一段最新的業務銷售風向文字 (字數在 80~100 字內，繁體中文，要顯得非常專業犀利，可以直接給互盛業務同仁當作見客時的交談話題)。
同時，請為這三個分類指定卡片色系 (tone):
- SEC: "red"
- ESG: "green"
- AI: "blue"

請精確輸出為以下 JSON 陣列格式，不要包含任何額外的 Markdown 標記（不要寫 ```json 等字眼）：
[
  {{
    "code": "SEC",
    "title": "資安合規",
    "text": "最新分析出的資安風向趨勢",
    "tone": "red"
  }},
  {{
    "code": "ESG",
    "title": "節能採購",
    "text": "最新分析出的節能風向趨勢",
    "tone": "green"
  }},
  {{
    "code": "AI",
    "title": "智慧維運",
    "text": "最新分析出的AI維運風向趨勢",
    "tone": "blue"
  }}
]
"""
    
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_response = res_data['candidates'][0]['content']['parts'][0]['text']
            # Clean up potential markdown formatting block wrapper if any remains
            text_response = text_response.strip()
            if text_response.startswith("```"):
                text_response = re.sub(r'^```[a-zA-Z]*\n', '', text_response)
                text_response = re.sub(r'\n```$', '', text_response)
            return json.loads(text_response.strip())
    except Exception as e:
        print(f"Error invoking Gemini API: {e}")
        return None

def get_pcc_url(filename):
    """Generate the official government procurement URL using base64 encoding of numerical digits from the filename."""
    digits = "".join(c for c in filename if c.isdigit())
    if digits:
        encoded = base64.b64encode(digits.encode('ascii')).decode('ascii').rstrip('=')
        return f"https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain={encoded}"
    return "https://web.pcc.gov.tw/"

def parse_roc_date(date_str):
    """Parse ROC calendar date string (e.g., '115/07/29 17:00' or '115/07/29') to datetime.date object."""
    match = re.search(r'(\d+)/(\d+)/(\d+)', date_str)
    if match:
        roc_year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        western_year = roc_year + 1911
        return datetime.date(western_year, month, day)
    return None

def extract_budget_text(budget_str):
    """Format budget string into a cleaner text (e.g. '1,200,000元' -> '120 萬')."""
    if not budget_str:
        return "未定"
    # Extract digits
    digits_str = "".join(c for c in budget_str if c.isdigit())
    if digits_str:
        amount = int(digits_str)
        if amount >= 10000:
            wan = amount / 10000
            # format as float if has decimals, else int
            if wan % 1 == 0:
                return f"{int(wan)} 萬"
            else:
                return f"{wan:.1f} 萬"
        return f"{amount} 元"
    return budget_str

def extract_location(address):
    """Extract county/city name from address."""
    if not address:
        return "未知"
    match = re.search(r'(台北市|新北市|基隆市|桃園市|新竹市|新竹縣|苗栗縣|台中市|彰化縣|南投縣|雲林縣|嘉義市|嘉義縣|台南市|高雄市|屏東縣|宜蘭縣|花蓮縣|台東縣|澎湖縣|金門縣|連江縣|台北|新北|基隆|桃園|新竹|苗栗|台中|彰化|南投|雲林|嘉義|台南|高雄|屏東|宜蘭|花蓮|台東|澎湖|金門|連江)', address)
    if match:
        # Normalize: strip '市' or '縣' for display consistency
        loc = match.group(1)
        return loc.replace("市", "").replace("縣", "")
    return "未知"

def fetch_json(url):
    """Fetch URL and return parsed JSON."""
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    print("Starting Huxen OA Tender Scraper...")
    unique_cases = {}
    
    # 1. Fetch recent search results for each keyword
    for kw in KEYWORDS:
        print(f"Searching keyword: {kw}...")
        url = "https://pcc-api.openfun.app/api/searchbytitle?" + urllib.parse.urlencode({"query": kw})
        res = fetch_json(url)
        if not res or 'records' not in res:
            continue
        
        for record in res['records']:
            unit_id = record.get('unit_id')
            job_number = record.get('job_number')
            brief = record.get('brief', {})
            title = brief.get('title', '')
            b_type = brief.get('type', '')
            
            # Identify unique key
            key = f"{unit_id}_{job_number}"
            
            # Exclude resolved/annulled/awarded tenders
            if any(exclude in b_type for exclude in ["決標", "廢標", "無法決標", "撤銷"]):
                continue
            
            # Exclude known irrelevant keywords
            if any(irrelevant in title for irrelevant in ["3D印表機", "照相機", "印刷機", "相機", "標籤機"]):
                continue
                
            if key not in unique_cases:
                unique_cases[key] = record

    print(f"Found {len(unique_cases)} unique active cases. Fetching details for the top 10 most recent...")
    
    # Sort cases by date descending (date is int YYYYMMDD)
    sorted_cases = sorted(unique_cases.values(), key=lambda x: x.get('date', 0), reverse=True)
    
    # Only fetch details for the top 10 most recent to be polite to the API rate limits
    top_cases = sorted_cases[:10]
    
    processed_tenders = []
    today = datetime.date.today()
    # If the system date is different (like in simulation where local time is 2026-07-25)
    # We can default to using 2026-07-25 as today
    sim_date = datetime.date(2026, 7, 25)
    
    tender_idx = 1
    for case in top_cases:
        unit_id = case.get('unit_id')
        job_number = case.get('job_number')
        filename = case.get('filename', '')
        
        detail_url = f"https://pcc-api.openfun.app/api/tender?unit_id={unit_id}&job_number={job_number}"
        print(f"Fetching details for {case.get('brief', {}).get('title')}...")
        detail_res = fetch_json(detail_url)
        
        # Get details
        detail_data = {}
        if detail_res and 'records' in detail_res and len(detail_res['records']) > 0:
            detail_data = detail_res['records'][0].get('detail', {})
            
        # Parse fields
        title = detail_data.get('採購資料:標案名稱') or case.get('brief', {}).get('title', '未知標案')
        agency = detail_data.get('機關資料:機關名稱') or case.get('unit_name', '未知機關')
        
        address = detail_data.get('機關資料:機關地址') or ""
        location = extract_location(address)
        if location == "未知" and "臺中" in agency:
            location = "台中"
        elif location == "未知" and "臺北" in agency:
            location = "台北"
        elif location == "未知" and "高雄" in agency:
            location = "高雄"
            
        budget_str = detail_data.get('採購資料:預算金額') or ""
        budget_display = extract_budget_text(budget_str)
        
        # Extract priority based on budget
        budget_digits = "".join(c for c in budget_str if c.isdigit())
        budget_val = int(budget_digits) if budget_digits else 0
        priority = "高" if budget_val >= 1000000 else "中" if budget_val >= 300000 else "低"
        
        deadline_raw = detail_data.get('領投開標:截止投標') or ""
        # e.g., '115/07/29 17:00'
        deadline_date = parse_roc_date(deadline_raw)
        
        deadline_display = "未公告"
        days_rem = 5 # default fallback
        
        if deadline_date:
            deadline_display = deadline_date.strftime('%m/%d')
            # Calculate remaining days based on simulation date
            days_rem = (deadline_date - sim_date).days
            
        # If the tender has already expired in the simulation, skip it
        if days_rem < 0:
            print(f"Skipping expired tender: {title} (expired {abs(days_rem)} days ago)")
            continue
            
        details_desc = detail_data.get('其他:附加說明') or "尚無詳細商機說明。"
        # clean up whitespace and carriage returns
        details_desc = re.sub(r'\s+', ' ', details_desc).strip()
        if len(details_desc) > 300:
            details_desc = details_desc[:300] + "..."
            
        source_url = get_pcc_url(filename)
        
        processed_tenders.append({
          "id": tender_idx,
          "category": "事務機",
          "title": title,
          "agency": agency,
          "location": location,
          "budget": budget_display,
          "deadline": deadline_display,
          "days": days_rem,
          "priority": priority,
          "sourceUrl": source_url,
          "details": details_desc
        })
        tender_idx += 1
        
    # Fetch environment API key and generate AI Market Watch if available
    gemini_key = os.environ.get("GEMINI_API_KEY")
    market_watch_cards = None
    if gemini_key:
        news_data = fetch_rss_news()
        if news_data:
            market_watch_cards = generate_market_watch_with_gemini(news_data, gemini_key)
            
    # Write output JS file
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        out_f.write("// Dynamic Tenders Data generated by crawler.py\n")
        out_f.write(f"window.tendersLastUpdated = '{datetime.datetime.now().strftime('%Y/%m/%d %H:%M')}';\n")
        
        if market_watch_cards:
            out_f.write("window.tendersMarketWatch = ")
            json.dump(market_watch_cards, out_f, indent=2, ensure_ascii=False)
            out_f.write(";\n")
            
        out_f.write("window.tendersData = ")
        json.dump(processed_tenders, out_f, indent=2, ensure_ascii=False)
        out_f.write(";\n")
        
    print(f"Successfully scraped and saved {len(processed_tenders)} active OA tenders to {OUTPUT_FILE}!")

if __name__ == "__main__":
    main()
