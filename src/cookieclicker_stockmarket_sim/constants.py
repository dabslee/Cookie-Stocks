from typing import Dict, List, NamedTuple, Tuple

# Stock metadata
class StockMetadata(NamedTuple):
    stock_id: int
    name: str
    symbol: str
    associated_building: str

STOCKS_METADATA = [
    StockMetadata(0, "Cereals", "CRL", "Farm"),
    StockMetadata(1, "Chocolate", "CHC", "Mine"),
    StockMetadata(2, "Butter", "BTR", "Factory"),
    StockMetadata(3, "Sugar", "SUG", "Bank"),
    StockMetadata(4, "Nuts", "NUT", "Temple"),
    StockMetadata(5, "Salt", "SLT", "Wizard Tower"),
    StockMetadata(6, "Vanilla", "VNL", "Shipment"),
    StockMetadata(7, "Eggs", "EGG", "Alchemy Lab"),
    StockMetadata(8, "Cinnamon", "CNM", "Portal"),
    StockMetadata(9, "Cream", "CRM", "Time Machine"),
    StockMetadata(10, "Jam", "JAM", "Antimatter Condenser"),
    StockMetadata(11, "White chocolate", "WCH", "Prism"),
    StockMetadata(12, "Honey", "HNY", "Chancemaker"),
    StockMetadata(13, "Cookies", "CKI", "Fractal Engine"),
    StockMetadata(14, "Recipes", "RCP", "Javascript Console"),
    StockMetadata(15, "Subsidiaries", "SBD", "Idleverse"),
    StockMetadata(16, "Publicists", "PBL", "Cortex Baker"),
    StockMetadata(17, "[Name of Bakery]", "YOU", "You"),
]

# Office levels
class OfficeInfo(NamedTuple):
    level: int
    name: str
    warehouse_bonus: int
    loan_slots: int
    has_multiplier: bool = False
    cursor_requirement: int = 0
    cursor_level_requirement: int = 0

OFFICE_LEVELS = {
    1: OfficeInfo(1, "Credit garage", 25, 0, False, 100, 2),
    2: OfficeInfo(2, "Tiny bank", 50, 1, False, 200, 4),
    3: OfficeInfo(3, "Loaning company", 75, 1, False, 350, 8),
    4: OfficeInfo(4, "Finance headquarters", 100, 2, False, 500, 10),
    5: OfficeInfo(5, "International exchange", 0, 3, True, 700, 12),
    6: OfficeInfo(6, "Palace of Greed", 0, 3, True, 0, 0), # Final level
}

# Loans
class LoanInfo(NamedTuple):
    id: int
    name: str
    cps_bonus: float
    bonus_duration: int # in ticks
    cps_penalty: float
    penalty_duration: int # in ticks
    downpayment_percent: float

LOANS = {
    1: LoanInfo(1, "Modest loan", 0.50, 2 * 60, -0.75, 4 * 60, 0.20),
    2: LoanInfo(2, "Pawnshop loan", 1.00, 40 // 60, -0.90, 40, 0.40), # 40 seconds is < 1 tick. Wiki says 40 seconds, then 40 minutes penalty.
    3: LoanInfo(3, "Retirement loan", 0.20, 2 * 24 * 60, -0.20, 5 * 24 * 60, 0.50),
}
# Correction for Loan 2: 40 seconds bonus is very short.
# "The listed loan effects pause when exiting the game in the real game."
# 40 seconds = 0.666 ticks. Let's round or handle fractional ticks if needed,
# but per-tick engine usually means 1 tick is the minimum.
# Actually, the user says "1 tick = 1 minute". So 40 seconds is slightly less than 1 tick.

# Dragon Auras
class AuraEffect(NamedTuple):
    delta_decay: float
    value_fluctuation_range: Tuple[float, float]
    delta_fluctuation_range: Tuple[float, float]
    chaotic_override_range: Tuple[float, float]
    max_mode_duration: int
    bypass_to_chaotic_chance: float
    instant_mode_change_chance: float

AURA_EFFECTS = {
    "Base": AuraEffect(0.97, (-5, 5), (-0.15, 0.15), (-1, 1), 700, 0.0, 0.10),
    "Supreme Intellect": AuraEffect(0.98, (-10, 10), (-0.25, 0.25), (-4, 4), 500, 0.5, 0.20),
    "Reality Bending": AuraEffect(0.971, (-5.5, 5.5), (-0.16, 0.16), (-1.3, 1.3), 680, 0.05, 0.11),
    "Both": AuraEffect(0.981, (-10.5, 10.5), (-0.26, 0.26), (-4.3, 4.3), 480, 0.5, 0.21),
}

# Mode selection probabilities
MODE_PROBABILITIES = [0.125, 0.25, 0.25, 0.125, 0.125, 0.125]

# Costs
BROKER_COST = 1200.0
