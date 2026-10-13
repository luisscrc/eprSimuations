"""
Visualización 3D de los campos E y H en los modos TE10 y TM11
de una guía rectangular WR-90.

- TE10: E sale del plano (E_z = 0), H en el plano.
- TM11: H sale del plano (H_z = 0), E en el plano.

Usa quiver3d para mostrar los vectores de campo en cada punto.
Se usa f = 20 GHz para que ambos modos sean propagantes.

Requisitos:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.lines import Line2D

# ============================================================
# PARÁMETROS FÍSICOS (guía WR-90)
# ============================================================
a = 22.86e-3
b = 10.16e-3
d = 50e-3        # longitud de la guía
f = 20e9         # 20 GHz → ambos modos propagantes
c = 299792458.0
mu0 = 4 * np.pi * 1e-7
eps0 = 1 / (mu0 * c**2)

omega = 2 * np.pi * f
k0 = omega / c

# Números de onda de corte
kc_te10 = np.pi / a
kc_tm11 = np.sqrt((np.pi / a)**2 + (np.pi / b)**2)

# Frecuencias de corte
fc_te10 = c / (2 * a)
fc_tm11 = c / 2 * np.sqrt((1 / a)**2 + (1 / b)**2)

# Constantes de propagación
beta_te10 = np.sqrt(k0**2 - kc_te10**2)
beta_tm11 = np.sqrt(k0**2 - kc_tm11**2)

# ============================================================
# MALLA 3D
# ============================================================
nx, ny, nz = 6, 4, 15
x = np.linspace(0.05 * a, 0.95 * a, nx)
y = np.linspace(0.05 * b, 0.95 * b, ny)
z = np.linspace(0, d, nz)
X, Y, Z = np.meshgrid(x, y, z, indexing='ij')

# ============================================================
# CAMPOS (parte real, t = 0)
# ============================================================
# --- TE10: E_z = 0 ---
Ey_te = np.sin(np.pi * X / a) * np.cos(beta_te10 * Z)
Ex_te = np.zeros_like(X)
Ez_te = np.zeros_like(X)
Hx_te = -(beta_te10 / (omega * mu0)) * np.sin(np.pi * X / a) * np.cos(beta_te10 * Z)
Hy_te = np.zeros_like(X)
Hz_te = (np.pi / (a * omega * mu0)) * np.cos(np.pi * X / a) * np.sin(beta_te10 * Z)

# --- TM11: H_z = 0 ---
Ez_tm = np.sin(np.pi * X / a) * np.sin(np.pi * Y / b) * np.cos(beta_tm11 * Z)
Ex_tm = (beta_tm11 / kc_tm11**2) * (np.pi / a) * np.cos(np.pi * X / a) * np.sin(np.pi * Y / b) * np.sin(beta_tm11 * Z)
Ey_tm = (beta_tm11 / kc_tm11**2) * (np.pi / b) * np.sin(np.pi * X / a) * np.cos(np.pi * Y / b) * np.sin(beta_tm11 * Z)
Hx_tm = (omega * eps0 / kc_tm11**2) * (np.pi / b) * np.sin(np.pi * X / a) * np.cos(np.pi * Y / b) * np.sin(beta_tm11 * Z)
Hy_tm = -(omega * eps0 / kc_tm11**2) * (np.pi / a) * np.cos(np.pi * X / a) * np.sin(np.pi * Y / b) * np.sin(beta_tm11 * Z)
Hz_tm = np.zeros_like(X)


# ============================================================
# UTILIDADES
# ============================================================
def normalize(U, V, W):
    """Normaliza un campo vectorial por su magnitud máxima."""
    mag = np.sqrt(U**2 + V**2 + W**2)
    mag_max = np.max(mag)
    if mag_max > 0:
        return U / mag_max, V / mag_max, W / mag_max
    return U, V, W


def draw_walls(ax):
    """Dibuja las paredes de la guía como wireframe."""
    corners = np.array([
        [0, 0, 0], [a, 0, 0], [a, b, 0], [0, b, 0],
        [0, 0, d], [a, 0, d], [a, b, d], [0, b, d]
    ]) * 1e3
    edges = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    for i, j in edges:
        ax.plot3D(
            [corners[i,0], corners[j,0]],
            [corners[i,1], corners[j,1]],
            [corners[i,2], corners[j,2]],
            color='gray', linewidth=1.5, alpha=0.6
        )


# ============================================================
# FIGURA
# ============================================================
fig = plt.figure(figsize=(18, 9), facecolor='white')

ARROW_LENGTH = 3.5

# ============================================================
# SUBPLOT 1: TE10
# ============================================================
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
draw_walls(ax1)

Exn, Eyn, Ezn = normalize(Ex_te, Ey_te, Ez_te)
Hxn, Hyn, Hzn = normalize(Hx_te, Hy_te, Hz_te)

# Campo E (rojo)
ax1.quiver(X * 1e3, Y * 1e3, Z * 1e3,
           Exn, Eyn, Ezn,
           color='red', length=ARROW_LENGTH,
           normalize=False, arrow_length_ratio=0.35,
           linewidth=0.9, alpha=0.85)

# Campo H (azul)
ax1.quiver(X * 1e3, Y * 1e3, Z * 1e3,
           Hxn, Hyn, Hzn,
           color='blue', length=ARROW_LENGTH,
           normalize=False, arrow_length_ratio=0.35,
           linewidth=0.9, alpha=0.7)

ax1.set_xlabel('x (mm)', fontsize=12)
ax1.set_ylabel('y (mm)', fontsize=12)
ax1.set_zlabel('z (mm)', fontsize=12)
ax1.set_title(r'TE$_{10}$  ($E_z = 0$)', fontsize=22,
              fontweight='bold', color='#1F4E79', pad=15)
ax1.set_box_aspect([1, 0.5, 3])
ax1.view_init(elev=25, azim=-50)

# ============================================================
# SUBPLOT 2: TM11
# ============================================================
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
draw_walls(ax2)

Exn, Eyn, Ezn = normalize(Ex_tm, Ey_tm, Ez_tm)
Hxn, Hyn, Hzn = normalize(Hx_tm, Hy_tm, Hz_tm)

# Campo E (rojo)
ax2.quiver(X * 1e3, Y * 1e3, Z * 1e3,
           Exn, Eyn, Ezn,
           color='red', length=ARROW_LENGTH,
           normalize=False, arrow_length_ratio=0.35,
           linewidth=0.9, alpha=0.85)

# Campo H (azul)
ax2.quiver(X * 1e3, Y * 1e3, Z * 1e3,
           Hxn, Hyn, Hzn,
           color='blue', length=ARROW_LENGTH,
           normalize=False, arrow_length_ratio=0.35,
           linewidth=0.9, alpha=0.7)

ax2.set_xlabel('x (mm)', fontsize=12)
ax2.set_ylabel('y (mm)', fontsize=12)
ax2.set_zlabel('z (mm)', fontsize=12)
ax2.set_title(r'TM$_{11}$  ($H_z = 0$)', fontsize=22,
              fontweight='bold', color='#B71C1C', pad=15)
ax2.set_box_aspect([1, 0.5, 3])
ax2.view_init(elev=25, azim=-50)

# ============================================================
# LEYENDA GLOBAL
# ============================================================
legend_elements = [
    Line2D([0], [0], color='red', linewidth=2.5, label='Campo E'),
    Line2D([0], [0], color='blue', linewidth=2.5, label='Campo H'),
]
fig.legend(handles=legend_elements, loc='lower center',
           ncol=2, fontsize=16, frameon=False, bbox_to_anchor=(0.5, 0.0))

# ============================================================
# GUARDAR
# ============================================================
plt.tight_layout(rect=[0, 0.05, 1, 1])
plt.savefig('modos_TE10_TM11_3D_campos.png', dpi=200,
            bbox_inches='tight', facecolor='white')
plt.show()

# ============================================================
# RESUMEN
# ============================================================
print(f"Frecuencia de operación: {f/1e9:.1f} GHz")
print(f"fc TE10 = {fc_te10/1e9:.2f} GHz → PROPAGANTE")
print(f"fc TM11 = {fc_tm11/1e9:.2f} GHz → PROPAGANTE")
print()
print("Propiedades físicas respetadas:")
print("  TE10: Ez = 0 → E perpendicular al eje de propagación")
print("  TM11: Hz = 0 → H perpendicular al eje de propagación")
print()
print("Imagen guardada: modos_TE10_TM11_3D_campos.png")