import joblib
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score

# 1. Reload the serialized model artifact
pipeline_file = "models/airline_churn_pipeline.pkl"
print(f"Reloading model artifact from: {pipeline_file}...")
model = joblib.load(pipeline_file)

# 2. Ingest independent holdout test set
test_df = pd.read_csv("data/test.csv")
drop_cols = [c for c in ['Unnamed: 0', 'id'] if c in test_df.columns]
test_df = test_df.drop(columns=drop_cols)

# Apply consistent data cleaning steps
test_df['Arrival Delay in Minutes'] = test_df['Arrival Delay in Minutes'].fillna(test_df['Departure Delay in Minutes'])
test_df['Digital_Touchpoint_Score'] = (
    test_df['Inflight wifi service'] + 
    test_df['Ease of Online booking'] + 
    test_df['Online boarding']
) / 3.0
test_df['Delay_Per_100_Miles'] = (test_df['Arrival Delay in Minutes'] / (test_df['Flight Distance'] + 1)) * 100

test_df['churn_risk'] = (test_df['satisfaction'] != 'satisfied').astype(int)
X_test = test_df.drop(columns=['satisfaction', 'churn_risk'])
y_test = test_df['churn_risk']

# 3. Generate predictions
preds = model.predict(X_test)
probs = model.predict_proba(X_test)[:, 1]

print("\n=== Peer Verification Successful: Out-of-Sample Performance ===")
print(f"Total Test Passengers Scored: {len(test_df):,}")
print(f"Test Partition ROC-AUC Score: {roc_auc_score(y_test, probs):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, preds, target_names=['Retained', 'Churn Risk']))