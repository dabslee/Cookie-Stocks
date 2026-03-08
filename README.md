# Cookie Clicker Stock Market Simulator

This repository contains a faithful Python replication of the Cookie Clicker Stock Market minigame engine. It is designed for simulation, backtesting, and strategy benchmarking.

## Features

- **Exact Engine Logic**: Implements the per-tick price update formulas, including all 6 market modes (Stable, Slow Rise, Slow Fall, Fast Rise, Fast Fall, Chaotic).
- **Infinite Liquidity**: Assumes infinite bank balance for trading and system upgrades. All values are in **$**.
- **Comprehensive Systems**: Includes Warehouse capacity (based on office upgrades and building levels), Broker overhead, and Dragon Auras (Supreme Intellect and Reality Bending).
- **Gymnasium Environment**: A `gym`-compatible interface for reinforcement learning or heuristic strategies.
- **Analytics & Plotting**: Built-in tools to record simulation data, including actions taken and system status. Generates profit curves and stacked holdings charts.
- **Benchmarking**: Scripts to compare multiple strategies across multiple trials with progress tracking.

## Installation

```bash
pip install -r requirements.txt
```

## Project Structure

- `src/cookieclicker_stockmarket_sim/`: Core engine and environment code.
  - `engine.py`: Price movement and mode logic.
  - `env.py`: Gymnasium environment wrapper.
  - `portfolio.py`: Tracking profit and shares with infinite money.
- `strategies/`: Heuristic trading strategies.
  - `deep_discount_mean_reversion.py`: Advanced heuristic strategy.
- `scripts/`: Run simulations and benchmarks.
  - `run_single.py`: Run one simulation with plots and detailed tick logs.
  - `run_benchmark.py`: Compare multiple strategies with tqdm progress bars.
- `tests/`: Unit tests for critical formulas.

## Usage

### Run a Single Simulation

```bash
python scripts/run_single.py --strategy deep_discount --ticks 5000 --seed 42
```

Results (plots and CSV including actions) will be saved in `results/single_runs/`.

### Run Benchmarks

```bash
python scripts/run_benchmark.py --strategies deep_discount buy_at_one naive_reversion --trials 50 --ticks 10000
```

Summary results will be printed and saved in `results/benchmarks/`.

## Implementation Details

- **Tick Rate**: 1 tick = 1 minute.
- **Resting Value**: `10 * (id + 1) + bank_level - 1`.
- **Market Cap**: `100 + 3 * (bank_level - 1)`.
- **Overhead**: `20% * (0.95 ^ brokers)`.
- **Capacity**: `(highest_owned * (1.5 if office_level >= 5 else 1.0)) + 10 * building_level + office_bonus`.
