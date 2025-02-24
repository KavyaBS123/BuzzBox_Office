import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.mock_data import generate_movie_data
from utils.predictive_analytics import (
    train_prediction_model,
    predict_box_office,
    get_confidence_metrics
)

st.set_page_config(page_title="Predictive Analytics", page_icon="📈")

def format_currency(amount):
    """Format amount in millions."""
    return f"${amount:.1f}M"

def main():
    st.title("📈 ML-Based Predictive Analytics")
    
    # Generate sample data and train model
    movie_data = generate_movie_data()
    model, scaler = train_prediction_model(movie_data["movies"])
    
    # Sidebar inputs
    st.sidebar.header("Movie Parameters")
    
    budget = st.sidebar.slider(
        "Production Budget ($M)",
        min_value=30,
        max_value=200,
        value=100,
        step=5
    )
    
    sentiment = st.sidebar.slider(
        "Sentiment Score",
        min_value=0.0,
        max_value=1.0,
        value=0.75,
        step=0.05
    )
    
    buzz_score = st.sidebar.slider(
        "Social Buzz Score",
        min_value=0,
        max_value=100,
        value=80,
        step=5
    )
    
    review_count = st.sidebar.slider(
        "Expected Review Count",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )
    
    positive_reviews = int(review_count * sentiment)
    
    # Create test movie data
    test_movie = {
        "budget": budget,
        "sentiment_score": sentiment,
        "social_buzz_score": buzz_score,
        "review_count": review_count,
        "positive_reviews": positive_reviews,
        "negative_reviews": review_count - positive_reviews
    }
    
    # Make prediction
    prediction = predict_box_office(model, scaler, test_movie)
    confidence = get_confidence_metrics(model, test_movie)
    
    # Display predictions
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Predicted Box Office Revenue",
            format_currency(prediction["predicted_revenue"]),
            delta=format_currency(prediction["predicted_revenue"] - budget)
        )
    
    with col2:
        st.metric(
            "Predicted ROI",
            f"{(prediction['predicted_revenue'] / budget - 1) * 100:.1f}%",
            delta="Based on current parameters"
        )
    
    # Confidence interval
    st.subheader("Prediction Confidence")
    ci_low, ci_high = confidence["confidence_interval"]
    st.write(f"95% Confidence Interval: {format_currency(ci_low)} - {format_currency(ci_high)}")
    
    # Feature importance plot
    st.subheader("Feature Importance Analysis")
    importance_df = pd.DataFrame({
        'Feature': list(prediction['feature_importance'].keys()),
        'Importance': list(prediction['feature_importance'].values())
    })
    
    fig = px.bar(
        importance_df,
        x='Importance',
        y='Feature',
        orientation='h',
        title='Feature Importance in Revenue Prediction'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Add prediction vs actual plot
    st.subheader("Historical Performance Analysis")
    historical_data = pd.DataFrame([
        {
            'Budget': m['budget'],
            'Predicted Revenue': predict_box_office(model, scaler, m)['predicted_revenue']
        }
        for m in movie_data['movies'][:20]  # Take first 20 movies for better visualization
    ])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=historical_data['Budget'],
        y=historical_data['Predicted Revenue'],
        mode='markers',
        name='Historical Predictions'
    ))
    
    # Add current prediction point
    fig.add_trace(go.Scatter(
        x=[budget],
        y=[prediction['predicted_revenue']],
        mode='markers',
        marker=dict(size=15, symbol='star'),
        name='Current Prediction'
    ))
    
    fig.update_layout(
        title='Budget vs Predicted Revenue',
        xaxis_title='Budget ($M)',
        yaxis_title='Predicted Revenue ($M)'
    )
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
