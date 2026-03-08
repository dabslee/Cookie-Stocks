import random
from .base import BaseStrategy
from typing import Dict, Any

class RandomStrategy(BaseStrategy):
    def __init__(self, num_stocks: int):
        self.num_stocks = num_stocks

    def decide_action(self, observation: Any, info: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "trades": [random.randint(0, 2) for _ in range(self.num_stocks)],
            "loans": [random.randint(0, 1) for _ in range(3)]
        }
