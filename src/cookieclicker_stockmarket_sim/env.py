import gymnasium as gym
from gymnasium import spaces
import numpy as np
from typing import Dict, Tuple, Any, Optional

from .engine import StockMarketEngine
from .portfolio import Portfolio
from .config import MarketConfig
from .office import WarehouseManager
from .brokers import BrokerManager
from .loans import LoanManager
from .constants import STOCKS_METADATA, LOANS
from .types import MarketObservation

class CookieClickerStockMarketEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, config: MarketConfig = MarketConfig()):
        super().__init__()
        self.config = config
        self.engine = StockMarketEngine(config)
        self.portfolio = Portfolio(config.starting_cash)
        self.loan_manager = LoanManager()
        self.tick_count = 0

        num_stocks = len(STOCKS_METADATA)

        # Action space:
        # For each stock: 0=Hold, 1=Buy Max, 2=Sell Max
        # This is a simplified action space.
        # Better: Discrete actions for buy/sell per stock, or continuous.
        # User requested: buy(stock_id, shares), sell(stock_id, shares), hold, etc.
        # To make it Gymnasium compatible, we'll use a MultiDiscrete or a Dict space.
        # Let's use MultiDiscrete for simplicity in basic RL: [num_stocks actions]
        # where each action is 0:hold, 1:buy, 2:sell.
        # Plus optional actions for loans (3 slots).
        self.action_space = spaces.Dict({
            "trades": spaces.MultiDiscrete([3] * num_stocks), # 0: hold, 1: buy max, 2: sell max
            "loans": spaces.MultiDiscrete([2] * 3), # 0: do nothing, 1: activate if possible
            "auras": spaces.MultiDiscrete([2, 2]), # [SI, RB] 0: off, 1: on
            "brokers": spaces.Discrete(2), # 0: do nothing, 1: hire one
        })

        # Observation space
        # We will use a Box for numeric values and keep it simple.
        # A more complex Dict space might be better for full info.
        obs_dim = num_stocks * 4 + 10 # prices, resting, holdings, max_shares + cash, etc.
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(obs_dim,), dtype=np.float32)

    def _get_obs(self) -> np.ndarray:
        prices = [s.value for s in self.engine.stocks]
        resting = [s.resting_value for s in self.engine.stocks]
        holdings = [float(s.shares_owned) for s in self.engine.stocks]
        max_shares = [float(s.max_shares) for s in self.engine.stocks]

        other_stats = [
            self.portfolio.cash,
            float(self.config.broker_count),
            BrokerManager.calculate_overhead(self.config.broker_count),
            float(self.config.office_level),
            float(self.config.bank_level),
            float(self.config.supreme_intellect),
            float(self.config.reality_bending),
            float(self.tick_count),
            self.portfolio.realized_pl,
            self.portfolio.get_portfolio_value(self.engine.stocks)
        ]

        return np.concatenate([prices, resting, holdings, max_shares, other_stats]).astype(np.float32)

    def _get_info(self) -> Dict[str, Any]:
        return {
            "stocks": self.engine.stocks,
            "cash": self.portfolio.cash,
            "broker_count": self.config.broker_count,
            "portfolio_value": self.portfolio.get_portfolio_value(self.engine.stocks),
            "unrealized_pl": self.portfolio.get_unrealized_pl(self.engine.stocks),
            "realized_pl": self.portfolio.realized_pl,
            "tick": self.tick_count,
            "loan_states": self.loan_manager.loans,
            "overhead": BrokerManager.calculate_overhead(self.config.broker_count)
        }

    def reset(self, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[np.ndarray, Dict]:
        super().reset(seed=seed)
        if seed is not None:
            self.config.seed = seed

        self.engine = StockMarketEngine(self.config)
        self.portfolio = Portfolio(self.config.starting_cash)
        self.loan_manager = LoanManager()
        self.tick_count = 0

        # Update initial capacities
        for stock in self.engine.stocks:
            meta = STOCKS_METADATA[stock.stock_id]
            stock.max_shares = WarehouseManager.calculate_capacity(stock.stock_id, meta.associated_building, self.config)

        return self._get_obs(), self._get_info()

    def step(self, action: Dict[str, Any]) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        # 1. Handle Auras
        if "auras" in action:
            self.config.supreme_intellect = bool(action["auras"][0])
            self.config.reality_bending = bool(action["auras"][1])

        # 2. Handle Brokers
        if action.get("brokers") == 1:
            max_brokers = WarehouseManager.get_max_brokers(self.config)
            if self.config.broker_count < max_brokers:
                from .constants import BROKER_COST
                if self.portfolio.cash >= BROKER_COST:
                    self.portfolio.cash -= BROKER_COST
                    self.config.broker_count += 1

        # 3. Handle Loans
        if "loans" in action:
            for i, act in enumerate(action["loans"]):
                loan_id = i + 1
                if act == 1:
                    downpayment = self.loan_manager.activate_loan(loan_id, self.portfolio.cash)
                    self.portfolio.cash -= downpayment

        # 4. Handle Trades
        overhead = BrokerManager.calculate_overhead(self.config.broker_count)
        if "trades" in action:
            for i, act in enumerate(action["trades"]):
                stock = self.engine.stocks[i]
                if act == 1: # Buy Max
                    self.portfolio.buy_stock(stock, stock.max_shares - stock.shares_owned, overhead)
                elif act == 2: # Sell Max
                    self.portfolio.sell_stock(stock, stock.shares_owned)

        # 5. Engine Tick
        self.engine.tick()
        self.loan_manager.tick()
        self.tick_count += 1

        # Update capacities (in case bank level or office level changed, though usually they are static during a run)
        for stock in self.engine.stocks:
            meta = STOCKS_METADATA[stock.stock_id]
            stock.max_shares = WarehouseManager.calculate_capacity(stock.stock_id, meta.associated_building, self.config)

        obs = self._get_obs()
        reward = self.portfolio.get_portfolio_value(self.engine.stocks) # Simple reward
        terminated = self.tick_count >= self.config.max_ticks
        truncated = False
        info = self._get_info()

        return obs, reward, terminated, truncated, info
