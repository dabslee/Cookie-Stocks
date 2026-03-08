import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.office import WarehouseManager
from src.cookieclicker_stockmarket_sim.config import MarketConfig

class TestCapacity(unittest.TestCase):
    def test_base_capacity(self):
        # Office Level 1: +25 warehouse space
        config = MarketConfig(office_level=1, highest_buildings_owned={"Farm": 100}, building_levels={"Farm": 1})
        # Base capacity = 100 + 10 * 1 = 110
        # Office bonus = 25
        # Total = 135
        cap = WarehouseManager.calculate_capacity(0, "Farm", config)
        self.assertEqual(cap, 135)

    def test_office_level_5_multiplier(self):
        # Office Level 5: +50% base warehouse space
        config = MarketConfig(office_level=5, highest_buildings_owned={"Farm": 100}, building_levels={"Farm": 1})
        # Base capacity = floor(100 * 1.5) + 10 * 1 = 150 + 10 = 160
        # Office bonus for level 5 is 0 (it uses multiplier)
        cap = WarehouseManager.calculate_capacity(0, "Farm", config)
        self.assertEqual(cap, 160)

if __name__ == "__main__":
    unittest.main()
