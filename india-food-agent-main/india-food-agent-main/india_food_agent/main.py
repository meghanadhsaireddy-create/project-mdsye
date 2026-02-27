"""
main.py
━━━━━━━
CLI entry point for India Food Trend Agent.

Usage:
  python main.py
  python main.py --city "Mumbai" --type "Street Food Café" --price "₹₹" --season "Monsoon"
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from scraper.trend_scraper  import scrape_all_trends
from llm.dish_generator     import run_full_pipeline
from reports.report_generator import save_all

CITIES = [
    "Hyderabad", "Chennai", "Mumbai", "Delhi", "Bengaluru",
    "Kolkata", "Lucknow", "Amritsar", "Goa", "Jaipur",
    "Kochi", "Indore", "Pune", "Ahmedabad", "Chandigarh",
    "Varanasi", "Agra", "Vizag", "Madurai", "Bhopal",
]

RESTAURANT_TYPES = [
    "Local Dhaba / Authentic",
    "Modern Café / Bistro",
    "Fine Dining",
    "Street Food Stall",
    "Cloud Kitchen / Delivery",
    "Family Restaurant",
    "Vegetarian / Pure Veg",
    "Seafood Specialty",
    "Biryani House",
    "Mughlai / Awadhi",
]

PRICE_RANGES = [
    "₹ (under ₹200/head)",
    "₹₹ (₹200–600/head)",
    "₹₹₹ (₹600–1500/head)",
    "₹₹₹₹ (₹1500+/head)",
]

SEASONS = [
    "Summer (Mar–Jun)",
    "Monsoon (Jul–Sep)",
    "Festive / Post-Monsoon (Oct–Nov)",
    "Winter (Dec–Feb)",
]


def interactive_mode():
    """Interactive prompts for non-CLI users."""
    print("\n" + "═"*55)
    print("  🇮🇳  INDIA FOOD TREND AGENT")
    print("  Python + Scraping + Claude AI")
    print("═"*55)

    print("\n📍 Available Cities:")
    for i, c in enumerate(CITIES, 1):
        print(f"  {i:2}. {c}")
    city_idx = int(input("\nSelect city number: ")) - 1
    city = CITIES[city_idx]

    print("\n🍽 Restaurant Types:")
    for i, t in enumerate(RESTAURANT_TYPES, 1):
        print(f"  {i}. {t}")
    type_idx = int(input("Select type number: ")) - 1
    rtype = RESTAURANT_TYPES[type_idx]

    print("\n💰 Price Range:")
    for i, p in enumerate(PRICE_RANGES, 1):
        print(f"  {i}. {p}")
    price_idx = int(input("Select price number: ")) - 1
    price = PRICE_RANGES[price_idx]

    print("\n🌦 Season:")
    for i, s in enumerate(SEASONS, 1):
        print(f"  {i}. {s}")
    season_idx = int(input("Select season number: ")) - 1
    season = SEASONS[season_idx]

    return city, rtype, price, season


def run(city, restaurant_type, price_range, season, save_reports=True):
    """Main pipeline runner."""
    print(f"\n🚀 Starting India Food Trend Agent")
    print(f"   City: {city} | Type: {restaurant_type} | Price: {price_range} | Season: {season}")

    # ── Step 1: Scrape ──
    scraped = scrape_all_trends(city, verbose=True)

    # ── Step 2: LLM Analysis + Generation ──
    output = run_full_pipeline(
        scraped_data    = scraped,
        restaurant_type = restaurant_type,
        price_range     = price_range,
        season          = season,
        verbose         = True,
    )

    # ── Step 3: Save Reports ──
    if save_reports:
        paths = save_all(output)
        output["saved_files"] = paths

    # ── Print Summary ──
    print("\n" + "═"*55)
    print(f"  ✅ DONE! Weekend specials for {city}:")
    print("═"*55)
    for i, dish in enumerate(output["specials"].get("weekend_specials", []), 1):
        demand_icon = "🔥" if dish["predicted_demand"] == "High" else ("⚡" if dish["predicted_demand"] == "Medium" else "💡")
        print(f"  {i}. {dish['dish_name']}")
        print(f"     {dish['category']} · {dish['suggested_price_range']} · {demand_icon} {dish['predicted_demand']} demand")
        print()

    insight = output["specials"].get("strategic_insight", "")
    if insight:
        print(f"💡 Strategic Insight:\n   {insight[:200]}...")

    return output


def main():
    parser = argparse.ArgumentParser(
        description="🇮🇳 India Food Trend Agent — Python + Scraping + Claude AI"
    )
    parser.add_argument("--city",    type=str, help="City name (e.g. 'Hyderabad')")
    parser.add_argument("--type",    type=str, help="Restaurant type")
    parser.add_argument("--price",   type=str, help="Price range")
    parser.add_argument("--season",  type=str, help="Season")
    parser.add_argument("--no-save", action="store_true", help="Don't save reports to disk")
    args = parser.parse_args()

    if args.city:
        city   = args.city
        rtype  = args.type   or "Modern Café / Bistro"
        price  = args.price  or "₹₹₹ (₹600–1500/head)"
        season = args.season or "Monsoon (Jul–Sep)"
    else:
        city, rtype, price, season = interactive_mode()

    run(city, rtype, price, season, save_reports=not args.no_save)


if __name__ == "__main__":
    main()
