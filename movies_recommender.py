import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Initialization (Prevents duplicate initialization)
if not firebase_admin._apps:
    cred = credentials.Certificate("insta-path-17e3a-firebase-adminsdk-fbsvc-acaf581017.json")
    firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

# TMDB API Key
TMDB_API_KEY = "b82b219879cef715b44be5c2b987df18"

# Fetch user movie history from Firestore
def get_user_movie_history(user_email):
    try:
        user_ref = db.collection("users").document(user_email).collection("history").document("movies")
        user_data = user_ref.get()
        return user_data.to_dict().get("watched", []) if user_data.exists else []
    except Exception as e:
        print(f"Error fetching user history: {e}")
        return []

# Store user movie interactions in Firestore
def store_user_interaction(user_email, movie_name):
    try:
        user_ref = db.collection("users").document(user_email).collection("history").document("movies")
        user_data = user_ref.get()
        watched_movies = user_data.to_dict().get("watched", []) if user_data.exists else []

        if movie_name not in watched_movies:
            watched_movies.append(movie_name)
            user_ref.set({"watched": watched_movies})
    except Exception as e:
        print(f"Error storing user interaction: {e}")

# Fetch movie recommendations from TMDB
def get_movie_recommendations(user_email, movie_name):
    try:
        # Get user's watch history
        user_history = get_user_movie_history(user_email)

        # Step 1: Search for the movie on TMDB
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
        search_response = requests.get(search_url, timeout=5)

        if search_response.status_code != 200:
            return [(f"Error: {search_response.status_code} - {search_response.reason}", "", "")]

        search_data = search_response.json()
        if not search_data.get("results"):
            return [("Movie not found.", "", "")]

        # Get the first matched movie ID
        movie_id = search_data["results"][0]["id"]

        # Step 2: Fetch recommendations based on movie ID
        recommend_url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}"
        recommend_response = requests.get(recommend_url, timeout=5)

        if recommend_response.status_code != 200:
            return [(f"Error: {recommend_response.status_code} - {recommend_response.reason}", "", "")]

        recommend_data = recommend_response.json()

        # Extract recommendations
        recommendations = [
            (
                movie.get("title", "Unknown"),
                f"https://image.tmdb.org/t/p/w500{movie.get('poster_path', '')}" if movie.get("poster_path") else "",
                f"https://www.themoviedb.org/movie/{movie.get('id', '')}"
            )
            for movie in recommend_data.get("results", [])
        ]

        # Filter out movies the user has already watched
        filtered_recommendations = [rec for rec in recommendations if rec[0] not in user_history]

        # Store user interaction
        store_user_interaction(user_email, movie_name)

        return filtered_recommendations if filtered_recommendations else [("No new recommendations found.", "", "")]

    except requests.exceptions.ConnectionError:
        return [("Connection error. Check your internet or API status.", "", "")]
    except requests.exceptions.Timeout:
        return [("Request timed out. The API might be slow.", "", "")]
    except requests.exceptions.RequestException as e:
        return [(f"API error: {str(e)}", "", "")]
    except Exception as e:
        return [(f"Unexpected error: {str(e)}", "", "")]
