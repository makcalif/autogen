import pandas as pd
import os

import json

from openai import OpenAI

class LLMDataAnalystAgent:
    # ...existing code...
    def __init__(self, api_key=None, model="gpt-4.1-nano"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def analyze(self, price_history: pd.DataFrame):
        if price_history.empty or 'Adj Close' not in price_history.columns:
            return {"insights": "No data"}
        # Print sample of price_history for sanity check
        print("[LLMDataAnalystAgent] Sample price_history (head):")
        print(price_history.head())
        print("[LLMDataAnalystAgent] Sample price_history (tail):")
        print(price_history.tail())

        # Compute MACD indicators
        exp12 = price_history['Adj Close'].ewm(span=12, adjust=False).mean()
        exp26 = price_history['Adj Close'].ewm(span=26, adjust=False).mean()
        macd_line = exp12 - exp26
        macd_signal = macd_line.ewm(span=9, adjust=False).mean()
        macd_hist = macd_line - macd_signal
        last_macd_line = macd_line.iloc[-1] if len(macd_line) > 0 else float('nan')
        last_macd_signal = macd_signal.iloc[-1] if len(macd_signal) > 0 else float('nan')
        last_macd_hist = macd_hist.iloc[-1] if len(macd_hist) > 0 else float('nan')

        # Compute 14-day Rate of Change (ROC)
        if len(price_history) >= 15:
            roc_14d = ((price_history['Adj Close'].iloc[-1] / price_history['Adj Close'].iloc[-15]) - 1) * 100
        else:
            roc_14d = float('nan')

        # Compute RSI-14 only
        delta = price_history['Adj Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain_14 = gain.rolling(window=14, min_periods=14).mean()
        avg_loss_14 = loss.rolling(window=14, min_periods=14).mean()
        rs_14 = avg_gain_14 / (avg_loss_14 + 1e-9)
        rsi_14 = 100 - (100 / (1 + rs_14))
        last_rsi_14 = rsi_14.iloc[-1]

        # Compute 14-day momentum
        if len(price_history) >= 15:
            momentum_14 = price_history['Adj Close'].iloc[-1] - price_history['Adj Close'].iloc[-15]
        else:
            momentum_14 = float('nan')

        # Compute ROC/Momentum indicator
        if momentum_14 != 0 and not (pd.isna(roc_14d) or pd.isna(momentum_14)):
            roc_momentum = roc_14d / momentum_14
        else:
            roc_momentum = float('nan')

        def nan_to_none(x):
            return None if pd.isna(x) else x

        features = {
            "roc_14d": nan_to_none(round(roc_14d, 4)),
            "rsi_14": nan_to_none(round(last_rsi_14, 4)),
            "momentum_14": nan_to_none(round(momentum_14, 4)),
            "roc_momentum": nan_to_none(round(roc_momentum, 4)),
            "macd_line": nan_to_none(round(last_macd_line, 4)),
            "macd_signal": nan_to_none(round(last_macd_signal, 4)),
            "macd_hist": nan_to_none(round(last_macd_hist, 4))
        }

        prompt = f'''
You are a financial analyst. Given the following 14-day summary and instructions, analyze the trend and provide a trading insight.
Respond ONLY with a valid JSON object in the following format and nothing else:
{{"insights": "<short explanation>", "signal": 1}}
Where 'signal' is 1 for BUY, -1 for SELL, 0 for HOLD.

Here is the data:
summary_14d: {json.dumps({
    'rsi': features['rsi_14'],
    'roc_14': features['roc_14d'],
    'macd_line': features['macd_line'],
    'macd_signal': features['macd_signal'],
    'macd_hist': features['macd_hist']
})}
instructions: {{
  "rules": {{
    "RSI": "RSI > 70 = overbought → consider SELL; RSI < 30 = oversold → consider BUY",
    "ROC_14": "ROC > +2% → bullish → BUY; ROC < -2% → bearish → SELL",
    "MACD": "MACD line > signal line → bullish → BUY; MACD line < signal line → bearish → SELL"
  }},
  "goal": "Using the above indicators, choose one action: BUY, SELL, or HOLD. Avoid staying neutral unless the indicators strongly conflict."
}}
Example response: {{"insights": "MACD is bearish, recommend SELL.", "signal": -1}}
'''

        print("[LLMDataAnalystAgent] Prompt for LLM:")
        print(prompt)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.2
            )
            # Parse LLM response
            content = response.choices[0].message.content
            print("[LLMDataAnalystAgent] Raw LLM response:", repr(content))
            try:
                result = json.loads(content)
                print("[LLMDataAnalystAgent] LLM response content:", content)
                print("[LLMDataAnalystAgent] signal:", result.get("signal"))
                return result
            except json.JSONDecodeError as jde:
                print(f"[LLMDataAnalystAgent] JSON decode error: {jde}")
                print("[LLMDataAnalystAgent] LLM response was not valid JSON:", repr(content))
                return {"insights": "LLM invalid JSON response", "signal": 0}
        except Exception as e:
            print(f"[LLMDataAnalystAgent] LLM call failed: {e}")
            return {"insights": "LLM error", "signal": 0}
        return {"insights": "LLM call commented out for debug", "signal": 0}
