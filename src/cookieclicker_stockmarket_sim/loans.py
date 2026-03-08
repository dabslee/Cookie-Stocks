from typing import List, Dict
from .constants import LOANS
from .types import LoanState

class LoanManager:
    def __init__(self):
        self.loans: Dict[int, LoanState] = {
            1: LoanState(1, 0, 0),
            2: LoanState(2, 0, 0),
            3: LoanState(3, 0, 0)
        }

    def activate_loan(self, loan_id: int, current_bank: float) -> float:
        """Returns the downpayment amount."""
        loan_info = LOANS[loan_id]
        loan_state = self.loans[loan_id]

        if loan_state.active or loan_state.penalty_remaining > 0:
            return 0.0 # Cannot activate if already active or in penalty

        loan_state.active = True
        loan_state.bonus_remaining = loan_info.bonus_duration
        loan_state.penalty_remaining = 0

        return current_bank * loan_info.downpayment_percent

    def tick(self):
        for loan_id, state in self.loans.items():
            if state.active:
                if state.bonus_remaining > 0:
                    state.bonus_remaining -= 1

                # Check again because it might have just hit 0
                if state.bonus_remaining == 0:
                    state.active = False
                    state.penalty_remaining = LOANS[loan_id].penalty_duration
            elif state.penalty_remaining > 0:
                state.penalty_remaining -= 1

    def get_cps_multiplier(self) -> float:
        mult = 1.0
        for loan_id, state in self.loans.items():
            info = LOANS[loan_id]
            if state.active and state.bonus_remaining > 0:
                mult += info.cps_bonus
            elif state.penalty_remaining > 0:
                mult += info.cps_penalty
        return max(0.01, mult) # Ensure CpS doesn't go below 1%
