from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bot_engine import PocketOptionBot

app = FastAPI(title="Pocket Option Multi-Timeframe Bot API", version="2.0.0")
bot = PocketOptionBot(api_token="YOUR_POCKET_OPTION_TOKEN")

class TradeRequest(BaseModel):
    pair: str
    open: list
    high: list
    low: list
    close: list
    amount: float = 1.0
    duration: int = 60  # Supports 3, 5, 15, 30, 60, 120, 180, 300

@app.get("/api/otc/pairs")
def get_otc_pairs():
    return {"supported_pairs": bot.get_supported_pairs()}

@app.get("/api/otc/timeframes")
def get_timeframes():
    return {"valid_timeframes_seconds": bot.get_valid_timeframes()}

@app.post("/api/bot/start")
def start_bot():
    bot.is_running = True
    return {"status": "success", "message": "Pocket Option bot started successfully."}

@app.post("/api/bot/stop")
def stop_bot():
    bot.is_running = False
    return {"status": "success", "message": "Pocket Option bot stopped."}

@app.post("/api/bot/analyze-and-trade")
def analyze_and_trade(data: TradeRequest):
    if not bot.is_running:
        raise HTTPException(status_code=400, detail="Bot is stopped. Start it first.")
    
    if data.pair not in bot.get_supported_pairs():
        raise HTTPException(status_code=400, detail=f"Pair '{data.pair}' is not supported.")
    
    if data.duration not in bot.get_valid_timeframes():
        raise HTTPException(status_code=400, detail=f"Invalid duration. Choose from: {bot.get_valid_timeframes()}")
    
    analysis = bot.analyze_candles(data.open, data.high, data.low, data.close)
    result = {"pair": data.pair, "duration_seconds": data.duration, "analysis": analysis}
    
    if analysis["signal"] in ["CALL", "PUT"]:
        trade_res = bot.execute_trade(data.pair, analysis["signal"], data.amount, data.duration)
        result["trade_execution"] = trade_res
    
    return result
  
