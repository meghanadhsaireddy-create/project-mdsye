"""
app.py  —  TrendAgent Streamlit Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run with:  streamlit run app.py
Theme: Editorial / Magazine — cream bg, dark dish cards, Playfair Display
"""

import streamlit as st
import json
import sys
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="TrendAgent — Hyper-Local Food Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS: TrendAgent Editorial Theme ────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700;1,900&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&family=DM+Mono:wght@400;500&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 400;
}

/* ── Page Background ── */
.main { background: #F5F2EC !important; }
.block-container { background: #F5F2EC !important; padding-top: 24px !important; }
section[data-testid="stSidebar"] { background: #EDEAD4 !important; border-right: 1px solid #DDD8CC; }

/* ── Hero Banner ── */
.hero-banner {
    background: #F5F2EC;
    border-bottom: 1.5px solid #E0DDD7;
    padding: 28px 0 20px;
    margin-bottom: 28px;
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F0C93A;
    color: #1A1A1A;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 14px;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 900;
    font-style: italic;
    line-height: 0.95;
    letter-spacing: -0.02em;
    color: #0D0D0D;
    margin: 10px 0 10px;
}
.hero-title span { color: #0D0D0D; font-style: normal; }
.hero-sub {
    font-size: 13px;
    color: #888;
    font-weight: 300;
    letter-spacing: 0.04em;
}

/* ── Sidebar styles ── */
.sidebar-logo {
    font-family: 'DM Mono', monospace;
    font-size: 15px;
    font-weight: 500;
    color: #0D0D0D;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 0 14px;
    border-bottom: 1px solid #DDD8CC;
    margin-bottom: 16px;
}
.logo-box {
    background: #0D0D0D;
    color: white;
    width: 30px; height: 30px;
    border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 18px;
    font-weight: 700;
    font-style: italic;
    color: #0D0D0D;
    margin: 24px 0 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #DDD8CC;
}
.section-label {
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #999;
    margin: 20px 0 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after { content: ''; flex: 1; height: 1px; background: #E0DDD7; }

/* ── Trend Panel (white card) ── */
.trend-panel {
    background: white;
    border-radius: 20px;
    padding: 28px;
    border: 1.5px solid #E0DDD7;
    margin-bottom: 20px;
}
.trend-panel-title {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    font-style: italic;
    color: #0D0D0D;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.trend-summary {
    font-size: 13px;
    line-height: 1.85;
    color: #555;
    font-weight: 300;
}

/* ── Color Swatches ── */
.swatches-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin: 20px 0;
}
.swatch-item { display: flex; flex-direction: column; gap: 6px; }
.swatch-block {
    width: 100%;
    aspect-ratio: 3/4;
    border-radius: 12px;
}
.swatch-lbl {
    font-size: 10px;
    color: #888;
    text-align: center;
    line-height: 1.4;
}

/* ── Ingredient Cards ── */
.ingredient-card {
    background: #F5F2EC;
    border: 1.5px solid #E0DDD7;
    border-radius: 16px;
    padding: 16px 18px;
    margin-bottom: 10px;
    position: relative;
    transition: box-shadow 0.2s;
}
.ingredient-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
.ing-tag {
    display: inline-block;
    font-size: 9px;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: 100px;
    margin-bottom: 8px;
}
.tag-viral    { background: #FEECEC; color: #C0392B; }
.tag-rising   { background: #FFF6D0; color: #A07800; }
.tag-stable   { background: #E8F5E9; color: #1A6E2E; }
.tag-steady   { background: #E8F5E9; color: #1A6E2E; }
.tag-hot      { background: #FEECEC; color: #C0392B; }
.tag-new      { background: #E8F0FF; color: #2C4DB3; }
.ing-score {
    position: absolute;
    top: 14px; right: 14px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #AAA;
}
.ing-name {
    font-family: 'Playfair Display', serif;
    font-size: 17px;
    font-weight: 700;
    color: #0D0D0D;
    margin-bottom: 6px;
    line-height: 1.2;
}
.ing-desc {
    font-size: 12px;
    color: #666;
    line-height: 1.65;
    font-weight: 300;
}

/* ── Dark Dish Cards (Weekend Specials) ── */
.dish-card-dark {
    background: #141414;
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 14px;
    border: 1px solid #2A2A2A;
    position: relative;
    overflow: hidden;
}
.dish-wm {
    position: absolute;
    right: 14px; top: 50%;
    transform: translateY(-50%);
    font-size: 68px;
    opacity: 0.06;
    color: white;
    line-height: 1;
    pointer-events: none;
}
.dish-num {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    color: #555;
    letter-spacing: 0.1em;
    margin-bottom: 12px;
}
.dish-dark-name {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 900;
    font-style: italic;
    color: white;
    line-height: 1.15;
    margin-bottom: 10px;
    max-width: 85%;
}
.dish-dark-desc {
    font-size: 12px;
    color: #777;
    line-height: 1.7;
    font-weight: 300;
    margin-bottom: 14px;
}
.dish-tags-row { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 16px; }
.dish-tag-dark {
    background: #252525;
    color: #999;
    border: 1px solid #333;
    padding: 4px 10px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 400;
}
.dish-footer-dark {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    padding-top: 14px;
    border-top: 1px solid #222;
}
.dish-target-lbl  { font-size: 8px; letter-spacing: 0.15em; text-transform: uppercase; color: #444; font-weight: 500; margin-bottom: 3px; }
.dish-target-txt  { font-size: 11px; color: #777; max-width: 200px; line-height: 1.4; }
.margin-lbl       { font-size: 8px; letter-spacing: 0.15em; text-transform: uppercase; color: #444; font-weight: 500; margin-bottom: 3px; text-align: right; }
.margin-high      { font-family: 'DM Mono', monospace; font-size: 13px; color: #3DC98A; font-weight: 500; }
.margin-medium    { font-family: 'DM Mono', monospace; font-size: 13px; color: #F0C93A; font-weight: 500; }
.margin-low       { font-family: 'DM Mono', monospace; font-size: 13px; color: #F05A5A; font-weight: 500; }

/* ── Ingredient Pill Cards (top-of-weekend) ── */
.ing-pill {
    background: #0D0D0D;
    color: white;
    border-radius: 12px;
    padding: 13px 16px;
    text-align: center;
    font-size: 13px;
    font-weight: 500;
}

/* ── Hashtag chips ── */
.htag {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 500;
    margin: 3px;
}
.htag-viral   { background: #FEECEC; color: #C0392B; border: 1px solid #F05A5A; }
.htag-hot     { background: #FFF6D0; color: #A07800; border: 1px solid #F0C93A; }
.htag-rising  { background: #E8F5E9; color: #1A6E2E; border: 1px solid #3DC98A; }
.htag-new     { background: #E8F0FF; color: #2C4DB3; border: 1px solid #6B8EF5; }

/* ── Strategic Insight ── */
.insight-box {
    background: #0D0D0D;
    color: white;
    border-radius: 18px;
    padding: 24px 28px;
    margin-top: 20px;
}
.insight-lbl { font-size: 9px; color: #F0C93A; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 500; margin-bottom: 10px; }
.insight-txt { font-size: 14px; color: #999; line-height: 1.8; font-weight: 300; }
.insight-rev { margin-top: 14px; font-size: 12px; color: #555; border-top: 1px solid #222; padding-top: 12px; }

/* ── Scraped Data Cards ── */
.scrape-card {
    background: white;
    border: 1px solid #E0DDD7;
    border-left: 3px solid #0D0D0D;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
}
.scrape-title { font-weight: 600; font-size: 12px; color: #0D0D0D; }
.scrape-sub   { font-size: 11px; color: #888; margin-top: 3px; }

/* ── Badge styles ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.badge-margin    { background: #E8F5E9; color: #1A6E2E; }
.badge-premium   { background: #F3E8FF; color: #6B21A8; }
.badge-insta     { background: #FFF6D0; color: #A07800; }
.badge-performer { background: #F5F2EC; color: #555; border: 1px solid #DDD8CC; }

/* ── Demand badges ── */
.demand-high   { background: #E8F5E9; color: #1A6E2E; padding: 2px 10px; border-radius: 100px; font-size: 10px; font-weight: 600; }
.demand-medium { background: #FFF6D0; color: #A07800; padding: 2px 10px; border-radius: 100px; font-size: 10px; font-weight: 600; }
.demand-low    { background: #F5F2EC; color: #888;    padding: 2px 10px; border-radius: 100px; font-size: 10px; font-weight: 600; }

/* ── Light dish card (for tab2 list view) ── */
.dish-card-light {
    background: white;
    border-radius: 18px;
    border: 1.5px solid #E0DDD7;
    padding: 22px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}
.dish-card-light::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
}
.dish-card-light.margin::before    { background: #0D0D0D; }
.dish-card-light.premium::before   { background: #7C3AED; }
.dish-card-light.insta::before     { background: #F0C93A; }
.dish-card-light.performer::before { background: #F05A5A; }

.dish-light-name  { font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 700; font-style: italic; color: #0D0D0D; }
.dish-light-price { font-family: 'DM Mono', monospace; font-size: 15px; font-weight: 500; color: #0D0D0D; }
.dish-light-desc  { font-size: 13px; color: #555; line-height: 1.7; margin: 10px 0; font-weight: 300; }

/* ── Table inside dish card ── */
.dish-table td { padding: 4px 0; font-size: 12px; }
.dish-table td:first-child { color: #999; width: 40%; }
.dish-table td:last-child  { font-weight: 500; text-align: right; color: #0D0D0D; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="logo-box">📈</div>
      TrendAgent
    </div>
    """, unsafe_allow_html=True)

    city = st.selectbox("📍 City", [
        "Hyderabad", "Chennai", "Mumbai", "Delhi", "Bengaluru",
        "Kolkata", "Lucknow", "Amritsar", "Goa", "Jaipur",
        "Kochi", "Indore", "Pune", "Ahmedabad", "Chandigarh",
        "Varanasi", "Agra", "Vizag", "Madurai", "Bhopal",
    ])

    rtype = st.selectbox("🍽 Restaurant Type", [
        "Local Dhaba / Authentic", "Modern Café / Bistro", "Fine Dining",
        "Street Food Stall", "Cloud Kitchen / Delivery", "Family Restaurant",
        "Vegetarian / Pure Veg", "Seafood Specialty", "Biryani House", "Mughlai / Awadhi",
    ])

    price = st.selectbox("💰 Price Range", [
        "₹ (under ₹200/head)", "₹₹ (₹200–600/head)",
        "₹₹₹ (₹600–1500/head)", "₹₹₹₹ (₹1500+/head)",
    ], index=2)

    season = st.selectbox("🌦 Season", [
        "Summer (Mar–Jun)", "Monsoon (Jul–Sep)",
        "Festive / Post-Monsoon (Oct–Nov)", "Winter (Dec–Feb)",
    ], index=1)

    st.markdown("---")
    scan_btn = st.button("📡 Scan Trends", use_container_width=True, type="secondary")
    gen_btn  = st.button("🤖 Generate Specials", use_container_width=True, type="primary")
    st.markdown("---")
    st.caption("**Stack:** Python · BeautifulSoup · Claude AI")
    st.caption("**Sources:** Google · Zomato · Times Food · Instagram")


# ── Session State ──────────────────────────────────────────────
if "scraped"    not in st.session_state: st.session_state.scraped    = None
if "analysis"   not in st.session_state: st.session_state.analysis   = None
if "specials"   not in st.session_state: st.session_state.specials   = None
if "report_txt" not in st.session_state: st.session_state.report_txt = None


# ── Hero Banner ───────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
  <div class="hero-pill">🍽 AI-Powered Food Intelligence</div>
  <div class="hero-title">Hyper-Local Food<br>Trend Agent</div>
  <div class="hero-sub">Analyze social media and web signals · Get data-backed dish recommendations · {city}, India</div>
</div>
""", unsafe_allow_html=True)


# ── SCAN TRENDS ───────────────────────────────────────────────
if scan_btn:
    from scraper.trend_scraper import scrape_all_trends
    with st.spinner(f"📡 Scanning Google, Zomato & Instagram for {city}..."):
        scraped = scrape_all_trends(city, verbose=False)
        st.session_state.scraped = scraped
    total = sum(len(v) for k, v in scraped.items() if isinstance(v, list))
    st.success(f"✅ Collected {total} data points from {city}. Now click **Generate Specials** →")


# ── SCRAPED DATA PREVIEW ──────────────────────────────────────
if st.session_state.scraped and not st.session_state.analysis:
    scraped = st.session_state.scraped
    st.markdown('<div class="section-label">📡 Raw Scraped Data Preview</div>', unsafe_allow_html=True)

    col_g, col_z = st.columns(2)
    with col_g:
        st.markdown("**🔍 Google Results**")
        for r in scraped.get("google_results", [])[:8]:
            st.markdown(f"""
            <div class="scrape-card">
                <div class="scrape-title">{r.get('title','')}</div>
                <div class="scrape-sub">{r.get('snippet','')[:120]}</div>
            </div>""", unsafe_allow_html=True)
        if not scraped.get("google_results"):
            st.caption("No Google results scraped (network may have blocked)")

    with col_z:
        st.markdown("**🍽 Zomato Trending**")
        for z in scraped.get("zomato_data", [])[:10]:
            icon = "🍴" if z.get("type") == "restaurant" else ("🏷" if z.get("type") == "collection" else "🌶")
            st.markdown(f"""
            <div class="scrape-card">
                <div class="scrape-title">{icon} {z.get('name','')}</div>
                <div class="scrape-sub">{z.get('type','').capitalize()}</div>
            </div>""", unsafe_allow_html=True)
        if not scraped.get("zomato_data"):
            st.caption("No Zomato data (may have been blocked)")

    col_a, col_h = st.columns(2)
    with col_a:
        st.markdown("**📰 Food Articles**")
        for a in scraped.get("articles", [])[:6]:
            st.markdown(f"""
            <div class="scrape-card">
                <div class="scrape-title">{a.get('headline','')}</div>
                <div class="scrape-sub">📰 {a.get('source','')}</div>
            </div>""", unsafe_allow_html=True)
        if not scraped.get("articles"):
            st.caption("No articles scraped")

    with col_h:
        st.markdown("**📸 Instagram Hashtags**")
        html = ""
        for h in scraped.get("hashtags", []):
            t = h.get("type", "hot")
            html += f'<span class="htag htag-{t}">{h["hashtag"]} +{h["estimated_growth_pct"]}%</span> '
        if html:
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.caption("No hashtag data")

    st.info("👆 Scraped data ready! Now click **🤖 Generate Specials** in the sidebar.")


# ── GENERATE SPECIALS ─────────────────────────────────────────
if gen_btn:
    if not st.session_state.scraped:
        st.warning("⚠️ Please scan trends first!")
    else:
        from llm.dish_generator import run_full_pipeline
        with st.spinner("🤖 Claude AI is analyzing trends and crafting weekend specials..."):
            output = run_full_pipeline(
                scraped_data    = st.session_state.scraped,
                restaurant_type = rtype,
                price_range     = price,
                season          = season,
                verbose         = False,
            )
        st.session_state.analysis   = output["trend_analysis"]
        st.session_state.specials   = output["specials"]
        st.session_state.report_txt = output["weekly_report"]

        from reports.report_generator import save_all
        save_all(output)
        st.success("✅ Weekend specials generated! Reports saved as JSON + TXT + CSV.")


# ── TABS ──────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Trend Overview", "🍽 Weekend Specials", "📋 Weekly Report"])


# ════════════════════════════════════════════════════
#  TAB 1: TREND OVERVIEW
# ════════════════════════════════════════════════════
with tab1:
    analysis = st.session_state.analysis

    if not analysis:
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:40px;text-align:center;border:1.5px solid #E0DDD7;margin-top:20px;">
          <div style="font-family:'Playfair Display',serif;font-size:28px;font-style:italic;color:#0D0D0D;margin-bottom:10px;">Ready to scan</div>
          <div style="font-size:13px;color:#888;font-weight:300;">Select a city in the sidebar → click <strong>Scan Trends</strong> → then <strong>Generate Specials</strong></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Stats Row ──
        stats = analysis.get("stats", {})
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Ingredients Tracked", len(analysis.get("trending_ingredients", [])), "+3 new this week")
        with c2: st.metric("Posts Analyzed", stats.get("posts_analyzed", "—"), "+18%")
        with c3: st.metric("Viral Hashtags", stats.get("hashtags_count", len(analysis.get("viral_hashtags", []))), "+8 new")
        with c4: st.metric("Top Dish Saves", stats.get("top_dish_saves", "—"), "+24%")

        # ── Trend Overview Panel ──
        st.markdown(f"""
        <div class="trend-panel" style="margin-top:20px">
          <div class="trend-panel-title">📊 Trend Overview: {analysis.get('city','')}, India</div>
          <div class="trend-summary">{analysis.get('analysis_summary','')}</div>
        </div>
        """, unsafe_allow_html=True)

        # ── Color Swatches from trending ingredients ──
        ings = analysis.get("trending_ingredients", [])
        swatch_colors = ["#F05A5A", "#F0C93A", "#1A1A1A", "#F07070", "#8B5CF6", "#34D399"]
        if ings:
            st.markdown('<div class="section-label">🎨 Trending Flavor Palette</div>', unsafe_allow_html=True)
            cols = st.columns(min(len(ings), 6))
            for i, (col, ing) in enumerate(zip(cols, ings[:6])):
                with col:
                    color = swatch_colors[i % len(swatch_colors)]
                    st.markdown(f"""
                    <div class="swatch-item">
                      <div class="swatch-block" style="background:{color};"></div>
                      <div class="swatch-lbl">{ing.get('name','')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")
        col_left, col_right = st.columns(2)

        # ── Trending Ingredients Cards ──
        with col_left:
            st.markdown('<div class="section-title">🔥 Trending Ingredients</div>', unsafe_allow_html=True)
            for ing in ings:
                status = ing.get("status", "rising").lower()
                tag_cls = f"tag-{status}"
                st.markdown(f"""
                <div class="ingredient-card">
                  <div class="ing-score">👍 {ing.get('growth_pct',0)}%</div>
                  <div><span class="ing-tag {tag_cls}">{status.title()}</span></div>
                  <div class="ing-name">{ing.get('emoji','')} {ing.get('name','')}</div>
                  <div class="ing-desc">{ing.get('context','')}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── Hashtags + Declining ──
        with col_right:
            st.markdown('<div class="section-title">🏷 Viral Hashtags</div>', unsafe_allow_html=True)
            tags = analysis.get("viral_hashtags", [])
            html = ""
            for h in tags:
                cls = f"htag-{h.get('type','hot')}"
                html += f'<span class="htag {cls}">{h["tag"]} +{h["growth_pct"]}%</span>'
            if html:
                st.markdown(html, unsafe_allow_html=True)

            st.markdown('<br><div class="section-label">📉 Declining — Avoid</div>', unsafe_allow_html=True)
            for d in analysis.get("declining_trends", []):
                st.markdown(f"""
                <div style="background:white;border:1px solid #E0DDD7;border-left:3px solid #F05A5A;
                            border-radius:8px;padding:8px 12px;margin-bottom:6px;">
                  <span style="font-weight:600;font-size:13px;color:#0D0D0D">{d['name']}</span>
                  <span style="font-size:11px;color:#F05A5A;margin-left:8px">{d['decline_pct']}</span>
                  <div style="font-size:11px;color:#888;margin-top:2px">{d.get('reason','')}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Trending Ingredients Bar Chart ──
            st.markdown('<div class="section-label" style="margin-top:20px">📈 Growth Chart</div>', unsafe_allow_html=True)
            if ings:
                df = pd.DataFrame([{
                    "Ingredient": f"{i.get('emoji','')} {i.get('name','')}",
                    "Growth %":   i.get("growth_pct", 0),
                    "Status":     i.get("status", "rising"),
                } for i in ings])
                color_map = {"hot": "#F05A5A", "rising": "#F0C93A", "steady": "#3DC98A", "viral": "#F05A5A", "new": "#6B8EF5"}
                fig = px.bar(df, x="Growth %", y="Ingredient", orientation="h",
                             color="Status", color_discrete_map=color_map,
                             template="simple_white",
                             labels={"Growth %": "Growth vs Last Week (%)"})
                fig.update_layout(
                    height=300, margin=dict(l=0, r=0, t=10, b=0),
                    showlegend=False,
                    plot_bgcolor="#F5F2EC",
                    paper_bgcolor="#F5F2EC",
                    font=dict(family="DM Sans", size=11),
                )
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

        # ── Famous Dishes Table ──
        st.markdown('<div class="section-title">🍜 Famous Dishes Trending Right Now</div>', unsafe_allow_html=True)
        dishes_trending = analysis.get("famous_dishes_trending", [])
        if dishes_trending:
            df2 = pd.DataFrame([{
                "Dish":       d.get("dish_name", ""),
                "Famous At":  d.get("famous_at", ""),
                "Saves":      d.get("saves_estimate", ""),
                "Engagement": d.get("engagement_pct", 0),
                "Why Famous": d.get("why_famous", ""),
            } for d in dishes_trending])
            st.dataframe(df2, use_container_width=True, hide_index=True,
                         column_config={"Engagement": st.column_config.ProgressColumn(
                             "Engagement", min_value=0, max_value=100, format="%d%%")})

        # ── Raw Scraped Sources expander ──
        scraped = st.session_state.scraped
        if scraped:
            with st.expander("📡 Raw Scraped Data (Google · Zomato · Articles · Hashtags)"):
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown("**🔍 Google Results**")
                    for r in scraped.get("google_results", [])[:10]:
                        st.markdown(f"""
                        <div class="scrape-card">
                          <div class="scrape-title">{r.get('title','')}</div>
                          <div class="scrape-sub">{r.get('snippet','')[:100]}</div>
                        </div>""", unsafe_allow_html=True)
                    st.markdown("**📰 Articles**")
                    for a in scraped.get("articles", [])[:6]:
                        st.markdown(f"📄 **{a.get('headline','')}** — `{a.get('source','')}`")
                with sc2:
                    st.markdown("**🍽 Zomato Trending**")
                    for z in scraped.get("zomato_data", [])[:12]:
                        icon = "🍴" if z.get("type") == "restaurant" else "🏷"
                        st.markdown(f"{icon} **{z.get('name','')}** `{z.get('type','')}`")
                    st.markdown("**📸 Hashtags**")
                    html = ""
                    for h in scraped.get("hashtags", []):
                        t = h.get("type", "hot")
                        html += f'<span class="htag htag-{t}">{h["hashtag"]} +{h["estimated_growth_pct"]}%</span> '
                    if html:
                        st.markdown(html, unsafe_allow_html=True)
                total_pts = sum(len(v) for k, v in scraped.items() if isinstance(v, list))
                st.caption(f"🗂 {total_pts} total data points · Scraped at: {scraped.get('scraped_at','—')}")


# ════════════════════════════════════════════════════
#  TAB 2: WEEKEND SPECIALS
# ════════════════════════════════════════════════════
with tab2:
    specials = st.session_state.specials

    if not specials:
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:40px;text-align:center;border:1.5px solid #E0DDD7;margin-top:20px;">
          <div style="font-family:'Playfair Display',serif;font-size:28px;font-style:italic;color:#0D0D0D;margin-bottom:10px;">Weekend Specials</div>
          <div style="font-size:13px;color:#888;font-weight:300;">Click <strong>Generate Specials</strong> in the sidebar to get AI-crafted dishes.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── Top Ingredients Pill Row ──
        top_ings = specials.get("top_weekend_ingredients", [])
        if top_ings:
            st.markdown('<div class="section-label">🏆 Top Revenue Ingredients This Weekend</div>', unsafe_allow_html=True)
            cols = st.columns(len(top_ings))
            for col, ing in zip(cols, top_ings):
                with col:
                    st.markdown(f'<div class="ing-pill">✦ {ing}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # ── Two-column layout: dark dish cards left, light detail right ──
        dishes = specials.get("weekend_specials", [])

        left_col, right_col = st.columns([1, 1])

        for i, dish in enumerate(dishes):
            cat = dish.get("category", "")
            if   "margin"    in cat.lower(): badge_lbl, badge_cls, card_cls = "💰 High Margin",    "badge-margin",    "margin"
            elif "premium"   in cat.lower(): badge_lbl, badge_cls, card_cls = "👑 Premium Upsell",  "badge-premium",   "premium"
            elif "instagram" in cat.lower(): badge_lbl, badge_cls, card_cls = "📸 Reels-Worthy",   "badge-insta",     "insta"
            else:                            badge_lbl, badge_cls, card_cls = "🔥 Weekend Hit",     "badge-performer", "performer"

            demand = dish.get("predicted_demand", "Medium")
            d_cls  = "demand-high" if demand == "High" else ("demand-medium" if demand == "Medium" else "demand-low")
            margin_cls = "margin-high" if demand == "High" else ("margin-medium" if demand == "Medium" else "margin-low")

            # Build ingredient tags html
            ing_tags = "".join([
                f'<span class="dish-tag-dark">{t}</span>'
                for t in dish.get("ingredients_needed", [])[:4]
            ])

            # Dark card (left side for odd, right for even)
            target_col = left_col if i % 2 == 0 else right_col
            with target_col:
                st.markdown(f"""
                <div class="dish-card-dark">
                  <div class="dish-wm">Ψ</div>
                  <div class="dish-num">0{i+1} SUGGESTION</div>
                  <div class="dish-dark-name">{dish.get('dish_name','')}</div>
                  <div class="dish-dark-desc">{dish.get('description','')}</div>
                  <div class="dish-tags-row">{ing_tags}</div>
                  <div class="dish-footer-dark">
                    <div>
                      <div class="dish-target-lbl">Target</div>
                      <div class="dish-target-txt">{dish.get('why_it_will_trend','')[:100]}</div>
                    </div>
                    <div style="text-align:right">
                      <div class="margin-lbl">Margin</div>
                      <div class="{margin_cls}">{demand}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Detail expander below each card
                with st.expander(f"📋 Details — {dish.get('dish_name','')}"):
                    d1, d2 = st.columns(2)
                    with d1:
                        st.markdown(f"**🏠 Inspired By:** {dish.get('inspired_by','—')}")
                        st.markdown(f"**🔑 Key Ingredient:** {dish.get('key_trending_ingredient','')}")
                        st.markdown(f"**💸 Food Cost:** {dish.get('food_cost_level','')} · {dish.get('estimated_food_cost_inr','')}")
                        st.markdown(f"**📈 Gross Margin:** {dish.get('gross_margin_pct','')}")
                    with d2:
                        st.markdown(f"**💰 Price Range:** {dish.get('suggested_price_range','')}")
                        st.markdown(f"**⏱ Prep Time:** {dish.get('prep_time_mins','')} mins")
                        st.markdown(f"**🍽 Best Served:** {dish.get('best_served','')}")
                    st.markdown(f"**📸 Plating:** {dish.get('plating_tip','')}")
                    st.markdown(f"**🎬 Reels Tip:** {dish.get('reels_tip','')}")

        # ── Strategic Insight ──
        if specials.get("strategic_insight"):
            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-lbl">💡 Strategic Insight for {specials.get('city','')}</div>
              <div class="insight-txt">{specials.get('strategic_insight','')}</div>
              <div class="insight-rev">📈 Revenue Projection: {specials.get('revenue_projection','')}</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Download CSV ──
        if dishes:
            st.markdown("---")
            df_dishes = pd.DataFrame([{
                "Dish":           d.get("dish_name",""),
                "Category":       d.get("category",""),
                "Price (₹)":      d.get("suggested_price_range",""),
                "Food Cost":      d.get("estimated_food_cost_inr",""),
                "Margin":         d.get("gross_margin_pct",""),
                "Demand":         d.get("predicted_demand",""),
                "Inspired By":    d.get("inspired_by",""),
                "Key Ingredient": d.get("key_trending_ingredient",""),
                "Prep (mins)":    d.get("prep_time_mins",""),
            } for d in dishes])
            csv_data = df_dishes.to_csv(index=False)
            st.download_button("⬇ Download Dishes CSV", csv_data,
                               file_name=f"weekend_specials_{city.lower()}.csv",
                               mime="text/csv")


# ════════════════════════════════════════════════════
#  TAB 3: WEEKLY REPORT
# ════════════════════════════════════════════════════
with tab3:
    if not st.session_state.report_txt:
        st.markdown("""
        <div style="background:white;border-radius:20px;padding:40px;text-align:center;border:1.5px solid #E0DDD7;margin-top:20px;">
          <div style="font-family:'Playfair Display',serif;font-size:28px;font-style:italic;color:#0D0D0D;margin-bottom:10px;">Weekly Report</div>
          <div style="font-size:13px;color:#888;font-weight:300;">Generate specials to produce the weekly consultant report.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"""
            <div style="font-family:'Playfair Display',serif;font-size:26px;font-style:italic;font-weight:700;color:#0D0D0D">
              Weekly Food Trend Report — {city}
            </div>
            <div style="font-size:11px;color:#888;margin-top:4px;font-weight:300">
              Generated: {datetime.now().strftime('%A, %d %B %Y at %I:%M %p')}
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.download_button(
                "⬇ Download Report",
                st.session_state.report_txt,
                file_name=f"weekly_report_{city.lower()}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        st.markdown("---")

        # Report in a styled panel
        st.markdown(f"""
        <div style="background:white;border-radius:20px;padding:28px 32px;border:1.5px solid #E0DDD7;
                    font-size:13.5px;line-height:1.9;color:#444;font-weight:300;">
          {st.session_state.report_txt.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)

        # Summary table
        if st.session_state.specials:
            st.markdown('<div class="section-title" style="margin-top:28px">📊 Recommended Weekend Menu</div>', unsafe_allow_html=True)
            dishes = st.session_state.specials.get("weekend_specials", [])
            if dishes:
                df3 = pd.DataFrame([{
                    "Dish":         d.get("dish_name",""),
                    "Category":     d.get("category",""),
                    "Inspired By":  d.get("inspired_by",""),
                    "Price (₹)":    d.get("suggested_price_range",""),
                    "Gross Margin": d.get("gross_margin_pct",""),
                    "Demand":       d.get("predicted_demand",""),
                } for d in dishes])
                st.dataframe(df3, use_container_width=True, hide_index=True)
