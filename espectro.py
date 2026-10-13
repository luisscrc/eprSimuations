"""
Espectro electromagnético simplificado con etiquetas de banda grandes.

- Eje inferior: Frecuencia (Hz).
- Eje superior: Longitud de onda (m).
- Bandas coloreadas: MF-UHF, Microondas, Microondas alta.

Requisitos:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# DATOS DE BANDAS
# =========================================================
bandas = [
    (300e3,  3e6,   "MF",  "MF-UHF"),
    (3e6,    30e6,  "HF",  "MF-UHF"),
    (30e6,   300e6, "VHF", "MF-UHF"),
    (300e6,  3e9,   "UHF", "MF-UHF"),
    (1e9,    2e9,   "L",   "Microondas"),
    (2e9,    4e9,   "S",   "Microondas"),
    (4e9,    8e9,   "C",   "Microondas"),
    (8e9,    12e9,  "X",   "Microondas"),
    (12e9,   18e9,  "Ku",  "Microondas alta"),
    (18e9,   26e9,  "K",   "Microondas alta"),
    (26e9,   40e9,  "Ka",  "Microondas alta"),
    (40e9,   60e9,  "U",   "Microondas alta"),
    (50e9,   75e9,  "V",   "Microondas alta"),
    (60e9,   90e9,  "E",   "Microondas alta"),
    (75e9,   110e9, "W",   "Microondas alta"),
    (90e9,   140e9, "F",   "Microondas alta"),
]

colores = {
    "MF-UHF":          "#4C72B0",
    "Microondas":      "#DD8452",
    "Microondas alta": "#55A868",
}

c = 3e8


# =========================================================
# TAMAÑOS DE FUENTE (AJUSTA AQUÍ SI QUIERES)
# =========================================================
FS_BANDAS      = 30    # Etiquetas dentro de la barra (MF, HF, VHF...)
FS_TICKS       = 22    # Números de los ejes (1 MHz, 10 MHz...)
FS_EJES        = 26    # Etiquetas de los ejes (Frecuencia, Longitud de onda)


# =========================================================
# FIGURA
# =========================================================
fig, ax = plt.subplots(figsize=(22, 5))   # más ancha y alta

y = 0
alto = 1.0

# Barra principal
for f_ini, f_fin, etiqueta, categoria in bandas:
    ax.barh(y, width=f_fin - f_ini, left=f_ini,
            height=alto, color=colores[categoria],
            edgecolor="white", linewidth=1.5, zorder=2)

    # Etiqueta dentro de la barra
    centro = np.sqrt(f_ini * f_fin)
    ax.text(centro, y, etiqueta,
            ha="center", va="center",
            fontsize=FS_BANDAS, fontweight="bold",
            color="white", zorder=3)

# =========================================================
# EJE X: FRECUENCIA (log)
# =========================================================
ax.set_xscale("log")
ax.set_xlim(300e3, 140e9)
ax.set_ylim(-0.9, 0.9)

ticks = [1e6, 1e7, 1e8, 1e9, 1e10, 1e11]
labels = ["1 MHz", "10 MHz", "100 MHz", "1 GHz", "10 GHz", "100 GHz"]
ax.set_xticks(ticks)
ax.set_xticklabels(labels, fontsize=FS_TICKS, fontweight="bold")
ax.set_xlabel("Frecuencia", fontsize=FS_EJES,
              fontweight="bold", labelpad=10)

ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)

ax.grid(axis="x", which="major", linestyle="--", alpha=0.3, zorder=0)

# =========================================================
# EJE SUPERIOR: LONGITUD DE ONDA
# =========================================================
ax2 = ax.secondary_xaxis(
    "top",
    functions=(lambda f: c / np.asarray(f, dtype=float),
               lambda lam: c / np.asarray(lam, dtype=float))
)

ticks_lam = [1e3, 1e2, 1e1, 1, 1e-1, 1e-2]
labels_lam = ["1 km", "100 m", "10 m", "1 m", "10 cm", "1 cm"]
ax2.set_xticks(ticks_lam)
ax2.set_xticklabels(labels_lam, fontsize=FS_TICKS, fontweight="bold")
ax2.set_xlabel(r"Longitud de onda ($\lambda = c/f$)",
               fontsize=FS_EJES, fontweight="bold", labelpad=8)

ax2.grid(axis="x", which="major", linestyle=":", alpha=0.25, zorder=0)

# =========================================================
# GUARDAR
# =========================================================
plt.tight_layout()
plt.savefig("espectro_simple.png", dpi=200, bbox_inches="tight")
plt.show()