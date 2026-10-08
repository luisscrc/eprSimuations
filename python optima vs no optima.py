
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ============================================================
# PARÁMETROS (guía WR-90, banda X)
# ============================================================
a = 22.86e-3   # ancho (m)
b = 10.16e-3   # alto (m)
d = 60.0e-3    # longitud (m)

# ============================================================
# FUNCIONES DE CAMPO
# ============================================================
def campo_no_optimo(x, z, a, d):
    """
    Simula un patrón irregular por interferencia de varios modos
    (TE10 + TE20 + TE30 con amplitudes y fases arbitrarias).
    """
    E = (
        1.0 * np.sin(1 * np.pi * x / a) * np.cos(2 * np.pi * z / d) +
        0.7 * np.sin(2 * np.pi * x / a) * np.cos(3 * np.pi * z / d + 0.8) +
        0.5 * np.sin(3 * np.pi * x / a) * np.cos(5 * np.pi * z / d + 1.5) +
        0.4 * np.sin(1 * np.pi * x / a) * np.cos(7 * np.pi * z / d + 2.1)
    )
    # Añadir ruido suave para simular pérdidas
    ruido = 0.15 * np.sin(11 * np.pi * x / a) * np.sin(9 * np.pi * z / d)
    return E + ruido


def campo_optimo(x, z, a, d):
    """
    Modo TE10 puro: patrón limpio, simétrico y bien definido.
    """
    return np.sin(1 * np.pi * x / a) * np.cos(2 * np.pi * z / d)


# ============================================================
# DIBUJAR SONDA COAXIAL
# ============================================================
def dibujar_sonda(ax, x_pos, y_top, y_bottom, escala=1.0):
    """
    Dibuja una sonda coaxial simple (círculo + líneas) en la posición dada.
    """
    # Punta de la sonda (esfera roja)
    ax.plot(
        [x_pos], [y_bottom],
        marker='o',
        markersize=14 * escala,
        markerfacecolor='red',
        markeredgecolor='darkred',
        markeredgewidth=2,
        zorder=10
    )
    # Cuerpo de la sonda (línea vertical)
    ax.plot(
        [x_pos, x_pos],
        [y_bottom, y_top],
        color='darkred',
        linewidth=3.5,
        zorder=9
    )
    # Conector superior (rectángulo)
    ax.add_patch(Rectangle(
        (x_pos - 1.2 * escala, y_top - 0.2 * escala),
        2.4 * escala, 1.8 * escala,
        facecolor='steelblue',
        edgecolor='black',
        linewidth=1.2,
        zorder=11
    ))


# ============================================================
# FIGURA PRINCIPAL
# ============================================================
def generar_figura():
    # Malla
    x = np.linspace(0, a, 400)
    z = np.linspace(0, d, 800)
    X, Z = np.meshgrid(x, z)

    # Campos
    E_no_opt = campo_no_optimo(X, Z, a, d)
    E_opt    = campo_optimo(X, Z, a, d)

    # Normalizar para que ambos tengan el mismo rango visual
    E_no_opt /= np.max(np.abs(E_no_opt))
    E_opt    /= np.max(np.abs(E_opt))

    # Figura con 2 paneles apilados
    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(14, 6),
        facecolor='white',
        gridspec_kw={'hspace': 0.25}
    )

    # --------------------------------------------------------
    # PANEL SUPERIOR: NO ÓPTIMA
    # --------------------------------------------------------
    cf1 = ax1.contourf(
        Z * 1e3, X * 1e3, E_no_opt,
        levels=60, cmap='jet'
    )
    ax1.contour(
        Z * 1e3, X * 1e3, E_no_opt,
        levels=12, colors='k', linewidths=0.3, alpha=0.35
    )
    # Paredes
    ax1.add_patch(Rectangle(
        (0, 0), d * 1e3, a * 1e3,
        fill=False, edgecolor='black', linewidth=2.5
    ))
    # Sonda
    dibujar_sonda(
        ax1,
        x_pos=d * 1e3 * 0.92,
        y_top=a * 1e3 + 5,
        y_bottom=a * 1e3 * 0.5,
        escala=1.0
    )
    ax1.set_xlim(-2, d * 1e3 + 2)
    ax1.set_ylim(-2, a * 1e3 + 8)
    ax1.set_ylabel('x (mm)', fontsize=11)
    ax1.set_title(
        'Transferencia NO óptima — campo irregular (multimodo)',
        fontsize=12, fontweight='bold'
    )
    ax1.set_aspect('equal')
    ax1.tick_params(labelbottom=False)

    # --------------------------------------------------------
    # PANEL INFERIOR: ÓPTIMA
    # --------------------------------------------------------
    cf2 = ax2.contourf(
        Z * 1e3, X * 1e3, E_opt,
        levels=60, cmap='jet'
    )
    ax2.contour(
        Z * 1e3, X * 1e3, E_opt,
        levels=12, colors='k', linewidths=0.3, alpha=0.35
    )
    ax2.add_patch(Rectangle(
        (0, 0), d * 1e3, a * 1e3,
        fill=False, edgecolor='black', linewidth=2.5
    ))
    dibujar_sonda(
        ax2,
        x_pos=d * 1e3 * 0.92,
        y_top=a * 1e3 + 5,
        y_bottom=a * 1e3 * 0.5,
        escala=1.0
    )
    ax2.set_xlim(-2, d * 1e3 + 2)
    ax2.set_ylim(-2, a * 1e3 + 8)
    ax2.set_xlabel('z (mm)', fontsize=11)
    ax2.set_ylabel('x (mm)', fontsize=11)
    ax2.set_title(
        'Transferencia ÓPTIMA — modo TE$_{10}$ dominante',
        fontsize=12, fontweight='bold'
    )
    ax2.set_aspect('equal')

    # --------------------------------------------------------
    # Barra de color compartida
    # --------------------------------------------------------
    cbar = fig.colorbar(
        cf1, ax=[ax1, ax2],
        orientation='vertical',
        fraction=0.025, pad=0.02
    )
    cbar.set_label('E$_y$ (u.a.)', fontsize=11)

    # --------------------------------------------------------
    # Guardar
    # --------------------------------------------------------
    plt.savefig(
        'transferencia_optima_vs_no_optima.png',
        dpi=200, facecolor='white', bbox_inches='tight'
    )
    plt.show()


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("Generando figura comparativa...")
    generar_figura()
    print("✅ Imagen guardada: transferencia_optima_vs_no_optima.png")