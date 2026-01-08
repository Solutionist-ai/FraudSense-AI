import streamlit as st
import numpy as np
import joblib
import random

# Load model
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("📊 Transaction Dashboard")

# Fake counter
if "tx_count" not in st.session_state:
    st.session_state.tx_count = random.randint(120000, 150000)
st.session_state.tx_count += random.randint(5, 20)
st.metric("Transactions Processed", f"{st.session_state.tx_count:,}")

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    amount = st.number_input("Transaction Amount (₹)", 10.0, step=100.0)
with col2:
    hour = st.slider("Transaction Hour", 0, 23, 12)
with col3:
    tx_24h = st.slider("Transactions (Last 24h)", 1, 50, 3)

if st.button("Analyze Risk", use_container_width=True):
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

    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append(score)

