import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_movie_titles():
    prefixes = ["The", "A", "Rise of", "Return of", "Legacy of", "Dawn of", "Fall of"]
    nouns = ["Kingdom", "Empire", "Hero", "Legend", "Warrior", "Champion", "Mystery"]
    adjectives = ["Lost", "Hidden", "Last", "Eternal", "Dark", "Golden", "Secret"]
    locations = ["Earth", "Moon", "Stars", "City", "World", "Paradise", "Realm"]

    titles = []
    for p in prefixes:
        for n in nouns:
            titles.append(f"{p} {n}")
        for a in adjectives:
            titles.append(f"{p} {a} {np.random.choice(locations)}")
    return titles

def generate_movie_data():
    # Generate realistic movie data
    np.random.seed(42)
    base_date = datetime(2024, 1, 1)
    genres = ["Action", "Drama", "Comedy", "Sci-Fi", "Horror", "Romance", "Thriller", 
             "Adventure", "Fantasy", "Animation", "Documentary", "Mystery"]

    movies = []
    titles = generate_movie_titles()

    for i, title in enumerate(titles[:100]):  # Take first 100 titles
        # Generate realistic release date
        days_offset = np.random.randint(-30, 365)  # Movies from last month to next year
        release_date = (base_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")

        # Generate realistic sentiment and review counts
        sentiment_score = np.clip(np.random.normal(0.75, 0.15), 0.3, 0.98)
        review_count = int(np.random.normal(1000, 500))
        positive_ratio = sentiment_score  # Use sentiment score as ratio for positive reviews

        movies.append({
            "title": title,
            "release_date": release_date,
            "genre": np.random.choice(genres),
            "sentiment_score": sentiment_score,
            "review_count": review_count,
            "positive_reviews": int(review_count * positive_ratio),
            "negative_reviews": int(review_count * (1 - positive_ratio)),
            "budget": np.random.randint(30, 200),  # Budget in millions
            "social_buzz_score": np.random.randint(60, 100)
        })

    return {"movies": movies}

def generate_demographic_data():
    return {
        "age_groups": {
            "13-17": 15,
            "18-24": 30,
            "25-34": 25,
            "35-44": 20,
            "45+": 10
        },
        "locations": {
            "North America": 45,
            "Europe": 30,
            "Asia": 15,
            "Latin America": 7,
            "Africa": 2,
            "Oceania": 1
        },
        "gender": {
            "Male": 52,
            "Female": 45,
            "Other": 3
        }
    }

def generate_competitor_data():
    movies = generate_movie_data()["movies"][:5]  # Get first 5 movies for competitor analysis

    return pd.DataFrame({
        "Movie": [m["title"] for m in movies],
        "Budget": [m["budget"] for m in movies],
        "Social_Buzz": [m["social_buzz_score"] for m in movies],
        "Sentiment_Score": [m["sentiment_score"] for m in movies],
        "Expected_ROI": [round(np.random.uniform(1.5, 3.2), 2) for _ in range(5)]
    })