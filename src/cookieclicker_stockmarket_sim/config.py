from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class MarketConfig:
    bank_level: int = 1
    office_level: int = 1
    supreme_intellect: bool = False
    reality_bending: bool = False

    # Building stats for capacity and brokers
    # Keys are building names like "Farm", "Mine", "Grandma"
    highest_buildings_owned: Dict[str, int] = field(default_factory=lambda: {
        "Grandma": 0, "Farm": 0, "Mine": 0, "Factory": 0, "Bank": 0,
        "Temple": 0, "Wizard Tower": 0, "Shipment": 0, "Alchemy Lab": 0,
        "Portal": 0, "Time Machine": 0, "Antimatter Condenser": 0,
        "Prism": 0, "Chancemaker": 0, "Fractal Engine": 0,
        "Javascript Console": 0, "Idleverse": 0, "Cortex Baker": 0, "You": 0
    })

    building_levels: Dict[str, int] = field(default_factory=lambda: {
        "Grandma": 1, "Farm": 1, "Mine": 1, "Factory": 1, "Bank": 1,
        "Temple": 1, "Wizard Tower": 1, "Shipment": 1, "Alchemy Lab": 1,
        "Portal": 1, "Time Machine": 1, "Antimatter Condenser": 1,
        "Prism": 1, "Chancemaker": 1, "Fractal Engine": 1,
        "Javascript Console": 1, "Idleverse": 1, "Cortex Baker": 1, "You": 1
    })

    starting_cash: float = 1000.0
    broker_count: int = 0

    # Simulation settings
    max_ticks: int = 10000
    seed: Optional[int] = None

    # Full information in observations
    include_deltas: bool = True
    include_modes: bool = True
