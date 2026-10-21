import joblib

# 1. Reload fitted pipeline
pipeline = joblib.load("models/airline_nlp_pipeline.pkl")
print("Successfully reloaded models/airline_nlp_pipeline.pkl")

# 2. Test unseen review samples
sample_reviews = [
    "Four hour flight delay, lost my luggage, and terrible customer service at the gate.",
    "Excellent boarding process, smooth flight, very clean cabin and friendly crew."
]

preds = pipeline.predict(sample_reviews)
probs = pipeline.predict_proba(sample_reviews)[:, 1]

for r, p, pr in zip(sample_reviews, preds, probs):
    label = "Positive / Recommended" if p == 1 else "Negative / Defection Risk"
    print(f"\nReview: '{r}'\nPredicted: {label} (Confidence: {pr:.1%})")