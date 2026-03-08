from .base import BaseStrategy
from typing import Dict, Any

class ThresholdStrategy(BaseStrategy):
    def __init__(self, buy_threshold: float = 0.7, sell_threshold: float = 1.1):
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def decide_action(self, observation: Any, info: Dict[str, Any]) -> Dict[str, Any]:
        stocks = info["stocks"]
        trades = []
        for stock in stocks:
            ratio = stock.value / stock.resting_value
            if ratio <= self.buy_threshold:
                trades.append(1)
            elif ratio >= self.sell_threshold:
                trades.append(2)
            else:
                trades.append(0)

        return {
            "trades": trades
        }
