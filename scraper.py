import os
import csv
from google_play_scraper import reviews, Sort
from langdetect import detect, DetectorFactory
from datetime import datetime
from pathlib import Path

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# Create data directory if it doesn't exist
Path("data").mkdir(parents=True, exist_ok=True)

# Output CSV path
output_path = os.path.join("data", "feedback_data.csv")

# App package name (e.g., 'com.whatsapp')
APP_PACKAGE_NAME = "com.instagram.android"  # You can change this

# Max reviews to scrape
NUM_REVIEWS = 10  # You can increase this based on your needs

def fetch_reviews(app_package: str, num_reviews: int):
    result, _ = reviews(
        app_package,
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=num_reviews
    )
    return result

def save_to_csv(reviews_data, path):
    with open(path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["review", "rating", "date", "language", "app"])
        for review in reviews_data:
            content = review.get("content", "").strip()
            rating = review.get("score", "")
            date = review.get("at", "")
            app_name = APP_PACKAGE_NAME
            if content:
                try:
                    lang = detect(content)
                except:
                    lang = "unknown"
                writer.writerow([content, rating, date, lang, app_name])

if __name__ == "__main__":
    print(f"Scraping reviews for: {APP_PACKAGE_NAME}")
    try:
        reviews_data = fetch_reviews(APP_PACKAGE_NAME, NUM_REVIEWS)
        if not reviews_data:
            print("⚠️ No reviews found.")
        else:
            save_to_csv(reviews_data, output_path)
            print(f"✅ Saved {len(reviews_data)} reviews to {output_path}")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
