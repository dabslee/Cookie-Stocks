from .base import BaseStrategy
from typing import Dict, Any

class NaiveMeanReversion(BaseStrategy):
    def decide_action(self, observation: Any, info: Dict[str, Any]) -> Dict[str, Any]:
        stocks = info["stocks"]
        trades = []
        for stock in stocks:
            if stock.value < stock.resting_value:
                trades.append(1) # Buy
            elif stock.value > stock.resting_value:
                trades.append(2) # Sell
            else:
                trades.append(0) # Hold

        return {
            "trades": trades,
            "loans": [0, 0, 0]
        }
