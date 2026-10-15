import numpy as np
import talib
import time

class PocketOptionBot:
    def __init__(self, api_token):
        self.api_token = api_token
        self.is_running = False
        
        # All Pocket Option OTC Pairs
        self.otc_pairs = [
            "EURUSD_OTC", "GBPUSD_OTC", "USDJPY_OTC", "AUDUSD_OTC", 
            "USDCAD_OTC", "NZDUSD_OTC", "USDCHF_OTC",
            "EURGBP_OTC", "EURJPY_OTC", "GBPJPY_OTC", "AUDJPY_OTC", 
            "EURAUD_OTC", "GBPCAD_OTC", "GBPNZD_OTC", "EURCAD_OTC",
            "Gold_OTC", "Silver_OTC", "USCrude_OTC", 
            "BTCUSD_OTC", "ETHUSD_OTC"
        ]
        
        # Valid Timeframes from 3s to 5m (in seconds)
        self.valid_timeframes = [3, 5, 15, 30, 60, 120, 180, 300]

    def get_supported_pairs(self):
        return self.otc_pairs

    def get_valid_timeframes(self):
        return self.valid_timeframes

    def analyze_candles(self, open_prices, high_prices, low_prices, close_prices):
        o = np.array(open_prices, dtype=float)
        h = np.array(high_prices, dtype=float)
        l = np.array(low_prices, dtype=float)
        c = np.array(close_prices, dtype=float)

        engulfing = talib.CDLENGULFING(o, h, l, c)
        sma = talib.SMA(c, timeperiod=14)
        
        latest_pattern = engulfing[-1]
        current_close = c[-1]
        current_sma = sma[-1]

        signal = "HOLD"
        if latest_pattern > 0 and current_close > current_sma:
            signal = "CALL"
        elif latest_pattern < 0 and current_close < current_sma:
            signal = "PUT"

        return {
            "signal": signal,
            "pattern_value": int(latest_pattern),
            "price": current_close
        }

    def execute_trade(self, pair, action, amount=1.0, duration=60):
        if not self.is_running:
            return {"status": "error", "message": "Bot is stopped"}
        
        if pair not in self.otc_pairs:
            return {"status": "error", "message": f"Invalid OTC pair: {pair}"}
        
        if duration not in self.valid_timeframes:
            return {"status": "error", "message": f"Invalid duration/timeframe: {duration}s"}
        
        print(f"[Pocket Option OTC] Executing {action} on {pair} | Timeframe: {duration}s | Amount: ${amount}")
        
        return {
            "status": "success",
            "broker": "Pocket Option",
            "market": "OTC",
            "pair": pair,
            "action": action,
            "amount": amount,
            "duration_seconds": duration,
            "timestamp": time.time()
        }
      
