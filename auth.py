import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime
import requests

# 🔹 Replace with your Firebase Web API Key
FIREBASE_WEB_API_KEY = "AIzaSyCRJMhxDFqAWLu-HYA0MKjfWk2mywnoCG4"

# 🔹 Initialize Firebase Admin SDK (if not already initialized)
if not firebase_admin._apps:
    cred = credentials.Certificate("insta-path-17e3a-firebase-adminsdk-fbsvc-b705105e1e.json")
    firebase_admin.initialize_app(cred)

# 🔹 Firestore client
db = firestore.client()

# --- 🔹 Register New User ---
def register_user(email, password, username):
    """Registers a new user in Firebase Authentication and Firestore."""
    try:
        # 🔹 Check if the user already exists
        try:
            auth.get_user_by_email(email)
            return {"status": "error", "message": "User already exists! Please log in."}
        except firebase_admin.auth.UserNotFoundError:
            pass  # User does not exist, continue registration

        # 🔹 Create user in Firebase Authentication
        user = auth.create_user(email=email, password=password, display_name=username)

        # 🔹 Store user details in Firestore
        user_data = {
            "email": email,
            "username": username,
            "created_at": datetime.utcnow().isoformat(),
            "history": []
        }
        db.collection("users").document(user.uid).set(user_data)

        return {"status": "success", "user_id": user.uid, "message": "Account created successfully! Please log in."}
    
    except Exception as e:
        return {"status": "error", "message": f"Error registering user: {str(e)}"}

import requests

# --- 🔹 Secure Login with Token-Based Authentication ---
def login_user(email, password):
    """Logs in a user and returns an authentication token."""
    try:
        # Firebase Authentication URL to log in with email and password
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
        
        # Payload for the login request
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        
        # Sending the POST request to Firebase Authentication
        response = requests.post(url, json=payload)

        # Debugging: Log the response status and content
        print("Response Status:", response.status_code)
        print("Response Content:", response.text)

        if response.status_code == 200:
            user_data = response.json()

            # Check if user_id and idToken exist in the response
            if "localId" in user_data and "idToken" in user_data:
                user_id = user_data["localId"]
                id_token = user_data["idToken"]

                # Check if the user exists in Firestore
                user_doc = db.collection("users").document(user_id).get()
                if user_doc.exists:
                    return {
                        "status": "success", 
                        "user_id": user_id, 
                        "id_token": id_token, 
                        "message": "Login successful."
                    }
                else:
                    return {"status": "error", "message": "User data not found in Firestore."}
            else:
                return {"status": "error", "message": "Invalid email or password."}
        else:
            # Log error message from Firebase response
            error_message = response.json().get("error", {}).get("message", "Unknown error")
            print("Firebase Error:", error_message)
            return {"status": "error", "message": f"Error logging in: {error_message}"}
    
    except Exception as e:
        return {"status": "error", "message": f"Exception occurred: {str(e)}"}

# --- 🔹 Get User Search History ---
def get_user_history(user_id):
    """Fetches the user's search history from Firestore."""
    user_doc = db.collection("users").document(user_id).get()
    if user_doc.exists:
        return user_doc.to_dict().get("history", [])
    else:
        return []

# --- 🔹 Update User Search History ---
def update_user_history(user_id, category, query):
    """Updates the user's search history in Firestore."""
    user_doc = db.collection("users").document(user_id)
    user_data = user_doc.get().to_dict()

    if user_data:
        history = user_data.get("history", [])
        history.append(f"{category.capitalize()}: {query}")
        user_doc.update({"history": history})
