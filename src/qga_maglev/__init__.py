"""PT-BR: Utilitários para os experimentos QGA aplicados ao sistema MAGLEV.

EN-US: Utilities for QGA experiments applied to the MAGLEV system.
"""

from .convergence import (
    estimate_time_by_generation_share,
    estimate_time_including_initial_population,
    first_generation_within_tolerance,
)
from .qga import decode_binary_parameters, executar_qga_maglev

__all__ = [
    "decode_binary_parameters",
    "estimate_time_by_generation_share",
    "estimate_time_including_initial_population",
    "executar_qga_maglev",
    "first_generation_within_tolerance",
]
