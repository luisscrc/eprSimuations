"""
Diagrama de niveles de energía del efecto Zeeman para un espín 1/2.
Versión con fuentes aumentadas para póster.

Requisitos:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# ============================================================
# PARÁMETROS
# ============================================================
g_e = 2.0023          # Factor de Landé del electrón libre
beta_e = 9.274e-24    # Magnetón de Bohr (J/T)
h = 6.626e-34         # Constante de Planck (J·s)
nu = 9.5e9            # Frecuencia de microondas (Hz)

# Campo resonante: hν = g β B → B = hν / (g β)
B_r = h * nu / (g_e * beta_e)   # ≈ 0.339 T

# Rango de campo magnético
B = np.linspace(0, 0.5, 500)    # Tesla

# Energías de los dos niveles
U_alpha = +0.5 * g_e * beta_e * B
U_beta  = -0.5 * g_e * beta_e * B

# Convertir a unidades más cómodas (J → escala arbitraria)
escala = 1e24
U_alpha_plot = U_alpha * escala
U_beta_plot  = U_beta  * escala


# ============================================================
# TAMAÑOS DE FUENTE (AJUSTA AQUÍ SI QUIERES)
# ============================================================
FS_EJES        = 26    # Etiquetas de los ejes (B y U)
FS_TICKS       = 22    # Números de los ejes
FS_ETIQUETAS   = 30    # α, β, M_s, ±1/2
FS_EXPRESIONES = 24    # Expresiones U_α y U_β
FS_ANOTACIONES = 24    # ΔU = hν, B_r, B = 0


# ============================================================
# FIGURA
# ============================================================
fig, ax = plt.subplots(figsize=(14, 9), facecolor='white')

# --- Línea horizontal que termina en B = 0 ---
B_horiz = np.linspace(-0.02, 0, 100)
U_horiz = np.zeros_like(B_horiz)
ax.plot(B_horiz, U_horiz, color='#1F4E79', linewidth=3, zorder=3)

# --- Líneas de los niveles α y β ---
ax.plot(B, U_alpha_plot, color='#1F4E79', linewidth=3,
        label=r'$\alpha$ ($M_s = +1/2$)')
ax.plot(B, U_beta_plot,  color='#1F4E79', linewidth=3,
        label=r'$\beta$ ($M_s = -1/2$)')

# --- Punto de bifurcación en B = 0 ---
ax.plot(0, 0, 'o', color='#1F4E79', markersize=9, zorder=4)

# --- Línea vertical en B = 0 (degeneración) ---
ax.axvline(x=0, ymin=0.42, ymax=0.58,
           color='black', linewidth=1.8, zorder=2)

# --- Línea punteada vertical en B_r ---
ax.axvline(x=B_r, ymin=0.2, ymax=0.72,
           color='gray', linestyle='--', linewidth=1.5, alpha=0.7)

# --- Flecha de transición ΔU = hν en B_r ---
idx = np.argmin(np.abs(B - B_r))
ax.annotate(
    '', xy=(B_r, U_alpha_plot[idx]),
    xytext=(B_r, U_beta_plot[idx]),
    arrowprops=dict(arrowstyle='<->', color='black', lw=2.5)
)

# Etiqueta ΔU = hν
ax.text(B_r - 0.05, 0,
        r'$\Delta U = h\nu$',
        fontsize=FS_ANOTACIONES, ha='right', va='center',
        fontweight='bold')

# --- Etiquetas de las expresiones de energía ---
ax.text(B[-1] + 0.008, U_alpha_plot[-1],
        r'$U_\alpha = +\dfrac{1}{2}\,g_e\,\beta_e\,B$',
        fontsize=FS_EXPRESIONES, color='#1F4E79', va='center',
        fontweight='bold')
ax.text(B[-1] + 0.008, U_beta_plot[-1],
        r'$U_\beta = -\dfrac{1}{2}\,g_e\,\beta_e\,B$',
        fontsize=FS_EXPRESIONES, color='#1F4E79', va='center',
        fontweight='bold')

# --- Etiquetas α y β sobre las líneas ---
ax.text(0.44, U_alpha_plot[-1] + 0.7, r'$\alpha$',
        fontsize=FS_ETIQUETAS, color='#1F4E79', fontweight='bold')
ax.text(0.44, U_beta_plot[-1] - 1.8, r'$\beta$',
        fontsize=FS_ETIQUETAS, color='#1F4E79', fontweight='bold')

# --- Etiqueta M_s = +1/2 y -1/2 ---
ax.text(0.27, U_alpha_plot[np.argmin(np.abs(B - 0.27))] + 0.7,
        r'$+\dfrac{1}{2}$', fontsize=FS_ETIQUETAS, ha='center',
        fontweight='bold')
ax.text(0.27, U_beta_plot[np.argmin(np.abs(B - 0.27))] - 1.3,
        r'$-\dfrac{1}{2}$', fontsize=FS_ETIQUETAS, ha='center',
        fontweight='bold')

# --- Etiqueta M_s en la parte superior ---
ax.text(0.27, 6.5, r'$M_s$', fontsize=FS_ETIQUETAS, ha='center',
        fontweight='bold')

# --- Etiqueta de B = 0 ---
ax.text(-0.015, -7.8, r'$B = 0$', fontsize=FS_ANOTACIONES,
        ha='center', fontweight='bold')

# --- Etiqueta del campo resonante B_r ---
ax.annotate(
    r'campo resonante $B_r$',
    xy=(B_r, U_beta_plot[idx] - 0.3),
    xytext=(B_r + 0.02, -7.8),
    fontsize=FS_ANOTACIONES, fontweight='bold',
    arrowprops=dict(arrowstyle='->', color='black', lw=1.8)
)

# ============================================================
# ESTILO
# ============================================================
ax.set_xlim(-0.04, 0.56)
ax.set_ylim(-9.5, 7.5)
ax.set_xlabel(r'Campo magnético $B$ (T)',
              fontsize=FS_EJES, fontweight='bold', labelpad=12)
ax.set_ylabel(r'Energía $U$',
              fontsize=FS_EJES, fontweight='bold', labelpad=12)

ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5])
ax.set_xticklabels(['0', '0.1', '0.2', '0.3', '0.4', '0.5'],
                   fontsize=FS_TICKS)
ax.set_yticks([])

# Quitar spines superior y derecho
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(2)
ax.spines['bottom'].set_linewidth(2)

plt.tight_layout()
plt.savefig('zeeman_energy_levels.png', dpi=200,
            facecolor='white', bbox_inches='tight')
plt.show()