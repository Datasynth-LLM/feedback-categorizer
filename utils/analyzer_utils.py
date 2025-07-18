from transformers import pipeline

def analyze_feedback(df, classifier, sentiment_analyzer):
    categories_list = [
        "Bug Report", "Feature Request", "User Experience",
        "Performance", "Security", "Pricing", "Support", "Other"
    ]

    results = []

    for _, row in df.iterrows():
        text = row['content']

        # Category prediction using zero-shot classification
        category_result = classifier(text, candidate_labels=categories_list)
        top_category = category_result["labels"][0]
        category_score = category_result["scores"][0]

        # Sentiment prediction
        sentiment_result = sentiment_analyzer(text)[0]
        sentiment = sentiment_result["label"]
        sentiment_score = sentiment_result["score"]

        # Urgency logic
        urgency = "High" if sentiment == "NEGATIVE" and category_score > 0.7 else "Low"

        results.append({
            "content": text,
            "category": top_category,
            "sentiment": sentiment,
            "urgency": urgency,
            "confidence": round(category_score, 2)
        })

    return results
