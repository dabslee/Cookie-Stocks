from typing import Dict
from .constants import OFFICE_LEVELS
from .config import MarketConfig

class WarehouseManager:
    @staticmethod
    def calculate_capacity(stock_id: int, building_name: str, config: MarketConfig) -> int:
        highest_owned = config.highest_buildings_owned.get(building_name, 0)
        building_level = config.building_levels.get(building_name, 1)
        office = OFFICE_LEVELS[config.office_level]

        # Base capacity = highest owned (with 50% bonus if office level 5+) + 10 * building level
        base_shares = highest_owned
        if office.has_multiplier:
            base_shares = int(base_shares * 1.5)

        capacity = base_shares + 10 * building_level

        # Additive office bonuses (Level 1-4)
        capacity += office.warehouse_bonus

        return capacity

    @staticmethod
    def get_max_brokers(config: MarketConfig) -> int:
        highest_grandmas = config.highest_buildings_owned.get("Grandma", 0)
        grandma_level = config.building_levels.get("Grandma", 1)
        # highest number of grandmas owned this run divided by 10, plus grandma level
        return (highest_grandmas // 10) + grandma_level
