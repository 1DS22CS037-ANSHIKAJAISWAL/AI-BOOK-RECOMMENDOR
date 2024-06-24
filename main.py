import streamlit as st
import requests
from transformers import pipeline

# Initialize Hugging Face pipeline for text generation
generator = pipeline("text-generation", model="gpt2")


# Define a function to fetch the top 100 books for a given genre
def fetch_top_books(genre):
    top_books = []
    max_results = 40
    fetched_books = 0

    for start_index in range(0, 100, max_results):
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genre}&startIndex={start_index}&maxResults={max_results}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            for book in items:
                if 'volumeInfo' in book and 'title' in book['volumeInfo']:
                    top_books.append(book['volumeInfo']['title'])
                    fetched_books += 1
                    if fetched_books >= 100:
                        break
            if fetched_books >= 100:
                break
        else:
            st.error(f"Failed to fetch books. Status code: {response.status_code}")
            return None

    return top_books[:100]  # Return up to 100 books


# Streamlit app setup
st.set_page_config(page_title="AI Book Recommender")
st.title('AI Book Recommender')

# Session state to store fetched books and genre
session_state = st.session_state.setdefault('session_state', {'top_books': None, 'genre': None})

st.markdown("""
## Welcome to AI Book Recommender
This app helps you find top books based on genres using the Google Books API.
""")

# User input for genre
genre = st.text_input('Enter a genre to find top books (e.g., fiction):')

if genre:
    # Store the genre in session state
    session_state['genre'] = genre

    # Button to fetch top 100 books
    if st.button('Fetch Top 100 Books'):
        session_state['top_books'] = fetch_top_books(genre)
        if session_state['top_books']:
            st.success('Top 100 books fetched successfully!')
            st.subheader(f"Top 100 books in {genre} genre:")
            for i, book in enumerate(session_state['top_books'], 1):
                st.write(f"{i}. {book}")

# Display top 10 books if fetched
if session_state['top_books']:
    # Button to filter top 10 books
    if st.button('Filter Top 10 Books'):
        top_10_books = session_state['top_books'][:10]
        if top_10_books:
            st.success('Top 10 books filtered successfully!')
            st.subheader(f"Top 10 books in {session_state['genre']} genre:")
            for i, book in enumerate(top_10_books, 1):
                st.write(f"{i}. {book}")

            # Dropdown to select top book from the top 10
            selected_index = st.selectbox('Select the top book from the list above:', [i for i in range(1, len(top_10_books) + 1)])
            if selected_index:
                selected_book = top_10_books[selected_index - 1]
                st.success(f"Selected Book: {selected_book}")
                st.write('Thank you for using the AI Book Recommender!')
