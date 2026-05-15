import streamlit as st
import numpy as np
import joblib
from pathlib import Path

from tensorflow import keras

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "fuel_efficiency_model.keras"
SCALER_PATH = BASE_DIR / "scaler.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

if not SCALER_PATH.exists():
    raise FileNotFoundError(f"Scaler file not found: {SCALER_PATH}")

@st.cache_resource
def load_model(path: Path):
    return keras.models.load_model(str(path))

@st.cache_resource
def load_scaler(path: Path):
    return joblib.load(str(path))

model = load_model(MODEL_PATH)
scaler = load_scaler(SCALER_PATH)

st.set_page_config(
    page_title="AI Vehicle Analytics",
    page_icon="🚗",
    layout="wide"
)

st.title("AI Vehicle Analytics Platform")
st.markdown(
    "Fuel-efficient driving starts with better predictions. Enter your vehicle specs and get instant MPG, fuel cost, and CO₂ results."
)

with st.container():
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    feature_col1.metric("MPG Forecast", "Smart vehicle insights")
    feature_col2.metric("Fuel Cost", "Cost per km optimized")
    feature_col3.metric("CO₂ Emission", "Cleaner decisions")

st.markdown("---")

# Sidebar inputs
with st.sidebar:
    st.header("Vehicle Details")
    cylinders = st.slider("Cylinders", 1, 16, 4)
    displacement = st.slider("Displacement (cu. in.)", 68.0, 455.0, 150.0, step=1.0)
    horsepower = st.slider("Horsepower", 46.0, 230.0, 100.0, step=1.0)
    weight = st.slider("Weight (lbs)", 1613.0, 5140.0, 2500.0, step=10.0)
    acceleration = st.slider("Acceleration (0-60 mph)", 8.0, 24.8, 15.0, step=0.1)
    model_year = st.slider("Model Year", 70, 82, 76)
    origin = st.radio("Origin", [1, 2, 3], format_func=lambda x: {1: 'USA', 2: 'Europe', 3: 'Japan'}[x])
    st.markdown("---")
    st.subheader("Cost Calculator")
    fuel_price = st.number_input("Fuel Price (₹ per litre)", min_value=0.0, value=100.0, step=1.0)
    distance = st.number_input("Distance per Month (km)", min_value=0.0, value=500.0, step=10.0)
    st.markdown(
        "### Notes\n- Model years are in the 1970-1982 range.\n- Origin values map to USA, Europe, Japan.\n- Fuel cost uses a litre-based estimate for better accuracy."
    )
    predict_now = st.button("Predict Now")

if predict_now:
    input_data = np.array([[
        cylinders,
        displacement,
        horsepower,
        weight,
        acceleration,
        model_year,
        origin,
    ]])

    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    mpg = float(prediction[0][0])

    if mpg <= 0 or np.isnan(mpg):
        st.error("Prediction produced an invalid MPG. Check the input values and try again.")
    else:
        distance_miles = distance * 0.621371
        gallons_used = distance_miles / mpg
        liters_used = gallons_used * 3.78541
        fuel_cost = liters_used * fuel_price
        co2 = liters_used * 2.31

        st.success("Prediction successful")
        st.markdown("## Results")

        result_col1, result_col2, result_col3 = st.columns(3)
        result_col1.metric("Predicted MPG", f"{mpg:.2f}")
        result_col2.metric("Estimated Fuel Cost", f"₹{fuel_cost:.2f}")
        result_col3.metric("Estimated CO₂", f"{co2:.2f} kg")

        with st.expander("View detailed summary"):
            st.write(
                {
                    "Cylinders": cylinders,
                    "Displacement": displacement,
                    "Horsepower": horsepower,
                    "Weight": weight,
                    "Acceleration": acceleration,
                    "Model Year": model_year,
                    "Origin": {1: 'USA', 2: 'Europe', 3: 'Japan'}[origin],
                    "Distance (km)": distance,
                    "Fuel price (₹/litre)": fuel_price,
                    "Predicted MPG": round(mpg, 2),
                    "Fuel used (litres)": round(liters_used, 2),
                    "Distance (miles)": round(distance_miles, 2),
                }
            )

        chart_col1, chart_col2 = st.columns([2, 1])
        chart_col1.bar_chart(
            {
                "MPG": [mpg],
                "Litres Used": [liters_used],
                "CO₂ (kg)": [co2],
            }
        )
        chart_col2.write("### Quick tips")
        chart_col2.markdown(
            "- Reduce weight and idling to improve MPG.\n- Maintain proper tire pressure.\n- Choose fuel-efficient routes when possible."
        )
