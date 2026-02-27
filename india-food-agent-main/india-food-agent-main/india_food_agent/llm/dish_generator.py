"""
llm/dish_generator.py
━━━━━━━━━━━━━━━━━━━━━
Uses Claude (Anthropic) to:
  1. Analyze raw scraped data → extract structured trend insights
  2. Generate high-margin weekend special dishes
  3. Build strategic weekly report
"""

import os
import json
import re
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL  = "claude-opus-4-6"   # best for analysis; swap to claude-haiku-4-5-20251001 for speed


# ══════════════════════════════════════════
#  STEP 1 — Analyze raw scraped data
# ══════════════════════════════════════════
def analyze_scraped_data(scraped_data: dict) -> dict:
    """
    Send raw scraped data to Claude and extract:
    - Top trending ingredients
    - Famous dishes & restaurants mentioned
    - Viral hashtags & their context
    - Declining trends
    - Engagement patterns
    """
    city = scraped_data.get("city", "India")

    # Build context from scraped data
    google_text = "\n".join([
        f"• {r.get('title','')}: {r.get('snippet','')[:120]}"
        for r in scraped_data.get("google_results", [])[:15]
    ])

    zomato_text = "\n".join([
        f"• [{z.get('type','')}] {z.get('name','')}"
        for z in scraped_data.get("zomato_data", [])[:15]
    ])

    articles_text = "\n".join([
        f"• {a.get('headline','')} ({a.get('source','')})"
        for a in scraped_data.get("articles", [])[:10]
    ])

    hashtags_text = "\n".join([
        f"• {h.get('hashtag','')} — +{h.get('estimated_growth_pct',0)}% ({h.get('type','')})"
        for h in scraped_data.get("hashtags", [])
    ])

    prompt = f"""You are an expert Indian food trend analyst.

I've scraped real-time data from Google, Zomato, food news sites, and Instagram for {city}.
Analyze this data and extract structured food trend insights.

━━ GOOGLE SEARCH RESULTS ━━
{google_text or "No data scraped (network issue)"}

━━ ZOMATO TRENDING ━━
{zomato_text or "No data scraped (network issue)"}

━━ FOOD NEWS ARTICLES ━━
{articles_text or "No data scraped (network issue)"}

━━ INSTAGRAM HASHTAGS ━━
{hashtags_text or "No data"}

Based on ALL above data + your knowledge of {city}'s food scene (real restaurants, famous dishes, local culture):

Return ONLY valid JSON (no markdown):
{{
  "city": "{city}",
  "analysis_summary": "2-3 sentence overview of what's trending",
  "trending_ingredients": [
    {{
      "name": "ingredient name",
      "emoji": "relevant emoji",
      "growth_pct": 0,
      "context": "why trending + real restaurant/dish context",
      "status": "hot|rising|steady"
    }}
  ],
  "famous_dishes_trending": [
    {{
      "dish_name": "dish",
      "famous_at": "real restaurant name",
      "saves_estimate": "Xk",
      "engagement_pct": 0,
      "why_famous": "brief reason"
    }}
  ],
  "viral_hashtags": [
    {{
      "tag": "#hashtag",
      "growth_pct": 0,
      "type": "viral|hot|rising|new"
    }}
  ],
  "declining_trends": [
    {{
      "name": "dish/trend",
      "decline_pct": "-X%",
      "reason": "why declining"
    }}
  ],
  "engagement_patterns": "What content gets most saves/shares in this city",
  "stats": {{
    "posts_analyzed": "XXk",
    "top_dish_saves": "XXk",
    "hashtags_count": 0
  }}
}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text
    # Clean JSON
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


# ══════════════════════════════════════════
#  STEP 2 — Generate Weekend Specials
# ══════════════════════════════════════════
def generate_weekend_specials(
    trend_analysis: dict,
    restaurant_type: str,
    price_range: str,
    season: str,
) -> dict:
    """
    Uses Claude to generate 5 high-margin weekend special dishes
    based on analyzed trend data.
    """
    city = trend_analysis.get("city", "India")

    # Format trend data for prompt
    ingredients = "\n".join([
        f"  • {i['name']} (+{i['growth_pct']}%) — {i['context']}"
        for i in trend_analysis.get("trending_ingredients", [])[:8]
    ])

    famous_dishes = "\n".join([
        f"  • \"{d['dish_name']}\" @ {d['famous_at']} ({d['saves_estimate']} saves) — {d['why_famous']}"
        for d in trend_analysis.get("famous_dishes_trending", [])[:8]
    ])

    hashtags = ", ".join([
        f"{h['tag']} (+{h['growth_pct']}%)"
        for h in trend_analysis.get("viral_hashtags", [])[:8]
    ])

    declining = ", ".join([
        f"{d['name']} ({d['decline_pct']})"
        for d in trend_analysis.get("declining_trends", [])
    ])

    engagement = trend_analysis.get("engagement_patterns", "")
    summary    = trend_analysis.get("analysis_summary", "")

    prompt = f"""You are India's #1 restaurant revenue strategist and food trend expert.

CITY: {city}
RESTAURANT TYPE: {restaurant_type}
PRICE RANGE: {price_range} (ALL prices in Indian Rupees ₹)
SEASON: {season}

━━ REAL TREND ANALYSIS (freshly scraped) ━━
Summary: {summary}

Top Trending Ingredients:
{ingredients}

Famous Dishes People Love Right Now:
{famous_dishes}

Viral Hashtags: {hashtags}

Engagement Pattern: {engagement}

