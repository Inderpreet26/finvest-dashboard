from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="News Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

news_db = [
    {
        "id": 1,
        "title": "Federal Reserve Holds Interest Rates Steady",
        "summary": "The Federal Reserve decided to maintain current interest rates, signaling a cautious approach to monetary policy amid ongoing economic uncertainty.",
        "category": "Economy",
        "source": "Financial Times",
        "time": "2 hours ago",
        "bullish": True
    },
    {
        "id": 2,
        "title": "Apple Reports Record Q4 Earnings",
        