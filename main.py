import streamlit as st
import plotly.express as px
import pandas as pd
from utils.mock_data import generate_movie_data, generate_demographic_data
from utils.advanced_sentiment import analyze_review_emotions, get_emotion_color

# Page configuration
st.set_page_config(
    page_title="Movie Analysis Portal",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .emotion-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🎬 Movie Analysis Portal")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page",
        ["Dashboard", "Advanced Sentiment Analysis", "Demographics"]
    )

    if page == "Dashboard":
        show_dashboard()
    elif page == "Advanced Sentiment Analysis":
        show_sentiment_analysis()
    else:
        show_demographics()

def show_dashboard():
    st.header("Movie Analytics Dashboard")

    # Get mock data
    movie_data = generate_movie_data()

    # Create columns for metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Movies Analyzed",
            value=len(movie_data["movies"]),
            delta="2 new"
        )

    with col2:
        avg_sentiment = sum(m["sentiment_score"] for m in movie_data["movies"]) / len(movie_data["movies"])
        st.metric(
            label="Average Sentiment Score",
            value=f"{avg_sentiment:.2f}",
            delta="0.05"
        )

    with col3:
        total_reviews = sum(m["review_count"] for m in movie_data["movies"])
        st.metric(
            label="Total Reviews",
            value=f"{total_reviews:,}",
            delta="150"
        )

    # Create sentiment trend chart using pandas DataFrame
    sentiment_df = pd.DataFrame([
        {"Movie": m["title"], "Sentiment": m["sentiment_score"], "Reviews": m["review_count"]}
        for m in movie_data["movies"]
    ])

    # Sort by sentiment score and take top 10 for better visualization
    top_10_movies = sentiment_df.nlargest(10, "Reviews")

    fig = px.bar(
        top_10_movies,
        x="Movie",
        y="Sentiment",
        title="Top 10 Most Reviewed Movies - Sentiment Analysis",
        color="Sentiment",
        color_continuous_scale="RdYlGn"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    # Add genre distribution
    genre_df = pd.DataFrame([{"Genre": m["genre"]} for m in movie_data["movies"]])
    genre_counts = genre_df["Genre"].value_counts()

    fig_genre = px.pie(
        values=genre_counts.values,
        names=genre_counts.index,
        title="Movie Distribution by Genre"
    )
    st.plotly_chart(fig_genre, use_container_width=True)


def show_sentiment_analysis():
    st.header("Advanced Sentiment Analysis")

    # Introduction
    st.markdown("""
    This advanced sentiment analysis tool provides:
    - Emotion Detection (Joy, Anger, Sadness, Surprise, Disgust)
    - Aspect-Based Analysis (Storyline, Acting, Visual Effects, Music)
    - Overall Sentiment Score
    - Key Themes Identification
    """)

    review_text = st.text_area(
        "Enter a movie review to analyze:",
        height=150,
        placeholder="Write or paste a movie review here..."
    )

    if st.button("Analyze Sentiment"):
        if review_text:
            with st.spinner("Performing advanced sentiment analysis..."):
                result = analyze_review_emotions(review_text)

                # Display emotion with color
                emotion = result.get('emotion', 'neutral')
                color = get_emotion_color(emotion)
                st.markdown(
                    f"""
                    <div class="emotion-box" style="background-color: {color}; color: white;">
                    Primary Emotion: {emotion}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Create columns for different aspects
                st.subheader("Aspect-Based Analysis")
                cols = st.columns(4)
                aspects = result.get('aspects', {})

                for col, (aspect, score) in zip(cols, aspects.items()):
                    col.metric(aspect, f"{score}/5")

                # Display sentiment score
                st.metric(
                    "Overall Sentiment Score",
                    f"{result.get('sentiment_score', 0.5):.2f}",
                    delta=None
                )

                # Display themes
                st.subheader("Key Themes")
                themes = result.get('themes', [])
                for theme in themes:
                    st.markdown(f"• {theme}")

                # Show review statistics
                st.subheader("Review Analysis")

                # Create aspect ratings chart
                aspect_df = pd.DataFrame([
                    {"Aspect": k, "Rating": v}
                    for k, v in aspects.items()
                ])

                fig = px.bar(
                    aspect_df,
                    x="Aspect",
                    y="Rating",
                    title="Aspect Ratings",
                    color="Rating",
                    color_continuous_scale="RdYlGn",
                    range_y=[0, 5]
                )
                st.plotly_chart(fig, use_container_width=True)

        else:
            st.warning("Please enter some text to analyze")

def show_demographics():
    st.header("Audience Demographics")

    demo_data = generate_demographic_data()

    col1, col2 = st.columns(2)

    with col1:
        # Age distribution
        fig_age = px.pie(
            values=list(demo_data["age_groups"].values()),
            names=list(demo_data["age_groups"].keys()),
            title="Age Distribution"
        )
        st.plotly_chart(fig_age)

    with col2:
        # Gender distribution
        fig_gender = px.pie(
            values=list(demo_data["gender"].values()),
            names=list(demo_data["gender"].keys()),
            title="Gender Distribution"
        )
        st.plotly_chart(fig_gender)

    # Location distribution
    fig_location = px.bar(
        x=list(demo_data["locations"].keys()),
        y=list(demo_data["locations"].values()),
        title="Geographical Distribution"
    )
    st.plotly_chart(fig_location, use_container_width=True)

if __name__ == "__main__":
    main()