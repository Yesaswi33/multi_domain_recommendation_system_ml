import pickle
import numpy as np

# Load the model and required data files
model = pickle.load(open('model.pkl', 'rb'))
books_name = pickle.load(open('books_name.pkl', 'rb'))
final_rating = pickle.load(open('final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('book_pivot.pkl', 'rb'))
nan_pivot = pickle.load(open('book_pivot.pkl', 'rb'))

# Replace 0 values with NaN for accurate mean calculations
nan_pivot[nan_pivot == 0] = np.nan

def fetch_poster(suggestion):
    """Fetch book poster URLs based on recommendations."""
    book_names = []
    ids_index = []
    poster_urls = []

    for book_id in suggestion:
        book_names.append(book_pivot.index[book_id])

    for name in book_names[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['img_url']
        poster_urls.append(url) 

    return poster_urls

def recommend_book(book_name):
    """Recommend similar books based on user selection."""
    book_list = []
    avg_ratings = []

    try:
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

        poster_urls = fetch_poster(suggestion)

        for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            
            for j in books:
                books_id = np.where(nan_pivot.index == j)[0][0]
                rating = np.round(np.nanmean(nan_pivot.iloc[books_id, :]), decimals=1)
                book_list.append(j)
                avg_ratings.append(rating)

        return book_list, poster_urls, avg_ratings
    except IndexError:
        return [], [], []

