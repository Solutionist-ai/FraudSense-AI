import streamlit as st
import time

st.set_page_config(
    page_title="FraudSense AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CSS for animated logo and styling ----------------
st.markdown("""
<style>
@keyframes glow {
    0% { text-shadow: 0 0 5px #00b4ff; }
    50% { text-shadow: 0 0 20px #00b4ff; }
    100% { text-shadow: 0 0 5px #00b4ff; }
}
.logo {
    font-size: 56px;
    font-weight: 900;
    color: #00b4ff;
    animation: glow 2s infinite;
    text-align: center;
}
.tagline {
    text-align: center;
    color: #9ba3af;
    font-size: 18px;
}
.box {
    background: #161b22;
    padding: 25px;
    border-radius: 16px;
    border: 1px solid #30363d;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN CREDENTIALS ----------------
USERNAME = "admin"
PASSWORD = "fraud2025"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN SCREEN ----------------
if not st.session_state.logged_in:
    st.markdown("<div class='logo'>🛡️ FraudSense AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='tagline'>Detect • Prevent • Secure</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='box'>🔒 Enter credentials to access the dashboard</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.success("✅ Login successful!")
            time.sleep(0.5)
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

# ---------------- SPLASH SCREEN AFTER LOGIN ----------------
if st.session_state.logged_in:
    if "loaded" not in st.session_state:
        st.session_state.loaded = False

    if not st.session_state.loaded:
        st.markdown("<div class='box'>Initializing FraudSense AI Dashboard...</div>", unsafe_allow_html=True)
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)
        st.session_state.loaded = True
        st.experimental_rerun()

    st.success("System initialized successfully 🚀")
    st.sidebar.title("🛡️ FraudSense AI")
    st.sidebar.info("Navigate the dashboard using the pages above")

