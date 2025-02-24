import pandas as pd
import numpy as np

def generate_movie_data():
    return {
        "movies": [
            {
                "title": "The Space Adventure",
                "release_date": "2024-06-15",
                "genre": "Sci-Fi",
                "sentiment_score": 0.85,
                "review_count": 1200,
                "positive_reviews": 950,
                "negative_reviews": 250
            },
            {
                "title": "Love in Paris",
                "release_date": "2024-07-01",
                "genre": "Romance",
                "sentiment_score": 0.75,
                "review_count": 800,
                "positive_reviews": 600,
                "negative_reviews": 200
            },
            {
                "title": "The Last Detective",
                "release_date": "2024-05-30",
                "genre": "Mystery",
                "sentiment_score": 0.92,
                "review_count": 1500,
                "positive_reviews": 1380,
                "negative_reviews": 120
            }
        ]
    }

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
            "Others": 10
        },
        "gender": {
            "Male": 52,
            "Female": 45,
            "Other": 3
        }
    }

def generate_competitor_data():
    return pd.DataFrame({
        "Movie": ["The Space Adventure", "Cosmic Journey", "Star Voyager"],
        "Budget": [100, 85, 120],
        "Social_Buzz": [85, 70, 90],
        "Sentiment_Score": [0.85, 0.75, 0.88],
        "Expected_ROI": [2.5, 2.0, 2.8]
    })
