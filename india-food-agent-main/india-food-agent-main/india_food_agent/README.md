# 🇮🇳 India Food Trend Agent
### Python + Web Scraping + Claude AI (LLM)

> Scrapes real food trends from Google, Zomato & Instagram — then uses Claude AI to generate high-margin weekend special dishes for any Indian city.

---

## 📁 Project Structure

```
india_food_agent/
│
├── app.py                    # 🖥  Streamlit dashboard (run this!)
├── main.py                   # ⌨  CLI runner
├── requirements.txt          # 📦 Python dependencies
├── .env                      # 🔑 Your API key (never commit!)
│
├── scraper/
│   └── trend_scraper.py      # 🕷  Web scraping (Google, Zomato, news, Instagram)
│
├── llm/
│   └── dish_generator.py     # 🤖 Claude AI analysis + dish generation
│
├── reports/
│   ├── report_generator.py   # 📄 Saves JSON / TXT / CSV reports
│   └── output/               # 📁 Generated reports saved here
│
└── data/                     # 📊 Cached scrape data (auto-created)
```

---

## 🚀 Quick Start

### 1. Clone / Download the project
```bash
cd india_food_agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Anthropic API key
```bash
# Edit .env file:
ANTHROPIC_API_KEY=your_key_here
```
Get your key at: https://console.anthropic.com

### 4. Run the Streamlit Dashboard (recommended)
```bash
streamlit run app.py
```
Opens at: http://localhost:8501

### 5. OR run via CLI
```bash
# Interactive mode
python main.py

# Direct mode
python main.py --city "Hyderabad" --type "Biryani House" --price "₹₹₹" --season "Monsoon"
```

---

## 🛠 Tech Stack

| Component        | Technology                          |
|-----------------|-------------------------------------|
| **Scraping**     | Python · requests · BeautifulSoup4 |
| **Sources**      | Google Search · Zomato · Times Food · NDTV Food · Instagram proxy |
| **LLM**          | Claude API (Anthropic)             |
| **UI Dashboard** | Streamlit                          |
| **Charts**       | Plotly                             |
| **Reports**      | JSON · TXT · CSV                   |

---

## 🌆 Supported Cities (25+)

South India: Hyderabad, Chennai, Bengaluru, Kochi, Vizag, Madurai, Mysuru

West India: Mumbai, Pune, Goa, Ahmedabad, Surat, Nashik

North India: Delhi, Lucknow, Amritsar, Chandigarh, Jaipur, Varanasi, Agra

East India: Kolkata, Bhubaneswar, Patna, Guwahati

Central India: Bhopal, Indore, Nagpur

---

## 📊 What It Does

### Step 1 — Scrape (scraper/trend_scraper.py)
- Scrapes **Google** for trending food queries in the selected city
- Scrapes **Zomato** trending collections & restaurants
- Scrapes **Times Food / NDTV Food** for food news articles
- Loads **Instagram hashtag** data (curated + growth metrics)

### Step 2 — Analyze with LLM (llm/dish_generator.py)
- Sends all scraped data to **Claude AI**
- Extracts: trending ingredients, famous dishes, viral hashtags, declining trends
- Identifies engagement patterns specific to the city

### Step 3 — Generate Dishes (llm/dish_generator.py)
- Claude generates **5 weekend specials** with:
  - 1 × High-Margin item
  - 1 × Premium Upsell
  - 1 × Instagrammable / Reels-worthy
  - 2 × Weekend Performers
- Each dish has: price (₹), food cost, gross margin %, plating tip, Reels tip, demand forecast

### Step 4 — Save Reports (reports/report_generator.py)
- **JSON**: Full machine-readable output
- **TXT**: Human-readable weekly report
- **CSV**: Dishes table (opens in Excel / Google Sheets)

---

## 🔑 Example Output

```
WEEKEND SPECIALS — HYDERABAD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Charcoal Dum Biryani
   💰 High Margin · ₹380–₹450 · 🔥 High Demand
   Inspired by: Paradise Biryani (Secunderabad)

2. Gulab Rose Khubani Panna Cotta
   👑 Premium Upsell · ₹280–₹320 · High Demand
   Inspired by: Traditional Hyderabadi double ka meetha

3. Smoke & Mirror Pathar Gosht Tacos
   📸 Instagrammable · ₹420–₹490 · High Demand
   Inspired by: Bawarchi Restaurant's pathar gosht

4. Irani Chai Crème Brûlée
   🔥 Weekend Hit · ₹180–₹220 · Medium Demand
   Inspired by: Nimrah Café, Charminar

5. Shah Ghouse-Style Haleem Sliders
   🔥 Weekend Hit · ₹320–₹380 · High Demand
   Inspired by: Shah Ghouse Café & Restaurant
```

---

## ⚠️ Notes

- **Scraping**: Google may occasionally block automated scraping — the app gracefully falls back to curated data + LLM knowledge
- **Rate limiting**: Built-in delays between requests to be polite to servers
- **API costs**: Each full run uses ~2,000–4,000 Claude tokens (~₹2–4 per run at current pricing)

---

## 📜 License
MIT — Free to use, modify, and deploy.
