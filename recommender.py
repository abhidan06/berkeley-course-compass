import pandas as pd
import pathlib
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import hashlib
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

path = pathlib.Path(__file__).parent / 'berkeley_courses.csv'
df = pd.read_csv(path).dropna(subset=["description", "title"])

def is_generic(desc):
    text = desc.lower()
    return any(kw in text for kw in [
        "individual study", "group studies", "topics to be selected",
        "supervised", "independent research"
    ])

df = df[~df['description'].apply(is_generic)].reset_index(drop=True)

df['text'] = df['title'].fillna('') + ". " + df['description'].fillna('')

def hash_descriptions(df):
    joined = ' '.join(df['text'].tolist())
    return hashlib.md5(joined.encode('utf-8')).hexdigest()

cache_name = f"embeddings_{hash_descriptions(df)}.npy"
model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

if os.path.exists(cache_name):
    desc_embeddings = np.load(cache_name)
else:
    desc_embeddings = model.encode(df['text'].tolist(), show_progress_bar=True)
    np.save(cache_name, desc_embeddings)

def get_keywords(text):
    words = set(text.lower().split())
    return words - ENGLISH_STOP_WORDS

def get_overlap_keywords(text1, text2):
    return get_keywords(text1) & get_keywords(text2)

def semantic_keyword_search(query, top_n=5):
    query_embedding = model.encode([query])
    sim_scores = cosine_similarity(query_embedding, desc_embeddings).flatten()

    top_indices = sim_scores.argsort()[::-1][:top_n * 5]
    results = df.iloc[top_indices][['course_code', 'title', 'description', 'text']].copy()
    results['score'] = sim_scores[top_indices]
    results = results[results['score'] > 0.4]
    results['reason'] = results['text'].apply(lambda t: ', '.join(get_overlap_keywords(t, query)))
    return results.drop(columns=['text'])

def get_semantic_recommendations(course_code, top_n=5, department_filter=None):
    norm_code = course_code.strip().upper()
    course_idx = df[df['course_code'].str.strip().str.upper() == norm_code].index

    if course_idx.empty:
        return f"Course code '{course_code}' not found."

    course_idx = course_idx[0]
    query_embedding = desc_embeddings[course_idx].reshape(1, -1)
    query_text = df.iloc[course_idx]['text']

    sim_scores = cosine_similarity(query_embedding, desc_embeddings).flatten()

    if department_filter:
        mask = df['course_code'].str.startswith(department_filter)
        df_filtered = df[mask].reset_index()
        sim_scores = sim_scores[mask.values]
    else:
        df_filtered = df.reset_index()

    filtered_idx = df_filtered[df_filtered['index'] == course_idx].index
    exclude_idx = filtered_idx[0] if not filtered_idx.empty else -1

    top_indices = sim_scores.argsort()[::-1]
    top_indices = [i for i in top_indices if i != exclude_idx][:top_n]

    results = df_filtered.iloc[top_indices][['course_code', 'title', 'description', 'text']].copy()
    results['score'] = sim_scores[top_indices]
    results = results[results['score'] > 0.4]
    results['reason'] = results['text'].apply(lambda t: ', '.join(get_overlap_keywords(t, query_text)))
    return results.drop(columns=['text'])
