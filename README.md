# 🎬 Movie Analysis Portal

A comprehensive analytics platform for movie industry stakeholders powered by machine learning and real-time sentiment analysis.

## 🚀 Features

### 1. Advanced Sentiment Analysis
- Multi-dimensional emotion detection (Joy, Anger, Sadness, Surprise, Disgust)
- Aspect-based sentiment analysis (Storyline, Acting, Visual Effects, Music)
- Real-time sentiment tracking via WebSocket
- GPT-4 powered natural language processing

### 2. Predictive Analytics
- Box office revenue prediction using Random Forest
- Feature importance analysis
- ROI prediction with confidence intervals
- Historical performance analysis

### 3. Audience Demographics
- Age distribution analysis
- Geographical distribution tracking
- Gender demographics
- Interactive visualization using Plotly

### 4. Competitor Analysis
- Market comparison metrics
- Social buzz tracking
- ROI benchmarking
- Performance insights

### 5. Real-time Processing
- WebSocket server for live data streaming
- Async/await patterns for concurrent connections
- Live dashboard updates

## 🛠️ Technical Stack

- **Backend:** Python, FastAPI (WebSocket)
- **Frontend:** Streamlit
- **Data Visualization:** Plotly
- **Machine Learning:** Scikit-learn (Random Forest)
- **NLP:** GPT-4

## 📊 Business Impact

- Data-driven decision making for movie investments
- Real-time audience sentiment tracking
- Demographic analysis for targeted marketing
- Revenue prediction for financial planning
- Competitive analysis for market positioning

## 🚀 Getting Started

1. Run the Streamlit app:
```bash
streamlit run main.py
```

2. Start the WebSocket server:
```bash
uvicorn utils.websocket_server:app --host 0.0.0.0 --port 8000
```

## 📈 Key Metrics

- Sentiment analysis accuracy
- Revenue prediction confidence intervals
- Real-time social buzz tracking
- Demographic segmentation
- Competitor benchmarking

## 🔒 Security

- Secure WebSocket connections
- Data encryption
- User authentication
- Rate limiting

## 📊 Dashboard Features

- Interactive visualizations
- Real-time updates
- Customizable metrics
- Export capabilities
- Multi-view analysis

## 🎯 Future Enhancements

- Enhanced ML models
- Additional data sources
- Advanced visualization options
- API integrations
- Mobile responsiveness
