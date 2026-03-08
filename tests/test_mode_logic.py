import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.engine import StockMarketEngine
from src.cookieclicker_stockmarket_sim.config import MarketConfig
from src.cookieclicker_stockmarket_sim.types import MarketMode

class TestModeLogic(unittest.TestCase):
    def test_mode_selection(self):
        config = MarketConfig(seed=42)
        engine = StockMarketEngine(config)

        # Test transition from Fast Rise
        new_mode = engine.select_new_mode(MarketMode.FAST_RISE)
        # 70% chance of Chaotic. With seed 42, it might or might not be.
        # We just check it returns a valid mode.
        self.assertIn(new_mode, list(MarketMode))

    def test_mode_duration(self):
        config = MarketConfig(seed=42)
        engine = StockMarketEngine(config)
        duration = engine.get_new_mode_duration()
        self.assertGreaterEqual(duration, 10)
        self.assertLessEqual(duration, 700)

if __name__ == "__main__":
    unittest.main()
