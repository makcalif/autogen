import pandas as pd
import os

class DataLoader:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None

    def load_data(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        self.data = pd.read_csv(self.data_path)
        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')
        return self.data

    def get_weekly_data(self, start_date, end_date):
        if self.data is None:
            self.load_data()
        # Failsafe: always ensure 'Date' is datetime before filtering
        self.data['Date'] = pd.to_datetime(self.data['Date'], errors='coerce')
        self.data = self.data.dropna(subset=['Date'])  # Remove rows with invalid dates
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (self.data['Date'] >= start_date) & (self.data['Date'] <= end_date)
        return self.data.loc[mask]
