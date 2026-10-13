import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.image as mpimg
import os

# =========================================================
# RUTAS DE LAS IMÁGENES
# =========================================================
IMG_RPI5 = r"C:\Users\aesca\OneDrive - Instituto Politecnico Nacional\DOCUMENTOS\MAESTRÍA ESFM\Tercer semestre\POSTER CNF\pi 5.png"
IMG_PICO = r"C:\Users\aesca\OneDrive - Instituto Politecnico Nacional\DOCUMENTOS\MAESTRÍA ESFM\Tercer semestre\POSTER CNF\pico.jpg"

# =========================================================
# CONFIGURACIÓN DE LA FIGURA
# =========================================================
fig, ax = plt.subplots(figsize=(20, 9))
ax.set_xlim(0, 20)
ax.set_ylim(0, 9)
ax.axis("off")
fig.patch.set_facecolor("white")

COLOR_BORDE  = "#000000"
COLOR_TEXTO  = "#000000"
COLOR_SOMBRA = "#CCCCCC"
LW = 2.5

# =========================================================
# FUNCIÓN: caja redondeada con imagen centrada
# =========================================================
def caja_imagen(x, y, w, h, ruta_imagen,
                color_borde=COLOR_BORDE,
                padding=0.15,
                sombra=True):
    if sombra:
        sombra_box = FancyBboxPatch(
            (x + 0.08, y - 0.08), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.25",
            linewidth=0,
            facecolor=COLOR_SOMBRA,
            alpha=0.5,
            zorder=1,
        )
        ax.add_patch(sombra_box)

    caja = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.25",
        linewidth=LW,
        edgecolor=color_borde,
        facecolor="white",
        zorder=2,
    )
    ax.add_patch(caja)

    if os.path.exists(ruta_imagen):
        try:
            img = mpimg.imread(ruta_imagen)
            ax.imshow(img,
                      extent=(x + padding,
                              x + w - padding,
                              y + padding,
                              y + h - padding),
                      aspect="auto",
                      zorder=3)
        except Exception as e:
            print(f"Error al cargar {ruta_imagen}: {e}")
            ax.text(x + w/2, y + h/2, "[img]",
                    ha="center", va="center",
                    fontsize=12, color="gray",
                    style="italic", zorder=3)
    else:
        print(f"No se encontró el archivo: {ruta_imagen}")
        ax.text(x + w/2, y + h/2, "[img]",
                ha="center", va="center",
                fontsize=12, color="gray",
                style="italic", zorder=3)


# =========================================================
# FUNCIÓN: caja redondeada con solo texto
# =========================================================
def caja_texto(x, y, w, h, texto, tam_texto=24,
               color_borde=COLOR_BORDE,
               color_fondo="white",
               color_texto=COLOR_TEXTO,
               sombra=True):
    if sombra:
        sombra_box = FancyBboxPatch(
            (x + 0.08, y - 0.08), w, h,
            boxstyle="round,pad=0.02,rounding_size=0.25",
            linewidth=0,
            facecolor=COLOR_SOMBRA,
            alpha=0.5,
            zorder=1,
        )
        ax.add_patch(sombra_box)

    caja = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.25",
        linewidth=LW,
        edgecolor=color_borde,
        facecolor=color_fondo,
        zorder=2,
    )
    ax.add_patch(caja)

    ax.text(x + w/2, y + h/2, texto,
            ha="center", va="center",
            fontsize=tam_texto, fontweight="bold",
            color=color_texto, zorder=3)


# =========================================================
# DIMENSIONES Y POSICIONES
# =========================================================

# --- Raspberry Pi 5 (MÁS GRANDE) ---
x_rpi5, y_rpi5 = 0.4, 2.6      # ← posición ajustada
w_rpi5, h_rpi5 = 5.5, 3.6      # ← antes 4.5 × 2.2  →  ahora 5.5 × 3.6

# --- Raspberry Pico ×3 ---
x_pico, w_pico, h_pico = 7.0, 4.2, 1.6
y_pico_1 = 6.2
y_pico_2 = 3.6
y_pico_3 = 1.0

# --- Bloques de función ---
x_func, w_func, h_func = 12.4, 7.2, 2.0
y_func_1 = 6.0
y_func_2 = 3.4
y_func_3 = 0.8

# =========================================================
# DIBUJAR BLOQUES
# =========================================================

# Raspberry Pi 5 (solo imagen, más grande)
caja_imagen(x_rpi5, y_rpi5, w_rpi5, h_rpi5, IMG_RPI5)

# Raspberry Pico ×3
caja_imagen(x_pico, y_pico_1, w_pico, h_pico, IMG_PICO)
caja_imagen(x_pico, y_pico_2, w_pico, h_pico, IMG_PICO)
caja_imagen(x_pico, y_pico_3, w_pico, h_pico, IMG_PICO)

# Bloques de función
caja_texto(x_func, y_func_1, w_func, h_func,
           "Alimentación y\nprotecciones",
           tam_texto=26)

caja_texto(x_func, y_func_2, w_func, h_func,
           "Sistema de\nrefrigeración",
           tam_texto=26)

caja_texto(x_func, y_func_3, w_func, h_func,
           "Barrido y sensado del\ncampo magnético",
           tam_texto=26)

# =========================================================
# FLECHAS
# =========================================================
def flecha(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-",
        linewidth=LW,
        color=COLOR_BORDE,
        zorder=1,
    ))

# Pi 5 → cada Pico
flecha(x_rpi5 + w_rpi5*0.5, y_rpi5 + h_rpi5,
       x_pico, y_pico_1 + h_pico*0.5)               # arriba
flecha(x_rpi5 + w_rpi5, y_rpi5 + h_rpi5*0.55,
       x_pico, y_pico_2 + h_pico*0.5)               # medio
flecha(x_rpi5 + w_rpi5*0.5, y_rpi5,
       x_pico, y_pico_3 + h_pico*0.5)               # abajo

# Cada Pico → su bloque
flecha(x_pico + w_pico, y_pico_1 + h_pico*0.5,
       x_func, y_func_1 + h_func*0.5)
flecha(x_pico + w_pico, y_pico_2 + h_pico*0.5,
       x_func, y_func_2 + h_func*0.5)
flecha(x_pico + w_pico, y_pico_3 + h_pico*0.5,
       x_func, y_func_3 + h_func*0.5)

# =========================================================
# GUARDAR
# =========================================================
plt.tight_layout()
plt.savefig("diagrama_raspberry.png",
            dpi=200, bbox_inches="tight",
            facecolor="white")
plt.show()