from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import uvicorn
from bot_engine import PocketOptionBot

app = FastAPI(title="Pocket Option OTC Bot API", version="2.0")

# Initialize Bot
bot = PocketOptionBot(api_token="YOUR_API_TOKEN")

class TradeRequest(BaseModel):
    pair: str
    action: str  # "CALL" or "PUT"
    amount: float = 1.0
    duration: int = 60

@app.get("/")
def home():
    return {
        "status": "online",
        "broker": "Pocket Option",
        "market": "OTC",
        "message": "Pocket Option OTC Bot API is running successfully!"
    }

@app.get("/pairs")
def get_pairs():
    return {"pairs": bot.get_supported_pairs()}

@app.get("/timeframes")
def get_timeframes():
    return {"timeframes": bot.get_valid_timeframes()}

@app.post("/start")
def start_bot():
    bot.is_running = True
    return {"status": "success", "message": "Bot started successfully"}

@app.post("/stop")
def stop_bot():
    bot.is_running = False
    return {"status": "success", "message": "Bot stopped successfully"}

@app.post("/trade")
def execute_trade(req: TradeRequest):
    result = bot.execute_trade(
        pair=req.pair,
        action=req.action.upper(),
        amount=req.amount,
        duration=req.duration
    )
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    
