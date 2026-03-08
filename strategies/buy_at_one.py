from .base import BaseStrategy
from typing import Dict, Any

class BuyAtOne(BaseStrategy):
    def decide_action(self, observation: Any, info: Dict[str, Any]) -> Dict[str, Any]:
        stocks = info["stocks"]
        trades = []
        for stock in stocks:
            if stock.value <= 1.5: # Hard floor is $1, so 1.5 is very close
                trades.append(1) # Buy
            elif stock.value >= 5.0: # Sell when it recovers a bit
                trades.append(2)
            else:
                trades.append(0)

        return {
            "trades": trades,
            "brokers": 1
        }
