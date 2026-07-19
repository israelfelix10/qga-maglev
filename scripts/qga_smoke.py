"""PT-BR: Executa um teste curto e determinístico da implementação do QGA.

EN-US: Run a short, deterministic smoke test of the QGA implementation.
"""

from __future__ import annotations

import argparse

import numpy as np

from qga_maglev import executar_qga_maglev


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def fitness(parameters: np.ndarray) -> float:
    """PT-BR: Maximiza o inverso da distância ao ponto (0,25; 0,75).

    EN-US: Maximize the inverse distance to the point (0.25, 0.75).
    """
    target = np.array([0.25, 0.75])
    return 1.0 / (1.0e-9 + float(np.sum((parameters - target) ** 2)))


if __name__ == "__main__":
    args = parse_args()
    parameters, best, history = executar_qga_maglev(
        fitness,
        [[0.0, 1.0], [0.0, 1.0]],
        2,
        8,
        12,
        10,
        seed_qga=args.seed,
    )
    print(f"Gerações registradas: {len(history)}")
    print(f"Melhores parâmetros: {np.round(parameters, 6)}")
    print(f"Aptidão: {best:.6e}")
