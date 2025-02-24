import json
import os
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "default-key")
client = OpenAI(api_key=OPENAI_API_KEY)

def analyze_review_sentiment(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the movie review sentiment and provide: "
                    "sentiment (positive/negative/neutral), confidence score (0-1), "
                    "and key themes mentioned. Return as JSON."
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {
            "sentiment": "neutral",
            "confidence": 0.5,
            "themes": ["error in analysis"],
            "error": str(e)
        }
