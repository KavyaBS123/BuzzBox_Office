import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "default-key")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_review_emotions(text):
    """
    Analyze emotions and aspects in movie reviews using GPT-4o.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the movie review and provide: "
                    "1. Primary emotion (Joy, Anger, Sadness, Surprise, Disgust) "
                    "2. Aspect-specific ratings (Storyline, Acting, Visual Effects, Music) on scale 1-5 "
                    "3. Overall sentiment score (0-1) "
                    "4. Key themes or highlights "
                    "Return as JSON with these exact keys: "
                    "emotion, aspects, sentiment_score, themes"
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "emotion": "neutral",
            "aspects": {
                "Storyline": 3,
                "Acting": 3,
                "Visual Effects": 3,
                "Music": 3
            },
            "sentiment_score": 0.5,
            "themes": ["error in analysis"],
            "error": str(e)
        }

def get_emotion_color(emotion):
    """
    Return a color code for each emotion for visualization.
    """
    colors = {
        "Joy": "#FFD700",  # Gold
        "Anger": "#FF4444",  # Red
        "Sadness": "#4444FF",  # Blue
        "Surprise": "#44FF44",  # Green
        "Disgust": "#800080",  # Purple
        "neutral": "#808080"  # Gray
    }
    return colors.get(emotion, colors["neutral"])
