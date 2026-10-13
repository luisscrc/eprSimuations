import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyBboxPatch
from matplotlib.lines import Line2D

# =========================================================
# CONFIGURACIÓN
# =========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

for ax in [ax1, ax2]:
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.axis('off')

# =========================================================
# SUBPLOT 1 (IZQUIERDA): MODO TE10 - REGLA DE LA MANO DERECHA
# =========================================================
# Paredes de la guía
ax1.plot([0, 9.5], [2.8, 2.8], 'k-', lw=3)
ax1.plot([0, 9.5], [0.2, 0.2], 'k-', lw=3)
ax1.plot([0, 0], [0.2, 2.8], 'k-', lw=3)

# 5 bucles magnéticos con flechas SOBRE los rectángulos
for i in range(5):
    cx = 1.2 + i * 1.9

    # --- Rectángulo EXTERIOR: pegado a las paredes ---
    ax1.add_patch(FancyBboxPatch(
        (cx - 0.7, 0.3),
        1.4, 2.4,
        boxstyle="round,pad=0,rounding_size=0.25",
        linewidth=1.5, edgecolor='blue',
        facecolor='none', linestyle='--'
    ))

    # --- Rectángulo INTERIOR MÁS GRANDE ---
    ax1.add_patch(FancyBboxPatch(
        (cx - 0.5, 0.7),               # más ancho y más alto
        1.0, 1.6,                      # antes 0.7 x 1.2 → ahora 1.0 x 1.6
        boxstyle="round,pad=0,rounding_size=0.2",
        linewidth=1.5, edgecolor='blue',
        facecolor='none', linestyle='--'
    ))

    # --- FLECHAS SOBRE LOS RECTÁNGULOS (circulación del campo H) ---
    # Flecha SUPERIOR EXTERIOR
    ax1.annotate('', xy=(cx + 0.2, 2.5), xytext=(cx - 0.2, 2.5),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=2))

    # Flecha INFERIOR EXTERIOR
    ax1.annotate('', xy=(cx - 0.2, 0.5), xytext=(cx + 0.2, 0.5),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=2))

    # Flecha SUPERIOR INTERIOR (ajustada al nuevo tamaño)
    ax1.annotate('', xy=(cx + 0.15, 2.1), xytext=(cx - 0.15, 2.1),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

    # Flecha INFERIOR INTERIOR (ajustada al nuevo tamaño)
    ax1.annotate('', xy=(cx - 0.15, 0.9), xytext=(cx + 0.15, 0.9),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=1.5))

ax1.text(5, -0.5, 'TE$_{10}$', fontsize=32, fontweight='bold',
         ha='center', va='top')


# =========================================================
# SUBPLOT 2 (DERECHA): MODO TM11
# =========================================================
# Paredes de la guía
ax2.plot([0, 9.5], [2.8, 2.8], 'k-', lw=3)
ax2.plot([0, 9.5], [0.2, 0.2], 'k-', lw=3)
ax2.plot([0, 0], [0.2, 2.8], 'k-', lw=3)

# --- Campo magnético (arcos rojos) ---
for i in range(3):
    cx = 2.0 + i * 3.0
    # Arco superior
    ax2.add_patch(Arc((cx, 2.4), 1.8, 1.2, angle=0,
                     theta1=180, theta2=360, color='red', lw=1.8))
    ax2.add_patch(Arc((cx, 2.4), 1.2, 0.8, angle=0,
                     theta1=180, theta2=360, color='red', lw=1.8))
    # Arco inferior
    ax2.add_patch(Arc((cx, 0.6), 1.8, 1.2, angle=0,
                     theta1=0, theta2=180, color='red', lw=1.8))
    ax2.add_patch(Arc((cx, 0.6), 1.2, 0.8, angle=0,
                     theta1=0, theta2=180, color='red', lw=1.8))
    # Flechas de dirección
    ax2.annotate('', xy=(cx + 0.9, 2.4), xytext=(cx + 0.7, 2.4),
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.8))
    ax2.annotate('', xy=(cx + 0.9, 0.6), xytext=(cx + 0.7, 0.6),
                 arrowprops=dict(arrowstyle='->', color='red', lw=1.8))

# --- Campo eléctrico (líneas verticales punteadas azules) ---
for x in [0.5, 3.5, 6.5]:
    for dx in [-0.1, 0, 0.1]:
        ax2.plot([x + dx, x + dx], [0.8, 2.2], 'b--', lw=1.5)
    ax2.annotate('', xy=(x + 0.1, 1.7), xytext=(x + 0.1, 1.4),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=1.8))
    ax2.annotate('', xy=(x - 0.1, 1.7), xytext=(x - 0.1, 1.4),
                 arrowprops=dict(arrowstyle='->', color='blue', lw=1.8))

ax2.text(5, -0.5, 'TM$_{11}$', fontsize=32, fontweight='bold',
         ha='center', va='top')


# =========================================================
# LEYENDA GLOBAL: E vs H
# =========================================================
legend_elements = [
    Line2D([0], [0], color='blue', linewidth=12, linestyle='--',
           label='Campo H (magnético)'),
    Line2D([0], [0], color='red', linewidth=12, linestyle='-',
           label='Campo E (eléctrico)'),
]

fig.legend(handles=legend_elements,
           loc='lower center',
           ncol=2,
           fontsize=20,
           frameon=False,
           bbox_to_anchor=(0.5, -0.02))

# =========================================================
# MOSTRAR
# =========================================================
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('modos_TE10_TM11_mano_derecha.png', dpi=300, bbox_inches='tight')
plt.show()