import pandas as pd
from typing import List, Dict, Any

class MarketAnalytics:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def record_tick(self, tick: int, info: Dict[str, Any]):
        entry = {
            "tick": tick,
            "cash": info["cash"],
            "portfolio_value": info["portfolio_value"],
            "unrealized_pl": info["unrealized_pl"],
            "realized_pl": info["realized_pl"],
        }

        for stock in info["stocks"]:
            prefix = f"stock_{stock.stock_id}"
            entry[f"{prefix}_price"] = stock.value
            entry[f"{prefix}_resting"] = stock.resting_value
            entry[f"{prefix}_shares"] = stock.shares_owned
            entry[f"{prefix}_delta"] = stock.delta
            entry[f"{prefix}_mode"] = int(stock.mode)

        self.history.append(entry)

    def get_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self.history)

    def save_csv(self, filepath: str):
        df = self.get_dataframe()
        df.to_csv(filepath, index=False)
