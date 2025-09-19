# Autogen Trading Simulation

This project is a modular multi-agent trading simulation using historical stock data (Amazon, 10 years daily). It features a real LLM (GPT-4.1 Nano) analyst agent, technical indicator computation, and robust trade logging.

## Features
- Modular agent design: Analyst, Strategy, Risk Manager, Portfolio, Performance Monitor
- LLMDataAnalystAgent uses OpenAI API for market analysis
- Technical indicators: MACD, ROC-14d, RSI-14, Momentum-14, ROC/Momentum
- Strict JSON output enforcement for LLM responses
- Historical data slicing to avoid lookahead bias
- Trade logging and performance tracking

## Getting Started
1. **Install dependencies**
   - Python 3.8+
   - pandas
   - openai (>=1.0.0)
   - (Optional) conda environment recommended

2. **Set up OpenAI API key**
   - Set the environment variable `OPENAI_API_KEY` with your key.

3. **Run the simulation**
   ```powershell
   python main.py
   ```

## File Structure
- `main.py` — Orchestrates the simulation
- `src/agents/llm_data_analyst.py` — LLM analyst agent
- `src/data/data_loader.py` — Loads historical data
- `src/agents/trading_strategy.py` — Strategy agent
- `src/agents/risk_manager.py` — Risk manager agent
- `src/agents/portfolio_manager.py` — Portfolio manager agent
- `src/agents/performance_monitor.py` — Performance monitor agent
- `data/amzn_raw.csv` — Historical price data
- `results/trades_log.csv` — Trade logs

## Notes
- The analyst agent requires at least 26 days of data for full indicator calculation.
- All LLM responses are parsed as strict JSON for reliability. test update

## License
MIT

