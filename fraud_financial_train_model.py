import pandas as pd
import numpy as np
import pickle
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

# --- 1. Load and Merge Datasets ---
print(" Loading datasets...")
df_fraud = pd.read_csv('fraud.csv', encoding='latin-1')
df_nonfraud = pd.read_csv('nonfraud.csv', encoding='latin-1')

df_fraud['label'] = 1
df_nonfraud['label'] = 0

def get_text_column(df):
    cols = df.select_dtypes(include=['object', 'string']).columns
    return df[cols].apply(lambda x: x.str.len().mean()).idxmax()

df = pd.concat([
    pd.DataFrame({'text': df_fraud[get_text_column(df_fraud)], 'label': 1}),
    pd.DataFrame({'text': df_nonfraud[get_text_column(df_nonfraud)], 'label': 0})
], ignore_index=True).dropna()

def clean_news(text):
    text = str(text).lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    return text

df['text'] = df['text'].apply(clean_news)

# --- 2. Split Data ---
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
)

# --- 3. THE UPDATED PIPELINE (ADD IT HERE) ---
# This configuration prevents "Overfitting" to neutral financial news
fraud_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        stop_words='english', 
        ngram_range=(1, 3), 
        max_features=10000,
        min_df=5,      # FIX: Ignores rare words that cause false alarms
        sublinear_tf=True
    )),
    ('classifier', RandomForestClassifier(
        n_estimators=200, 
        max_depth=20,  # FIX: Limits the model so it doesn't "over-memorize"
        random_state=42, 
        n_jobs=-1
    ))
])

# --- 4. Train & Evaluate ---
print(f" Re-Training Model with Overfitting Protection...")
fraud_pipeline.fit(X_train, y_train)

predictions = fraud_pipeline.predict(X_test)
acc = accuracy_score(y_test, predictions)

print(f"\n UPDATED ACCURACY: {acc:.2%}")
print(classification_report(y_test, predictions))

# --- 5. Save Model ---
with open('fraud_news_model.pkl', 'wb') as f:
    pickle.dump(fraud_pipeline, f)

print(f"\n Model updated and saved!")