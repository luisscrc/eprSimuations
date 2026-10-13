"""
Diagrama de dos pares de bobinas de Helmholtz (versión compacta):
  - Par grande (rojo) conectado a X+ y X−
  - Par pequeño (azul) conectado a Xs+ y Xs−

Requisitos:
    pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Circle
import numpy as np

# ============================================================
# COLORES
# ============================================================
ROJO = '#CC0000'
AZUL = '#0033CC'
VERDE = '#1F7A1F'
NEGRO = '#000000'

# ============================================================
# FIGURA (más ancha, menos alta)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.set_aspect('equal')
ax.axis('off')

# ============================================================
# PARÁMETROS DE LAS BOBINAS
# ============================================================
bobina_grande_x1 = 2.5
bobina_grande_x2 = 7.5
bobina_grande_y  = 4.8
bobina_grande_w  = 1.8
bobina_grande_h  = 4.0

bobina_peq_x1 = 2.5
bobina_peq_x2 = 7.5
bobina_peq_y  = 4.8
bobina_peq_w  = 1.2
bobina_peq_h  = 3.2


# ============================================================
# DIBUJAR BOBINA GRANDE (ROJA)
# ============================================================
def dibujar_bobina_grande(ax, cx, cy, w, h, nombre):
    ax.add_patch(Ellipse((cx, cy), w, h,
                        facecolor='none', edgecolor=ROJO,
                        linewidth=2.5, linestyle='-'))
    ax.add_patch(Ellipse((cx + 0.12, cy), w, h,
                        facecolor='none', edgecolor=ROJO,
                        linewidth=1.2, linestyle='-'))
    ax.add_patch(Ellipse((cx - 0.12, cy), w, h,
                        facecolor='none', edgecolor=ROJO,
                        linewidth=1.2, linestyle='-'))
    ax.text(cx, cy, nombre, fontsize=18, fontweight='bold',
            ha='center', va='center', color='black')


# ============================================================
# DIBUJAR BOBINA PEQUEÑA (AZUL PUNTEADA)
# ============================================================
def dibujar_bobina_pequena(ax, cx, cy, w, h):
    ax.add_patch(Ellipse((cx, cy), w, h,
                        facecolor='none', edgecolor=AZUL,
                        linewidth=2.5, linestyle='--'))
    ax.add_patch(Ellipse((cx + 0.1, cy), w, h,
                        facecolor='none', edgecolor=AZUL,
                        linewidth=1.2, linestyle='--'))


# Dibujar bobinas
dibujar_bobina_grande(ax, bobina_grande_x1, bobina_grande_y,
                     bobina_grande_w, bobina_grande_h, 'X-a')
dibujar_bobina_grande(ax, bobina_grande_x2, bobina_grande_y,
                     bobina_grande_w, bobina_grande_h, 'X-b')

dibujar_bobina_pequena(ax, bobina_peq_x1, bobina_peq_y,
                      bobina_peq_w, bobina_peq_h)
dibujar_bobina_pequena(ax, bobina_peq_x2, bobina_peq_y,
                      bobina_peq_w, bobina_peq_h)


# ============================================================
# ETIQUETAS SUPERIORES (REORDENADAS)
# ============================================================
# --- Par X (rojo) alineado a la izquierda ---
ax.text(9.5, 6, 'Par X', fontsize=16, fontweight='bold',
        ha='center', va='center', color=ROJO, style='italic')

# --- Par Xs (azul) alineado a la derecha ---
ax.text(9.5, 4, 'Par Xs', fontsize=16, fontweight='bold',
        ha='center', va='center', color=AZUL, style='italic')

# ============================================================
# TERMINALES INFERIORES
# ============================================================
# Caja Xs (izquierda)
ax.add_patch(FancyBboxPatch((0.3, 0.2), 2.4, 0.9,
                            boxstyle="round,pad=0.05",
                            facecolor='#EEEEEE',
                            edgecolor='black', linewidth=1.5,
                            linestyle='--'))
ax.text(0.4, 1.15, 'Xs+', fontsize=13, fontweight='bold',
        ha='center', va='bottom', color='black')
ax.text(2.0, 1.15, 'Xs-', fontsize=13, fontweight='bold',
        ha='center', va='bottom', color='black')
ax.add_patch(Circle((0.7, 0.7), 0.1, facecolor='white',
                    edgecolor='black', linewidth=1.5))
ax.add_patch(Circle((2.3, 0.7), 0.1, facecolor='white',
                    edgecolor='black', linewidth=1.5))

# Caja X (derecha)
ax.add_patch(FancyBboxPatch((7.3, 0.2), 2.4, 0.9,
                            boxstyle="round,pad=0.05",
                            facecolor='#EEEEEE',
                            edgecolor='black', linewidth=1.5,
                            linestyle='--'))
ax.text(7.4, 1.15, 'X+', fontsize=13, fontweight='bold',
        ha='center', va='bottom', color='black')
ax.text(9.0, 1.15, 'X-', fontsize=13, fontweight='bold',
        ha='center', va='bottom', color='black')
ax.add_patch(Circle((7.7, 0.7), 0.1, facecolor='white',
                    edgecolor='black', linewidth=1.5))
ax.add_patch(Circle((9.3, 0.7), 0.1, facecolor='white',
                    edgecolor='black', linewidth=1.5))


# ============================================================
# CONEXIONES ELÉCTRICAS (CABLES)
# ============================================================
# --- Cables Xs (azules) ---
ax.plot([0.7, 0.7], [0.7, 2.3], color=AZUL, linewidth=2)
ax.plot([0.7, 2.0], [2.3, 2.3], color=AZUL, linewidth=2)
ax.plot([2.5, 7.5], [6.4, 6.4], color=AZUL, linewidth=2)
ax.plot([2.0, 2.0], [2.3, 3.8], color=AZUL, linewidth=2)

ax.plot([2.3, 2.3], [0.7, 2.6], color=AZUL, linewidth=2)
ax.plot([2.3, 7.7], [2.6, 2.6], color=AZUL, linewidth=2)
ax.plot([7.7, 7.7], [2.6, 3.3], color=AZUL, linewidth=2)

# --- Cables X (rojos) ---
ax.plot([7.7, 7.7], [0.7, 1.8], color=ROJO, linewidth=2)
ax.plot([7.7, 3.0], [1.8, 1.8], color=ROJO, linewidth=2)
ax.plot([2.5, 7.5], [6.8, 6.8], color=ROJO, linewidth=2)
ax.plot([3.0, 3.0], [1.8, 3.1], color=ROJO, linewidth=2)

ax.plot([9.3, 9.3], [0.7, 2.0], color=ROJO, linewidth=2)
ax.plot([9.3, 7.0], [2.0, 2.0], color=ROJO, linewidth=2)
ax.plot([7.0, 7.0], [2.0, 3.1], color=ROJO, linewidth=2)


# ============================================================
# MOSTRAR
# ============================================================
plt.tight_layout()
plt.savefig('bobinas_helmholtz.png', dpi=300,
            bbox_inches='tight', facecolor='white')
plt.show()

print("Imagen guardada: bobinas_helmholtz.png")