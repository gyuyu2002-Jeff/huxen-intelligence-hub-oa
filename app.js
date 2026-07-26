// --- HUXEN OA Intelligence Hub - Application Script ---

// 1. Tenders Data (Photocopiers / Multi-function Printers / MFP / Printer only)
const tenders = window.tendersData || [
  {
    id: 1,
    category: "事務機",
    title: "115年度多功能數位彩色複合機與列印管理系統租賃採購案",
    agency: "財政部臺北國稅局",
    location: "台北",
    budget: "380 萬",
    deadline: "08/05",
    days: 11,
    priority: "高",
    sourceUrl: "https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain=NzEyODEwMzk",
    details: "本案採購項目包含多功能數位複合機（彩色/黑白）共32台，包含網路列印控管系統建置、刷卡取件機制、LDAP/AD 帳號整合以及每月用印抄表計費維護服務。資安需求包括硬碟資料清除機制、日誌留存及弱點管理評核。"
  },
  {
    id: 2,
    category: "事務機",
    title: "臺中區漁會漁民活動中心及辦事處設備購置－事務機器",
    agency: "臺中區漁會",
    location: "台中",
    budget: "31 萬",
    deadline: "07/28",
    days: 4,
    priority: "中",
    sourceUrl: "https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain=NzEyODEwNTM",
    details: "採購中型數位複合機2台、辦公雷射印表機3台及相關耗材零件。需含安裝設定、既有驅動整合，並提供一年期到府維護服務。"
  },
  {
    id: 3,
    category: "事務機",
    title: "115-116年度辦公室數位黑白及彩色影印機租賃服務案",
    agency: "高雄市立美術館",
    location: "高雄",
    budget: "95 萬",
    deadline: "08/12",
    days: 18,
    priority: "中",
    sourceUrl: "https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain=NzEyODA0OTY",
    details: "高雄市立美術館及行政庫房辦公室數位黑白及彩色影印機/複合機租賃服務，租期為24個月。機型規格需達每分鐘30張以上輸出，並具備環保標章與低能耗認證。"
  },
  {
    id: 4,
    category: "事務機",
    title: "115年高速彩色與黑白數位複合機採購案",
    agency: "國立臺灣大學",
    location: "台北",
    budget: "120 萬",
    deadline: "08/02",
    days: 8,
    priority: "高",
    sourceUrl: "https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain=NzEyNzgxMTE",
    details: "臺灣大學行政大樓與圖書館高速彩色複合機5台、黑白複合機8台購置。要求廠商具備原廠授權書、環保標章、能效等級標章。投標文件需檢附詳細規格對應表。"
  },
  {
    id: 5,
    category: "事務機",
    title: "115年度辦公室印表設備與多功能複合機按張計費勞務採購案",
    agency: "台灣電力公司南投區營業處",
    location: "南投",
    budget: "165 萬",
    deadline: "08/08",
    days: 14,
    priority: "高",
    sourceUrl: "https://web.pcc.gov.tw/tps/QueryTender/query/searchTenderDetail?pkPmsMain=NzEyNzc5ODk",
    details: "本案採按張計費（Pay-per-page）之勞務委外模式，包含設備租用、定期維護、碳粉零件供應。基本張數彩色每月5,000張，黑白80,000張。超出部分需載明單張計費單價。"
  }
];

