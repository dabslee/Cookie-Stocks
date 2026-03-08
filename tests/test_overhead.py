import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.brokers import BrokerManager

class TestOverhead(unittest.TestCase):
    def test_overhead_formula(self):
        # overhead = 0.01 * 20 * (0.95 ** brokers)
        # 0 brokers: 0.01 * 20 * 1 = 0.20 (20%)
        self.assertAlmostEqual(BrokerManager.calculate_overhead(0), 0.20)

        # 58 brokers: ~1%
        overhead_58 = BrokerManager.calculate_overhead(58)
        self.assertLess(overhead_58, 0.011)
        self.assertGreater(overhead_58, 0.009)

        # 72 brokers: < 0.5%
        overhead_72 = BrokerManager.calculate_overhead(72)
        self.assertLess(overhead_72, 0.005)

if __name__ == "__main__":
    unittest.main()
