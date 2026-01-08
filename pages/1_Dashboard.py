import streamlit as st
import os
import joblib
import numpy as np
import random

# ------------------ Paths for model and scaler ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # points to pages/
MODEL_PATH = os.path.join(BASE_DIR, "..", "model.pkl")  # root folder
SCALER_PATH = os.path.join(BASE_DIR, "..", "scaler.pkl")

# ------------------ Load model and scaler ------------------
@st.cache_data(show_spinner=False)
def load_model():
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    return model, scaler

model, scaler = load_model()

# ------------------ Page Content ------------------
st.title("📊 Dashboard - FraudSense AI")

# Fake transactions processed counter
if "tx_count" not in st.session_state:
    st.session_state.tx_count = random.randint(120000,150000)
st.session_state.tx_count += random.randint(5,20)
st.markdown(f"<div style='background:#0d1117;padding:20px;border-radius:12px;text-align:center;color:#00b4ff;border:1px solid #30363d;'>Transactions Processed: {st.session_state.tx_count:,}</div>", unsafe_allow_html=True)

st.divider()

# ------------------ Transaction Input ------------------
col1, col2, col3 = st.columns(3)
with col1:
    amount = st.number_input("Transaction Amount (₹)", 10.0, step=100.0)
with col2:
    hour = st.slider("Transaction Hour", 0, 23, 12)
with col3:
    tx_24h = st.slider("Transactions (Last 24h)", 1, 50, 3)

# ------------------ Risk Analysis ------------------
if st.button("Analyze Risk"):
    X = np.array([[amount, hour, tx_24h]])
    X_scaled = scaler.transform(X)

    pred = model.predict(X_scaled)
    score = abs(model.decision_function(X_scaled)[0])

    if pred[0] == -1:
        st.error("🚨 HIGH RISK TRANSACTION")
    else:
        st.success("✅ LOW RISK TRANSACTION")

    st.progress(min(score, 1.0))
    st.write(f"Risk Score: **{score:.2f}**")

    # Save history
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(score)
