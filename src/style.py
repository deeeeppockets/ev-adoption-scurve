"""Shared figure style: colours, fonts and a save helper (PDF + PNG for the website)."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE = "#2a78d6"     # logistic model
ORANGE = "#eb6834"   # comparison model (exponential / naive trend)
AQUA = "#1baf7a"     # third highlight
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#e4e3df"
SURFACE = "#fcfcfb"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK2,
    "axes.titlesize": 10,
    "axes.titleweight": "bold",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.6,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "pdf.fonttype": 42,
    "legend.frameon": False,
})

ROOT = Path(__file__).resolve().parents[1]


def save(fig, name):
    """Write figures/<name>.pdf (repo deliverable) and docs/img/<name>.png (website)."""
    (ROOT / "figures").mkdir(exist_ok=True)
    (ROOT / "docs" / "img").mkdir(parents=True, exist_ok=True)
    fig.savefig(ROOT / "figures" / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(ROOT / "docs" / "img" / f"{name}.png", dpi=200, bbox_inches="tight")
    plt.close(fig)
