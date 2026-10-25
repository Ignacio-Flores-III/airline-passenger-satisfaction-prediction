import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, mean_squared_error

# Ensure output directory exists
os.makedirs("assets", exist_ok=True)
os.makedirs("models", exist_ok=True)

# 1. LOAD & CLEAN DATA
df = pd.read_csv("data/train.csv")
drop_cols = [c for c in ['Unnamed: 0', 'id'] if c in df.columns]
df = df.drop(columns=drop_cols)

# Impute missing arrival delays with departure delay
df['Arrival Delay in Minutes'] = df['Arrival Delay in Minutes'].fillna(df['Departure Delay in Minutes'])

# Binary Target: 1 = Satisfied, 0 = Neutral/Dissatisfied
df['target'] = (df['satisfaction'] == 'satisfied').astype(int)

X = df.drop(columns=['satisfaction', 'target'])
y = df['target']

cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

# 2. STATSMODELS OLS (Linear Probability Model for Course Econometrics)
print("--- 1. Running OLS Linear Regression (Linear Probability Model) ---")
# Prepare simple encoded numeric subset for OLS summary
X_ols = pd.get_dummies(X, drop_first=True, dtype=float)
X_ols_imputed = X_ols.fillna(X_ols.median())
X_ols_const = sm.add_constant(X_ols_imputed)

ols_model = sm.OLS(y, X_ols_const).fit()
# Print top significant drivers from OLS
ols_summary_path = "assets/ols_regression_coefficients.txt"
with open(ols_summary_path, "w") as f:
    f.write(str(ols_model.summary()))
print(f"Saved full OLS statistical summary (p-values & R-squared) to {ols_summary_path}")

# 3. SCIKIT-LEARN PIPELINES FOR COURSE BENCHMARK COMPARISON
preprocessor = ColumnTransformer(
    transformers=[
        ('num', Pipeline([('imputer', SimpleImputer(strategy='median')), ('scaler', StandardScaler())]), num_cols),
        ('cat', Pipeline([('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'))]), cat_cols)
    ]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Fit preprocessor on train data
X_train_prep = preprocessor.fit_transform(X_train)
X_test_prep = preprocessor.transform(X_test)

# Candidate Models taught in MSBA coursework:
models = {
    # 1. Linear Regression (OLS via scikit-learn)
    "OLS Linear Regression": LinearRegression(),
    
    # 2. Logistic Regression (Logit with L2 Regularization)
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    
    # 3. Gradient Descent (Stochastic Gradient Descent with Log-Loss)
    "SGD Classifier (Gradient Descent)": SGDClassifier(loss='log_loss', max_iter=1000, tol=1e-3, random_state=42),
    
    # 4. Ensemble Random Forest
    "Random Forest (100 Trees)": RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
}

results = []

for name, model in models.items():
    print(f"Training: {name}...")
    model.fit(X_train_prep, y_train)
    
    if name == "OLS Linear Regression":
        # Continuous linear predictions clipped to [0, 1] for classification decision
        cont_preds = model.predict(X_test_prep)
        preds = (cont_preds >= 0.5).astype(int)
        probs = np.clip(cont_preds, 0, 1)
    else:
        preds = model.predict(X_test_prep)
        probs = model.predict_proba(X_test_prep)[:, 1]
    
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds)
    roc = roc_auc_score(y_test, probs)
    
    results.append({
        "Model": name,
        "Accuracy": acc,
        "F1-Score": f1,
        "ROC-AUC": roc
    })

benchmark_df = pd.DataFrame(results)
print("\n=== Model Benchmark Comparison Across Course Techniques ===")
print(benchmark_df.to_string(index=False))

# 4. EXPORT VISUAL ASSET FOR SLIDES / REPORT
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(10, 5))

x = np.arange(len(benchmark_df))
width = 0.25

ax.bar(x - width, benchmark_df['Accuracy'], width, label='Accuracy', color='#3498db')
ax.bar(x, benchmark_df['F1-Score'], width, label='F1-Score', color='#2ecc71')
ax.bar(x + width, benchmark_df['ROC-AUC'], width, label='ROC-AUC', color='#9b59b6')

ax.set_xticks(x)
ax.set_xticklabels(benchmark_df['Model'], rotation=10, ha='right', fontsize=10)
ax.set_ylabel("Metric Score (0.0 - 1.0)")
ax.set_title("Model Architecture Comparison: Linear vs. Gradient Descent vs. Random Forest", fontsize=12, fontweight='bold')
ax.legend(loc='lower right')
ax.set_ylim(0.70, 1.02)
plt.tight_layout()

chart_path = "assets/course_models_benchmark.png"
plt.savefig(chart_path, dpi=300)
plt.close()
print(f"\nSaved benchmark comparison graph to: {chart_path}")