// 2. Competitors Data
const competitors = [
  {
    brand: "FUJIFILM BI",
    family: "Apeos",
    signal: "強調安全、雲端文件流程、行動連線與遠端維運。",
    response: "把比較焦點從單機規格拉回帳號權限、跨據點流程、維護窗口與整體服務責任。",
    talk: "如果安全與雲端是重點，我們建議不要只比功能表，而是一起確認誰負責權限、流程整合與後續維運，才能看出真正的使用成本。",
    question: "目前掃描文件最後會進到哪個系統？權限與異常事件由誰管理？",
    source: "https://www.fujifilm.com/us/en/business/office-printers"
  },
  {
    brand: "Canon",
    family: "imageFORCE / imageRUNNER ADVANCE DX",
    signal: "聚焦企業工作流程、掃描效率、設備管理與安全。",
    response: "先拆解客戶真正使用的掃描、OCR、簽核及儲存情境，再對應 RICOH 可落地的流程方案。",
    talk: "規格都能列得很完整，真正影響同仁效率的是文件從掃描到歸檔要經過幾個步驟；我們可以直接用您的實際流程做驗證。",
    question: "最常掃描的是合約、發票還是公文？後續需要命名、分類或簽核嗎？",
    source: "https://tw.canon/zh_TW/business/products/search?category=printing&subCategory=multi-functional-devices"
  },
  {
    brand: "Konica Minolta",
    family: "bizhub",
    signal: "以彩色品質、應用程式擴充、工作流程與生產型列印延伸切入。",
    response: "確認客戶是在意色彩輸出，還是需要文件自動化；兩種需求應以不同測試稿與效益指標回應。",
    talk: "如果重點是色彩，我們用實際文件比較一致性；如果重點是流程，就用每份文件可減少多少人工步驟來評估，避免只看展示功能。",
    question: "彩色輸出的品質要求來自品牌文件，還是一般辦公用途？每月實際量有多少？",
    source: "https://www.konicaminolta.com/"
  },
  {
    brand: "Sharp",
    family: "A3 MFP",
    signal: "主打大型觸控操作、混合辦公、智慧掃描與設備安全。",
    response: "把操作便利轉換成可量化的上手時間、誤操作率與教育成本，再比較服務可及性。",
    talk: "介面看起來直覺只是第一步，我們更在意不同部門是否能快速上手，以及人員異動後是否仍能穩定使用。",
    question: "目前最常發生的操作問題是掃描設定、登入，還是耗材與故障通報？",
    source: "https://www.sharp.eu/printers-photocopiers/sharp-a3-range"
  },
  {
    brand: "Epson",
    family: "WorkForce Enterprise",
    signal: "以 Heat-Free 商用噴墨、低耗能、低介入次數與環境效益切入。",
    response: "將能源優勢放入完整 TCO，連同耗材、紙材相容性、停機、服務反應及輸出需求一起計算。",
    talk: "節能值得比較，但不能只看瞬間功耗；我們建議把耗材、維護、紙材、停機與服務都放進同一張三年成本表。",
    question: "貴單位最重視的是電力、碳排數據，還是整體三年營運成本？",
    source: "https://epson.com/office-printers"
  },
  {
    brand: "HP",
    family: "LaserJet Enterprise",
    signal: "強調內建防護、裝置韌性、企業設備管理與分散式列印。",
    response: "區分單機安全功能與全生命週期治理，確認韌體、帳號、日誌、弱點與維護責任是否能持續落實。",
    talk: "安全不是買到一個功能就完成，我們會協助把韌體、權限、日誌與維護責任整理成可稽核的管理流程。",
    question: "印表設備是否已納入資產盤點、韌體更新與資安事件通報？",
    source: "https://www.hp.com/us-en/printers/enterprise-printers.html"
  }
];

// 3. State Management
let savedTenders = JSON.parse(localStorage.getItem('savedTenders')) || [1, 3]; // Default saved ids
let searchQuery = "";
let filterLocation = "";
let sortBy = "days-asc"; // default sort by urgency
let activeTab = "active"; // "active" or "award"

// Helper to parse budget string to number for sorting and filtering
function parseBudgetVal(budgetStr) {
  if (!budgetStr || budgetStr.includes("未定")) return -1;
  const match = budgetStr.match(/([\d\.]+)\s*萬/);
  if (match) {
    return parseFloat(match[1]) * 10000;
  }
  const cleanStr = budgetStr.replace(/[^\d]/g, '');
  return cleanStr ? parseInt(cleanStr) : -1;
}

// 4. DOM Elements
const tenderListEl = document.getElementById('tender-list');
const resultCountEl = document.getElementById('result-count-num');
const metricNewTendersEl = document.getElementById('metric-new-tenders');
const metricSavedEl = document.getElementById('metric-saved');
const metricAwardsEl = document.getElementById('metric-awards');
const searchInputEl = document.getElementById('search-input');
const refreshButtonEl = document.getElementById('refresh-button');
const competitorGridEl = document.getElementById('competitor-grid');

const filterLocationEl = document.getElementById('filter-location');
const sortByEl = document.getElementById('sort-by');
const tabActiveEl = document.getElementById('tab-active-tenders');
const tabAwardEl = document.getElementById('tab-award-tenders');
const radarSubtitleEl = document.getElementById('radar-subtitle');

// Modals
const guideModalEl = document.getElementById('guide-modal');
const detailModalEl = document.getElementById('detail-modal');
const btnGuideTriggerEl = document.getElementById('btn-guide-trigger');

