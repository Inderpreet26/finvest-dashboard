from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Watchlist Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

watchlists_db = {
    "user1": [
        {"symbol": "AAPL", "name": "Apple Inc.", "price": 178.50, "change": 2.3},
        {"symbol": "NVDA", "name": "NVIDIA Corp.", "price": 875.00, "change": 4.5},
        {"symbol": "BTC", "name": "Bitcoin", "price": 45000.00, "change": 3.5},
    ]
}

class WatchlistItem(BaseModel):
    username: str
    symbol: str
    name: str
    price: float
    change: float

@app.get("/")
def root():
    return {"service": "Watchlist Service", "status": "running"}

@app.get("/watchlist/{username}")
def get_watchlist(username: str):
    if username not in watchlists_db:
        return {"success": True, "username": username, "watchlist": []}
    return {
        "success": True,
        "username": username,
        "total": len(watchlists_db[username]),
        "watchlist": watchlists_db[username]
    }

@app.post("/watchlist/add")
def add_to_watchlist(item: WatchlistItem):
    if item.username not in watchlists_db:
        watchlists_db[item.username] = []
    
    symbols = [i["symbol"] for i in watchlists_db[item.username]]
    if item.symbol in symbols:
        return {"success": False, "message": "Already in watchlist"}
    
    watchlists_db[item.username].append({
        "symbol": item.symbol,
        "name": item.name,
        "price": item.price,
        "change": item.change
    })
    return {"success": True, "message": f"{item.symbol} added to watchlist"}

@app.delete("/watchlist/{username}/{symbol}")
def remove_from_watchlist(username: str, symbol: str):
    if username not in watchlists_db:
        return {"success": False, "message": "User not found"}
    
    watchlists_db[username] = [
        i for i in watchlists_db[username] if i["symbol"] != symbol
    ]
    return {"success": True, "message": f"{symbol} removed from watchlist"}