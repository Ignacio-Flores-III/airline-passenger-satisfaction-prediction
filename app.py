import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Airline Churn & Capex Simulator", layout="wide")

@st.cache_resource
def load_model():
    return joblib.load("artifacts/model.joblib")

model = load_model()

st.title("Commercial Aviation Churn & Fleet Capex Simulator")
st.markdown("**Decision Support System:** Evaluating Digital Infrastructure ($6M–$8M) vs. Physical Cabin Seating ($25M–$50M)")

tab1, tab2 = st.tabs(["1. Passenger Friction Simulator", "2. Capex & Recovery ROI Optimizer"])

with tab1:
    st.subheader("Real-Time Churn Risk Scoring (`artifacts/model.joblib`)")
    col1, col2, col3 = st.columns(3)

    with col1:
        customer_type = st.selectbox("Customer Type", ["Loyal Customer", "disloyal Customer"])
        travel_type = st.selectbox("Type of Travel", ["Business travel", "Personal Travel"])
        cabin_class = st.selectbox("Cabin Class", ["Business", "Eco", "Eco Plus"])
        age = st.slider("Passenger Age", 18, 80, 42)
        flight_distance = st.slider("Flight Distance (miles)", 100, 4000, 1200)

    with col2:
        online_boarding = st.slider("Online Boarding (1–5)", 1, 5, 2)
        inflight_wifi = st.slider("Inflight Wi-Fi Service (1–5)", 1, 5, 2)
        online_booking = st.slider("Ease of Online Booking (1–5)", 1, 5, 3)
        dep_delay = st.slider("Departure Delay (minutes)", 0, 180, 25)
        arr_delay = st.slider("Arrival Delay (minutes)", 0, 180, 25)

    with col3:
        seat_comfort = st.slider("Seat Comfort (1–5)", 1, 5, 3)
        leg_room = st.slider("Leg Room Service (1–5)", 1, 5, 3)
        inflight_ent = st.slider("Inflight Entertainment (1–5)", 1, 5, 3)
        onboard_service = st.slider("On-board Service (1–5)", 1, 5, 3)
        cleanliness = st.slider("Cleanliness (1–5)", 1, 5, 4)

    sample_row = pd.DataFrame([{
        "Gender": "Male",
        "Customer Type": customer_type,
        "Age": age,
        "Type of Travel": travel_type,
        "Class": cabin_class,
        "Flight Distance": flight_distance,
        "Inflight wifi service": inflight_wifi,
        "Departure/Arrival time convenient": 3,
        "Ease of Online booking": online_booking,
        "Gate location": 3,
        "Food and drink": 3,
        "Online boarding": online_boarding,
        "Seat comfort": seat_comfort,
        "Inflight entertainment": inflight_ent,
        "On-board service": onboard_service,
        "Leg room service": leg_room,
        "Baggage handling": 4,
        "Checkin service": 3,
        "Inflight service": 4,
        "Cleanliness": cleanliness,
        "Departure Delay in Minutes": dep_delay,
        "Arrival Delay in Minutes": arr_delay,
    }])

    probs = model.predict_proba(sample_row)[0]
    classes = list(model.classes_)
    churn_idx = classes.index("neutral or dissatisfied") if "neutral or dissatisfied" in classes else 0
    churn_prob = float(probs[churn_idx])

    st.divider()
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Defection Risk", f"{churn_prob:.1%}", delta="High Risk" if churn_prob >= 0.18 else "Low Risk", delta_color="inverse")
    m2.metric("Annual Repeat Revenue at Stake", "$1,800" if customer_type == "Loyal Customer" else "$450")
    m3.metric("Recommended Action", "Trigger Bonus Miles / Lounge Pass" if churn_prob >= 0.18 else "No Intervention Needed")

with tab2:
    st.subheader("Fleet Capex & Monte Carlo Sensitivity Simulator")
    c1, c2 = st.columns([1, 2])
    with c1:
        capex_m = st.slider("Digital Wi-Fi & Boarding Capex ($M)", 5.0, 12.0, 7.0, 0.5)
        avg_fare = st.slider("Average Round-Trip Fare ($)", 300, 650, 450, 25)
        trips_yr = st.slider("Repeat Trips / Year", 2, 8, 4)
        save_rate = st.slider("Recovery Campaign Save Rate (%)", 20, 80, 55, 5) / 100.0
        voucher_cost = st.slider("Service Recovery Cost / Flagged Flyer ($)", 10, 75, 25, 5)

    at_risk_cohort = 10778  # Holdout dissatisfied cohort size
    ltv = avg_fare * trips_yr
    gross_saved_m = (at_risk_cohort * save_rate * ltv) / 1e6
    recovery_cost_m = (at_risk_cohort * voucher_cost) / 1e6
    net_val_m = gross_saved_m - recovery_cost_m
    first_year_roi = (net_val_m - capex_m) / capex_m

    with c2:
        k1, k2, k3 = st.columns(3)
        k1.metric("Gross Revenue Saved", f"${gross_saved_m:.2f}M")
        k2.metric("Net Recovery Value", f"${net_val_m:.2f}M", delta=f"-${recovery_cost_m:.2f}M cost")
        k3.metric("Year-1 Digital Capex ROI", f"{first_year_roi:.1%}")

        rng = np.random.default_rng(42)
        sim_fares = rng.normal(avg_fare, 55, 1000)
        sim_saves = rng.uniform(max(0.15, save_rate - 0.15), min(0.90, save_rate + 0.15), 1000)
        sim_net = (at_risk_cohort * sim_saves * (sim_fares * trips_yr) - at_risk_cohort * voucher_cost) / 1e6
        ci_low, ci_high = np.percentile(sim_net, [2.5, 97.5])
        st.info(f"**1,000-Trial Monte Carlo 95% Confidence Interval:** Net Value Created ranges from **${ci_low:.2f}M to ${ci_high:.2f}M**.")
        st.bar_chart(pd.DataFrame({"Simulated Net Value ($M)": sim_net[:100]}))
