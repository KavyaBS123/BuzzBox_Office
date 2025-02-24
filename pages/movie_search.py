import streamlit as st
import plotly.express as px
from utils.mock_data import generate_movie_data

st.set_page_config(page_title="Movie Search", page_icon="🔍")

def main():
    st.title("🔍 Movie Search")
    
    # Search box
    search_term = st.text_input("Search for a movie:")
    
    # Get mock data
    movies = generate_movie_data()["movies"]
    
    if search_term:
        filtered_movies = [
            movie for movie in movies
            if search_term.lower() in movie["title"].lower()
        ]
    else:
        filtered_movies = movies
    
    # Display results
    for movie in filtered_movies:
        with st.expander(f"{movie['title']} ({movie['genre']})"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"Release Date: {movie['release_date']}")
                st.write(f"Genre: {movie['genre']}")
                st.write(f"Sentiment Score: {movie['sentiment_score']:.2f}")
            
            with col2:
                # Create a mini sentiment chart
                fig = px.pie(
                    values=[movie["positive_reviews"], movie["negative_reviews"]],
                    names=["Positive", "Negative"],
                    title="Review Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
