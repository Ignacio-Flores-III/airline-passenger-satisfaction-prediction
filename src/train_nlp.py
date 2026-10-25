import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# Ensure folders exist
os.makedirs("models", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# 1. Load Data
df = pd.read_csv("data/airline_reviews.csv")

# Identify text and target fields
text_col = [c for c in df.columns if 'review' in c.lower() and c.lower() != 'review_date'][0]
target_col = [c for c in df.columns if 'recommend' in c.lower() or 'overall' in c.lower()][0]

print(f"Loaded {len(df):,} reviews. Using text column: '{text_col}', target column: '{target_col}'")

# Data Cleaning: drop nulls in review text and target
df = df.dropna(subset=[text_col, target_col]).copy()

# Target definition: 1 = Recommended / Positive, 0 = Defection / Negative
if df[target_col].dtype == object:
    df['target'] = df[target_col].astype(str).str.strip().str.lower().apply(
        lambda x: 1 if x in ['yes', '1', 'recommended'] else 0
    )
else:
    df['target'] = (df[target_col] >= 6).astype(int)

# Basic text cleaning: lowercase and remove non-letters
df['clean_text'] = df[text_col].astype(str).str.lower().str.replace(r'[^a-zA-Z\s]', '', regex=True)

# 80/20 Stratified Split
X_train, X_test, y_train, y_test = train_test_split(
    df['clean_text'], df['target'], test_size=0.2, random_state=42, stratify=df['target']
)

# 2. Build NLP Pipeline: TF-IDF (Unigrams + Bigrams) + Regularized Logistic Regression
nlp_pipeline = Pipeline(steps=[
    ('tfidf', TfidfVectorizer(max_features=2500, stop_words='english', ngram_range=(1, 2))),
    ('classifier', LogisticRegression(max_iter=1000, random_state=42))
])

print("Fitting TF-IDF Vectorizer and Logistic Regression Classifier...")
nlp_pipeline.fit(X_train, y_train)

# 3. Model Evaluation
y_pred = nlp_pipeline.predict(X_test)
y_proba = nlp_pipeline.predict_proba(X_test)[:, 1]

print("\n=== Model Diagnostic Report ===")
print(classification_report(y_test, y_pred, target_names=['Defection (Negative)', 'Recommended (Positive)']))
print(f"Test ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# 4. Save Reproducible Handoff Artifact (.pkl)
joblib.dump(nlp_pipeline, "models/airline_nlp_pipeline.pkl")
print("Saved fitted model artifact to: models/airline_nlp_pipeline.pkl")

# 5. GRAPH: Top Lexical Drivers of Churn vs. Retention
feature_names = np.array(nlp_pipeline.named_steps['tfidf'].get_feature_names_out())
coefs = nlp_pipeline.named_steps['classifier'].coef_[0]

top_neg = np.argsort(coefs)[:8]
top_pos = np.argsort(coefs)[-8:]
combined_idx = np.concatenate([top_neg, top_pos])

words = feature_names[combined_idx]
scores = coefs[combined_idx]
# Ensure negative coefficients (churn words) are red, positive coefficients (loyalty words) are green
colors = ['#e74c3c' if s < 0 else '#2ecc71' for s in scores]

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.figure(figsize=(9, 5))
plt.barh(words, scores, color=colors)
plt.axvline(0, color='black', linestyle='--', linewidth=0.8)
plt.title("NLP Drivers of Passenger Recommendation vs. Churn", fontsize=12, fontweight='bold')
plt.xlabel("Log-Odds Impact on Recommendation")
plt.tight_layout()
plt.savefig("assets/nlp_sentiment_drivers.png", dpi=300)
plt.close()
print("Saved presentation visual to assets/nlp_sentiment_drivers.png")