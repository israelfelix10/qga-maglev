from __future__ import annotations

import unittest

import numpy as np

from qga_maglev import decode_binary_parameters, executar_qga_maglev


class DecodeTests(unittest.TestCase):
    def test_binary_extremes_map_to_bounds(self) -> None:
        bounds = [[5.0, 50.0], [1.0, 30.0]]
        lower = decode_binary_parameters([0] * 8, bounds, 4)
        upper = decode_binary_parameters([1] * 8, bounds, 4)
        np.testing.assert_allclose(lower, [5.0, 1.0])
        np.testing.assert_allclose(upper, [50.0, 30.0])

    def test_invalid_chromosome_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            decode_binary_parameters([0, 1], [[0.0, 1.0]], 4)


class ReproducibilityTests(unittest.TestCase):
    @staticmethod
    def fitness(parameters: np.ndarray) -> float:
        return 1.0 / (1.0e-9 + float(np.sum((parameters - 0.4) ** 2)))

    def run_once(self):
        return executar_qga_maglev(
            self.fitness,
            [[0.0, 1.0], [0.0, 1.0]],
            2,
            5,
            8,
            6,
            seed_qga=42,
            verbose=False,
        )

    def test_fixed_seed_repeats_exactly(self) -> None:
        parameters_a, fitness_a, history_a = self.run_once()
        parameters_b, fitness_b, history_b = self.run_once()
        np.testing.assert_array_equal(parameters_a, parameters_b)
        self.assertEqual(fitness_a, fitness_b)
        self.assertEqual(history_a, history_b)
        self.assertEqual(len(history_a), 6)
        np.testing.assert_allclose(
            parameters_a,
            [0.2903225806451613, 0.6129032258064516],
        )
        self.assertAlmostEqual(fitness_a, 17.43468764958754)


if __name__ == "__main__":
    unittest.main()
