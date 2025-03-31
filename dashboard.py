import streamlit as st
from auth import check_auth, logout

# Import recommendation modules
import movies_recommender
import songs_recommender

st.set_page_config(page_title="Multi-Domain Dashboard", layout="wide")

# Check authentication
if not check_auth():
    st.warning("Please log in first.")
    st.stop()

st.title("📌 Multi-Domain Recommendation System")

# Available domains and their modules
domains = {
    "Movies": movies_recommender,
    "Music": songs_recommender,
    "books":books_recommender,
}

# Retrieve user-selected domain
user_domain = st.session_state.get("domain", "Movies","Books")

# User selects a domain
selected_domain = st.selectbox("Choose a domain for recommendations", list(domains.keys()), index=list(domains.keys()).index(user_domain))

if st.button("Proceed"):
    st.session_state["domain"] = selected_domain
    st.experimental_rerun()  # Refresh UI to update content

# Display recommendations for the selected domain
st.write(f"### {st.session_state['domain']} Recommendations")
domains[st.session_state["domain"].lower()].show_recommendations()

# Logout button in sidebar
st.sidebar.button("Logout", on_click=logout)
