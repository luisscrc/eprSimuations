"""
Genera imágenes estilo COMSOL/CST de:
  1. Superficie 3D del campo eléctrico en una guía de onda TE10.
  2. Mapa de contorno 2D del campo en una cavidad resonante.
  3. Vista transversal con la sonda de acoplamiento.

Requisitos:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Rectangle, FancyArrowPatch

# ============================================================
# PARÁMETROS FÍSICOS (guía WR-90, banda X)
# ============================================================
a = 22.86e-3   # ancho (m)
b = 10.16e-3   # alto (m)
d = 45.72e-3   # longitud (m)
f = 10.0e9     # frecuencia (Hz)
c = 299792458  # velocidad de la luz

# ============================================================
# 1. SUPERFICIE 3D DEL CAMPO E EN GUÍA TE10
# ============================================================
def plot_3d_te10():
    # Malla
    x = np.linspace(0, a, 120)
    y = np.linspace(0, b, 60)
    z = np.linspace(0, d, 300)
    X, Z = np.meshgrid(x, z)

    # Modo TE10: Ey ∝ sin(πx/a) · cos(βz)
    beta = 2 * np.pi * f / c
    Y = np.sin(np.pi * X / a) * np.cos(beta * Z)
    Y = Y * b * 0.9  # escala vertical

    fig = plt.figure(figsize=(12, 5), facecolor='white')
    ax = fig.add_subplot(111, projection='3d')

    # Superficie coloreada
    surf = ax.plot_surface(
        X * 1e3, Z * 1e3, Y * 1e3,
        cmap='jet',
        linewidth=0,
        antialiased=True,
        alpha=0.95,
        rstride=2, cstride=2
    )

    # Marco de la guía (aristas)
    corners = np.array([
        [0, 0, 0], [a, 0, 0], [a, 0, d], [0, 0, d],
        [0, b, 0], [a, b, 0], [a, b, d], [0, b, d]
    ]) * 1e3

    edges = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    for i, j in edges:
        ax.plot(
            [corners[i,0], corners[j,0]],
            [corners[i,1], corners[j,1]],
            [corners[i,2], corners[j,2]],
            color='gray', linewidth=1.5, alpha=0.5
        )

    # Etiqueta
    ax.text(
        a*1e3/2, 0, d*1e3*1.05,
        'CAMPO ELÉCTRICO',
        fontsize=16, ha='center', color='black'
    )

    ax.set_xlabel('x (mm)')
    ax.set_ylabel('z (mm)')
    ax.set_zlabel('E_y (u.a.)')
    ax.set_title('Modo TE$_{10}$ en guía rectangular', fontsize=14)
    ax.view_init(elev=20, azim=-60)
    ax.set_box_aspect([1, 3, 1])

    plt.tight_layout()
    plt.savefig('campo_e_3d.png', dpi=200, facecolor='white')
    plt.show()


# ============================================================
# 2. MAPA DE CONTORNO 2D (vista longitudinal)
# ============================================================
def plot_2d_longitudinal():
    x = np.linspace(0, a, 300)
    z = np.linspace(0, d, 600)
    X, Z = np.meshgrid(x, z)

    beta = 2 * np.pi * f / c
    E = np.sin(np.pi * X / a) * np.cos(beta * Z)

    fig, ax = plt.subplots(figsize=(12, 3.5), facecolor='white')

    cf = ax.contourf(
        Z * 1e3, X * 1e3, E,
        levels=50, cmap='jet'
    )
    ax.contour(
        Z * 1e3, X * 1e3, E,
        levels=10, colors='k', linewidths=0.3, alpha=0.4
    )

    # Sonda de acoplamiento (esfera + línea)
    ax.plot([d*1e3*0.9], [a*1e3/2], 'o',
            markersize=18, markerfacecolor='red',
            markeredgecolor='darkred', markeredgewidth=2)
    ax.plot([d*1e3*0.9, d*1e3*0.9], [a*1e3/2, a*1e3/2+3],
            color='darkred', linewidth=3)

    ax.set_xlabel('z (mm)')
    ax.set_ylabel('x (mm)')
    ax.set_title('Campo eléctrico E$_y$ — vista longitudinal', fontsize=13)
    ax.set_aspect('equal')

    plt.colorbar(cf, ax=ax, label='E$_y$ (u.a.)')
    plt.tight_layout()
    plt.savefig('campo_e_2d_longitudinal.png', dpi=200, facecolor='white')
    plt.show()


# ============================================================
# 3. MAPA DE CONTORNO 2D (vista transversal)
# ============================================================
def plot_2d_transversal():
    x = np.linspace(0, a, 300)
    y = np.linspace(0, b, 200)
    X, Y = np.meshgrid(x, y)

    # Modo TE10: E_y ∝ sin(πx/a) — solo depende de x
    E = np.sin(np.pi * X / a)

    fig, ax = plt.subplots(figsize=(10, 4), facecolor='white')

    cf = ax.contourf(
        X * 1e3, Y * 1e3, E,
        levels=50, cmap='jet'
    )
    ax.contour(
        X * 1e3, Y * 1e3, E,
        levels=10, colors='k', linewidths=0.3, alpha=0.4
    )

    # Paredes
    ax.add_patch(Rectangle(
        (0, 0), a*1e3, b*1e3,
        fill=False, edgecolor='black', linewidth=2
    ))

    # Sonda coaxial
    ax.plot([a*1e3*0.75], [b*1e3*0.5], 'o',
            markersize=14, markerfacecolor='red',
            markeredgecolor='darkred', markeredgewidth=2)
    ax.plot([a*1e3*0.75, a*1e3*0.75], [b*1e3*0.5, b*1e3*1.2],
            color='darkred', linewidth=3)
    ax.plot([a*1e3*0.75-1, a*1e3*0.75+1], [b*1e3*1.15, b*1e3*1.15],
            color='darkred', linewidth=4)

    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    ax.set_title('Campo eléctrico E$_y$ — vista transversal', fontsize=13)
    ax.set_aspect('equal')

    plt.colorbar(cf, ax=ax, label='E$_y$ (u.a.)')
    plt.tight_layout()
    plt.savefig('campo_e_2d_transversal.png', dpi=200, facecolor='white')
    plt.show()

# ============================================================
# 4. CAVIDAD RESONANTE — patrón 2D
# ============================================================
def plot_cavidad():
    x = np.linspace(0, a, 300)
    z = np.linspace(0, d, 600)
    X, Z = np.meshgrid(x, z)

    # Modo TE101: E_y ∝ sin(πx/a) · sin(πz/d)
    E = np.sin(np.pi * X / a) * np.sin(np.pi * Z / d)

    fig, ax = plt.subplots(figsize=(12, 3.5), facecolor='white')

    cf = ax.contourf(
        Z * 1e3, X * 1e3, E,
        levels=50, cmap='jet'
    )
    ax.contour(
        Z * 1e3, X * 1e3, E,
        levels=10, colors='k', linewidths=0.3, alpha=0.4
    )

    # Paredes de la cavidad (marco)
    ax.add_patch(Rectangle(
        (0, 0), d*1e3, a*1e3,
        fill=False, edgecolor='black', linewidth=2
    ))

    ax.set_xlabel('z (mm)')
    ax.set_ylabel('x (mm)')
    ax.set_title('Modo TE$_{101}$ en cavidad resonante', fontsize=13)
    ax.set_aspect('equal')

    plt.colorbar(cf, ax=ax, label='E$_y$ (u.a.)')
    plt.tight_layout()
    plt.savefig('cavidad_te101.png', dpi=200, facecolor='white')
    plt.show()

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("Generando imágenes...")
    plot_3d_te10()
    plot_2d_longitudinal()
    plot_2d_transversal()
    plot_cavidad()
    print("✅ Listo. Archivos PNG generados.")