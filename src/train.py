import os
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Ensure output directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# 1. Load Data
df = pd.read_csv("data/train.csv")

# Clean unneeded index columns
drop_cols = [c for c in ['Unnamed: 0', 'id'] if c in df.columns]
df = df.drop(columns=drop_cols)

# Target: 1 for satisfied, 0 for neutral or dissatisfied
df['target'] = (df['satisfaction'] == 'satisfied').astype(int)
X = df.drop(columns=['satisfaction', 'target'])
y = df['target']

# Identify feature types
cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

# 2. Build Preprocessor Pipeline
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

# 3. Stratified 80/20 Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Model Pipeline & Fitting
rf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1))
])

print("Training Random Forest Classifier on 83,000+ records...")
rf_pipeline.fit(X_train, y_train)

# 5. Evaluate
y_pred = rf_pipeline.predict(X_test)
y_proba = rf_pipeline.predict_proba(X_test)[:, 1]

print("\n=== Model Performance ===")
print(classification_report(y_test, y_pred, target_names=['Dissatisfied/Neutral', 'Satisfied']))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# 6. Save Reproducible Handoff Artifact (.pkl)
joblib.dump(rf_pipeline, "models/airline_satisfaction_pipeline.pkl")
print("Saved model artifact to models/airline_satisfaction_pipeline.pkl")

# 7. Generate Feature Importance Visual Asset
cat_encoder = rf_pipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
encoded_cat_names = list(cat_encoder.get_feature_names_out(cat_cols))
all_features = num_cols + encoded_cat_names

importances = rf_pipeline.named_steps['classifier'].feature_importances_
top_indices = np.argsort(importances)[-10:]

plt.figure(figsize=(9, 5))
plt.barh([all_features[i] for i in top_indices], importances[top_indices], color='#1f77b4')
plt.title("Top 10 Drivers of Airline Passenger Satisfaction", fontsize=13, fontweight='bold')
plt.xlabel("Random Forest Feature Importance")
plt.tight_layout()
plt.savefig("assets/satisfaction_feature_importance.png", dpi=300)
plt.close()
print("Saved chart to assets/satisfaction_feature_importance.png")