AVOID (Declining): {declining}

━━ YOUR TASK ━━
Generate 5 UNIQUE weekend special dishes. Each must:
- Be inspired by REAL local dishes/restaurants (mentioned above)
- Add a creative, modern twist — not just a copy
- Match the restaurant type and price range
- Be operationally realistic for a busy weekend kitchen
- Have strong visual appeal for Instagram Reels

Exactly:
- 1 × "low-cost high-margin" (low food cost, max profit)
- 1 × "premium upsell" (luxury, high perceived value)
- 1 × "highly instagrammable" (viral visual wow factor)
- 2 × "weekend performer" (solid crowd-pleasers)

Return ONLY valid JSON (no markdown):
{{
  "city": "{city}",
  "generated_at": "timestamp",
  "top_weekend_ingredients": ["ing1", "ing2", "ing3"],
  "weekend_specials": [
    {{
      "dish_name": "",
      "category": "low-cost high-margin|premium upsell|highly instagrammable|weekend performer",
      "key_trending_ingredient": "",
      "inspired_by": "real dish + real restaurant name",
      "description": "2-3 sentence mouth-watering description",
      "ingredients_needed": ["ing1", "ing2", "ing3", "ing4"],
      "prep_time_mins": 0,
      "food_cost_level": "Low|Medium|High",
      "estimated_food_cost_inr": "₹XX–₹YY per plate",
      "suggested_price_range": "₹XXX–₹YYY",
      "gross_margin_pct": "approx XX%",
      "plating_tip": "specific visual plating instruction",
      "reels_tip": "how to film/present for Instagram Reels",
      "why_it_will_trend": "specific reason tied to local trends",
      "predicted_demand": "Low|Medium|High",
      "best_served": "lunch|dinner|both"
    }}
  ],
  "strategic_insight": "3-4 sentence strategic recommendation for this city this weekend",
  "revenue_projection": "Expected uplift in weekend revenue if all 5 specials added"
}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text
    raw = re.sub(r"```json|```", "", raw).strip()

    result = json.loads(raw)
    from datetime import datetime
    result["generated_at"] = datetime.now().isoformat()
    return result


# ══════════════════════════════════════════
#  STEP 3 — Weekly Report Narrative
# ══════════════════════════════════════════
def generate_weekly_report(
    trend_analysis: dict,
    specials: dict,
) -> str:
    """
    Generates a professional weekly trend report narrative using Claude.
    """
    city = trend_analysis.get("city", "India")
    dishes = specials.get("weekend_specials", [])

    dishes_summary = "\n".join([
        f"  {i+1}. {d['dish_name']} ({d['category']}) — {d['suggested_price_range']} — {d['predicted_demand']} demand"
        for i, d in enumerate(dishes)
    ])

    prompt = f"""Write a professional weekly food trend report for a restaurant owner in {city}.

TREND DATA:
{trend_analysis.get('analysis_summary', '')}

RECOMMENDED DISHES:
{dishes_summary}

STRATEGIC INSIGHT:
{specials.get('strategic_insight', '')}

Write a concise, actionable report (300-400 words) covering:
1. This Week's Food Trend Summary for {city}
2. Why These 5 Dishes Were Chosen
3. Operational Tips for the Weekend
4. Social Media & Marketing Recommendations
5. Revenue Outlook

Use clear headers. Be specific to {city}'s food culture. 
Write like a paid consultant — confident, data-backed, actionable."""

    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text


# ══════════════════════════════════════════
#  CONVENIENCE — run full pipeline
# ══════════════════════════════════════════
def run_full_pipeline(
    scraped_data: dict,
    restaurant_type: str = "Modern Indian Bistro",
    price_range: str = "₹₹₹ (₹600–1500/head)",
    season: str = "Monsoon (Jul–Sep)",
    verbose: bool = True,
) -> dict:
    """
    Runs the complete LLM pipeline:
    scraped_data → trend_analysis → specials → report

    Returns dict with all three outputs.
    """
    city = scraped_data.get("city", "India")

    if verbose: print(f"\n🤖 Running LLM analysis for {city}...")

    if verbose: print("  [1/3] Analyzing scraped data with Claude...")
    trend_analysis = analyze_scraped_data(scraped_data)

    if verbose: print("  [2/3] Generating weekend specials...")
    specials = generate_weekend_specials(
        trend_analysis, restaurant_type, price_range, season
    )

    if verbose: print("  [3/3] Writing weekly report...")
    report = generate_weekly_report(trend_analysis, specials)

    if verbose: print("  ✅ LLM pipeline complete!")

    return {
        "city": city,
        "trend_analysis": trend_analysis,
        "specials": specials,
        "weekly_report": report,
    }


if __name__ == "__main__":
    # Quick test with dummy data
    dummy = {
        "city": "Hyderabad",
        "scraped_at": "2025-02-27T10:00:00",
        "google_results": [
            {"title": "Best Biryani in Hyderabad 2025", "snippet": "Paradise and Shah Ghouse top the charts"},
        ],
        "zomato_data": [{"type": "restaurant", "name": "Paradise Biryani", "city": "Hyderabad"}],
        "articles": [{"headline": "Haleem season kicks off in Hyderabad", "source": "timesofindia.com"}],
        "hashtags": [{"hashtag": "#HyderabadBiryani", "estimated_growth_pct": 720, "type": "viral"}],
    }

    result = run_full_pipeline(dummy)
    print(json.dumps(result["specials"], indent=2, ensure_ascii=False))
