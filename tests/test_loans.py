import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.cookieclicker_stockmarket_sim.loans import LoanManager
from src.cookieclicker_stockmarket_sim.constants import LOANS

class TestLoans(unittest.TestCase):
    def test_loan_activation(self):
        manager = LoanManager()
        current_bank = 1000.0

        # Activate Loan 1
        downpayment = manager.activate_loan(1, current_bank)
        self.assertEqual(downpayment, 200.0)
        self.assertTrue(manager.loans[1].active)
        self.assertEqual(manager.loans[1].bonus_remaining, LOANS[1].bonus_duration)

    def test_loan_cps_multiplier(self):
        manager = LoanManager()
        manager.activate_loan(1, 1000.0)
        # Bonus is +50%
        self.assertEqual(manager.get_cps_multiplier(), 1.5)

        # Tick until bonus expires
        for _ in range(LOANS[1].bonus_duration):
            manager.tick()

        # Should now be in penalty (-75%)
        self.assertEqual(manager.get_cps_multiplier(), 0.25)

if __name__ == "__main__":
    unittest.main()
