[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://berkeley-course-compass.streamlit.app)

# 🎓 Berkeley Course Compass

Find your next favorite Berkeley class with AI-powered recommendations.

This app uses semantic search powered by sentence-transformers to recommend courses based on either:
- A **keyword/topic** (e.g., 'machine learning', 'climate change')
- An **existing course** (e.g., 'COMPSCI 61A')

## 🔍 Features
- Semantic keyword search across 4,000+ Berkeley courses
- Course-to-course recommendations using vector similarity
- Optional department filtering
- Explanation for why each course was recommended
- Streamlit-based interactive UI

## 🚀 Getting Started

### Installation
```bash
git clone https://github.com/yourusername/berkeley-course-compass.git
cd berkeley-course-compass
pip install -r requirements.txt
streamlit run app.py
```

### File Overview
- `app.py` – Streamlit frontend
- `recommender.py` – Embedding logic and recommendation engine
- `scraper.py` – Optional course data scraper
- `berkeley_courses.csv` – Cleaned course dataset

## 🧠 Example
Search for:
- Keyword: `architecture` or `machine learning`
- Course Code: `COMPSCI 61A`, `DATA C100`

## 📜 License
MIT
