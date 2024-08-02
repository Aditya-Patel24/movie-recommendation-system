import streamlit as st
import pickle
import pandas as pd


def recommend(movie):
    # Get the index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]

    # Get similarity scores for the selected movie
    distances = similarity[movie_index]

    # Sort movies based on similarity scores and get top 5 recommendations
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []

    # Fetch details for recommended movies
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# Streamlit app setup
st.set_page_config(page_title='Movie Recommender System', layout='wide')
st.title('🎬 Movie Recommender System')

# Load data
try:
    movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Check and adjust data structure
if not isinstance(movies, pd.DataFrame):
    st.error("Movies data is not in DataFrame format")
    st.stop()

if 'title' not in movies.columns:
    st.error("'title' column is missing from movies data")
    st.stop()

if 'movie_id' not in movies.columns:
    st.error("'movie_id' column is missing from movies data")
    st.stop()

# Movie list for dropdown
movie_list = movies['title'].tolist()
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names = recommend(selected_movie)

    # Display recommended movies with styled layout
    st.subheader('Recommended Movies:')
    st.write("---")  # Adds a horizontal line for separation

    # Create columns to display movie names
    for name in recommended_movie_names:
        st.markdown(f"""
            <div style="background-color: #f0f0f0; border-radius: 10px; padding: 10px; margin: 5px; text-align: center;">
                <h3 style="color: #333;">{name}</h3>
            </div>
        """, unsafe_allow_html=True)
