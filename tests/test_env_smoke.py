import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.env import CookieClickerStockMarketEnv
from src.cookieclicker_stockmarket_sim.config import MarketConfig

class TestEnvSmoke(unittest.TestCase):
    def test_env_reset_step(self):
        config = MarketConfig(max_ticks=10)
        env = CookieClickerStockMarketEnv(config)
        obs, info = env.reset(seed=42)

        self.assertEqual(len(obs), 18 * 4 + 10)

        action = {
            "trades": [0] * 18,
            "loans": [0, 0, 0]
        }
        obs, reward, terminated, truncated, info = env.step(action)
        self.assertEqual(info["tick"], 1)
        self.assertFalse(terminated)

if __name__ == "__main__":
    unittest.main()