// 5. Render Functions
function renderTenders() {
  const currentSource = activeTab === "active" ? tenders : (window.tendersAwardData || []);
  
  // 1. Filter
  let filtered = currentSource.filter(t => {
    // Search filter
    const q = searchQuery.trim().toLowerCase();
    if (q) {
      const matchSearch = (
        t.title.toLowerCase().includes(q) ||
        t.agency.toLowerCase().includes(q) ||
        t.location.toLowerCase().includes(q)
      );
      if (!matchSearch) return false;
    }

    // Location filter
    if (filterLocation) {
      if (!t.location.toLowerCase().includes(filterLocation.toLowerCase())) {
        return false;
      }
    }

    return true;
  });

  // 2. Sort
  if (activeTab === "active") {
    if (sortBy === "days-asc") {
      filtered.sort((a, b) => a.days - b.days);
    } else if (sortBy === "budget-desc") {
      filtered.sort((a, b) => {
        const valA = parseBudgetVal(a.budget);
        const valB = parseBudgetVal(b.budget);
        if (valA === -1 && valB !== -1) return 1;
        if (valB === -1 && valA !== -1) return -1;
        return valB - valA;
      });
    } else if (sortBy === "days-desc") {
      filtered.sort((a, b) => a.id - b.id);
    }
  } else {
    // Award tab sorting
    if (sortBy === "budget-desc") {
      filtered.sort((a, b) => {
        const valA = parseBudgetVal(a.awardAmount);
        const valB = parseBudgetVal(b.awardAmount);
        if (valA === -1 && valB !== -1) return 1;
        if (valB === -1 && valA !== -1) return -1;
        return valB - valA;
      });
    } else {
      // Default to resolution date (newest first, which is original array index order)
      filtered.sort((a, b) => a.id - b.id);
    }
  }

  // 3. Render HTML
  if (filtered.length === 0) {
    tenderListEl.innerHTML = `<div class="empty-state">沒有符合條件的項目，請調整搜尋或篩選條件。</div>`;
  } else {
    tenderListEl.innerHTML = filtered.map(t => {
      if (activeTab === "active") {
        const isSaved = savedTenders.includes(t.id);
        return `
          <article class="tender-row" data-id="${t.id}">
            <div class="tender-icon">OA</div>
            <div class="tender-main">
              <div class="tender-head">
                <span class="tender-priority ${t.priority === '高' ? 'high' : 'mid'}">${t.priority}優先</span>
                <h3 class="tender-click-title" style="cursor:pointer;" onclick="openTenderDetail(${t.id}, 'active')">${t.title}</h3>
              </div>
              <p class="tender-agency">${t.agency}<span>·</span>${t.location}</p>
              <div class="tender-meta">
                <span>預算 <b>${t.budget}</b></span>
                <span>截止 <b>${t.deadline}</b></span>
                <span class="${t.days <= 10 ? 'urgent' : ''}">剩 ${t.days} 天</span>
                <a href="${t.sourceUrl}" target="_blank" rel="noreferrer" class="tender-link">開啟案件 ↗</a>
                <button class="tender-btn-ai" onclick="openTenderDetail(${t.id}, 'active')">✨ AI 投標分析</button>
              </div>
            </div>
            <button class="btn-save ${isSaved ? 'saved' : ''}" onclick="toggleSave(${t.id}, event)" aria-label="${isSaved ? '取消收藏' : '收藏'}">
              ${isSaved ? '★' : '☆'}
            </button>
          </article>
        `;
      } else {
        // Award tab layout
        return `
          <article class="tender-row award-row" data-id="${t.id}">
            <div class="tender-icon" style="background: var(--green-soft); color: var(--green); border-color: var(--green);">🏆</div>
            <div class="tender-main">
              <div class="tender-head">
                <span class="tender-priority" style="background: var(--green-soft); color: var(--green);">已決標</span>
                <h3 class="tender-click-title" style="cursor:pointer;" onclick="openTenderDetail(${t.id}, 'award')">${t.title}</h3>
              </div>
              <p class="tender-agency">${t.agency}<span>·</span>${t.location}</p>
              <div class="tender-meta">
                <span>預算 <b>${t.budget}</b></span>
                <span style="color: var(--green);">決標 <b>${t.awardAmount}</b></span>
                <span>底價 <b>${t.basePrice}</b></span>
                <span>決標日 <b>${t.date}</b></span>
                <a href="${t.sourceUrl}" target="_blank" rel="noreferrer" class="tender-link" style="color: var(--green); border-color: var(--green-soft);">決標公告 ↗</a>
                <button class="tender-btn-ai award" onclick="openTenderDetail(${t.id}, 'award')">🏆 決標行情分析</button>
              </div>
            </div>
          </article>
        `;
      }
    }).join('');
  }

  // Update count
  resultCountEl.textContent = filtered.length;
  metricNewTendersEl.textContent = tenders.length;
  metricSavedEl.textContent = savedTenders.length;
  if (metricAwardsEl) {
    metricAwardsEl.textContent = (window.tendersAwardData || []).length;
  }
}

