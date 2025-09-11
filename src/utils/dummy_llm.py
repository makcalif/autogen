class DummyLLM:
    """
    Dummy LLM that acts as a rule engine for analysis, signal generation, and risk evaluation.
    Replace this with a real LLM service later.
    """
    def analyze_data(self, weekly_data):
        # Simple rule: if average close > average open, market is bullish
        if weekly_data.empty:
            return {"insights": "No data"}
        avg_open = weekly_data['Open'].mean()
        avg_close = weekly_data['Close'].mean()
        if avg_close > avg_open:
            return {"insights": "Bullish week"}
        elif avg_close < avg_open:
            return {"insights": "Bearish week"}
        else:
            return {"insights": "Sideways week"}

    def generate_signals(self, analysis_result):
        # Simple rule: buy if bullish, sell if bearish
        if analysis_result.get("insights") == "Bullish week":
            return {"signals": [{"action": "BUY", "symbol": "AMZN", "quantity": 10}]}
        elif analysis_result.get("insights") == "Bearish week":
            return {"signals": [{"action": "SELL", "symbol": "AMZN", "quantity": 10}]}
        else:
            return {"signals": []}

    def evaluate_risk(self, trading_signals):
        # Simple rule: always approve trade, fixed position size
        if trading_signals.get("signals"):
            return {"risk": "approved", "position_size": 10}
        else:
            return {"risk": "none"}