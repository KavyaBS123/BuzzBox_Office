import asyncio
import json
from datetime import datetime
import random
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store connected clients
connected_clients = set()

async def generate_live_data():
    """Generate sample live movie data."""
    data = {
        "timestamp": datetime.now().isoformat(),
        "movie_id": random.randint(1, 100),
        "sentiment_score": round(random.uniform(0.3, 0.95), 2),
        "review_count": random.randint(10, 50),
        "social_buzz_score": random.randint(60, 100)
    }
    return json.dumps(data)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # Generate and send live data every 5 seconds
            data = await generate_live_data()
            await websocket.send_text(data)
            await asyncio.sleep(5)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        connected_clients.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)