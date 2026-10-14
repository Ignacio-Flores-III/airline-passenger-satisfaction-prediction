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

# Ensure output directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# 1. Load Data
df = pd.read_csv("data/train.csv")
drop_cols = [c for c in ['Unnamed: 0', 'id'] if c in df.columns]
df = df.drop(columns=drop_cols)

# Target Definition: 1 = Satisfied, 0 = Neutral / Dissatisfied
df['target'] = (df['satisfaction'] == 'satisfied').astype(int)

# Set visual styling
sns.set_theme(style="whitegrid")

# GRAPH 1: Target Distribution Across Travel Classes
plt.figure(figsize=(8, 5))
order_classes = ['Eco', 'Eco Plus', 'Business']
sns.countplot(data=df, x='Class', hue='satisfaction', order=order_classes, palette=['#e74c3c', '#2ecc71'])
plt.title("Passenger Satisfaction by Flight Cabin Class", fontsize=13, fontweight='bold')
plt.xlabel("Cabin Class")
plt.ylabel("Number of Passengers")
plt.legend(title="Satisfaction", labels=['Neutral / Dissatisfied', 'Satisfied'])
plt.tight_layout()
plt.savefig("assets/target_distribution_by_class.png", dpi=300)
plt.close()

# GRAPH 2: Delay Impact (Arrival Delay <= 120 mins)
plt.figure(figsize=(9, 5))
delay_subset = df[df['Arrival Delay in Minutes'] <= 120].dropna(subset=['Arrival Delay in Minutes'])
sns.kdeplot(data=delay_subset, x='Arrival Delay in Minutes', hue='satisfaction', 
            common_norm=False, fill=True, palette=['#e74c3c', '#2ecc71'], alpha=0.3)
plt.title("Arrival Delay Density: Satisfied vs. Dissatisfied Passengers", fontsize=13, fontweight='bold')
plt.xlabel("Arrival Delay (Minutes)")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig("assets/flight_delay_vs_satisfaction.png", dpi=300)
plt.close()

# 2. Build Pipeline
X = df.drop(columns=['satisfaction', 'target'])
y = df['target']

cat_cols = X.select_dtypes(include=['object']).columns.tolist()
num_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()

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

# 3. Stratified Split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Train Model
rf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1))
])

print("Fitting Random Forest Classifier on training partition...")
rf_pipeline.fit(X_train, y_train)

# 5. Evaluate
y_pred = rf_pipeline.predict(X_test)
y_proba = rf_pipeline.predict_proba(X_test)[:, 1]

print("\n=== Model Performance ===")
print(classification_report(y_test, y_pred, target_names=['Dissatisfied/Neutral', 'Satisfied']))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

# Save fitted artifact (.pkl)
joblib.dump(rf_pipeline, "models/airline_satisfaction_pipeline.pkl")
print("Saved model artifact to models/airline_satisfaction_pipeline.pkl")

# GRAPH 3: Confusion Matrix Heatmap
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Dissatisfied', 'Satisfied'], 
            yticklabels=['Dissatisfied', 'Satisfied'])
plt.title("Random Forest Confusion Matrix", fontsize=12, fontweight='bold')
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.savefig("assets/confusion_matrix_heatmap.png", dpi=300)
plt.close()

# GRAPH 4: Top 10 Drivers of Satisfaction
cat_encoder = rf_pipeline.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot']
encoded_cat_names = list(cat_encoder.get_feature_names_out(cat_cols))
all_features = num_cols + encoded_cat_names

importances = rf_pipeline.named_steps['classifier'].feature_importances_
top_indices = np.argsort(importances)[-10:]

plt.figure(figsize=(9, 5))
plt.barh([all_features[i] for i in top_indices], importances[top_indices], color='#2980b9')
plt.title("Top 10 Drivers of Airline Passenger Satisfaction", fontsize=13, fontweight='bold')
plt.xlabel("Relative Feature Importance Score")
plt.tight_layout()
plt.savefig("assets/satisfaction_feature_importance.png", dpi=300)
plt.close()

print("\nAll 4 presentation charts saved to 'assets/' directory.")