from math import nan
import unittest

from procurement import ControllerParameters, update_posted_price


class ProcurementControllerTests(unittest.TestCase):
    def test_shortage_raises_price_with_bounded_step(self) -> None:
        parameters = ControllerParameters(kappa=1.0, max_step=0.1)
        self.assertAlmostEqual(update_posted_price(10, 50, 100, parameters), 11)

    def test_surplus_lowers_price_with_bounded_step(self) -> None:
        parameters = ControllerParameters(kappa=1.0, max_step=0.2)
        self.assertAlmostEqual(update_posted_price(10, 200, 100, parameters), 8)

    def test_target_supply_leaves_price_unchanged(self) -> None:
        parameters = ControllerParameters(kappa=0.5, max_step=0.1)
        self.assertAlmostEqual(update_posted_price(10, 100, 100, parameters), 10)

    def test_absolute_floor_and_ceiling_apply(self) -> None:
        parameters = ControllerParameters(
            kappa=1.0, max_step=1.0, floor=9.0, ceiling=10.5
        )
        self.assertAlmostEqual(update_posted_price(10, 0, 100, parameters), 10.5)
        self.assertAlmostEqual(update_posted_price(10, 300, 100, parameters), 9.0)

    def test_invalid_inputs_are_rejected(self) -> None:
        parameters = ControllerParameters(kappa=1.0, max_step=0.1)
        with self.assertRaises(ValueError):
            update_posted_price(10, 1, 0, parameters)
        with self.assertRaises(ValueError):
            update_posted_price(10, -1, 1, parameters)
        with self.assertRaises(ValueError):
            update_posted_price(10, 1, 1, ControllerParameters(-1, 0.1))
        with self.assertRaises(ValueError):
            update_posted_price(10, 1, 1, ControllerParameters(1, 0.1, ceiling=nan))


if __name__ == "__main__":
    unittest.main()
