import argparse
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.env import CookieClickerStockMarketEnv
from src.cookieclicker_stockmarket_sim.config import MarketConfig
from src.cookieclicker_stockmarket_sim.analytics import MarketAnalytics
from src.cookieclicker_stockmarket_sim.plots import MarketPlotter
from strategies import DeepDiscountMeanReversion, BuyAtOne, NaiveMeanReversion, RandomStrategy, ThresholdStrategy

STRATEGIES = {
    "deep_discount": DeepDiscountMeanReversion,
    "buy_at_one": BuyAtOne,
    "naive_reversion": NaiveMeanReversion,
    "random": lambda: RandomStrategy(18),
    "threshold": ThresholdStrategy
}

def main():
    parser = argparse.ArgumentParser(description="Run a single simulation of the Cookie Clicker Stock Market.")
    parser.add_argument("--strategy", type=str, default="deep_discount", choices=STRATEGIES.keys())
    parser.add_argument("--ticks", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--bank-level", type=int, default=10)
    parser.add_argument("--office-level", type=int, default=1)
    parser.add_argument("--si", action="store_true", help="Enable Supreme Intellect")
    parser.add_argument("--rb", action="store_true", help="Enable Reality Bending")
    parser.add_argument("--outdir", type=str, default="results/single_runs")

    args = parser.parse_args()

    config = MarketConfig(
        max_ticks=args.ticks,
        seed=args.seed,
        bank_level=args.bank_level,
        office_level=args.office_level,
        supreme_intellect=args.si,
        reality_bending=args.rb,
        highest_buildings_owned={k: 500 for k in [
            "Grandma", "Farm", "Mine", "Factory", "Bank",
            "Temple", "Wizard Tower", "Shipment", "Alchemy Lab",
            "Portal", "Time Machine", "Antimatter Condenser",
            "Prism", "Chancemaker", "Fractal Engine",
            "Javascript Console", "Idleverse", "Cortex Baker", "You"
        ]}
    )

    env = CookieClickerStockMarketEnv(config)
    strategy = STRATEGIES[args.strategy]()
    analytics = MarketAnalytics()

    obs, info = env.reset(seed=args.seed)
    analytics.record_tick(0, info)

    for t in range(1, args.ticks + 1):
        action = strategy.decide_action(obs, info)
        obs, reward, terminated, truncated, info = env.step(action)
        analytics.record_tick(t, info)
        if terminated or truncated:
            break

    # Save results
    os.makedirs(args.outdir, exist_ok=True)
    df = analytics.get_dataframe()
    analytics.save_csv(os.path.join(args.outdir, f"run_{args.strategy}_seed{args.seed}.csv"))

    plotter = MarketPlotter(df, args.outdir)
    plotter.plot_all()

    print(f"Simulation complete. Final portfolio value: {info['portfolio_value']:.2f}")
    print(f"Results saved to {args.outdir}")

if __name__ == "__main__":
    main()
