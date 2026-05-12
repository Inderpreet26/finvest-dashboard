from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Portfolio Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake portfolio database
portfolios_db = {
    "user1": [
        {"symbol": "AAPL", "name": "Apple Inc.", "shares": 10, "buy_price": 150.00, "current_price": 178.50},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "shares": 5, "buy_price": 2800.00, "current_price": 3100.00},
        {"symbol": "TSLA", "name": "Tesla Inc.", "shares": 8, "buy_price": 700.00, "current_price": 850.00},
        {"symbol": "MSFT", "name": "Microsoft Corp.", "shares": 15, "buy_price": 280.00, "current_price": 310.00},
    ]
}

class Investment(BaseModel):
    username: str
    symbol: str
    name: str
    shares: float
    buy_price: float
    current_price: float

@app.get("/")
def root():
    return {"service": "Portfolio Service", "status": "running"}

@app.get("/portfolio/{username}")
def get_portfolio(username: str):
    if username not in portfolios_db:
        return {"success": False, "message": "No portfolio found"}
    
    portfolio = portfolios_db[username]
    total_invested = sum(i["shares"] * i["buy_price"] for i in portfolio)
    total_current = sum(i["shares"] * i["current_price"] for i in portfolio)
    profit_loss = total_current - total_invested
    
    return {
        "success": True,
        "username": username,
        "investments": portfolio,
        "total_invested": round(total_invested, 2),
        "total_current_value": round(total_current, 2),
        "profit_loss": round(profit_loss, 2),
        "profit_loss_percent": round((profit_loss / total_invested) * 100, 2)
    }

@app.post("/portfolio/add")
def add_investment(investment: Investment):
    if investment.username not in portfolios_db:
        portfolios_db[investment.username] = []
    
    portfolios_db[investment.username].append({
        "symbol": investment.symbol,
        "name": investment.name,
        "shares": investment.shares,
        "buy_price": investment.buy_price,
        "current_price": investment.current_price
    })
    return {"success": True, "message": "Investment added successfully"}

@app.delete("/portfolio/{username}/{symbol}")
def remove_investment(username: str, symbol: str):
    if username not in portfolios_db:
        return {"success": False, "message": "User not found"}
    
    portfolios_db[username] = [
        i for i in portfolios_db[username] if i["symbol"] != symbol
    ]
    return {"success": True, "message": f"{symbol} removed from portfolio"}