import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pandas as pd

def prepare_features(movies_data):
    """
    Prepare features for the prediction model from movie data.
    """
    features = []
    for movie in movies_data:
        feature_dict = {
            'sentiment_score': movie['sentiment_score'],
            'review_count': movie['review_count'],
            'positive_ratio': movie['positive_reviews'] / (movie['review_count'] + 1),  # Add 1 to avoid division by zero
            'social_buzz_score': movie['social_buzz_score'],
            'budget': movie['budget']
        }
        features.append(feature_dict)
    
    return pd.DataFrame(features)

def train_prediction_model(movies_data):
    """
    Train a Random Forest model for box office prediction.
    """
    # Prepare features
    X = prepare_features(movies_data)
    
    # Generate synthetic target variable (box office revenue) based on features
    # This is a simplified model for demonstration
    y = np.array([
        m['budget'] * (1 + m['sentiment_score']) * (m['social_buzz_score'] / 50)
        for m in movies_data
    ])
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_scaled, y)
    
    return model, scaler

def predict_box_office(model, scaler, movie_data):
    """
    Predict box office revenue for a movie.
    """
    # Prepare features for prediction
    features = prepare_features([movie_data])
    X_scaled = scaler.transform(features)
    
    # Make prediction
    prediction = model.predict(X_scaled)[0]
    
    # Get feature importance
    feature_importance = dict(zip(
        features.columns,
        model.feature_importances_
    ))
    
    return {
        'predicted_revenue': prediction,
        'feature_importance': feature_importance
    }

def get_confidence_metrics(model, movie_data):
    """
    Calculate confidence metrics for the prediction.
    """
    features = prepare_features([movie_data])
    predictions = []
    
    # Generate multiple predictions with bootstrapping
    for _ in range(100):
        # Randomly sample features with replacement
        sample_idx = np.random.choice(model.n_estimators, size=50)
        pred = np.mean([
            tree.predict(features)[0]
            for tree in np.array(model.estimators_)[sample_idx]
        ])
        predictions.append(pred)
    
    return {
        'mean_prediction': np.mean(predictions),
        'std_prediction': np.std(predictions),
        'confidence_interval': (
            np.percentile(predictions, 5),
            np.percentile(predictions, 95)
        )
    }
