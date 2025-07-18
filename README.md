# feedback-analyzer


A Streamlit-powered web app that intelligently categorizes and analyzes user feedback using NLP and Hugging Face Transformers.

---

## 🚀 Features

- ✅ Zero-shot feedback classification using BART
- ✅ Sentiment analysis using DistilBERT
- ✅ Urgency scoring and keyword extraction
- ✅ Language detection (multilingual feedback support)
- ✅ CSV upload & interactive filtering
- ✅ Model confidence score display
- ✅ Future enhancements: PDF reports, alert system, webhook integration
- ## 📒 Notebooks

The `notebooks/` folder contains exploration and prototyping code used during development (optional).


---

## 🗂️ Folder Structure
feedback-analyzer/
├── app.py
├── scraper.py
├── run_app.bat          
├── run_scraper.bat     
├── train_model.py
├── requirements.txt
├── training_data.csv
├── data/
│   └── feedback_data.csv
    └── synthetic_data.csv
    └── training_data.csv
├── models/
│   └── feedback_classifier.joblib
├── utils/
│   ├── analyzer_utils.py
│   ├── language_utils.py
│   └── scraper_utils.py
├── .gitignore
├── README.md


    ## description
    | Folder/File      | Purpose                                                                     |
| ---------------- | --------------------------------------------------------------------------- |
| `app.py`         | Runs the full app including scraping, analysis, and visualization           |
| `train_model.py` | Trains the classifier and vectorizer and saves `.joblib` files in `models/` |
| `models/`        | Stores the trained ML models                                                |
| `data/`          | Stores input and output CSVs                                                |
| `notebooks/`     | Stores development Jupyter notebooks                                        |
| `utils/`         | Contains all modular logic (scraping, analyzing, language detection)        |
| `autorun         | Automation with `.bat` files to launch components                           |


## 🛠️ Usage

1. 📦 Install dependencies:
   ```bash
   pip install -r requirements.txt
   python train_model.py
   streamlit run app.py
   Optional automation (on Windows):
Double-click run_app.bat or scraper.bat
install langchain individually to avoid errors






