"""PT-BR: Regenera a figura-resumo das métricas finais de desempenho.

EN-US: Regenerate the summary figure of the final performance metrics.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


LABELS = [
    "FT1 QGA",
    "IT2-FLC QGA",
    "FT1 Original",
    "IT2-FLC Original",
    "FT1 GA",
    "IT2-FLC GA",
]

METRICS = {
    "ITAE": [6.125e-4, 6.051e-4, 1.600e-3, 1.582e-3, 6.356e-4, 6.097e-4],
    "IG": [0.8193, 0.8216, 0.6687, 0.6693, 0.8088, 0.8169],
    "RMS": [0.737, 0.734, 1.187, 1.188, 0.747, 0.737],
    "ESF": [25.094, 25.107, 23.777, 23.795, 25.029, 25.089],
    "TEMPO": [0.254, 0.244, 0.588, 0.492, 0.280, 0.246],
    "OS": [22.23, 21.23, 3.87, 3.47, 21.36, 21.20],
}


def create_figure(output: Path) -> Path:
    """PT-BR: Cria a figura e retorna o caminho absoluto do arquivo gravado.

    EN-US: Create the figure and return the absolute path of the saved file.
    """
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 14,
            "axes.labelsize": 14,
            "axes.titlesize": 16,
            "legend.fontsize": 12,
            "lines.linewidth": 2,
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
        }
    )

    figure, axes = plt.subplots(3, 2, figsize=(14, 11))
    figure.suptitle(
        "Comparação de Métricas de Desempenho",
        fontsize=16,
        fontweight="bold",
    )
    specifications = [
        ("ITAE", "ITAE", "steelblue", "ITAE", axes[0, 0]),
        ("IG", "Índice de Goodhart", "gold", "IG", axes[0, 1]),
        ("RMS", "Erro RMS (mm)", "coral", "Erro RMS (mm)", axes[1, 0]),
        (
            "ESF",
            "Esforço de Controle (V·s)",
            "lightgreen",
            "Esforço (V·s)",
            axes[1, 1],
        ),
        (
            "TEMPO",
            "Tempo de Acomodação (s)",
            "skyblue",
            "Tempo (s)",
            axes[2, 0],
        ),
        ("OS", "Sobressinal (%)", "lightcoral", "Sobressinal (%)", axes[2, 1]),
    ]

    for key, title, color, ylabel, axis in specifications:
        axis.bar(
            LABELS,
            METRICS[key],
            color=color,
            alpha=0.85,
            edgecolor="gray",
            linewidth=0.4,
        )
        axis.set_title(title, fontweight="bold")
        axis.set_ylabel(ylabel)
        axis.grid(True, axis="y", alpha=0.3)
        for label in axis.get_xticklabels():
            label.set_rotation(30)
            label.set_ha("right")
            label.set_fontsize(11)

    figure.tight_layout(rect=[0, 0, 1, 0.97])
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=300, bbox_inches="tight")
    plt.close(figure)
    return output


def parse_args() -> argparse.Namespace:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=root / "results" / "figures" / "comparacao_metricas_desempenho.png",
        help="Arquivo PNG de saída.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    destination = create_figure(parse_args().output)
    print(f"Figura gravada em: {destination}")
