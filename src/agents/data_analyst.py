from src.utils.dummy_llm import DummyLLM

class DataAnalystAgent:
    def __init__(self):
        self.llm = DummyLLM()

    def analyze(self, weekly_data):
        # Use dummy LLM to analyze data
        return self.llm.analyze_data(weekly_data)
