import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
import os

# Load data
df = pd.read_csv("data/training_data.csv")
df.dropna(subset=['content', 'category'], inplace=True)

# Features and labels
X = df['content']
y = df['category']

# Create and train pipeline
vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
classifier = LogisticRegression(max_iter=1000)

X_vec = vectorizer.fit_transform(X)
classifier.fit(X_vec, y)

# Save models
os.makedirs("models", exist_ok=True)
joblib.dump(classifier, "models/category_classifier.joblib")
joblib.dump(vectorizer, "models/category_vectorizer.joblib")

print("✅ Model and vectorizer saved to /models")
