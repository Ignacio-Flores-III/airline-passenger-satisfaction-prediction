import joblib
import pandas as pd
import sklearn

# 1. Load the fitted preprocessing + model pipeline in a fresh session
artifact_path = "artifacts/model.joblib"
loaded_pipeline = joblib.load(artifact_path)
print(f"Successfully loaded pipeline from {artifact_path} (scikit-learn v{sklearn.__version__})")

# 2. Construct two distinct passenger profiles to test both outcome classes
sample_passengers = pd.DataFrame([
    {
        # Profile A: High friction & personal travel (Expected: Neutral or Dissatisfied)
        "Gender": "Male", "Customer Type": "disloyal Customer", "Age": 29,
        "Type of Travel": "Personal Travel", "Class": "Eco", "Flight Distance": 850,
        "Inflight wifi service": 1, "Departure/Arrival time convenient": 2,
        "Ease of Online booking": 1, "Gate location": 2, "Food and drink": 2,
        "Online boarding": 1, "Seat comfort": 3, "Inflight entertainment": 2,
        "On-board service": 2, "Leg room service": 3, "Baggage handling": 2,
        "Checkin service": 2, "Inflight service": 2, "Cleanliness": 2,
        "Departure Delay in Minutes": 65, "Arrival Delay in Minutes": 70.0
    },
    {
        # Profile B: Seamless digital touchpoints (Expected: Satisfied)
        "Gender": "Female", "Customer Type": "Loyal Customer", "Age": 41,
        "Type of Travel": "Business travel", "Class": "Eco", "Flight Distance": 1200,
        "Inflight wifi service": 5, "Departure/Arrival time convenient": 4,
        "Ease of Online booking": 5, "Gate location": 4, "Food and drink": 3,
        "Online boarding": 5, "Seat comfort": 2, "Inflight entertainment": 3,
        "On-board service": 4, "Leg room service": 2, "Baggage handling": 4,
        "Checkin service": 4, "Inflight service": 4, "Cleanliness": 4,
        "Departure Delay in Minutes": 0, "Arrival Delay in Minutes": 0.0
    }
])

# 3. Generate predictions
predictions = loaded_pipeline.predict(sample_passengers)
probabilities = loaded_pipeline.predict_proba(sample_passengers)[:, 1]

for idx, (pred, prob) in enumerate(zip(predictions, probabilities), start=1):
    label = "Satisfied" if pred == 1 else "Neutral or Dissatisfied (Churn Risk)"
    print(f"Passenger {idx} -> Prediction: {label} | Satisfaction Probability: {prob:.2%}")
