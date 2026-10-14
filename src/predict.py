import joblib
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score

# 1. Reload the serialized model artifact
pipeline_path = "models/airline_satisfaction_pipeline.pkl"
print(f"Loading fitted model artifact from {pipeline_path}...")
model = joblib.load(pipeline_path)

# 2. Ingest independent test data
test_df = pd.read_csv("data/test.csv")
drop_cols = [c for c in ['Unnamed: 0', 'id'] if c in test_df.columns]
test_df = test_df.drop(columns=drop_cols)

# Define target and features
test_df['target'] = (test_df['satisfaction'] == 'satisfied').astype(int)
X_holdout = test_df.drop(columns=['satisfaction', 'target'])
y_holdout = test_df['target']

# 3. Generate Predictions using the reloaded pipeline
predictions = model.predict(X_holdout)
probabilities = model.predict_proba(X_holdout)[:, 1]

# 4. Output Peer Verification Performance Metrics
print("\n=== Peer Replication Verification: Out-of-Sample Test Results ===")
print(f"Total Test Observations Scored: {len(test_df):,}")
print(f"Holdout ROC-AUC Score: {roc_auc_score(y_holdout, probabilities):.4f}")
print("\nClassification Report:")
print(classification_report(y_holdout, predictions, target_names=['Dissatisfied/Neutral', 'Satisfied']))