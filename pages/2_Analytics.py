import streamlit as st
import pandas as pd

st.title("📈 Risk Analytics")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.warning("No transaction data available yet.")
else:
    df = pd.DataFrame({
        "Transaction": range(1, len(st.session_state.history) + 1),
        "Risk Score": st.session_state.history
    })
    st.line_chart(df.set_index("Transaction"))

    st.markdown("""
    **Insights:**
    - Peaks indicate anomalous transactions
    - System adapts dynamically using AI
    """)

