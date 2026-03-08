import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import List
from .constants import STOCKS_METADATA

class MarketPlotter:
    def __init__(self, df: pd.DataFrame, output_dir: str):
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def plot_portfolio_value(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df["tick"], self.df["portfolio_value"], label="Portfolio Value")
        plt.plot(self.df["tick"], self.df["cash"], label="Cash", alpha=0.7)
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Tick")
        plt.ylabel("Cookies")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.output_dir, "portfolio_value.png"))
        plt.close()

    def plot_stock_prices(self, stock_ids: List[int] = None):
        if stock_ids is None:
            stock_ids = [0, 1, 2, 3] # Plot first few by default

        plt.figure(figsize=(12, 8))
        for sid in stock_ids:
            name = STOCKS_METADATA[sid].name
            plt.plot(self.df["tick"], self.df[f"stock_{sid}_price"], label=f"{name} Price")
            plt.plot(self.df["tick"], self.df[f"stock_{sid}_resting"], linestyle="--", alpha=0.5, label=f"{name} Resting")

        plt.title("Stock Prices vs Resting Values")
        plt.xlabel("Tick")
        plt.ylabel("Price ($)")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.output_dir, "stock_prices.png"))
        plt.close()

    def plot_holdings(self, stock_ids: List[int] = None):
        if stock_ids is None:
            stock_ids = [0, 1, 2, 3]

        plt.figure(figsize=(12, 8))
        for sid in stock_ids:
            name = STOCKS_METADATA[sid].name
            plt.fill_between(self.df["tick"], self.df[f"stock_{sid}_shares"], label=f"{name} Shares", alpha=0.3)

        plt.title("Stock Holdings Over Time")
        plt.xlabel("Tick")
        plt.ylabel("Shares")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.output_dir, "holdings.png"))
        plt.close()

    def plot_all(self):
        self.plot_portfolio_value()
        self.plot_stock_prices()
        self.plot_holdings()
