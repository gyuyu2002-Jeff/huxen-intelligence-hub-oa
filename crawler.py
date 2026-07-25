import urllib.request
import urllib.parse
import json
import re
import base64
import datetime
import os
import xml.etree.ElementTree as ET
import time

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

def generate_tender_ai_analysis(tender_title, agency, budget, details, api_key):
    """Generate professional competitor threat, target price, and sales strategy for a given tender."""
    if not api_key:
        return None
    
    print(f"Calling Gemini API to analyze sales strategy for: {tender_title}...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    prompt = f"""
你是一位高階的台灣公家機關辦公設備 (OA, 影印機, 複合機, MFP) 投標決策與競爭策略分析專家。
現有一筆台灣政府機關的複合機/影印機租賃與採購招標案，資料如下：
- 招標機關：{agency}
- 標案名稱：{tender_title}
- 預算金額：{budget}
- 詳細說明：{details}

請代表「互盛資訊 (RICOH)」進行智能投標沙盤推演與對手分析，並精確輸出為以下 JSON 格式（繁體中文，不要包含任何 Markdown 標記，不要寫 ```json 字樣）：
{{
  "aiCompetitor": "分析主要的競爭對手是誰（如台灣富士全錄 Fujifilm BI、台灣佳能 Canon、東芝 Toshiba 或 Epson 噴墨印表機），評估他們的威脅程度與優勢劣勢，字數在 70 字內。",
  "aiTargetPrice": "建議互盛的合理得標底價區間預估或報價折數策略（例如：建議以預算金額的 88% - 93% 投標，或提醒該機關以往走低價標需防禦低價競爭等），字數在 70 字內。",
  "aiStrategy": "給予互盛業務同仁的防禦與強攻策略（例如：強調 Ricoh 的零信任資安認證、文件掃描客製流程、或每月抄表維護責任等，如何寫規格防堵對手），字數在 80 字內。"
}}
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
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_response = res_data['candidates'][0]['content']['parts'][0]['text']
            text_response = text_response.strip()
            if text_response.startswith("```"):
                text_response = re.sub(r'^```[a-zA-Z]*\n', '', text_response)
                text_response = re.sub(r'\n```$', '', text_response)
            return json.loads(text_response.strip())
    except Exception as e:
        print(f"Error generating tender AI analysis: {e}")
        return None

def generate_mock_tender_ai_analysis(title, agency, budget):
    """Generate realistic rule-based OA business strategy when Gemini API key is not present."""
    if "法院" in agency or "檢察署" in agency or "稅局" in agency or "警察" in agency:
        competitor = "此案為高資安敏感機關，主要對手為台灣富士全錄 (Fujifilm BI)，其在司法與公家核心機關佔有率高，主打硬體加密防護。"
        target_price = "司法與警政機關對履約品質與後續維護要求極高，預估得標區間落於預算金額的 90% - 95%，不宜過度砍價搶標。"
        strategy = "建議同仁積極推廣 Ricoh 零信任資安架構，主打硬碟資料防護抹除（符合公部門最新資安指引）與完整用印日誌留存，在資安面上設立防線。"
    elif "學校" in agency or "大學" in agency or "國小" in agency or "高中" in agency:
        competitor = "教育單位預算極為吃緊，需嚴防台灣愛普生 (Epson) 以省電型微噴印表機進行低單價搶標，以及 Canon 以低階複合機切入。"
        target_price = "學校單位為傳統價格紅海，競爭極其激烈。建議合理投標區間為預算的 82% - 87% 進場，以防對手以破壞性低單價搶標。"
        strategy = "主攻複合機與列印管理系統之整合（如刷卡安全取件及師生計費點數拷貝），強調互盛優於同業的 2 小時快速到府維修與定期保養承諾。"
    else:
        competitor = "主要競爭對手為台灣佳能 (Canon) 與夏普 (Sharp)，兩者在此類公務機關多以租賃月租費與單張抄表費用折扣進行價格戰。"
        target_price = "預估得標區間為預算金額的 86% - 91%。此案建議提出符合大印量的合理標準合約，避免捲入無謂殺價。"
        strategy = "主打互盛 Smart Integration 雲端文件流程，強調能與該單位現有的文件簽核系統整合，並凸顯綠色採購環保與節能標章優勢。"
        
    return {
        "aiCompetitor": competitor,
        "aiTargetPrice": target_price,
        "aiStrategy": strategy
    }

def get_pcc_url(filename, date_int):
    """Generate the official government procurement redirector URL."""
    if filename and date_int:
        return f"https://web.pcc.gov.tw/prkms/tender/common/noticeDate/redirectPublic?ds={date_int}&fn={filename}.xml"
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

def extract_location(address, agency=""):
    """Extract county/city name from address or fall back to matching from the agency name."""
    if address:
        match = re.search(r'(台北市|新北市|基隆市|桃園市|新竹市|新竹縣|苗栗縣|台中市|彰化縣|南投縣|雲林縣|嘉義市|嘉義縣|台南市|高雄市|屏東縣|宜蘭縣|花蓮縣|台東縣|澎湖縣|金門縣|連江縣|台北|新北|基隆|桃園|新竹|苗栗|台中|彰化|南投|雲林|嘉義|台南|高雄|屏東|宜蘭|花蓮|台東|澎湖|金門|連江|臺北|臺中|臺南)', address)
        if match:
            # Normalize: strip '市' or '縣' for display consistency and convert 臺 to 台
            loc = match.group(1)
            return loc.replace("市", "").replace("縣", "").replace("臺", "台")
            
    if agency:
        # Check if agency contains city names
        match = re.search(r'(台北|新北|基隆|桃園|新竹|苗栗|台中|彰化|南投|雲林|嘉義|台南|高雄|屏東|宜蘭|花蓮|台東|澎湖|金門|連江|臺北|臺中|臺南)', agency)
        if match:
            return match.group(1).replace("臺", "台")
        # Custom logic for major organizations
        if "台灣電力" in agency:
            return "台北"
        if "榮民總醫院" in agency:
            if "台中" in agency or "臺中" in agency: return "台中"
            if "高雄" in agency: return "高雄"
            return "台北"
            
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
    unique_awards = {}
    
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
            
            # Check resolved/awarded tenders
            if any(exclude in b_type for exclude in ["決標", "廢標", "無法決標", "撤銷"]):
                if any(aw in b_type for aw in ["決標公告", "更正決標公告", "決標"]):
                    if key not in unique_awards:
                        unique_awards[key] = record
                continue
            
            # Exclude known irrelevant keywords
            if any(irrelevant in title for irrelevant in ["3D印表機", "照相機", "印刷機", "相機", "標籤機"]):
                continue
                
            if key not in unique_cases:
                unique_cases[key] = record

    print(f"Found {len(unique_cases)} unique active cases and {len(unique_awards)} unique award cases.")
    
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
        # Sleep for 1.5 seconds to respect the API rate limit and avoid 429
        time.sleep(1.5)
        
        # Get details
        detail_data = {}
        if detail_res and 'records' in detail_res and len(detail_res['records']) > 0:
            detail_data = detail_res['records'][0].get('detail', {})
            
        # Parse fields
        title = detail_data.get('採購資料:標案名稱') or case.get('brief', {}).get('title', '未知標案')
        agency = detail_data.get('機關資料:機關名稱') or case.get('unit_name', '未知機關')
        
        address = detail_data.get('機關資料:機關地址') or ""
        location = extract_location(address, agency)
            
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
            
        source_url = get_pcc_url(filename, case.get('date'))
        
        # AI strategy analysis
        ai_analysis = None
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            ai_analysis = generate_tender_ai_analysis(title, agency, budget_display, details_desc, gemini_key)
        if not ai_analysis:
            ai_analysis = generate_mock_tender_ai_analysis(title, agency, budget_display)
        
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
          "details": details_desc,
          "aiCompetitor": ai_analysis.get("aiCompetitor", ""),
          "aiTargetPrice": ai_analysis.get("aiTargetPrice", ""),
          "aiStrategy": ai_analysis.get("aiStrategy", "")
        })
        tender_idx += 1
        
    # 3. Fetch details for top resolved awards
    print("Fetching details for top resolved awards...")
    sorted_awards = sorted(unique_awards.values(), key=lambda x: x.get('date', 0), reverse=True)
    top_awards = sorted_awards[:8]
    processed_awards = []
    award_idx = 1
    for case in top_awards:
        unit_id = case.get('unit_id')
        job_number = case.get('job_number')
        filename = case.get('filename', '')
        
        detail_url = f"https://pcc-api.openfun.app/api/tender?unit_id={unit_id}&job_number={job_number}"
        print(f"Fetching award detail: {case.get('brief', {}).get('title')}...")
        detail_res = fetch_json(detail_url)
        time.sleep(1.5)
        
        detail_data = {}
        if detail_res and 'records' in detail_res and len(detail_res['records']) > 0:
            for r in detail_res['records']:
                if '決標' in r.get('brief', {}).get('type', ''):
                    detail_data = r.get('detail', {})
                    break
            if not detail_data:
                detail_data = detail_res['records'][0].get('detail', {})
                
        title = detail_data.get('已公告資料:標案名稱') or detail_data.get('採購資料:標案名稱') or case.get('brief', {}).get('title', '未知標案')
        agency = detail_data.get('機關資料:機關名稱') or case.get('unit_name', '未知機關')
        address = detail_data.get('機關資料:機關地址') or ""
        location = extract_location(address, agency)
        
        budget_str = detail_data.get('已公告資料:預算金額') or detail_data.get('採購資料:預算金額') or ""
        budget_display = extract_budget_text(budget_str)
        
        award_str = detail_data.get('決標資料:總決標金額') or ""
        award_display = extract_budget_text(award_str)
        
        base_str = detail_data.get('決標資料:底價金額') or ""
        base_display = extract_budget_text(base_str)
        
        raw_date = detail_data.get('決標資料:決標日期') or ""
        if raw_date:
            date_display = raw_date
        else:
            date_int = case.get('date', 0)
            if date_int:
                date_str = str(date_int)
                date_display = f"{int(date_str[:4])-1911}/{date_str[4:6]}/{date_str[6:]}"
            else:
                date_display = "未知"
                
        source_url = get_pcc_url(filename, case.get('date'))
        
        processed_awards.append({
            "id": award_idx,
            "title": title,
            "agency": agency,
            "location": location,
            "budget": budget_display,
            "awardAmount": award_display,
            "basePrice": base_display,
            "date": date_display,
            "sourceUrl": source_url
        })
        award_idx += 1
        
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
            
        out_f.write("window.tendersAwardData = ")
        json.dump(processed_awards, out_f, indent=2, ensure_ascii=False)
        out_f.write(";\n")
        
        out_f.write("window.tendersData = ")
        json.dump(processed_tenders, out_f, indent=2, ensure_ascii=False)
        out_f.write(";\n")
        
    print(f"Successfully scraped and saved {len(processed_tenders)} active and {len(processed_awards)} award OA tenders to {OUTPUT_FILE}!")

if __name__ == "__main__":
    main()
