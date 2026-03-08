import random
from typing import List, Optional, Tuple
import numpy as np

from .constants import STOCKS_METADATA, AURA_EFFECTS, MODE_PROBABILITIES
from .types import StockState, MarketMode
from .config import MarketConfig

class StockMarketEngine:
    def __init__(self, config: MarketConfig):
        self.config = config
        self.rng = random.Random(config.seed)

        # Initialize stocks
        self.stocks: List[StockState] = []
        for meta in STOCKS_METADATA:
            resting_val = self.calculate_resting_value(meta.stock_id)
            # Initial values are often around resting value
            val = max(1.0, resting_val + self.rng.uniform(-5, 5))

            mode = self.rng.choices(list(MarketMode), weights=MODE_PROBABILITIES)[0]
            duration = self.get_new_mode_duration()

            self.stocks.append(StockState(
                stock_id=meta.stock_id,
                value=val,
                delta=0.0,
                mode=mode,
                mode_duration=duration,
                resting_value=resting_val,
                max_shares=0 # Will be set by portfolio/office logic
            ))

    def calculate_resting_value(self, stock_id: int) -> float:
        # resting_value = 10 * (stock_id + 1) + bank_level - 1
        return 10 * (stock_id + 1) + self.config.bank_level - 1

    def calculate_market_cap(self) -> float:
        # market_cap = 100 + 3 * (bank_level - 1)
        return 100 + 3 * (self.config.bank_level - 1)

    def get_aura_state_key(self) -> str:
        si = self.config.supreme_intellect
        rb = self.config.reality_bending
        if si and rb: return "Both"
        if si: return "Supreme Intellect"
        if rb: return "Reality Bending"
        return "Base"

    def get_new_mode_duration(self) -> int:
        aura_key = self.get_aura_state_key()
        aura = AURA_EFFECTS[aura_key]
        return self.rng.randint(10, aura.max_mode_duration)

    def select_new_mode(self, current_mode: MarketMode) -> MarketMode:
        aura_key = self.get_aura_state_key()
        aura = AURA_EFFECTS[aura_key]

        # Exception: Fast Rise/Fall -> 70% chance of Chaotic
        if current_mode in [MarketMode.FAST_RISE, MarketMode.FAST_FALL]:
            if self.rng.random() < 0.70:
                return MarketMode.CHAOTIC

        # Bypass to Chaotic chance
        if self.rng.random() < aura.bypass_to_chaotic_chance:
            return MarketMode.CHAOTIC

        return self.rng.choices(list(MarketMode), weights=MODE_PROBABILITIES)[0]

    def tick(self):
        aura_key = self.get_aura_state_key()
        aura = AURA_EFFECTS[aura_key]
        market_cap = self.calculate_market_cap()

        # Instant mode change event
        if self.rng.random() < aura.instant_mode_change_chance:
            self.trigger_instant_mode_change()

        for stock in self.stocks:
            # 1. Apply per-tick delta decay
            stock.delta *= aura.delta_decay

            # 2. Add delta to value
            stock.value += stock.delta

            # 3. Pull value 1% toward resting value
            stock.resting_value = self.calculate_resting_value(stock.stock_id)
            stock.value += (stock.resting_value - stock.value) * 0.01

            # 4. Apply centered random value fluctuation: value += 3 * random[-1, 1]^11
            val_fluct = self.rng.uniform(-1, 1)
            stock.value += 3 * (val_fluct ** 11)

            # 5. Random delta/value fluctuations
            stock.delta += self.rng.uniform(-0.05, 0.05)

            if self.rng.random() < 0.15:
                stock.value += self.rng.uniform(-1.5, 1.5)

            if self.rng.random() < 0.03:
                stock.value += self.rng.uniform(aura.value_fluctuation_range[0], aura.value_fluctuation_range[1])

            if self.rng.random() < 0.10:
                stock.delta += self.rng.uniform(aura.delta_fluctuation_range[0], aura.delta_fluctuation_range[1])

            # 6. Mode-specific rules
            self.apply_mode_rules(stock, aura)

            # 7. Handle mode duration
            stock.mode_duration -= 1
            if stock.mode_duration <= 0:
                stock.mode = self.select_new_mode(stock.mode)
                stock.mode_duration = self.get_new_mode_duration()

            # 9. Value floor / low-price correction / market-cap damping
            # Hard floor
            if stock.value < 1.0:
                stock.value = 1.0

            # Low-price correction
            if stock.value < 5.0:
                stock.value += (5.0 - stock.value) / 2.0
                if stock.delta < 0:
                    stock.delta *= 0.95 # Wiki says "decreased by an additional 5%", assuming multiplicative decay

            # Market cap damping
            if stock.value > market_cap:
                if stock.delta > 0:
                    stock.delta *= 0.90 # "decreased by an additional 10%"

    def apply_mode_rules(self, stock: StockState, aura):
        if stock.mode == MarketMode.STABLE:
            stock.delta *= 0.95
            stock.delta += self.rng.uniform(-0.025, 0.025)
        elif stock.mode == MarketMode.SLOW_RISE:
            stock.delta *= 0.99
            stock.delta += self.rng.uniform(-0.005, 0.045)
        elif stock.mode == MarketMode.SLOW_FALL:
            stock.delta *= 0.99
            stock.delta += self.rng.uniform(-0.045, 0.005)
        elif stock.mode == MarketMode.FAST_RISE:
            stock.value += self.rng.uniform(0, 5)
            stock.delta += self.rng.uniform(-0.015, 0.135)
            if self.rng.random() < 0.30:
                stock.value += self.rng.uniform(-7, 3)
                stock.delta += self.rng.uniform(-0.05, 0.05)
            if self.rng.random() < 0.03:
                stock.mode = MarketMode.FAST_FALL
        elif stock.mode == MarketMode.FAST_FALL:
            stock.value += self.rng.uniform(-5, 0)
            stock.delta += self.rng.uniform(-0.135, 0.015)
            if self.rng.random() < 0.30:
                stock.value += self.rng.uniform(-3, 7)
                stock.delta += self.rng.uniform(-0.05, 0.05)
        elif stock.mode == MarketMode.CHAOTIC:
            stock.delta += self.rng.uniform(-0.15, 0.15)
            if self.rng.random() < 0.50:
                stock.value += self.rng.uniform(-5, 5)
            if self.rng.random() < 0.20:
                stock.delta = self.rng.uniform(aura.chaotic_override_range[0], aura.chaotic_override_range[1])

    def trigger_instant_mode_change(self):
        globD = self.rng.uniform(-1, 1)
        for stock in self.stocks:
            if self.rng.random() < 0.25:
                stock.mode = self.select_new_mode(stock.mode)
                stock.mode_duration = self.get_new_mode_duration()

                # value += -globD * (2 + 7 * random[0,1]^3 + 7 * delta * random[0,1]^3)
                r1 = self.rng.random() ** 3
                r2 = self.rng.random() ** 3
                stock.value += -globD * (2 + 7 * r1 + 7 * stock.delta * r2)

                # delta += globD * random[1,5]
                stock.delta += globD * self.rng.uniform(1, 5)
