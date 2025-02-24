import streamlit as st
import plotly.express as px
from utils.mock_data import generate_demographic_data

st.set_page_config(page_title="Demographics Analysis", page_icon="📊")

def main():
    st.title("📊 Demographics Analysis")
    
    demo_data = generate_demographic_data()
    
    # Time period selector
    time_period = st.selectbox(
        "Select Time Period",
        ["Last 7 days", "Last 30 days", "Last 3 months", "Last year"]
    )
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Age Analysis", "Geographic Distribution", "Gender Analysis"])
    
    with tab1:
        st.header("Age Distribution")
        fig_age = px.pie(
            values=list(demo_data["age_groups"].values()),
            names=list(demo_data["age_groups"].keys()),
            title="Audience Age Distribution"
        )
        st.plotly_chart(fig_age, use_container_width=True)
        
        # Age insights
        st.subheader("Key Insights")
        st.write("• Majority of audience is in the 18-34 age range")
        st.write("• Growing trend in the 35-44 age group")
        st.write("• Opportunity to expand in the 45+ segment")
    
    with tab2:
        st.header("Geographic Distribution")
        fig_geo = px.bar(
            x=list(demo_data["locations"].keys()),
            y=list(demo_data["locations"].values()),
            title="Audience by Region"
        )
        st.plotly_chart(fig_geo, use_container_width=True)
        
        # Geographic insights
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Top Region", "North America", "+5%")
        with col2:
            st.metric("Fastest Growing", "Asia", "+12%")
    
    with tab3:
        st.header("Gender Distribution")
        fig_gender = px.pie(
            values=list(demo_data["gender"].values()),
            names=list(demo_data["gender"].keys()),
            title="Gender Distribution"
        )
        st.plotly_chart(fig_gender, use_container_width=True)
        
        # Gender insights
        st.subheader("Trends")
        st.write("• Balanced gender distribution with slight male majority")
        st.write("• Increasing diversity in audience composition")

if __name__ == "__main__":
    main()
