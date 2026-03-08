from typing import List, Dict
from .types import StockState
from .brokers import BrokerManager

class Portfolio:
    def __init__(self, starting_cash: float):
        self.cash = starting_cash
        self.realized_pl = 0.0
        self.total_fees_paid = 0.0

    def buy_stock(self, stock: StockState, shares: int, overhead: float) -> bool:
        if shares <= 0:
            return False

        max_buyable = stock.max_shares - stock.shares_owned
        shares_to_buy = min(shares, max_buyable)

        if shares_to_buy <= 0:
            return False

        buy_price = BrokerManager.get_buy_price(stock.value, overhead)
        total_cost = shares_to_buy * buy_price

        if total_cost > self.cash:
            # Optionally buy as many as possible
            shares_to_buy = int(self.cash // buy_price)
            if shares_to_buy <= 0:
                return False
            total_cost = shares_to_buy * buy_price

        # Update average cost basis
        old_total_cost = stock.shares_owned * stock.average_cost_basis
        new_total_cost = old_total_cost + (shares_to_buy * buy_price)
        stock.shares_owned += shares_to_buy
        stock.average_cost_basis = new_total_cost / stock.shares_owned

        self.cash -= total_cost
        self.total_fees_paid += shares_to_buy * stock.value * overhead
        return True

    def sell_stock(self, stock: StockState, shares: int) -> bool:
        if shares <= 0 or stock.shares_owned <= 0:
            return False

        shares_to_sell = min(shares, stock.shares_owned)
        sell_price = BrokerManager.get_sell_price(stock.value)
        revenue = shares_to_sell * sell_price

        # Calculate realized P/L
        profit = shares_to_sell * (sell_price - stock.average_cost_basis)
        self.realized_pl += profit

        stock.shares_owned -= shares_to_sell
        if stock.shares_owned == 0:
            stock.average_cost_basis = 0.0

        self.cash += revenue
        return True

    def get_unrealized_pl(self, stocks: List[StockState]) -> float:
        unrealized = 0.0
        for stock in stocks:
            if stock.shares_owned > 0:
                unrealized += stock.shares_owned * (stock.value - stock.average_cost_basis)
        return unrealized

    def get_portfolio_value(self, stocks: List[StockState]) -> float:
        equity = sum(s.shares_owned * s.value for s in stocks)
        return self.cash + equity