function renderCompetitors() {
  competitorGridEl.innerHTML = competitors.map((c, idx) => {
    return `
      <article class="competitor-card">
        <div class="comp-head">
          <span class="comp-idx">0${idx + 1}</span>
          <div class="comp-name">
            <h3>${c.brand}</h3>
            <p>${c.family}</p>
          </div>
          <a href="${c.source}" target="_blank" rel="noreferrer" class="comp-source">官方來源 ↗</a>
        </div>
        
        <div class="intel-block">
          <b>競品主打</b>
          <p>${c.signal}</p>
        </div>
        
        <div class="intel-block ricoh">
          <b>RICOH 回應</b>
          <p>${c.response}</p>
        </div>
        
        <blockquote>「${c.talk}」</blockquote>
        
        <div class="comp-probe">
          <span>探詢問題</span>
          <p>${c.question}</p>
        </div>
        
        <button class="btn-copy" onclick="copyTalkText('${c.brand}', \`${c.talk.replace(/`/g, '\\`').replace(/\$/g, '\\$')}\`, this)">
          複製業務話術
        </button>
        
        <div class="fallback-wrapper" id="fallback-${c.brand.replace(/\s+/g, '')}" style="display: none;">
          <div class="copy-fallback">
            瀏覽器未允許自動複製，請手動複製下方文字：
            <textarea readOnly onclick="this.select()">${c.talk}</textarea>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

// 6. Action Functions
window.toggleSave = function(id, event) {
  event.stopPropagation();
  if (savedTenders.includes(id)) {
    savedTenders = savedTenders.filter(item => item !== id);
  } else {
    savedTenders.push(id);
  }
  localStorage.setItem('savedTenders', JSON.stringify(savedTenders));
  renderTenders();
};

window.copyTalkText = function(brand, text, btnElement) {
  const fallbackId = `fallback-${brand.replace(/\s+/g, '')}`;
  const fallbackEl = document.getElementById(fallbackId);
  
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text)
      .then(() => {
        btnElement.textContent = "已複製話術 ✓";
        btnElement.classList.add('copied');
        fallbackEl.style.display = 'none';
        
        setTimeout(() => {
          btnElement.textContent = "複製業務話術";
          btnElement.classList.remove('copied');
        }, 2000);
      })
      .catch(err => {
        console.error('Clipboard copy failed:', err);
        fallbackEl.style.display = 'block';
      });
  } else {
    fallbackEl.style.display = 'block';
  }
};

window.openTenderDetail = function(id, type = 'active') {
  const dataSource = type === 'active' ? tenders : (window.tendersAwardData || []);
  const tender = dataSource.find(t => t.id === id);
  if (!tender) return;

  document.getElementById('detail-title').textContent = tender.title;
  document.getElementById('detail-agency-loc').innerHTML = `${tender.agency} <span>·</span> ${tender.location}`;
  
  const aiBlock = document.getElementById('detail-ai-block');
  const awardBlock = document.getElementById('detail-award-block');
  const activeBudgetTable = document.querySelector('#detail-modal .guide-table');
  const historySec = document.getElementById('detail-history-sec');
  const historyList = document.getElementById('detail-history-list');
  
  if (type === 'active') {
    if (aiBlock) aiBlock.style.display = 'block';
    if (awardBlock) awardBlock.style.display = 'none';
    if (activeBudgetTable) activeBudgetTable.style.display = 'table';
    
    // Render dynamic historical records table
    if (historySec && historyList) {
      if (tender.historyRecords && tender.historyRecords.length > 0) {
        historySec.style.display = 'block';
        let html = `
          <table class="guide-table" style="font-size: 11px; width: 100%;">
            <thead>
              <tr style="background: var(--blue-soft); color: var(--blue-deep);">
                <th style="padding: 6px; text-align: left;">日期</th>
                <th style="padding: 6px; text-align: left;">歷史標案名稱</th>
                <th style="padding: 6px; text-align: right;">預算</th>
                <th style="padding: 6px; text-align: right;">決標金</th>
                <th style="padding: 6px; text-align: center;">折數</th>
              </tr>
            </thead>
            <tbody>
        `;
        tender.historyRecords.forEach(h => {
          html += `
            <tr>
              <td style="padding: 6px; font-weight: 500; font-family: var(--font-sans);">${h.date}</td>
              <td style="padding: 6px; max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${h.title}">${h.title}</td>
              <td style="padding: 6px; text-align: right; font-family: var(--font-sans);">${h.budget}</td>
              <td style="padding: 6px; text-align: right; color: var(--green); font-weight: 700; font-family: var(--font-sans);">${h.awardAmount}</td>
              <td style="padding: 6px; text-align: center; font-weight: 700; color: var(--blue); font-family: var(--font-sans);">${h.ratio}</td>
            </tr>
          `;
        });
        html += `
            </tbody>
          </table>
        `;
        historyList.innerHTML = html;
      } else {
        historySec.style.display = 'none';
      }
    }
    
    document.getElementById('detail-budget').textContent = tender.budget;
    document.getElementById('detail-deadline').textContent = tender.deadline;
    document.getElementById('detail-days').textContent = `剩 ${tender.days} 天`;
    if (tender.days <= 10) {
      document.getElementById('detail-days').classList.add('urgent');
    } else {
      document.getElementById('detail-days').classList.remove('urgent');
    }
    
    document.getElementById('detail-ai-competitor').textContent = tender.aiCompetitor || "暫無對手威脅評估。";
    document.getElementById('detail-ai-target-price').textContent = tender.aiTargetPrice || "暫無得標底價估計。";
    
    document.getElementById('detail-desc-sec').style.display = 'block';
    document.getElementById('detail-desc').innerHTML = `<p>${tender.details}</p>`;
    document.getElementById('detail-link-btn').innerHTML = "前往政府電子採購網招標公告 ↗";
    document.getElementById('detail-link-btn').style.color = "";
    document.getElementById('detail-link-btn').style.borderColor = "";
  } else {
    if (aiBlock) aiBlock.style.display = 'none';
    if (awardBlock) awardBlock.style.display = 'block';
    if (activeBudgetTable) activeBudgetTable.style.display = 'none';
    if (historySec) historySec.style.display = 'none';
    
    document.getElementById('detail-award-base').textContent = tender.basePrice || "未公告底價";
    document.getElementById('detail-award-amount').textContent = tender.awardAmount || "未定";
    document.getElementById('detail-award-date').textContent = tender.date || "未知";
    
    // Calculate ratio
    let ratioText = "無法計算 (預算或底價未公開)";
    const awardVal = parseBudgetVal(tender.awardAmount);
    const baseVal = parseBudgetVal(tender.basePrice);
    const budgetVal = parseBudgetVal(tender.budget);
    
    if (awardVal > 0 && baseVal > 0) {
      ratioText = ((awardVal / baseVal) * 100).toFixed(1) + "% (決標價 / 底價)";
    } else if (awardVal > 0 && budgetVal > 0) {
      ratioText = ((awardVal / budgetVal) * 100).toFixed(1) + "% (決標價 / 預算比)";
    }
    document.getElementById('detail-award-ratio').textContent = ratioText;
    
    document.getElementById('detail-desc-sec').style.display = 'none';
    document.getElementById('detail-link-btn').innerHTML = "前往政府電子採購網決標公告 ↗";
    document.getElementById('detail-link-btn').style.color = "var(--green)";
    document.getElementById('detail-link-btn').style.borderColor = "var(--green-soft)";
  }
  
  document.getElementById('detail-link-btn').setAttribute('href', tender.sourceUrl);
  
  openModal(detailModalEl);
};

function openModal(modalEl) {
  modalEl.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModal(modalEl) {
  modalEl.classList.remove('active');
  document.body.style.overflow = '';
}

// 7. Event Listeners
searchInputEl.addEventListener('input', (e) => {
  searchQuery = e.target.value;
  renderTenders();
});

// Dropdown filter change listeners (ezbid style)
if (filterLocationEl) {
  filterLocationEl.addEventListener('change', (e) => {
    filterLocation = e.target.value;
    renderTenders();
  });
}
if (sortByEl) {
  sortByEl.addEventListener('change', (e) => {
    sortBy = e.target.value;
    renderTenders();
  });
}

// Tab Click Event Listeners
if (tabActiveEl && tabAwardEl) {
  tabActiveEl.addEventListener('click', () => {
    activeTab = "active";
    tabActiveEl.classList.add('active');
    tabAwardEl.classList.remove('active');
    if (radarSubtitleEl) radarSubtitleEl.textContent = "依截止日與商機適配度排序";
    sortBy = "days-asc";
    if (sortByEl) sortByEl.value = "days-asc";
    renderTenders();
  });
  
  tabAwardEl.addEventListener('click', () => {
    activeTab = "award";
    tabActiveEl.classList.remove('active');
    tabAwardEl.classList.add('active');
    if (radarSubtitleEl) radarSubtitleEl.textContent = "依決標公告日期排序";
    sortBy = "days-desc";
    if (sortByEl) sortByEl.value = "days-desc";
    renderTenders();
  });
}

refreshButtonEl.addEventListener('click', () => {
  searchInputEl.value = "";
  searchQuery = "";
  filterLocation = "";
  sortBy = "days-asc";
  activeTab = "active";
  
  if (filterLocationEl) filterLocationEl.value = "";
  if (sortByEl) sortByEl.value = "days-asc";
  if (tabActiveEl) tabActiveEl.classList.add('active');
  if (tabAwardEl) tabAwardEl.classList.remove('active');
  if (radarSubtitleEl) radarSubtitleEl.textContent = "依截止日與商機適配度排序";
  
  renderTenders();
  
  refreshButtonEl.textContent = "整理中...";
  refreshButtonEl.disabled = true;
  setTimeout(() => {
    refreshButtonEl.textContent = "重新整理畫面";
    refreshButtonEl.disabled = false;
  }, 1000);
});

btnGuideTriggerEl.addEventListener('click', () => {
  openModal(guideModalEl);
});

// Modal close button actions
document.querySelectorAll('.btn-close-modal').forEach(btn => {
  btn.addEventListener('click', (e) => {
    closeModal(e.target.closest('.modal-overlay'));
  });
});

document.querySelectorAll('.modal-overlay').forEach(overlay => {
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) {
      closeModal(overlay);
    }
  });
});

// Keyboard shortcuts
window.addEventListener('keydown', (e) => {
  // Focus search with Cmd/Ctrl + K
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault();
    searchInputEl.focus();
  }
  // Close modals with Escape
  if (e.key === 'Escape') {
    const activeModal = document.querySelector('.modal-overlay.active');
    if (activeModal) {
      closeModal(activeModal);
    }
  }
});

// Render Market Watch Trends
function renderMarketWatch() {
  const panel = document.getElementById('market-watch-panel');
  if (!panel) return;
  
  const marketWatchData = window.tendersMarketWatch || [
    {
      code: "SEC",
      title: "資安合規",
      text: "零信任架構、設備硬碟防護與管理日誌留存正全面進入政府機關採購規格限制中。",
      tone: "red"
    },
    {
      code: "ESG",
      title: "節能採購",
      text: "綠色能源效率標章、耗材碳足跡數據與包裝回收率已成為政商客戶評選加分項目。",
      tone: "green"
    },
    {
      code: "AI",
      title: "智慧維運",
      text: "用量主動預測、故障自動告警及遠端在線排除，可大幅降低客戶總持有維修成本。",
      tone: "blue"
    }
  ];

  const headerHtml = `
    <div class="panel-header compact">
      <div class="panel-title">
        <p class="kicker">MARKET WATCH</p>
        <h2>市場風向</h2>
      </div>
    </div>
  `;
  
  const listHtml = marketWatchData.map(e => `
    <article class="trend-card ${e.tone}">
      <span class="trend-icon">${e.code}</span>
      <div class="trend-info">
        <strong>${e.title}</strong>
        <p>${e.text}</p>
      </div>
    </article>
  `).join('');
  
  panel.innerHTML = headerHtml + `<div style="padding-top: 16px;">${listHtml}</div>`;
}

// 8. Initialization
function init() {
  renderTenders();
  renderCompetitors();
  renderMarketWatch();
  
  // Dynamic update date binding
  if (window.tendersLastUpdated) {
    const headerDateEl = document.getElementById('header-date-label');
    if (headerDateEl) {
      headerDateEl.textContent = `標案更新：${window.tendersLastUpdated} (以政府公告為準)`;
    }
    
    // Extract MM/DD (e.g. 2026/07/25 17:15 -> 07/25)
    const match = window.tendersLastUpdated.match(/\/(\d{2})\/(\d{2})/);
    if (match) {
      const metricDateEl = document.getElementById('metric-date-label');
      if (metricDateEl) {
        metricDateEl.textContent = `${match[1]}/${match[2]} 仍在招標`;
      }
    }
  }
}

init();
