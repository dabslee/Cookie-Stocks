import math
from .config import MarketConfig

class BrokerManager:
    @staticmethod
    def calculate_overhead(brokers: int) -> float:
        # overhead = 0.01 * 20 * (0.95 ** brokers)
        return 0.01 * 20 * (0.95 ** brokers)

    @staticmethod
    def get_buy_price(base_price: float, overhead: float) -> float:
        return base_price * (1.0 + overhead)

    @staticmethod
    def get_sell_price(base_price: float) -> float:
        return base_price
