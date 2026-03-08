import argparse
import os
import sys
import pandas as pd
import numpy as np
from tqdm import tqdm

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.env import CookieClickerStockMarketEnv
from src.cookieclicker_stockmarket_sim.config import MarketConfig
from strategies import DeepDiscountMeanReversion, BuyAtOne, NaiveMeanReversion, RandomStrategy, ThresholdStrategy

STRATEGIES = {
    "deep_discount": DeepDiscountMeanReversion,
    "buy_at_one": BuyAtOne,
    "naive_reversion": NaiveMeanReversion,
    "random": lambda: RandomStrategy(18),
    "threshold": ThresholdStrategy
}

def run_trial(strategy_name, config, seed):
    env = CookieClickerStockMarketEnv(config)
    strategy = STRATEGIES[strategy_name]()
    obs, info = env.reset(seed=seed)

    total_overhead = 0
    num_trades = 0

    for _ in range(config.max_ticks):
        action = strategy.decide_action(obs, info)

        # Track trades for analytics
        trades = action.get("trades", [])
        for t in trades:
            if t != 0:
                num_trades += 1

        obs, reward, terminated, truncated, info = env.step(action)
        if terminated or truncated:
            break

    return {
        "strategy": strategy_name,
        "seed": seed,
        "final_value": info["portfolio_value"],
        "realized_pl": info["realized_pl"],
        "unrealized_pl": info["unrealized_pl"],
        "total_fees": info["total_fees"],
        "num_trades": num_trades
    }

def main():
    parser = argparse.ArgumentParser(description="Benchmark multiple strategies head-to-head.")
    parser.add_argument("--strategies", nargs="+", default=list(STRATEGIES.keys()))
    parser.add_argument("--trials", type=int, default=10)
    parser.add_argument("--ticks", type=int, default=2000)
    parser.add_argument("--bank-level", type=int, default=10)
    parser.add_argument("--outdir", type=str, default="results/benchmarks")

    args = parser.parse_args()

    results = []

    for strat_name in args.strategies:
        print(f"Running benchmark for {strat_name}...")
        for i in tqdm(range(args.trials), desc=f"Trial Progress"):
            seed = 1000 + i
            config = MarketConfig(
                max_ticks=args.ticks,
                bank_level=args.bank_level,
                highest_buildings_owned={k: 500 for k in [
                    "Grandma", "Farm", "Mine", "Factory", "Bank",
                    "Temple", "Wizard Tower", "Shipment", "Alchemy Lab",
                    "Portal", "Time Machine", "Antimatter Condenser",
                    "Prism", "Chancemaker", "Fractal Engine",
                    "Javascript Console", "Idleverse", "Cortex Baker", "You"
                ]}
            )
            res = run_trial(strat_name, config, seed)
            results.append(res)

    df = pd.DataFrame(results)
    os.makedirs(args.outdir, exist_ok=True)
    df.to_csv(os.path.join(args.outdir, "benchmark_results.csv"), index=False)

    summary = df.groupby("strategy").agg({
        "final_value": ["mean", "std", "median"],
        "realized_pl": ["mean"],
        "total_fees": ["mean"],
        "num_trades": ["mean"]
    })

    print("\nBenchmark Summary:")
    print(summary)
    summary.to_csv(os.path.join(args.outdir, "benchmark_summary.csv"))

if __name__ == "__main__":
    main()
