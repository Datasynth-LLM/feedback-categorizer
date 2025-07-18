import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import altair as alt
from transformers import pipeline
from collections import Counter
import datetime
from langdetect import detect, DetectorFactory
from utils.analyzer_utils import analyze_feedback
from utils.language_utils import detect_language
from utils.scraper_utils import get_sample_reviews
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
DetectorFactory.seed = 42  # for reproducibility

# Streamlit UI settings
st.set_page_config(page_title="AI Feedback Categorizer", layout="wide")
st.title("🧠 AI Feedback Categorizer with Business Insights")

# Load models only once
@st.cache_resource
def load_models():
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
        revision="af0f99b"
    )
    return classifier, sentiment_analyzer

classifier, sentiment_analyzer = load_models()

# Logic Functions
def classify_feedback(feedback, labels):
    result = classifier(feedback, labels)
    return result['labels'][0], result['scores'][0]

def analyze_sentiment(text):
    result = sentiment_analyzer(text)[0]
    return result['label'], result['score']

def assign_urgency(feedback):
    text = feedback.lower()
    if any(word in text for word in ["crash", "urgent", "fail", "error", "issue"]):
        return "High"
    elif any(word in text for word in ["slow", "delay", "not working"]):
        return "Medium"
    return "Low"

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def extract_keywords(texts):
    all_words = " ".join(texts).lower().split()
    stopwords = set(pd.read_csv(
        "https://raw.githubusercontent.com/stopwords-iso/stopwords-en/master/stopwords-en.txt",
        header=None)[0].tolist())
    keywords = [word for word in all_words if word.isalpha() and word not in stopwords and len(word) > 3]
    return Counter(keywords).most_common(20)

# Sidebar file uploader
uploaded_file = st.sidebar.file_uploader("📁 Upload a CSV with 'feedback' column", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'review' in df.columns:
        df.rename(columns={'review': 'feedback'}, inplace=True)

    if 'feedback' not in df.columns:
        st.error("Uploaded file must have a 'feedback' column.")
    else:
        with st.spinner("🔍 Analyzing feedback..."):
            labels = ["Bug", "Feature Request", "Compliment", "Complaint", "General Feedback"]
            df['category'], df['confidence'] = zip(*df['feedback'].apply(lambda x: classify_feedback(x, labels)))
            df['sentiment'], df['sentiment_score'] = zip(*df['feedback'].apply(analyze_sentiment))
            df['urgency'] = df['feedback'].apply(assign_urgency)
            df['language'] = df['feedback'].apply(detect_language)
            df['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            keyword_freq = extract_keywords(df['feedback'])

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Dashboard", "🧾 Data View", "📈 Keyword Trends", "💡 Business Insights"
        ])

        with tab1:
            st.subheader("Category Distribution")
            fig1, ax1 = plt.subplots()
            sns.countplot(y='category', data=df, ax=ax1, hue='category', palette="viridis", legend=False)
            st.pyplot(fig1)

            st.subheader("Sentiment Distribution")
            fig2, ax2 = plt.subplots()
            sns.countplot(x='sentiment', data=df, ax=ax2, hue='sentiment', palette="Set2", legend=False)
            st.pyplot(fig2)

            st.subheader("Urgency Levels")
            fig3, ax3 = plt.subplots()
            sns.countplot(x='urgency', data=df, ax=ax3, hue='urgency', palette="Reds", legend=False)
            st.pyplot(fig3)

        with tab2:
            st.subheader("Processed Feedback Data")
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download CSV", csv, "processed_feedback.csv", "text/csv")

        with tab3:
            st.subheader("Top Keywords from Feedback")
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(keyword_freq))
            fig_wc, ax_wc = plt.subplots(figsize=(10, 4))
            ax_wc.imshow(wordcloud, interpolation='bilinear')
            ax_wc.axis("off")
            st.pyplot(fig_wc)

            st.subheader("Keyword Frequency Chart")
            keyword_df = pd.DataFrame(keyword_freq, columns=['keyword', 'count'])
            chart = alt.Chart(keyword_df).mark_bar().encode(
                x=alt.X('keyword', sort='-y'),
                y='count',
                tooltip=['keyword', 'count']
            ).properties(height=400)
            st.altair_chart(chart, use_container_width=True)

        with tab4:
            st.subheader("Business Insights")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Feedback", len(df))
                st.metric("% Urgent Issues", f"{round((df['urgency']=='High').sum() / len(df) * 100, 2)}%")
            with col2:
                st.metric("Positive Feedback", (df['sentiment']=='POSITIVE').sum())
                st.metric("Bugs Detected", (df['category']=='Bug').sum())

            st.write("### Weekly Category Summary")
            summary = df.groupby('category').agg({
                'sentiment': lambda x: x.value_counts().idxmax(),
                'urgency': lambda x: x.value_counts().idxmax(),
                'feedback': 'count'
            }).rename(columns={'feedback': 'count'}).reset_index()
            st.dataframe(summary)

else:
    st.info("Upload a CSV file to begin analysis. It must have a 'feedback' column.")

st.caption("Made  using Streamlit, Transformers, and Python.")
