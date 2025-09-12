from src.data.data_loader import DataLoader
from src.agents.data_analyst import DataAnalystAgent
from src.agents.trading_strategy import TradingStrategyAgent
from src.agents.risk_manager import RiskManagerAgent
from src.agents.portfolio_manager import PortfolioManagerAgent
from src.agents.performance_monitor import PerformanceMonitorAgent
import datetime

DATA_PATH = 'data/amzn_raw.csv'
START_DATE = datetime.datetime(1997, 5, 16)
END_DATE = datetime.datetime(2007, 12, 31)
WEEK = datetime.timedelta(days=7)

def main():
    data_loader = DataLoader(DATA_PATH)
    data_loader.load_data()
    data_analyst = DataAnalystAgent()
    strategy_agent = TradingStrategyAgent()
    risk_manager = RiskManagerAgent()
    portfolio_manager = PortfolioManagerAgent()
    performance_monitor = PerformanceMonitorAgent()

    current_date = START_DATE
    while current_date <= END_DATE:
        print(f"Processing week starting: {current_date.date()}")
        week_end = current_date + WEEK - datetime.timedelta(days=1)
        # Ensure week_end does not go past the last available date in the data
        if data_loader.data is not None and 'Date' in data_loader.data.columns:
            last_data_date = data_loader.data['Date'].max()
            if week_end > last_data_date:
                week_end = last_data_date
        # Pass all data up to week_end for correct SMA calculation
        price_history = data_loader.get_weekly_data(START_DATE, week_end)
        analysis_result = data_analyst.analyze(price_history)
        # Only proceed if analysis_result is valid
        if analysis_result.get('insights') == 'No data':
            current_date += WEEK
            continue
        trading_signals = strategy_agent.generate_signals(analysis_result)
        risk_assessment = risk_manager.evaluate_risk(trading_signals)
        # Get the actual Adj Close price for the trade date (week_end)
        trade_price = None
        if not price_history.empty:
            # Find the last available price on or before week_end
            price_row = price_history[price_history['Date'] <= week_end]
            if not price_row.empty:
                trade_price = price_row.iloc[-1]['Adj Close']
        trades = portfolio_manager.execute_trades(risk_assessment, trade_date=week_end, trade_price=trade_price)
        # Update portfolio and track performance (to be implemented)
        performance_monitor.log_weekly_results()
        current_date += WEEK

if __name__ == "__main__":
    main()
