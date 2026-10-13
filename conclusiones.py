"""
Genera 6 íconos en una columna vertical con textos grandes,
sin cuadros de color, solo texto.

Requisitos:
    pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch

# Colores institucionales (IPN)
GUINDA = '#6E162E'
BLANCO = '#FFFFFF'
AZUL = '#1F4E79'
ROJO = '#B71C1C'
VERDE = '#1F7A1F'


# ============================================================
# ÍCONO 1: SPINES ALINEADOS (✗) vs DESALINEADOS (✓)
# ============================================================
def icono_espin(ax):
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-1.2, 2.5)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(Rectangle((0, 1.3), 1.0, 1.0,
                           facecolor='white', edgecolor='black', linewidth=2))
    ax.annotate('', xy=(0.35, 2.15), xytext=(0.35, 1.45),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(0.65, 1.45), xytext=(0.65, 2.15),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    for i in range(3):
        ax.add_patch(Rectangle((1.5 + i*1.0, 1.3), 1.0, 1.0,
                               facecolor='white', edgecolor='black', linewidth=2))
        ax.annotate('', xy=(2.0 + i*1.0, 2.15), xytext=(2.0 + i*1.0, 1.45),
                    arrowprops=dict(arrowstyle='->', color='black', lw=2))

    ax.plot([5.0, 5.4], [2.0, 2.4], color=ROJO, linewidth=4)
    ax.plot([5.4, 5.0], [2.0, 2.4], color=ROJO, linewidth=4)

    ax.add_patch(Rectangle((0, -0.3), 1.0, 1.0,
                           facecolor='white', edgecolor='black', linewidth=2))
    ax.annotate('', xy=(0.35, 0.55), xytext=(0.35, -0.15),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(0.65, -0.15), xytext=(0.65, 0.55),
                arrowprops=dict(arrowstyle='->', color='black', lw=2))

    patron_desalineado = ['up', 'down', 'up']
    for i, direccion in enumerate(patron_desalineado):
        ax.add_patch(Rectangle((1.5 + i*1.0, -0.3), 1.0, 1.0,
                               facecolor='white', edgecolor='black', linewidth=2))
        if direccion == 'up':
            ax.annotate('', xy=(2.0 + i*1.0, 0.55),
                        xytext=(2.0 + i*1.0, -0.15),
                        arrowprops=dict(arrowstyle='->', color='black', lw=2))
        else:
            ax.annotate('', xy=(2.0 + i*1.0, -0.15),
                        xytext=(2.0 + i*1.0, 0.55),
                        arrowprops=dict(arrowstyle='->', color='black', lw=2))

    ax.plot([4.9, 5.2, 5.5], [0.3, 0.0, 0.5],
            color=VERDE, linewidth=3.5)
    ax.plot([5.5, 5.2, 4.9], [0.5, 0.0, 0.3],
            color=VERDE, linewidth=3.5)


# ============================================================
# ÍCONO 2: RUIDO
# ============================================================
def icono_ruido(ax):
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    np.random.seed(42)
    x = np.linspace(-0.9, 0.9, 200)
    y = 0.35 * np.sin(8 * x) + 0.15 * np.random.randn(200)
    ax.plot(x, y, color=AZUL, linewidth=2.5)

    ax.axhline(0, color='black', linewidth=0.5, alpha=0.3)

    ax.add_patch(Rectangle((-0.9, -0.9), 1.8, 0.3,
                           facecolor=ROJO, alpha=0.2,
                           edgecolor=ROJO, linewidth=1.5))
    ax.text(0, -0.75, 'RUIDO', fontsize=11, ha='center',
            color=ROJO, fontweight='bold')


# ============================================================
# ÍCONO 3: COMPLEJIDAD / COSTO
# ============================================================
def icono_caro(ax):
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    theta = np.linspace(0, 2*np.pi, 100)
    r_outer = 0.6 + 0.1 * np.sign(np.sin(8 * theta))
    ax.plot(r_outer * np.cos(theta), r_outer * np.sin(theta),
            color=GUINDA, linewidth=2)

    ax.add_patch(Circle((0, 0), 0.25, facecolor='white',
                        edgecolor=GUINDA, linewidth=2))

    ax.text(0, 0, '$', fontsize=42, ha='center', va='center',
            color=ROJO, fontweight='bold')

    for dx in [-0.7, 0, 0.7]:
        ax.annotate('', xy=(dx, 0.9), xytext=(dx, 0.5),
                    arrowprops=dict(arrowstyle='->', color=ROJO, lw=2))


# ============================================================
# ÍCONO 4: NO DESTRUCTIVO
# ============================================================
def icono_no_destructivo(ax):
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((-0.35, -0.6), 0.7, 0.9,
                                boxstyle="round,pad=0.05",
                                facecolor='#D6EAF8',
                                edgecolor=AZUL, linewidth=2))

    ax.add_patch(Rectangle((-0.15, 0.3), 0.3, 0.2,
                           facecolor='#D6EAF8',
                           edgecolor=AZUL, linewidth=2))

    ax.add_patch(Rectangle((-0.3, -0.55), 0.6, 0.5,
                           facecolor='#5DADE2', alpha=0.7,
                           edgecolor='none'))

    ax.text(0.6, 0.6, '✓', fontsize=36, ha='center', va='center',
            color=VERDE, fontweight='bold')


# ============================================================
# ÍCONO 5: BAJO COSTO + DIGITAL
# ============================================================
def icono_barato(ax):
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(FancyBboxPatch((-0.5, -0.4), 1.0, 0.8,
                                boxstyle="round,pad=0.03",
                                facecolor='#2C3E50',
                                edgecolor='black', linewidth=2))

    for i in range(4):
        x = -0.4 + i * 0.27
        ax.plot([x, x], [0.4, 0.55], color='black', linewidth=2)
        ax.plot([x, x], [-0.4, -0.55], color='black', linewidth=2)

    ax.text(0, 0, 'µC', fontsize=22, ha='center', va='center',
            color='white', fontweight='bold')

    ax.text(0, -0.75, '$', fontsize=28, ha='center', va='center',
            color=ROJO, fontweight='bold')
    ax.plot([-0.13, 0.13], [-0.75, -0.75], color=ROJO, linewidth=3)


# ============================================================
# ÍCONO 6: MOLÉCULA COMPLEJA → MOLÉCULA SIMPLE
# ============================================================
def icono_dpph(ax):
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-2.2, 1.5)
    ax.set_aspect('equal')
    ax.axis('off')

    atomos = [
        (-1.0, 0.7, '#E74C3C', 'O'),
        (-0.6, 0.5, '#3498DB', 'N'),
        (-0.2, 0.7, '#9B59B6', 'C'),
        ( 0.1, 0.4, '#95A5A6', 'C'),
        ( 0.4, 0.7, '#3498DB', 'C'),
        ( 0.8, 0.5, '#E74C3C', 'O'),
        ( 1.1, 0.8, '#9B59B6', 'N'),
    ]

    for i in range(len(atomos) - 1):
        x1, y1, _, _ = atomos[i]
        x2, y2, _, _ = atomos[i+1]
        ax.plot([x1, x2], [y1, y2], color='#555555',
                linewidth=2, zorder=1)

    for x, y, color, elem in atomos:
        ax.add_patch(Circle((x, y), 0.12, facecolor=color,
                            edgecolor='black', linewidth=1, zorder=2))
        ax.text(x, y, elem, fontsize=8, ha='center', va='center',
                color='white', fontweight='bold', zorder=3)

    hidrogenos = [
        (-1.0, 0.95), (-0.6, 0.25), (-0.2, 0.95),
        (0.1, 0.15), (0.4, 0.95), (0.8, 0.25), (1.1, 1.05)
    ]
    for x, y in hidrogenos:
        ax.add_patch(Circle((x, y), 0.05, facecolor='#95A5A6',
                            edgecolor='black', linewidth=0.5, zorder=2))

    ax.annotate('', xy=(0, -1.0), xytext=(0, 0.1),
                arrowprops=dict(arrowstyle='<|-',
                                color='#333333',
                                lw=2.5,
                                linestyle='--'))

    atomos_simples = [
        (-0.5, -1.4, '#E74C3C'),
        (-0.1, -1.5, '#3498DB'),
        ( 0.4, -1.3, '#9B59B6'),
        ( 0.7, -1.5, '#95A5A6'),
    ]
    for x, y, color in atomos_simples:
        ax.add_patch(Circle((x, y), 0.11, facecolor=color,
                            edgecolor='black', linewidth=1, zorder=2))


# ============================================================
# FIGURA VERTICAL: 6 filas (ícono | texto)
# ============================================================
fig = plt.figure(figsize=(14, 26), facecolor='white')   # ← más alta

textos = [
    "La técnica es no destructiva con\nla mayoría de las muestras.",
    "La espectroscopía por EPR permite\nidentificar moléculas con electrones\ndesapareados.",
    "El ruido por microondas y campos\nmagnéticos hace críticas\nlas etapas de filtrado y propagación\nen las guías de onda.",
    "Esta complejidad encarece la\nconstrucción de los espectrómetros.",
    "Entendiendo el funcionamiento físico\nes posible replicar el experimento\ncon componentes comerciales de\nbajo costo y control digital embebido.",
    "La detección de DPPH abre la puerta\na una nueva fase para detectar\nmoléculas de contextos médicos."
]

iconos = [icono_no_destructivo, icono_espin, icono_ruido, icono_caro,
           icono_barato, icono_dpph]

gs = fig.add_gridspec(6, 2, width_ratios=[1, 3.2], hspace=0.4, wspace=0.1)

for i, (icono, texto) in enumerate(zip(iconos, textos)):
    ax_icon = fig.add_subplot(gs[i, 0])
    icono(ax_icon)

    ax_text = fig.add_subplot(gs[i, 1])
    ax_text.set_xlim(0, 1)
    ax_text.set_ylim(0, 1)
    ax_text.axis('off')

    # --- SOLO TEXTO, SIN CUADRO DE COLOR, FUENTE GRANDE ---
    ax_text.text(0.5, 0.5, texto,
                 fontsize=26,                 # ← antes 18, ahora 26
                 ha='center', va='center',
                 color='black', fontweight='bold',
                 wrap=True)

plt.savefig('iconos_verticales.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.show()

print("Imagen guardada: iconos_verticales.png")