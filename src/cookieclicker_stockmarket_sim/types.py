from enum import IntEnum
from dataclasses import dataclass, field
from typing import List, Optional, Dict

class MarketMode(IntEnum):
    STABLE = 0
    SLOW_RISE = 1
    SLOW_FALL = 2
    FAST_RISE = 3
    FAST_FALL = 4
    CHAOTIC = 5

@dataclass
class StockState:
    stock_id: int
    value: float
    delta: float
    mode: MarketMode
    mode_duration: int
    resting_value: float
    max_shares: int
    shares_owned: int = 0
    average_cost_basis: float = 0.0

@dataclass
class MarketObservation:
    prices: List[float]
    resting_values: List[float]
    holdings: List[int]
    max_shares: List[int]
    deltas: Optional[List[float]] = None
    modes: Optional[List[int]] = None
    cash: float = 0.0
    broker_count: int = 0
    overhead: float = 0.0
    office_level: int = 1
    bank_level: int = 1
    supreme_intellect: bool = False
    reality_bending: bool = False
    tick: int = 0
    realized_pl: float = 0.0
    unrealized_pl: float = 0.0
    portfolio_value: float = 0.0
