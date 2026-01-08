import streamlit as st
import time
import numpy as np
import joblib
import random
import pandas as pd

# ----------------- Page Config -----------------
st.set_page_config(page_title="FraudSense AI", page_icon="🛡️", layout="wide")

# ----------------- CSS Styling -----------------
st.markdown("""
<style>
h1 { text-align:center; color:#00b4ff; font-size:48px; }
h3 { text-align:center; color:#9ba3af; font-weight:400; }
.box { background: #161b22; padding: 20px; border-radius: 15px; text-align:center; color:white; border: 1px solid #30363d; }
.metric-box { background: #0d1117; padding:20px; border-radius:12px; text-align:center; color:#00b4ff; border:1px solid #30363d; }
</style>
""", unsafe_allow_html=True)

# ----------------- Session State -----------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "fraud2025"}  # default user
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "loaded" not in st.session_state:
    st.session_state.loaded = False
if "tx_count" not in st.session_state:
    st.session_state.tx_count = random.randint(120000,150000)
if "history" not in st.session_state:
    st.session_state.history = []
if "reviews" not in st.session_state:
    st.session_state.reviews = []

# ----------------- Login / Registration -----------------
st.markdown("<h1>🛡️ FraudSense AI</h1>", unsafe_allow_html=True)
st.markdown("<h3>Detect • Prevent • Secure</h3>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in st.session_state.users and st.session_state.users[username]==password:
            st.success("✅ Login successful!")
            st.session_state.logged_in = True
            st.session_state.loaded = False
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

with tab2:
    new_user = st.text_input("Choose Username", key="reg_user")
    new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
    if st.button("Register"):
        if new_user in st.session_state.users:
            st.error("Username already exists!")
        elif new_user=="" or new_pass=="":
            st.error("Please fill both fields")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("✅ Registration successful! You can now log in")

# ----------------- Splash Screen -----------------
if st.session_state.logged_in:
    if not st.session_state.loaded:
        st.markdown("<div class='box'>Initializing FraudSense AI Dashboard...</div>", unsafe_allow_html=True)
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)
        st.session_state.loaded = True
        st.experimental_rerun()

# ----------------- Sidebar Navigation -----------------
if st.session_state.logged_in and st.session_state.loaded:
    st.sidebar.title("🛡️ FraudSense AI Dashboard")
    page = st.sidebar.radio("Navigate", ["Dashboard", "Analytics", "Review"])

    # ----------------- Dashboard Page -----------------
    if page=="Dashboard":
        st.title("📊 Dashboard")
        # Fake counter
        st.session_state.tx_count += random.randint(5,20)
        st.markdown(f"<div class='metric-box'>Transactions Processed: {st.session_state.tx_count:,}</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            amount = st.number_input("Transaction Amount (₹)", 10.0, step=100.0)
        with col2:
            hour = st.slider("Transaction Hour", 0, 23, 12)
        with col3:
            tx_24h = st.slider("Transactions (Last 24h)", 1, 50, 3)

        if st.button("Analyze Risk"):
            # Load model & scaler
            model = joblib.load("model.pkl")
            scaler = joblib.load("scaler.pkl")
            X = np.array([[amount, hour, tx_24h]])
            X_scaled = scaler.transform(X)
            pred = model.predict(X_scaled)
            score = abs(model.decision_function(X_scaled)[0])

            if pred[0]==-1:
                st.error("🚨 HIGH RISK TRANSACTION")
            else:
                st.success("✅ LOW RISK TRANSACTION")

            st.progress(min(score,1.0))
            st.write(f"Risk Score: **{score:.2f}**")

            # Save history
            st.session_state.history.append(score)

    # ----------------- Analytics Page -----------------
    elif page=="Analytics":
        st.title("📈 Risk Analytics")
        if len(st.session_state.history)==0:
            st.warning("No transaction data available yet.")
        else:
            df = pd.DataFrame({
                "Transaction": range(1,len(st.session_state.history)+1),
                "Risk Score": st.session_state.history
            })
            st.line_chart(df.set_index("Transaction"))
            st.markdown("""
            **Insights:**  
            - Peaks indicate anomalous transactions  
            - System adapts dynamically using AI
            """)

    # ----------------- Review Page -----------------
    elif page=="Review":
        st.title("📝 Reviews & Feedback")
        name = st.text_input("Your Name", key="rev_name")
        review = st.text_area("Your Feedback / Review", key="rev_text")
        if st.button("Submit Review"):
            if name!="" and review!="":
                st.session_state.reviews.append(f"**{name}**: {review}")
                st.success("Thank you for your feedback!")
            else:
                st.error("Please fill both fields")

        st.divider()
        st.subheader("All Reviews")
        for r in reversed(st.session_state.reviews):
            st.markdown(r)
