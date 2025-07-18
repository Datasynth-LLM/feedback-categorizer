# utils/scraper_utils.py

from google_play_scraper import Sort, reviews
import pandas as pd

def get_sample_reviews(app_id="com.example.app", count=5):
    result, _ = reviews(
        app_id,
        lang='en',
        country='us',
        sort=Sort.NEWEST,
        count=count
    )
    df = pd.DataFrame(result)
    if 'content' in df.columns:
        return df[['content']]
    else:
        return pd.DataFrame(columns=["content"])
