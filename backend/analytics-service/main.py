from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI(title="Analytics Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_price_history(base_price, days=30):
    history = []
    price = base_price
    for i in range(days):
        price = round(price + random.uniform(-10, 10), 2)
        history.append({
            "day": i + 1,
            "price": price
        })
    return history

@app.get("/")
def root():
    return {"service": "Analytics Service", "status": "running"}

@app.get("/analytics/price-history/{symbol}")
def get_price_history(symbol: str):
    base_prices = {
        "AAPL": 178.50,
        "GOOGL": 3100.00,
        "TSLA": 850.00,
        "MSFT": 310.00,
        "NVDA": 875.00,
        "BTC": 45000.00,
        "ETH": 3200.00,
    }
    symbol = symbol.upper()
    if symbol not in base_prices:
        return {"success": False, "message": "Symbol not found"}
    
    history = generate_price_history(base_prices[symbol])
    return {
        "success": True,
        "symbol": symbol,
        "history": history
    }

@app.get("/analytics/portfolio-performance/{username}")
def portfolio_performance(username: str):
    monthly_data = []
    value = 10000
    for month in ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
        value = round(value + random.uniform(-500, 1000), 2)
        monthly_data.append({"month": month, "value": value})
    
    return {
        "success": True,
        "username": username,
        "starting_value": 10000,
        "current_value": value,
        "monthly_performance": monthly_data
    }

@app.get("/analytics/sector-breakdown")
def sector_breakdown():
    return {
        "success": True,
        "sectors": [
            {"sector": "Technology", "percentage": 35},
            {"sector": "Healthcare", "percentage": 20},
            {"sector": "Finance", "percentage": 15},
            {"sector": "Energy", "percentage": 10},
            {"sector": "Consumer", "percentage": 12},
            {"sector": "Crypto", "percentage": 8},
        ]
    }

@app.get("/analytics/risk-score/{username}")
def risk_score(username: str):
    score = random.randint(30, 85)
    if score < 40:
        risk_level = "Low"
    elif score < 70:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    return {
        "success": True,
        "username": username,
        "risk_score": score,
        "risk_level": risk_level,
        "recommendation": "Diversify your portfolio for better risk management"
    }