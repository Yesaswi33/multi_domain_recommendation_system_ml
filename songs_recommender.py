import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = "96ab3de27589430cb843d0e6091a3549"
SPOTIFY_CLIENT_SECRET = "e33a15e355da49b2b0dfd5d8f9e1d6ca"

# Initialize Spotify Client
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get album cover & Spotify URL
def get_song_details(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        spotify_url = track["external_urls"]["spotify"]
        return album_cover_url, spotify_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png", "#"

# Function to get Spotify Music Recommendations
def get_spotify_recommendations(genre):
    results = sp.search(q=genre, type="track", limit=10)
    tracks = results["tracks"]["items"]
    
    # Collect the original track names, artist names, and other details
    recommendations = []
    for track in tracks:
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        
        # Safely check for album cover URL availability
        if "album" in track and "images" in track["album"] and len(track["album"]["images"]) > 0:
            album_cover_url = track["album"]["images"][0]["url"]
        else:
            album_cover_url = "https://i.postimg.cc/0QNxYz4V/social.png"  # Use a default image if not available
        
        spotify_url = track["external_urls"]["spotify"]
        recommendations.append((genre, track_name, artist_name, album_cover_url, spotify_url))
    
    return recommendations
