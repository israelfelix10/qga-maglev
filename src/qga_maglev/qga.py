# SPDX-FileCopyrightText: 2016 ResearchCodesHub
# SPDX-FileCopyrightText: 2026 Israel da Silva Felix de Lima
# SPDX-License-Identifier: MIT

"""PT-BR: Algoritmo genético de inspiração quântica dos experimentos MAGLEV.

Este módulo preserva a dinâmica numérica da implementação adaptada utilizada na
dissertação: indexação interna iniciada em 1, medição por limiar fixo, rotação
arredondada para duas casas e memória explícita do melhor indivíduo global.

Origem e licença (PT-BR)
------------------------
A implementação contém trechos modificados do ``QUANTUM GENETIC ALGORITHM`` de
R. Lahoz-Beltra (24/05/2016), publicado pelo ResearchCodesHub sob licença MIT,
na revisão ``d20ad57f0a2576a6c48d8c8c4f7870a6192275e8``. O copyright de 2016,
a licença upstream e o aviso original estão preservados em ``LICENSES``. As
modificações deste repositório são distribuídas sob a licença MIT da raiz, sem
remover os direitos e avisos da implementação upstream.

EN-US: Quantum-inspired genetic algorithm used in the MAGLEV experiments.

This module preserves the numerical behavior of the adapted implementation
used in the dissertation: one-based internal indexing, fixed-threshold
measurement, rotation rounded to two decimal places, and explicit memory of
the global-best individual.

Origin and license (EN-US)
--------------------------
The implementation contains modified portions of R. Lahoz-Beltra's ``QUANTUM
GENETIC ALGORITHM`` (May 24, 2016), published by ResearchCodesHub under the MIT
License at revision ``d20ad57f0a2576a6c48d8c8c4f7870a6192275e8``. The 2016
copyright, upstream license, and original notice are preserved in
``LICENSES``. Modifications in this repository are distributed under the root
MIT License without removing the rights and notices that apply to the upstream
implementation.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from typing import Any

import numpy as np
from numpy.typing import NDArray


FitnessFunction = Callable[[NDArray[np.float64]], float]

# PT-BR: O estado interno é mantido em nível de módulo para preservar a
# interface e o comportamento da versão empregada nos experimentos.
# EN-US: Module-level internal state is retained to preserve the interface and
# behavior of the version used in the experiments.
N = 50
Genome = 4
generation_max = 450
popSize = N + 1
genomeLength = Genome + 1

MAGLEV_EXTERNAL_FITNESS_FUNC: FitnessFunction | None = None
MAGLEV_VAR_BOUNDS: NDArray[np.float64] | None = None
MAGLEV_BITS_PER_PARAM = 0
MAGLEV_NUM_PARAMS = 0

fitness: NDArray[np.float64]
qpv: NDArray[np.float64]
nqpv: NDArray[np.float64]
chromosome: NDArray[np.int_]
best_chrom: NDArray[np.int_]


def _allocate_state() -> None:
    """PT-BR: Aloca vetores com a indexação 1..N da implementação-base.

    EN-US: Allocate arrays using the base implementation's 1..N indexing.
    """
    global fitness, qpv, nqpv, chromosome, best_chrom

    fitness = np.empty(popSize, dtype=float)
    qpv = np.empty((popSize, genomeLength, 3), dtype=float)
    nqpv = np.empty((popSize, genomeLength, 3), dtype=float)
    chromosome = np.empty((popSize, genomeLength), dtype=np.int_)
    best_chrom = np.empty(generation_max, dtype=np.int_)


_allocate_state()


def decode_maglev_chromosome(
    binary_chromosome: Sequence[int] | NDArray[np.int_],
) -> NDArray[np.float64]:
    """PT-BR: Decodifica um cromossomo nos limites reais de cada parâmetro.

    EN-US: Decode a binary chromosome into each parameter's real bounds.
    """
    if MAGLEV_VAR_BOUNDS is None:
        raise RuntimeError("Os limites das variáveis ainda não foram configurados.")
    if MAGLEV_BITS_PER_PARAM <= 0 or MAGLEV_NUM_PARAMS <= 0:
        raise RuntimeError("A codificação do cromossomo ainda não foi configurada.")

    return decode_binary_parameters(
        binary_chromosome,
        MAGLEV_VAR_BOUNDS,
        MAGLEV_BITS_PER_PARAM,
        start_index=1,
    )


def decode_binary_parameters(
    binary_chromosome: Sequence[int] | NDArray[np.int_],
    variable_bounds: Sequence[Sequence[float]],
    bits_per_parameter: int,
    *,
    start_index: int = 0,
) -> NDArray[np.float64]:
    """PT-BR: Converte blocos binários em valores reais por interpolação linear.

    EN-US: Convert binary blocks into real values through linear interpolation.
    """
    bounds = np.asarray(variable_bounds, dtype=float)
    if bounds.ndim != 2 or bounds.shape[1] != 2:
        raise ValueError("variable_bounds deve ter formato (n, 2).")
    if bits_per_parameter <= 0:
        raise ValueError("bits_per_parameter deve ser positivo.")

    expected_bits = bounds.shape[0] * bits_per_parameter
    available_bits = len(binary_chromosome) - start_index
    if available_bits < expected_bits:
        raise ValueError(
            f"Cromossomo possui {available_bits} bits úteis; "
            f"eram esperados {expected_bits}."
        )

    decoded: list[float] = []
    max_integer = (2**bits_per_parameter) - 1
    start = start_index
    for lower, upper in bounds:
        stop = start + bits_per_parameter
        integer_value = int("".join(map(str, binary_chromosome[start:stop])), 2)
        value = lower + (integer_value / max_integer) * (upper - lower)
        decoded.append(float(value))
        start = stop
    return np.asarray(decoded, dtype=float)


def _initialize_population() -> None:
    """PT-BR: Inicializa os pares de amplitudes conforme a implementação original.

    EN-US: Initialize amplitude pairs according to the original implementation.
    """
    hadamard = np.array(
        [[1 / math.sqrt(2.0), 1 / math.sqrt(2.0)],
         [1 / math.sqrt(2.0), -1 / math.sqrt(2.0)]]
    )
    qubit_zero = np.array([1.0, 0.0])
    amplitudes_h = hadamard @ qubit_zero

    for individual in range(1, popSize):
        for gene in range(1, genomeLength):
            theta = math.radians(np.random.uniform(0.0, 1.0) * 90.0)
            rotation = np.array(
                [[math.cos(theta), -math.sin(theta)],
                 [math.sin(theta), math.cos(theta)]]
            )
            alpha, beta = rotation @ amplitudes_h

            # PT-BR: O fator 2 e o arredondamento pertencem à implementação avaliada.
            # EN-US: The factor of 2 and rounding belong to the evaluated implementation.
            qpv[individual, gene, 0] = np.around(2 * alpha**2, 2)
            qpv[individual, gene, 1] = np.around(2 * beta**2, 2)


def _measure(alpha_threshold: float) -> None:
    """PT-BR: Obtém cromossomos clássicos usando o limiar fixo informado.

    EN-US: Obtain classical chromosomes using the specified fixed threshold.
    """
    for individual in range(1, popSize):
        for gene in range(1, genomeLength):
            chromosome[individual, gene] = int(
                alpha_threshold > qpv[individual, gene, 0]
            )


def _evaluate_population(generation_index: int) -> None:
    """PT-BR: Avalia a população e registra o índice do melhor da geração.

    EN-US: Evaluate the population and record the generation-best index.
    """
    if MAGLEV_EXTERNAL_FITNESS_FUNC is None:
        raise RuntimeError("A função de aptidão não foi configurada.")

    for individual in range(1, N + 1):
        parameters = decode_maglev_chromosome(chromosome[individual])
        fitness[individual] = float(MAGLEV_EXTERNAL_FITNESS_FUNC(parameters))

    best_index = 1
    best_value = fitness[1]
    for individual in range(1, N + 1):
        # PT-BR: O desempate pelo último indivíduo reproduz o operador >= original.
        # EN-US: Selecting the last tied individual reproduces the original >= operator.
        if fitness[individual] >= best_value:
            best_value = fitness[individual]
            best_index = individual

    best_chrom[generation_index] = best_index


def _rotate_population(generation_index: int) -> None:
    """PT-BR: Rotaciona indivíduos piores em direção ao melhor da geração.

    EN-US: Rotate worse individuals toward the generation-best individual.
    """
    best_index = int(best_chrom[generation_index])

    for individual in range(1, N + 1):
        if individual == best_index or fitness[individual] >= fitness[best_index]:
            continue

        for gene in range(1, genomeLength):
            current_bit = chromosome[individual, gene]
            best_bit = chromosome[best_index, gene]

            if current_bit == 0 and best_bit == 1:
                delta_theta = 0.0785398163
            elif current_bit == 1 and best_bit == 0:
                delta_theta = -0.0785398163
            else:
                continue

            cos_theta = math.cos(delta_theta)
            sin_theta = math.sin(delta_theta)
            nqpv[individual, gene, 0] = (
                cos_theta * qpv[individual, gene, 0]
                - sin_theta * qpv[individual, gene, 1]
            )

            alpha = round(nqpv[individual, gene, 0], 2)
            qpv[individual, gene, 0] = max(0.0, min(1.0, alpha))
            qpv[individual, gene, 1] = round(
                1.0 - qpv[individual, gene, 0], 2
            )


def _mutate_population(
    population_mutation_rate: float,
    gene_mutation_rate: float,
) -> None:
    """PT-BR: Aplica a porta Pauli-X trocando as duas amplitudes armazenadas.

    EN-US: Apply the Pauli-X gate by swapping the two stored amplitudes.
    """
    for individual in range(1, N + 1):
        population_draw = np.random.randint(0, 101) / 100.0
        if population_draw > population_mutation_rate:
            continue

        for gene in range(1, genomeLength):
            gene_draw = np.random.randint(0, 101) / 100.0
            if gene_draw <= gene_mutation_rate:
                qpv[individual, gene, 0], qpv[individual, gene, 1] = (
                    qpv[individual, gene, 1],
                    qpv[individual, gene, 0],
                )


def _validate_configuration(
    variable_bounds: Sequence[Sequence[float]],
    number_of_parameters: int,
    bits_per_parameter: int,
    population_size: int,
    number_of_generations: int,
    alpha_threshold: float,
    population_mutation_rate: float,
    gene_mutation_rate: float,
) -> NDArray[np.float64]:
    bounds = np.asarray(variable_bounds, dtype=float)
    if bounds.shape != (number_of_parameters, 2):
        raise ValueError(
            "maglev_var_bounds_ext deve ter formato (número de parâmetros, 2)."
        )
    if np.any(bounds[:, 0] >= bounds[:, 1]):
        raise ValueError("Cada limite inferior deve ser menor que o superior.")
    if bits_per_parameter <= 0:
        raise ValueError("O número de bits por parâmetro deve ser positivo.")
    if population_size <= 0 or number_of_generations <= 0:
        raise ValueError("População e número de gerações devem ser positivos.")
    for name, value in {
        "qga_measure_p_alpha": alpha_threshold,
        "qga_pop_mutation_rate": population_mutation_rate,
        "qga_gene_mutation_rate": gene_mutation_rate,
    }.items():
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} deve pertencer ao intervalo [0, 1].")
    return bounds


def executar_qga_maglev(
    maglev_fitness_func_ext: FitnessFunction,
    maglev_var_bounds_ext: Sequence[Sequence[float]],
    maglev_num_params_ext: int,
    maglev_bits_per_param_ext: int,
    qga_N_ext: int,
    qga_generation_max_ext: int,
    qga_measure_p_alpha: float = 0.5,
    qga_pop_mutation_rate: float = 0.01,
    qga_gene_mutation_rate: float = 0.001,
    seed_qga: int | None = None,
    *,
    verbose: bool = True,
) -> tuple[NDArray[np.float64], float, list[dict[str, Any]]]:
    """PT-BR: Executa o QGA para maximizar uma função de aptidão.

    Os seis primeiros nomes de parâmetros são mantidos por compatibilidade com
    o notebook usado na dissertação. O histórico contém o melhor valor da
    geração e o melhor global acumulado.

    EN-US: Run the QGA to maximize a fitness function.

    The first six parameter names are retained for compatibility with the
    notebook used in the dissertation. The history contains the best value of
    each generation and the cumulative global-best value.
    """
    global N, Genome, generation_max, popSize, genomeLength
    global MAGLEV_EXTERNAL_FITNESS_FUNC, MAGLEV_VAR_BOUNDS
    global MAGLEV_BITS_PER_PARAM, MAGLEV_NUM_PARAMS

    bounds = _validate_configuration(
        maglev_var_bounds_ext,
        maglev_num_params_ext,
        maglev_bits_per_param_ext,
        qga_N_ext,
        qga_generation_max_ext,
        qga_measure_p_alpha,
        qga_pop_mutation_rate,
        qga_gene_mutation_rate,
    )

    if seed_qga is not None:
        np.random.seed(seed_qga)

    MAGLEV_EXTERNAL_FITNESS_FUNC = maglev_fitness_func_ext
    MAGLEV_VAR_BOUNDS = bounds
    MAGLEV_BITS_PER_PARAM = maglev_bits_per_param_ext
    MAGLEV_NUM_PARAMS = maglev_num_params_ext
    N = qga_N_ext
    generation_max = qga_generation_max_ext
    Genome = MAGLEV_NUM_PARAMS * MAGLEV_BITS_PER_PARAM
    popSize = N + 1
    genomeLength = Genome + 1
    _allocate_state()

    if verbose:
        seed_text = f", seed={seed_qga}" if seed_qga is not None else ""
        print(
            f"QGA: população={N}, bits={Genome}, "
            f"gerações={generation_max}{seed_text}"
        )

    generation = 0
    _initialize_population()
    _measure(qga_measure_p_alpha)
    _evaluate_population(generation)

    best_index = int(best_chrom[generation])
    best_fitness = float(fitness[best_index])
    best_chromosome = chromosome[best_index].copy()
    history: list[dict[str, Any]] = [
        {
            "geracao": generation,
            "melhor_aptidao_geracao": best_fitness,
            "melhor_aptidao_global": best_fitness,
        }
    ]

    while generation < generation_max - 1:
        _rotate_population(generation)
        _mutate_population(qga_pop_mutation_rate, qga_gene_mutation_rate)
        generation += 1
        _measure(qga_measure_p_alpha)
        _evaluate_population(generation)

        generation_best_index = int(best_chrom[generation])
        generation_best_fitness = float(fitness[generation_best_index])
        if generation_best_fitness > best_fitness:
            best_fitness = generation_best_fitness
            best_chromosome = chromosome[generation_best_index].copy()
            if verbose:
                print(
                    f"Geração {generation}: novo melhor global = "
                    f"{best_fitness:.4e}"
                )

        history.append(
            {
                "geracao": generation,
                "melhor_aptidao_geracao": generation_best_fitness,
                "melhor_aptidao_global": best_fitness,
            }
        )

    best_parameters = decode_maglev_chromosome(best_chromosome)
    if verbose:
        print(f"Melhor aptidão global: {best_fitness:.4e}")
        print(f"Parâmetros decodificados: {np.round(best_parameters, 5)}")

    return best_parameters, best_fitness, history


__all__ = [
    "decode_binary_parameters",
    "decode_maglev_chromosome",
    "executar_qga_maglev",
]
