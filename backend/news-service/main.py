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
        "summary": "Apple Inc. surpassed analyst expectations with record quarterly earnings, driven by strong iPhone 15 sales and growing services revenue.",
        "category": "Stocks",
        "source": "Bloomberg",
        "time": "4 hours ago",
        "bullish": True
    },
    {
        "id": 3,
        "title": "Bitcoin Surges Past $45,000",
        "summary": "Bitcoin crossed the $45,000 mark for the first time in months, fueled by institutional buying and positive sentiment around ETF approvals.",
        "category": "Crypto",
        "source": "CoinDesk",
        "time": "6 hours ago",
        "bullish": True
    },
    {
        "id": 4,
        "title": "Tesla Stock Drops on Production Concerns",
        "summary": "Tesla shares fell sharply after reports of production slowdowns at its Gigafactory, raising concerns about delivery targets for the quarter.",
        "category": "Stocks",
        "source": "Reuters",
        "time": "8 hours ago",
        "bullish": False
    },
    {
        "id": 5,
        "title": "Global Markets Rally on Strong Jobs Data",
        "summary": "World markets surged after US jobs data came in stronger than expected, boosting investor confidence in economic resilience.",
        "category": "Economy",
        "source": "CNBC",
        "time": "10 hours ago",
        "bullish": True
    },
    {
        "id": 6,
        "title": "NVIDIA Announces Next Gen AI Chips",
        "summary": "NVIDIA unveiled its next generation AI accelerator chips, sending its stock to an all time high and sparking excitement across the tech sector.",
        "category": "Technology",
        "source": "TechCrunch",
        "time": "12 hours ago",
        "bullish": True
    },
]

@app.get("/")
def root():
    return {"service": "News Service", "status": "running"}

@app.get("/news")
def get_all_news():
    return {"success": True, "total": len(news_db), "news": news_db}

@app.get("/news/category/{category}")
def get_news_by_category(category: str):
    filtered = [n for n in news_db if n["category"].lower() == category.lower()]
    return {"success": True, "category": category, "news": filtered}

@app.get("/news/{news_id}")
def get_news_by_id(news_id: int):
    news = next((n for n in news_db if n["id"] == news_id), None)
    if not news:
        return {"success": False, "message": "News not found"}
    return {"success": True, "news": news}

@app.get("/news/sentiment/summary")
def sentiment_summary():
    bullish = len([n for n in news_db if n["bullish"]])
    bearish = len([n for n in news_db if not n["bullish"]])
    return {
        "success": True,
        "bullish": bullish,
        "bearish": bearish,
        "overall_sentiment": "Bullish" if bullish > bearish else "Bearish"
    }