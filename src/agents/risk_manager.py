from src.utils.dummy_llm import DummyLLM

class RiskManagerAgent:
    def __init__(self):
        self.llm = DummyLLM()

    def evaluate_risk(self, trading_signals):
        # Use dummy LLM to evaluate risk
        return self.llm.evaluate_risk(trading_signals)
