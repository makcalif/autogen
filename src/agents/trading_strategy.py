from src.utils.dummy_llm import DummyLLM

class TradingStrategyAgent:
    def __init__(self):
        self.llm = DummyLLM()

    def generate_signals(self, analysis_result):
        # Use dummy LLM to generate trading signals
        return self.llm.generate_signals(analysis_result)
