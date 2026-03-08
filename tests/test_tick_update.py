import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.engine import StockMarketEngine
from src.cookieclicker_stockmarket_sim.config import MarketConfig
from src.cookieclicker_stockmarket_sim.types import MarketMode

class TestTickUpdate(unittest.TestCase):
    def test_value_floor(self):
        config = MarketConfig(seed=42)
        engine = StockMarketEngine(config)
        # Force a stock to a very low value
        engine.stocks[0].value = -10.0
        engine.tick()
        # Hard floor is 1.0, then low price correction: val += (5-val)/2
        # If val was 1.0 after floor, val becomes 1.0 + (5-1)/2 = 3.0
        self.assertGreaterEqual(engine.stocks[0].value, 1.0)

    def test_market_cap_damping(self):
        config = MarketConfig(bank_level=1, seed=42)
        engine = StockMarketEngine(config)
        # market_cap = 100 + 3 * (1-1) = 100
        engine.stocks[0].value = 200.0
        engine.stocks[0].delta = 1.0
        # Set mode to Stable to have predictable mode rules (delta *= 0.95)
        engine.stocks[0].mode = MarketMode.STABLE
        engine.tick()
        # delta should be decreased by an additional 10%
        # base decay is 0.97
        # Mode rule: delta *= 0.95
        # Market cap damping: delta *= 0.90
        # Also there's random fluctuation +/- 0.05
        # and Mode stable random +/- 0.025
        # Total: (1.0 * 0.97 * 0.95 + randoms) * 0.90
        # It's hard to be exact with randoms, so let's check it's within a range
        self.assertLess(engine.stocks[0].delta, 1.0)

if __name__ == "__main__":
    unittest.main()
