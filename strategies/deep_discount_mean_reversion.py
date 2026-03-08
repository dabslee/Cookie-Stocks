from .base import BaseStrategy
from typing import Dict, Any
from src.cookieclicker_stockmarket_sim.office import WarehouseManager
from src.cookieclicker_stockmarket_sim.constants import BROKER_COST

class DeepDiscountMeanReversion(BaseStrategy):
    def decide_action(self, observation: Any, info: Dict[str, Any]) -> Dict[str, Any]:
        stocks = info["stocks"]
        trades = []

        # Broker awareness: Hire brokers if we have cash and haven't reached useful thresholds (58, 72)
        broker_action = 0
        current_brokers = info.get("broker_count", 0) # Should be in info or obs
        # If not in info, we'll try to get it from somewhere else or just assume it's in info now
        # Actually I added it to info in env.py _get_info? No, let me check.
        # Wait, I didn't add broker_count to _get_info in env.py. Let's fix that too.

        # Heuristic: Hire brokers until at least 72 if cash allows
        if info.get("cash", 0) > BROKER_COST * 2: # Keep some buffer
             broker_action = 1

        for stock in stocks:
            ratio = stock.value / stock.resting_value

            # Deep discount: <= 50% resting value
            if ratio <= 0.50:
                trades.append(1) # Buy aggressively
            # Strong buy: 50% to 65%
            elif ratio <= 0.65:
                trades.append(1)
            # Selective buy: 65% to 80% if momentum is favorable (delta > 0)
            elif ratio <= 0.80 and stock.delta > 0:
                trades.append(1)
            # Sell near resting value
            elif ratio >= 0.95:
                trades.append(2)
            else:
                trades.append(0)

        # Tactical Aura Toggling:
        # Supreme Intellect makes modes change faster and increases volatility.
        # Good for finding deals, but maybe switch off when waiting for reversion?
        # For now, let's just keep SI on if we want volatility.
        si_active = 1
        rb_active = 1

        return {
            "trades": trades,
            "loans": [0, 0, 0],
            "auras": [si_active, rb_active],
            "brokers": broker_action
        }
