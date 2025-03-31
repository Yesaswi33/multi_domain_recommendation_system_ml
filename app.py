import pickle
import streamlit as st
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from auth import register_user, login_user, get_user_history, update_user_history
from movies_recommender import get_movie_recommendations
from songs_recommender import get_spotify_recommendations
from books_recommender import recommend_book, books_name

# API Credentials
SPOTIFY_CLIENT_ID = "96ab3de27589430cb843d0e6091a3549"
SPOTIFY_CLIENT_SECRET = "e33a15e355da49b2b0dfd5d8f9e1d6ca"
TMDB_API_KEY = "b82b219879cef715b44be5c2b987df18"
st.set_page_config(page_title="Multi-domain Recommender", layout="wide")

# Initialize Spotify Client
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# --- 🔥 CUSTOM CSS for Amazon Music Theme ---
st.markdown(
    """
    <style>
        * { font-family: 'Times New Roman', serif; }
        body { background: linear-gradient(to right, #1e1e2f, #12121c); color: white; }
        .title { text-align: center; font-size: 36px; font-weight: bold; color: #f8b400; text-shadow: 2px 2px 10px rgba(255, 200, 0, 0.8); }
        .recommendation-box { border-radius: 15px; box-shadow: 5px 5px 15px rgba(255, 140, 0, 0.5); padding: 10px; margin: 20px; background: linear-gradient(to right, #232526, #414345); text-align: center; transition: transform 0.3s ease-in-out; }
        .recommendation-box:hover { transform: scale(1.05); box-shadow: 0px 20px 20px rgba(255, 140, 0, 0.7); }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit App Header
st.markdown("<h1 class='title'>🎥🎵📚 Multi-Domain Recommender System</h1>", unsafe_allow_html=True)

# --- USER AUTHENTICATION ---
menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("🔑 Menu", menu)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.email = None

# --- LOGIN ---
if choice == "Login" and not st.session_state.authenticated:
    st.subheader("🔐 Login")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Login"):
        result = login_user(email, password)
        if result["status"] == "success":
            st.session_state.authenticated = True
            st.session_state.user_id = result["user_id"]
            st.session_state.email = email
            st.success(f"✅ Welcome, {email}!")
        else:
            st.error(f"❌ {result['message']}")

# --- SIGN UP ---
elif choice == "Sign Up" and not st.session_state.authenticated:
    st.subheader("🆕 Create New Account")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    username = st.text_input("👤 Username")
    
    if st.button("Sign Up"):
        result = register_user(email, password, username)
        if result["status"] == "success":
            st.success("✅ Account created successfully! You can now log in.")
        else:
            st.error(f"❌ {result['message']}")

# --- LOGGED-IN USER INTERFACE ---
if st.session_state.authenticated:
    st.sidebar.write(f"✅ Logged in as: {st.session_state.email}")
    
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]  # Clears all session state variables
        st.rerun()

    # --- Intermediate Domain Selection ---
    domain_choice = st.radio("🌐 Select a Domain", ("Entertainment","Education","Organization","Instution"))

    if domain_choice == "Entertainment":
        app_mode = st.radio("🔍 Choose Recommendation Type", ("Movies", "Music", "Books"))

        # --- 🎬 Movie Recommendations ---
        if app_mode == "Movies":
            movie_name = st.text_input("🎥 Enter a movie name:")
            if st.button("Get Recommendations"):
                if movie_name:
                    # Normalize the movie name
                    normalized_movie_name = movie_name.strip().lower()
            
                    # Get recommendations based on the movie name
                    recommendations = get_movie_recommendations(st.session_state.email, normalized_movie_name)
                    if recommendations:
                        for movie_name, poster_path, link in recommendations:
                            st.markdown(
                                f"""
                                <div class="recommendation-box">
                                    <img src="https://image.tmdb.org/t/p/w500{poster_path}" width="200">
                                    <h4>{movie_name}</h4>
                                    <a href="{link}" target="_blank">🎥 Watch Now</a>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    
                        # Debugging: Check if movie name is stored correctly
                        st.write(f"Debug: Storing {normalized_movie_name} to history.")

                        # Update user history with normalized movie name
                        update_user_history(st.session_state.user_id, "movie", normalized_movie_name)
                    else:
                        st.warning("❌ No movie recommendations found.")
                else:
                    st.warning("⚠️ Please enter a movie name.")

        # --- 🎵 Music Recommendations ---
        elif app_mode == "Music":
            genre = st.text_input("🎶 Enter a music genre:")
            if st.button("Get Recommendations"):
                music_recommendations = get_spotify_recommendations(genre)
                if music_recommendations:
                    for _, track_name, artist_name, album_cover_url, spotify_url in music_recommendations:
                        st.markdown(
                            f"""
                            <div class="recommendation-box">
                                <img src="{album_cover_url}" width="200">
                                <h4>{track_name} by {artist_name}</h4>
                                <a href="{spotify_url}" target="_blank">🎵 Listen on Spotify</a>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    update_user_history(st.session_state.user_id, "music", genre)
                else:
                    st.warning("❌ No music recommendations found.")

        # --- 📚 Book Recommendations ---
        elif app_mode == "Books":
            book_name = st.selectbox("📖 Select a book:", books_name)
            if st.button("Get Recommendations"):
                recommendation_books, poster_urls, avg_ratings = recommend_book(book_name)
                if recommendation_books:
                    for i in range(len(recommendation_books)):
                        st.markdown(
                            f"""
                            <div class="recommendation-box">
                                <img src="{poster_urls[i]}" width="200">
                                <h4>{recommendation_books[i]}</h4>
                                <p>⭐ {avg_ratings[i]}/10</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    update_user_history(st.session_state.user_id, "book", book_name)
                else:
                    st.warning("❌ No book recommendations found.")

    st.subheader("📜 Your Search History")
    history = get_user_history(st.session_state.user_id)
    if history:
        for item in reversed(history):
            st.write(f"🔹 {item}")
    else:
        st.write("🚀 No history yet!")
