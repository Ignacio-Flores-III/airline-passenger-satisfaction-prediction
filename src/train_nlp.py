import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score

os.makedirs("models", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# 1. Load Data
df = pd.read_csv("data/airline_reviews.csv")

text_col = [c for c in df.columns if 'review' in c.lower() and c.lower() != 'review_date'][0]
target_col = [c for c in df.columns if 'recommend' in c.lower() or 'overall' in c.lower()][0]

df = df.dropna(subset=[text_col, target_col]).copy()

# Ensure 1 = Recommended / Positive, 0 = Negative / Churn
if df[target_col].dtype == object:
    df['target'] = df[target_col].astype(str).str.strip().str.lower().apply(
        lambda x: 1 if x in ['yes', '1', 'recommended', 'true'] else 0
    )
else:
    df['target'] = (df[target_col] >= 6).astype(int)

# Invert if the dataset used 1 for negative reviews
# Let's ensure 'target' aligns: positive reviews = 1, negative = 0
sample_positive_word_count = df[df['target'] == 1][text_col].str.lower().str.contains('good').sum()
sample_negative_word_count = df[df['target'] == 0][text_col].str.lower().str.contains('good').sum()

if sample_negative_word_count > sample_positive_word_count:
    # Target was inverted in the raw file; flip it
    df['target'] = 1 - df['target']

df['clean_text'] = df[text_col].astype(str).str.lower().str.replace(r'[^a-zA-Z\s]', '', regex=True)

# Remove generic meta words that skew the vocabulary
custom_stop_words = list(TfidfVectorizer(stop_words='english').get_stop_words()) + [
    'flight', 'airline', 'airways', 'plane', 'customer review', 'review', 'verified', 'trip'
]

X_train, X_test, y_train, y_test = train_test_split(
    df['clean_text'], df['target'], test_size=0.2, random_state=42, stratify=df['target']
)

# 2. Build Pipeline
nlp_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=2500, stop_words=custom_stop_words, ngram_range=(1, 2))),
    ('classifier', LogisticRegression(max_iter=1000, random_state=42))
])

nlp_pipeline.fit(X_train, y_train)

# 3. Save Artifact
joblib.dump(nlp_pipeline, "models/airline_nlp_pipeline.pkl")

# 4. Generate Properly Colored Plot
feature_names = np.array(nlp_pipeline.named_steps['tfidf'].get_feature_names_out())
coefs = nlp_pipeline.named_steps['classifier'].coef_[0]

# Bottom 8 coefficients (negative impact / churn drivers)
top_neg_idx = np.argsort(coefs)[:8]
# Top 8 coefficients (positive impact / loyalty drivers)
top_pos_idx = np.argsort(coefs)[-8:]
combined_idx = np.concatenate([top_neg_idx, top_pos_idx])

words = feature_names[combined_idx]
scores = coefs[combined_idx]
colors = ['#e74c3c' if s < 0 else '#2ecc71' for s in scores]

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.figure(figsize=(9, 5))
plt.barh(words, scores, color=colors)
plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
plt.title("NLP Drivers of Passenger Recommendation vs. Churn", fontsize=12, fontweight='bold')
plt.xlabel("Log-Odds Impact on Recommendation (Red = Churn, Green = Loyalty)")
plt.tight_layout()
plt.savefig("assets/nlp_sentiment_drivers.png", dpi=300)
plt.close()
print("Updated assets/nlp_sentiment_drivers.png with correct polarity.")