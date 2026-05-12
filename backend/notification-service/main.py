from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Notification Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

notifications_db = {
    "user1": [
        {
            "id": 1,
            "type": "price_alert",
            "message": "AAPL crossed $180 target price!",
            "symbol": "AAPL",
            "read": False,
            "time": "2 hours ago"
        },
        {
            "id": 2,
            "type": "news_alert",
            "message": "Breaking: Federal Reserve announces rate decision",
            "symbol": None,
            "read": False,
            "time": "4 hours ago"
        },
        {
            "id": 3,
            "type": "portfolio_alert",
            "message": "Your portfolio is up 5% today!",
            "symbol": None,
            "read": True,
            "time": "6 hours ago"
        },
        {
            "id": 4,
            "type": "price_alert",
            "message": "BTC dropped below $44,000 warning level!",
            "symbol": "BTC",
            "read": False,
            "time": "8 hours ago"
        },
    ]
}

alerts_db = {}

class Alert(BaseModel):
    username: str
    symbol: str
    target_price: float
    condition: str

class MarkRead(BaseModel):
    username: str
    notification_id: int

@app.get("/")
def root():
    return {"service": "Notification Service", "status": "running"}

@app.get("/notifications/{username}")
def get_notifications(username: str):
    if username not in notifications_db:
        return {"success": True, "notifications": []}
    
    notifs = notifications_db[username]
    unread = len([n for n in notifs if not n["read"]])
    
    return {
        "success": True,
        "username": username,
        "total": len(notifs),
        "unread": unread,
        "notifications": notifs
    }

@app.post("/notifications/mark-read")
def mark_as_read(data: MarkRead):
    if data.username not in notifications_db:
        return {"success": False, "message": "User not found"}
    
    for notif in notifications_db[data.username]:
        if notif["id"] == data.notification_id:
            notif["read"] = True
            return {"success": True, "message": "Notification marked as read"}
    
    return {"success": False, "message": "Notification not found"}

@app.post("/alerts/set")
def set_alert(alert: Alert):
    if alert.username not in alerts_db:
        alerts_db[alert.username] = []
    
    alerts_db[alert.username].append({
        "symbol": alert.symbol,
        "target_price": alert.target_price,
        "condition": alert.condition,
        "active": True
    })
    return {
        "success": True,
        "message": f"Alert set for {alert.symbol} at ${alert.target_price}"
    }

@app.get("/alerts/{username}")
def get_alerts(username: str):
    if username not in alerts_db:
        return {"success": True, "alerts": []}
    return {
        "success": True,
        "username": username,
        "alerts": alerts_db[username]
    }