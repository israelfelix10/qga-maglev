"""PT-BR: Exibe um resumo dos resultados precomputados do estudo MAGLEV.

EN-US: Display a summary of the precomputed results from the MAGLEV study.
"""

from __future__ import annotations

import argparse
import pickle
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data",
        help="Diretório que contém os quatro arquivos pickle confiáveis.",
    )
    return parser.parse_args()


def main() -> int:
    data_dir = parse_args().data_dir.resolve()
    files = sorted(data_dir.glob("maglev_complete_optimization_data_*bits.pkl"))
    if not files:
        print(f"Nenhum arquivo encontrado em {data_dir}")
        return 1

    print("AVISO: pickle deve ser carregado somente de uma origem confiável.\n")
    for path in files:
        with path.open("rb") as stream:
            data = pickle.load(stream)

        config = data.get("config_info", {})
        ga_config = config.get("ga_standard", {})
        qga_config = config.get("qga", {})
        print(path.name)
        print(f"  chaves: {len(data)}")
        print(f"  seed global: {data.get('GLOBAL_SEED', config.get('seed_global'))}")
        print(
            "  GA: população={0}, gerações={1}".format(
                ga_config.get("populacao", "?"),
                ga_config.get("geracoes", "?"),
            )
        )
        print(
            "  QGA: população={0}, gerações={1}, bits/parâmetro={2}".format(
                qga_config.get("populacao", "?"),
                qga_config.get("geracoes", "?"),
                qga_config.get("bits_por_parametro", "?"),
            )
        )
        for key, label in [
            ("ga_best_poles_T1_fitness", "ITAE objetivo GA FT1"),
            ("ga_best_poles_T2I_fitness", "ITAE objetivo GA IT2-FLC"),
            ("qga_melhor_itae_qga_t1", "ITAE objetivo QGA FT1"),
            ("qga_melhor_itae_qga_t2i", "ITAE objetivo QGA IT2-FLC"),
        ]:
            value = data.get(key)
            print(f"  {label}: {value:.6e}" if value is not None else f"  {label}: N/D")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
