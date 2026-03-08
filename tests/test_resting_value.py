import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.engine import StockMarketEngine
from src.cookieclicker_stockmarket_sim.config import MarketConfig
from src.cookieclicker_stockmarket_sim.constants import STOCKS_METADATA

class TestRestingValue(unittest.TestCase):
    def test_resting_value_formula(self):
        config = MarketConfig(bank_level=1)
        engine = StockMarketEngine(config)
        # resting_value = 10 * (stock_id + 1) + bank_level - 1
        # For stock_id 0 (CRL): 10 * 1 + 1 - 1 = 10
        self.assertEqual(engine.calculate_resting_value(0), 10.0)
        # For stock_id 3 (SUG): 10 * 4 + 1 - 1 = 40
        self.assertEqual(engine.calculate_resting_value(3), 40.0)

    def test_resting_value_with_bank_level(self):
        config = MarketConfig(bank_level=10)
        engine = StockMarketEngine(config)
        # For stock_id 0 (CRL): 10 * 1 + 10 - 1 = 19
        self.assertEqual(engine.calculate_resting_value(0), 19.0)

if __name__ == "__main__":
    unittest.main()
