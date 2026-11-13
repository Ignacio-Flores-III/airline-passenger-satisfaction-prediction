import os
import joblib
import pandas as pd
import numpy as np
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score

# 1. Locate dataset (adjust path if stored in a subfolder like data/raw/)
train_path = "data/train.csv" if os.path.exists("data/train.csv") else "train.csv"
test_path = "data/test.csv" if os.path.exists("data/test.csv") else "test.csv"

print(f"Loading data from {train_path} and {test_path}...")
train_df = pd.read_csv(train_path)
test_df = pd.read_csv(test_path)

# Drop index/ID columns if present
drop_cols = [col for col in ["Unnamed: 0", "id"] if col in train_df.columns]
train_df = train_df.drop(columns=drop_cols)
test_df = test_df.drop(columns=drop_cols)

# 2. Separate features and target
target_col = "satisfaction"
X_train = train_df.drop(columns=[target_col])
y_train = (train_df[target_col] == "satisfied").astype(int)

X_test = test_df.drop(columns=[target_col])
y_test = (test_df[target_col] == "satisfied").astype(int)

# 3. Define feature groups
categorical_cols = X_train.select_dtypes(include=["object", "category"]).columns.tolist()
numeric_cols = X_train.select_dtypes(include=["int64", "float64"]).columns.tolist()

# 4. Build unified preprocessing + Random Forest pipeline
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)

full_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
])

# 5. Fit and evaluate on holdout test set
print("Fitting unified preprocessing + Random Forest pipeline...")
full_pipeline.fit(X_train, y_train)

preds = full_pipeline.predict(X_test)
probs = full_pipeline.predict_proba(X_test)[:, 1]

print(f"Holdout Accuracy: {accuracy_score(y_test, preds):.4f}")
print(f"Holdout F1-Score: {f1_score(y_test, preds):.4f}")
print(f"Holdout ROC-AUC:  {roc_auc_score(y_test, probs):.4f}")

# 6. Save artifact and metadata for P2 reproducibility
os.makedirs("artifacts", exist_ok=True)
artifact_path = "artifacts/model.joblib"
joblib.dump(full_pipeline, artifact_path)
print(f"Saved complete pipeline artifact to {artifact_path}")
print(f"Environment versions -> scikit-learn: {sklearn.__version__}, pandas: {pd.__version__}, numpy: {np.__version__}")