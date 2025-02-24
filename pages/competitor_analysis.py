import streamlit as st
import plotly.express as px
from utils.mock_data import generate_competitor_data

st.set_page_config(page_title="Competitor Analysis", page_icon="📈")

def main():
    st.title("📈 Competitor Analysis")
    
    competitor_data = generate_competitor_data()
    
    # Metrics selector
    metric = st.selectbox(
        "Select Metric for Comparison",
        ["Budget", "Social_Buzz", "Sentiment_Score", "Expected_ROI"]
    )
    
    # Create comparison chart
    fig = px.bar(
        competitor_data,
        x="Movie",
        y=metric,
        title=f"Competitor Comparison - {metric}",
        color=metric,
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed analysis table
    st.subheader("Detailed Comparison")
    st.dataframe(competitor_data)
    
    # Key insights
    st.subheader("Key Insights")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Market Leaders")
        leader = competitor_data.loc[competitor_data[metric].idxmax()]
        st.metric(
            "Top Performer",
            leader["Movie"],
            f"{leader[metric]:.2f}"
        )
    
    with col2:
        st.write("Areas of Opportunity")
        opportunity = competitor_data.loc[competitor_data[metric].idxmin()]
        st.metric(
            "Growth Potential",
            opportunity["Movie"],
            f"{opportunity[metric]:.2f}"
        )

if __name__ == "__main__":
    main()
