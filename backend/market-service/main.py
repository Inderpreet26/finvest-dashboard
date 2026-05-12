from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Market Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake market data
stocks = {
    "AAPL": {"name": "Apple Inc.", "price": 178.50, "change": 2.3},
    "GOOGL": {"name": "Alphabet Inc.", "price": 3100.00, "change": -1.2},
    "TSLA": {"name": "Tesla Inc.", "price": 850.00, "change": 5.1},
    "MSFT": {"name": "Microsoft Corp.", "price": 310.00, "change": 1.8},
    "AMZN": {"name": "Amazon.com Inc.", "price": 3400.00, "change": -0.5},
    "META": {"name": "Meta Platforms Inc.", "price": 320.00, "change": 3.2},
    "NFLX": {"name": "Netflix Inc.", "price": 550.00, "change": -2.1},
    "NVDA": {"name": "NVIDIA Corp.", "price": 875.00, "change": 4.5},
}

crypto = {
    "BTC": {"name": "Bitcoin", "price": 45000.00, "change": 3.5},
    "ETH": {"name": "Ethereum", "price": 3200.00, "change": 2.1},
    "BNB": {"name": "Binance Coin", "price": 420.00, "change": -1.5},
    "SOL": {"name": "Solana", "price": 110.00, "change": 6.2},
}

@app.get("/")
def root():
    return {"service": "Market Service", "status": "running"}

@app.get("/stocks")
def get_all_stocks():
    return {"success": True, "stocks": stocks}

@app.get("/stocks/{symbol}")
def get_stock(symbol: str):
    symbol = symbol.upper()
    if symbol not in stocks:
        return {"success": False, "message": "Stock not found"}
    
    # Simulate live price change
    stock = stocks[symbol].copy()
    stock["price"] = round(stock["price"] + random.uniform(-5, 5), 2)
    stock["change"] = round(random.uniform(-5, 5), 2)
    
    return {"success": True, "symbol": symbol, "data": stock}

@app.get("/crypto")
def get_all_crypto():
    return {"success": True, "crypto": crypto}

@app.get("/crypto/{symbol}")
def get_crypto(symbol: str):
    symbol = symbol.upper()
    if symbol not in crypto:
        return {"success": False, "message": "Crypto not found"}
    
    coin = crypto[symbol].copy()
    coin["price"] = round(coin["price"] + random.uniform(-100, 100), 2)
    coin["change"] = round(random.uniform(-5, 5), 2)
    
    return {"success": True, "symbol": symbol, "data": coin}

@app.get("/market/summary")
def market_summary():
    return {
        "success": True,
        "total_stocks": len(stocks),
        "total_crypto": len(crypto),
        "market_status": "Open",
        "top_gainer": "NVDA",
        "top_loser": "NFLX"
    }