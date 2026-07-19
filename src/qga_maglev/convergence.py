"""PT-BR: Critérios de convergência usados na análise dos históricos.

EN-US: Convergence criteria used to analyze optimization histories.
"""

from __future__ import annotations

from collections.abc import Sequence


def first_generation_within_tolerance(
    objective_history: Sequence[float],
    best_value: float | None = None,
    tolerance_percent: float = 1.0,
) -> int:
    """PT-BR: Retorna a primeira geração dentro da tolerância do melhor valor.

    EN-US: Return the first generation within tolerance of the best value.
    """
    if not objective_history:
        raise ValueError("O histórico não pode ser vazio.")
    if tolerance_percent < 0:
        raise ValueError("A tolerância não pode ser negativa.")

    final_best = min(objective_history) if best_value is None else best_value
    target = final_best * (1.0 + tolerance_percent / 100.0)
    for generation, value in enumerate(objective_history):
        if value <= target:
            return generation
    return len(objective_history) - 1


def estimate_time_by_generation_share(
    total_time_seconds: float,
    convergence_generation: int,
    maximum_generations: int,
) -> float:
    """PT-BR: Aplica o rateio ``t_total * g_conv / G_max`` usado no texto.

    EN-US: Apply the ``t_total * g_conv / G_max`` allocation used in the text.
    """
    if total_time_seconds < 0:
        raise ValueError("O tempo total não pode ser negativo.")
    if maximum_generations <= 0:
        raise ValueError("O número máximo de gerações deve ser positivo.")
    if not 0 <= convergence_generation <= maximum_generations:
        raise ValueError("A geração de convergência está fora do intervalo.")
    return total_time_seconds * convergence_generation / maximum_generations


def estimate_time_including_initial_population(
    total_time_seconds: float,
    convergence_generation: int,
    maximum_generations: int,
) -> float:
    """PT-BR: Rateia também a avaliação da população inicial (geração zero).

    EN-US: Also allocate time to the initial-population evaluation (generation zero).
    """
    if total_time_seconds < 0:
        raise ValueError("O tempo total não pode ser negativo.")
    if maximum_generations <= 0:
        raise ValueError("O número máximo de gerações deve ser positivo.")
    if not 0 <= convergence_generation <= maximum_generations:
        raise ValueError("A geração de convergência está fora do intervalo.")
    return (
        total_time_seconds
        * (convergence_generation + 1)
        / (maximum_generations + 1)
    )
