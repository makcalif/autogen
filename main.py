from src.data.data_loader import DataLoader
from src.agents.data_analyst import DataAnalystAgent
from src.agents.trading_strategy import TradingStrategyAgent
from src.agents.risk_manager import RiskManagerAgent
from src.agents.portfolio_manager import PortfolioManagerAgent
from src.agents.performance_monitor import PerformanceMonitorAgent
import datetime

DATA_PATH = 'data/amzn_raw.csv'
START_DATE = datetime.datetime(1995, 1, 1)
END_DATE = datetime.datetime(2005, 12, 31)
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
        week_end = current_date + WEEK - datetime.timedelta(days=1)
        weekly_data = data_loader.get_weekly_data(current_date, week_end)
        print(f"Processing week: {current_date.date()} to {week_end.date()}" )
        analysis_result = data_analyst.analyze(weekly_data)
        trading_signals = strategy_agent.generate_signals(analysis_result)
        risk_assessment = risk_manager.evaluate_risk(trading_signals)
        trades = portfolio_manager.execute_trades(risk_assessment, trade_date=week_end)
        # Update portfolio and track performance (to be implemented)
        performance_monitor.log_weekly_results()
        current_date += WEEK

if __name__ == "__main__":
    main()
