# multi_domain_recommendation_system_ml
[mp.pdf](https://github.com/user-attachments/files/21229863/mp.pdf)



## Multi-Domain Recommendation System

### Project Overview

This project implements a **multi-domain recommender system** that provides **personalized recommendations for Movies, Music, and Books** through a **single unified dashboard**.

The system leverages **external APIs, collaborative filtering, and user interaction history** to deliver relevant suggestions while maintaining secure authentication and persistent personalization using Firebase.

---

## Objective

* Recommend **Movies, Music, and Books** based on user preferences and interactions
* Provide a centralized, personalized recommendation experience
* Secure user authentication and history tracking
* Deliver an interactive and responsive dashboard using Streamlit

---

## Key Features

* User authentication (Sign Up, Login, Logout)
* Multi-domain recommendations:

  * Movies via TMDB API
  * Music via Spotify API
  * Books via Collaborative Filtering
* Persistent user history stored in Firestore
* Personalized recommendations by filtering previously seen items
* Interactive Streamlit dashboard with modern UI

---

## Methodology & Workflow

### Step 1: User Authentication

**Technology Used**

* Firebase Authentication
* Firebase Admin SDK
* Firestore Database

**Workflow**

* Users register and log in using email and password
* Firebase Authentication validates credentials using REST API (`signInWithPassword`)
* Upon successful login, a unique user ID is retrieved
* User search history is stored and updated in Firestore for personalization

**History Tracking**

* Every search query is appended to the user's Firestore document
* This history is later used to avoid redundant recommendations

---

### Step 2: Domain-Specific Recommendation

#### A. Movie Recommendations

**API Used**

* TMDB (The Movie Database API)

**Workflow**

* User enters a movie name
* TMDB Search API fetches the movie ID
* TMDB Recommendation API retrieves similar movies
* Movies already watched by the user are filtered using Firestore history
* Results include movie title, poster URL, and reference link

**Technical Details**

* REST API calls handled using the `requests` library
* Error handling for empty results and API failures
* Firestore integration ensures personalized filtering

---

#### B. Music Recommendations

**API Used**

* Spotify API (via `spotipy`)

**Workflow**

* User selects a genre or music type
* Spotify API fetches top tracks for the selected genre
* Top 10 tracks are displayed with:

  * Track name
  * Artist name
  * Album cover image
  * Spotify playback link

**Technical Details**

* OAuth authentication using `SpotifyClientCredentials`
* JSON responses parsed to extract metadata
* Album covers and external URLs enhance UI experience

---

#### C. Book Recommendations

**Approach**

* Collaborative Filtering using K-Nearest Neighbors (KNN)

**Data Used**

* `model.pkl` – Trained KNN model
* `book_pivot.pkl` – User × Book rating matrix
* `final_rating.pkl` – Book metadata with poster URLs
* `books_name.pkl` – List of book titles

**Workflow**

* User selects a book
* KNN model identifies 5–6 similar books
* Average ratings computed using NaN-aware calculations
* Books already interacted with are excluded
* Book posters and metadata displayed dynamically

**Technical Details**

* `numpy` used for similarity computation and missing value handling
* `pickle` used for loading pre-trained models and datasets
* Collaborative filtering improves personalization

---

## Frontend / Dashboard

**Framework**

* Streamlit

**Features**

* Sidebar for Login and Sign Up
* Domain selection using radio buttons
* Dynamic recommendation display
* Real-time user history visualization
* Interactive recommendation cards with custom CSS styling

**Technical Context**

* `st.session_state` manages authentication state and user sessions
* `st.selectbox` and `st.radio` enable dynamic UI rendering
* Recommendations rendered using HTML inside `st.markdown`

---

## Technical Stack

| Component       | Technology               | Purpose                        |
| --------------- | ------------------------ | ------------------------------ |
| Backend         | Python 3.12              | Core programming language      |
| Web Framework   | Streamlit                | Dashboard and UI               |
| Authentication  | Firebase Auth + REST API | Secure login and signup        |
| Database        | Firestore                | User data and history storage  |
| Movie API       | TMDB API                 | Movie recommendations          |
| Music API       | Spotify API (spotipy)    | Music recommendations          |
| Books           | KNN + Pickle             | Collaborative filtering        |
| Data Processing | NumPy, Pandas            | Matrix operations and analysis |
| UI Styling      | Streamlit + CSS          | Interactive design             |

---

## Interview-Relevant Concepts

### Recommender Systems

* Collaborative filtering
* User-item similarity
* History-based filtering to avoid redundancy
* KNN-based recommendation modeling

### API & REST Integration

* TMDB API for movie metadata
* Spotify API with OAuth authentication
* Firebase Authentication REST API

### Data Handling

* Pivot tables for user-item matrices
* Handling missing values using `np.nan`
* Model serialization using `pickle`

### Streamlit & UI

* Session handling with `st.session_state`
* Conditional rendering for performance optimization
* HTML + CSS integration inside Streamlit

### Firebase & Firestore

* Secure authentication using Firebase Auth
* Firestore CRUD operations:

  * `.collection().document().set()`
  * `.update()` for history tracking

---

## Error Handling & Optimization

* Graceful handling of API failures
* Avoids unnecessary API calls through conditional execution
* Lazy loading to improve performance
* Filters previously recommended items for better personalization

---

## Methodology Summary

1. Requirement analysis for a multi-domain recommendation system
2. Data collection from APIs and book datasets
3. Offline training of KNN model for books
4. Integration of APIs with Python backend
5. Firebase-based authentication and history tracking
6. Streamlit dashboard development
7. Testing, validation, and UI optimization

---

## Summary

This project demonstrates how **multiple recommendation techniques**, **real-time APIs**, and **user behavior tracking** can be unified into a single scalable platform.
The system delivers a personalized, secure, and interactive recommendation experience across multiple content domains.
