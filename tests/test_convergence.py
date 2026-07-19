from __future__ import annotations

import unittest

from qga_maglev import (
    estimate_time_by_generation_share,
    estimate_time_including_initial_population,
    first_generation_within_tolerance,
)


class ConvergenceTests(unittest.TestCase):
    def test_first_generation_within_one_percent(self) -> None:
        history = [2.0, 1.2, 1.009, 1.0]
        self.assertEqual(first_generation_within_tolerance(history, 1.0, 1.0), 2)

    def test_rateio_used_in_text(self) -> None:
        total_seconds = 91.4 * 60
        estimated = estimate_time_by_generation_share(total_seconds, 1, 50)
        self.assertAlmostEqual(estimated / 60, 1.828, places=3)

    def test_initial_population_estimate_is_distinct(self) -> None:
        total_seconds = 91.4 * 60
        estimated = estimate_time_including_initial_population(
            total_seconds, 1, 50
        )
        self.assertAlmostEqual(estimated / 60, 3.584313725, places=6)


if __name__ == "__main__":
    unittest.main()

