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

        # Calculate profit relative to start
        start_cash = self.df.iloc[0]["cash"]
        self.df["profit_portfolio"] = self.df["portfolio_value"] - self.df["portfolio_value"].iloc[0]
        self.df["profit_cash"] = self.df["cash"] - self.df["cash"].iloc[0]

    def plot_portfolio_value(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df["tick"], self.df["profit_portfolio"], label="Total Profit (Portfolio)")
        plt.plot(self.df["tick"], self.df["profit_cash"], label="Cash Profit", alpha=0.7)
        plt.title("Profit Over Time")
        plt.xlabel("Tick")
        plt.ylabel("Profit ($)")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(self.output_dir, "profit_over_time.png"))
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
            stock_ids = list(range(len(STOCKS_METADATA)))

        plt.figure(figsize=(12, 8))

        labels = [STOCKS_METADATA[sid].name for sid in stock_ids]
        data = [self.df[f"stock_{sid}_shares"] for sid in stock_ids]

        plt.stackplot(self.df["tick"], data, labels=labels, alpha=0.8)

        plt.title("Stacked Stock Holdings Over Time")
        plt.xlabel("Tick")
        plt.ylabel("Total Shares")
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize='small')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "holdings_stacked.png"))
        plt.close()

    def plot_all(self):
        self.plot_portfolio_value()
        self.plot_stock_prices()
        self.plot_holdings()
