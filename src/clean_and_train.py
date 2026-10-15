import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# Ensure target directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# 1. LOAD RAW DATA
df = pd.read_csv("data/train.csv")
print(f"Loaded {len(df):,} raw passenger survey records.")

# 2. EXPLICIT DATA CLEANING & PREPROCESSING PIPELINE
# A. Drop unneeded primary key columns
drop_cols = [c for c in ['Unnamed: 0', 'id'] if c in df.columns]
df = df.drop(columns=drop_cols)

# B. Clean & Impute Missing Delay Values (Arrival Delay contains ~310 nulls)
missing_delays = df['Arrival Delay in Minutes'].isnull().sum()
print(f"Data Cleaning: Found {missing_delays:,} null values in 'Arrival Delay in Minutes'. Imputing with departure delay values.")
df['Arrival Delay in Minutes'] = df['Arrival Delay in Minutes'].fillna(df['Departure Delay in Minutes'])

# C. Outlier Capping on Delays (IQR Method to handle extreme weather anomalies)
q75 = df['Arrival Delay in Minutes'].quantile(0.75)
q25 = df['Arrival Delay in Minutes'].quantile(0.25)
iqr = q75 - q25
upper_bound = q75 + (3.0 * iqr)
capped_outliers = (df['Arrival Delay in Minutes'] > upper_bound).sum()
print(f"Data Cleaning: Capped {capped_outliers:,} extreme arrival delay outliers at {upper_bound:.1f} minutes.")
df['Arrival Delay in Minutes'] = np.clip(df['Arrival Delay in Minutes'], 0, upper_bound)

# D. Feature Engineering: Digital Index & Delay Severity Ratio
# Combine digital touchpoints into an aggregated score
df['Digital_Touchpoint_Score'] = (
    df['Inflight wifi service'] + 
    df['Ease of Online booking'] + 
    df['Online boarding']
) / 3.0

# Calculate delay impact per 100 miles of flight distance
df['Delay_Per_100_Miles'] = (df['Arrival Delay in Minutes'] / (df['Flight Distance'] + 1)) * 100

# 3. DEFINE TARGET & SPLIT
# 1 = Churn Risk (Neutral/Dissatisfied), 0 = Retained (Satisfied)
df['churn_risk'] = (df['satisfaction'] != 'satisfied').astype(int)
X = df.drop(columns=['satisfaction', 'churn_risk'])
y = df['churn_risk']

cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

# 4. PREPROCESSING PIPELINES
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, num_cols),
        ('cat', categorical_transformer, cat_cols)
    ]
)

# 5. STRATIFIED SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 6. MODEL TRAINING (Random Forest: 100 Estimators)
rf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1))
])

print("\nTraining Random Forest Churn Classifier on 83,000+ cleaned records...")
rf_pipeline.fit(X_train, y_train)

# 7. EVALUATION & FINANCIAL COST MATRIX
y_pred = rf_pipeline.predict(X_test)
y_proba = rf_pipeline.predict_proba(X_test)[:, 1]

cm = confusion_matrix(y_test, y_pred)
# cm structure: [ [True Retained (TN), False Churn (FP)],
#                 [Missed Churn (FN), Caught Churn (TP)] ]
tn, fp, fn, tp = cm.ravel()

# Financial Assumptions:
# Annual LTV lost per missed churn customer = $1,800
# Retention intervention voucher cost per false alarm = $50
total_revenue_saved = tp * 1800
cost_of_false_alarms = fp * 50
net_financial_value = total_revenue_saved - cost_of_false_alarms

print("\n=== Model Diagnostic & Financial Impact Report ===")
print(f"Test Set ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")
print(f"Correctly Identified Churn Customers (True Positives): {tp:,}")
print(f"Missed Churn Defects (False Negatives): {fn:,}")
print(f"Gross At-Risk Revenue Preserved: ${total_revenue_saved:,.2f}")
print(f"Net Economic Value Delivered on Test Cohort: ${net_financial_value:,.2f}")

# 8. SAVE REPRODUCIBLE PIPELINE ARTIFACT (.pkl)
joblib.dump(rf_pipeline, "models/airline_churn_pipeline.pkl")
print("Saved production pipeline artifact to: models/airline_churn_pipeline.pkl")

# 9. GRAPH 1: Financial Capex Allocation Chart
cat_encoder = rf_pipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
all_features = num_cols + list(cat_encoder.get_feature_names_out(cat_cols))
importances = rf_pipeline.named_steps['classifier'].feature_importances_
top_idx = np.argsort(importances)[-8:]

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.figure(figsize=(9, 5))
plt.barh([all_features[i] for i in top_idx], importances[top_idx] * 100, color='#2980b9')
plt.title("Fleet ROI: Top Operational Levers Driving Customer Churn", fontsize=12, fontweight='bold')
plt.xlabel("Percentage Share of Churn Predictive Power (%)")
plt.tight_layout()
plt.savefig("assets/churn_capex_feature_importance.png", dpi=300)
plt.close()

# 10. GRAPH 2: Financial ROI Trade-off Plot
plt.figure(figsize=(7, 5))
categories = ['Gross Revenue Saved', 'Retention Cost', 'Net Value Created']
values = [total_revenue_saved / 1e6, cost_of_false_alarms / 1e6, net_financial_value / 1e6]
colors = ['#27ae60', '#e74c3c', '#2980b9']

plt.bar(categories, values, color=colors)
plt.title("Net Economic Value Created on Holdout Test Cohort ($ Millions)", fontsize=12, fontweight='bold')
plt.ylabel("$ Millions (USD)")
for i, v in enumerate(values):
    plt.text(i, v + 0.3, f"${v:.2f}M", ha='center', fontweight='bold')
plt.ylim(0, max(values) + 3)
plt.tight_layout()
plt.savefig("assets/economic_value_created.png", dpi=300)
plt.close()
print("Saved financial presentation charts to 'assets/' folder.")