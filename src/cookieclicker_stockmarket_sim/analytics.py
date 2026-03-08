import pandas as pd
from typing import List, Dict, Any, Optional

class MarketAnalytics:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def record_tick(self, tick: int, info: Dict[str, Any], action: Optional[Dict[str, Any]] = None):
        entry = {
            "tick": tick,
            "cash": info["cash"],
            "portfolio_value": info["portfolio_value"],
            "unrealized_pl": info["unrealized_pl"],
            "realized_pl": info["realized_pl"],
            "broker_count": info["broker_count"],
            "supreme_intellect": info["supreme_intellect"],
            "reality_bending": info["reality_bending"],
        }

        # Record actions if provided
        if action:
            entry["action_brokers"] = action.get("brokers", 0)
            if "auras" in action:
                entry["action_si"] = action["auras"][0]
                entry["action_rb"] = action["auras"][1]

            trades = action.get("trades", [])
            for i, t in enumerate(trades):
                entry[f"action_stock_{i}"] = t

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
