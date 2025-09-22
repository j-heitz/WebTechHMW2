from bs4 import BeautifulSoup
import json

with open("listing_fr.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "lxml")

business_info = {
    "name": "Chimis Fresh Mex",
    "category": "Mexican",
    "city": "FLorissant, MO",
    "price_range": "$$",
    "overall_rating": "3.9",
    "total_reviews": "119"
}

reviews_html = soup.select("p.comment__09f24__D0cxf")[:5]

parsed_reviews = []

for review in reviews_html:
    text_tag = review.select_one("span[lang]")
    review_text = text_tag.get_text(strip=True) if text_tag else "N/A"

    rating_tag = review.find_previous("div", role="img")
    rating = rating_tag["aria-label"] if rating_tag and "aria-label" in rating_tag.attrs else "N/A"

    date_tag = review.find_next("span", class_="y-css-1vi7y4e")
    review_date = date_tag.get_text(strip=True) if date_tag else "N/A"

    reviewer_tag = review.find_previous("a", href=lambda x: x and x.startswith("/user_details?userid="))
    reviewer_name = reviewer_tag.get_text(strip=True) if reviewer_tag else "N/A"

    parsed_reviews.append({
        "business_name": business_info["name"],
        "category": business_info["category"],
        "city": business_info["city"],
        "price_range": business_info["price_range"],
        "overall_rating": business_info["overall_rating"],
        "total_reviews": business_info["total_reviews"],
        "reviewer_name": reviewer_name,
        "review_date": review_date,
        "review_text": review_text,
        "star_rating": rating
    })

with open("parsed.json", "w", encoding="utf-8") as f:
    json.dump(parsed_reviews, f, indent=2, ensure_ascii=False)

print(f"Parsing complete. Saved {len(parsed_reviews)} reviews to parsed.json")
