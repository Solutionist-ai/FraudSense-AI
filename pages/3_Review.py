import streamlit as st

st.title("📝 Reviews & Feedback")

if "reviews" not in st.session_state:
    st.session_state.reviews = []

name = st.text_input("Your Name")
review = st.text_area("Your Feedback / Review")

if st.button("Submit Review"):
    if name and review:
        st.session_state.reviews.append(f"**{name}**: {review}")
        st.success("Thank you for your feedback!")
    else:
        st.error("Please fill both fields")

st.divider()

st.subheader("All Reviews")
for r in reversed(st.session_state.reviews):
    st.markdown(r)

