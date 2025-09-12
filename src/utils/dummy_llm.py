
# Dummy LLM for rule-based analysis
import pandas as pd

class DummyLLM:
    """
    Dummy LLM that acts as a rule engine for analysis, signal generation, and risk evaluation.
    Replace this with a real LLM service later.
    """
    def analyze_data(self, price_history):
        # Calculate 20-day and 50-day SMA of Adj Close
        if price_history.empty or 'Adj Close' not in price_history.columns:
            print("[DEBUG] price_history is empty or missing 'Adj Close'")
            return {"insights": "No data"}
        price_history = price_history.copy()
        # Sort by date to ensure correct rolling calculation
        if 'Date' in price_history.columns:
            price_history = price_history.sort_values('Date')
        price_history['SMA20'] = price_history['Adj Close'].rolling(window=20).mean()
        price_history['SMA50'] = price_history['Adj Close'].rolling(window=50).mean()
        # Debug: print last few rows
        print("[DEBUG] Last 5 rows before crossover check:")
        print(price_history[['Date', 'Adj Close', 'SMA20', 'SMA50']].tail(5))
        # Find crossover for the last available day
        last = price_history.iloc[-1]
        prev = price_history.iloc[-2] if len(price_history) > 1 else last
        print(f"[DEBUG] last SMA20: {last['SMA20']}, SMA50: {last['SMA50']}")
        print(f"[DEBUG] prev SMA20: {prev['SMA20']}, SMA50: {prev['SMA50']}")
        signal = 0
        if not pd.isna(last['SMA20']) and not pd.isna(last['SMA50']) and not pd.isna(prev['SMA20']) and not pd.isna(prev['SMA50']):
            if prev['SMA20'] < prev['SMA50'] and last['SMA20'] > last['SMA50']:
                print(f"[DEBUG] BUY crossover detected: prev_SMA20={prev['SMA20']}, prev_SMA50={prev['SMA50']}, last_SMA20={last['SMA20']}, last_SMA50={last['SMA50']}")
                signal = 1  # Buy
            elif prev['SMA20'] > prev['SMA50'] and last['SMA20'] < last['SMA50']:
                print(f"[DEBUG] SELL crossover detected: prev_SMA20={prev['SMA20']}, prev_SMA50={prev['SMA50']}, last_SMA20={last['SMA20']}, last_SMA50={last['SMA50']}")
                signal = -1 # Sell
        return {
            "insights": {
                "SMA20": last['SMA20'],
                "SMA50": last['SMA50'],
                "signal": signal
            }
        }

    def generate_signals(self, analysis_result):
        # Use moving average crossover signal
        insights = analysis_result.get("insights", {})
        signal = analysis_result.get("signal", 0) if isinstance(analysis_result, dict) else 0
        if signal == 1:
            return {"signals": [{"action": "BUY", "symbol": "AMZN", "quantity": 10}]}
        elif signal == -1:
            return {"signals": [{"action": "SELL", "symbol": "AMZN", "quantity": 10}]}
        else:
            return {"signals": []}

    def evaluate_risk(self, trading_signals):
        # Simple rule: always approve trade, fixed position size
        # Always include the signals in the risk assessment
        if trading_signals.get("signals"):
            return {"risk": "approved", "position_size": 10, "signals": trading_signals["signals"]}
        else:
            return {"risk": "none", "signals": []}