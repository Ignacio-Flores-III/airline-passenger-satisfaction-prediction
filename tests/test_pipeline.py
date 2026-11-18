import joblib
import numpy as np
import pandas as pd

if not hasattr(np, "long"):
    np.long = int


def test_artifact_inference_and_sensitivity():
    model = joblib.load("artifacts/model.joblib")
    base = {
        "Gender": "Male",
        "Customer Type": "Loyal Customer",
        "Age": 40,
        "Type of Travel": "Business travel",
        "Class": "Business",
        "Flight Distance": 1500,
        "Inflight wifi service": 1,
        "Departure/Arrival time convenient": 3,
        "Ease of Online booking": 2,
        "Gate location": 3,
        "Food and drink": 3,
        "Online boarding": 1,
        "Seat comfort": 3,
        "Inflight entertainment": 3,
        "On-board service": 3,
        "Leg room service": 3,
        "Baggage handling": 4,
        "Checkin service": 3,
        "Inflight service": 4,
        "Cleanliness": 4,
        "Departure Delay in Minutes": 30,
        "Arrival Delay in Minutes": 30.0,
    }
    upgraded = {**base, "Inflight wifi service": 5, "Online boarding": 5}
    df = pd.DataFrame([base, upgraded])
    probs = model.predict_proba(df)
    assert probs.shape == (2, 2)
    assert np.all((probs >= 0.0) & (probs <= 1.0))
    classes = list(model.classes_)
    churn_idx = classes.index("neutral or dissatisfied") if "neutral or dissatisfied" in classes else 0
    assert probs[1, churn_idx] < probs[0, churn_idx]