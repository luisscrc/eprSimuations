"""
Gráfica del protocolo CAN como trenes de pulsos.

Panel superior:
    CAN_High / CAN_Low

Panel inferior:
    Driver Logic

Características:
    - Pulsos cuadrados.
    - Sin dientes de sierra.
    - CAN_High y CAN_Low complementarios durante bits dominantes.
    - Eje X compartido.
    - Límites de bit claramente visibles.
    - Patrón binario mostrado sobre la señal.
    - Diferencia entre estado dominante y recesivo.

Requisitos:
    pip install numpy matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# PARÁMETROS
# ============================================================

V_RECESSIVE = 2.5
V_DOM_HIGH = 3.75
V_DOM_LOW = 1.25

# 0 = Recessive
# 1 = Dominant
bit_pattern = [
    0, 1, 1, 1, 0, 1, 1, 1,
    0, 1, 1, 0, 1, 1, 1, 0,
    1, 1, 1, 0, 1, 1
]

BIT_DURATION = 1.0


# ============================================================
# CONSTRUIR SEÑALES CAN
# ============================================================

def build_can_signals(pattern, bit_duration):
    """
    Construye CAN_High y CAN_Low como trenes de pulsos.

    0 -> Recessive:
         CAN_High = 2.5 V
         CAN_Low  = 2.5 V

    1 -> Dominant:
         CAN_High = 3.75 V
         CAN_Low  = 1.25 V
    """

    t = np.arange(len(pattern) + 1) * bit_duration

    can_high = []
    can_low = []

    for bit in pattern:

        if bit == 1:
            can_high.append(V_DOM_HIGH)
            can_low.append(V_DOM_LOW)

        else:
            can_high.append(V_RECESSIVE)
            can_low.append(V_RECESSIVE)

    # Repetir el último valor para que step() cierre correctamente
    can_high.append(can_high[-1])
    can_low.append(can_low[-1])

    return t, np.array(can_high), np.array(can_low)


# ============================================================
# DRIVER LOGIC
# ============================================================

def build_driver_logic(pattern, bit_duration):

    t = np.arange(len(pattern) + 1) * bit_duration

    driver = [
        2.5 if bit == 1 else 0.0
        for bit in pattern
    ]

    driver.append(driver[-1])

    return t, np.array(driver)


# ============================================================
# GRAFICAR
# ============================================================

def plot_can_protocol():

    t_can, can_high, can_low = build_can_signals(
        bit_pattern,
        BIT_DURATION
    )

    t_drv, driver = build_driver_logic(
        bit_pattern,
        BIT_DURATION
    )

    n_bits = len(bit_pattern)

    # ========================================================
    # FIGURA
    # ========================================================

    fig, (ax1, ax2) = plt.subplots(
        2,
        1,
        figsize=(17, 9),
        sharex=True,
        facecolor="white",
        gridspec_kw={
            "height_ratios": [2, 1],
            "hspace": 0.08
        }
    )

    # ========================================================
    # PANEL SUPERIOR
    # CAN HIGH / CAN LOW
    # ========================================================

    ax1.step(
        t_can,
        can_high,
        where="post",
        color="#F5A623",
        linewidth=3,
        label=""
    )

    ax1.step(
        t_can,
        can_low,
        where="post",
        color="#2E86DE",
        linewidth=3,
        label=""
    )

    # Línea de tensión recesiva
    ax1.axhline(
        V_RECESSIVE,
        color="gray",
        linestyle="--",
        linewidth=1.3,
        alpha=0.7
    )

    # ========================================================
    # LÍMITES DE LOS BITS
    # ========================================================

    for i in range(n_bits + 1):

        ax1.axvline(
            i * BIT_DURATION,
            color="gray",
            linestyle=":",
            linewidth=0.8,
            alpha=0.35
        )

        ax2.axvline(
            i * BIT_DURATION,
            color="gray",
            linestyle=":",
            linewidth=0.8,
            alpha=0.35
        )

    # ========================================================
    # NÚMERO DE BIT
    # ========================================================

    for i, bit in enumerate(bit_pattern):

        x_center = i * BIT_DURATION + BIT_DURATION / 2

        ax1.text(
            x_center,
            4.35,
            f"{bit}",
            ha="center",
            va="center",
            fontsize=14,
            fontweight="bold"
        )

        ax2.text(
            x_center,
            2.82,
            f"{bit}",
            ha="center",
            va="center",
            fontsize=13,
            fontweight="bold"
        )

    # ========================================================
    # CONFIGURACIÓN PANEL SUPERIOR
    # ========================================================

    ax1.set_ylim(0.7, 4.7)

    ax1.set_yticks([
        V_DOM_LOW,
        V_RECESSIVE,
        V_DOM_HIGH
    ])

    ax1.set_yticklabels([
        "1.25 V",
        "2.50 V",
        "3.75 V"
    ], fontsize=13)

    ax1.set_ylabel(
        "Señal referencia diferencial",
        color="#F5A623",
        fontsize=17,
        fontweight="bold"
        )

    ax1.tick_params(
        axis="y",
        length=7,
        width=2
    )

    ax1.set_title(
        "CAN Message Signal",
        fontsize=23,
        fontweight="bold",
        color="#6A1B9A",
        pad=18
    )

    # ========================================================
    # ETIQUETAS CAN
    # ========================================================

    ax1.text(
        0.25,
        V_DOM_HIGH + 0.12,
        "",
        color="#F5A623",
        fontsize=15,
        fontweight="bold"
    )

    ax1.text(
        0.25,
        V_DOM_LOW - 0.22,
        "",
        color="#2E86DE",
        fontsize=15,
        fontweight="bold"
    )

    # ========================================================
    # ESTADO DOMINANTE
    # ========================================================

    ax1.annotate(
        "",
        xy=(0.30, V_DOM_HIGH),
        xytext=(0.30, V_DOM_LOW),
        arrowprops=dict(
            arrowstyle="<->",
            color="#E67E22",
            linewidth=2.5
        )
    )

    ax1.text(
        0.48,
        2.5,
        "",
        color="#E67E22",
        fontsize=13,
        fontweight="bold",
        va="center"
    )

    # ========================================================
    # ESTADO RECESIVO
    # ========================================================

    ax1.text(
        0.25,
        2.63,
        "",
        color="gray",
        fontsize=12,
        fontweight="bold"
    )

    # ========================================================
    # LEYENDA
    # ========================================================

    ax1.legend(
        loc="upper right",
        fontsize=12,
        frameon=False
    )

    # ========================================================
    # PANEL INFERIOR
    # DRIVER LOGIC
    # ========================================================

    ax2.step(
        t_drv,
        driver,
        where="post",
        color="#27AE60",
        linewidth=3,
        label=""
    )

    ax2.set_ylim(-0.3, 3.2)

    ax2.set_yticks([
        0,
        2.5
    ])

    ax2.set_yticklabels([
        "0 V",
        "2.5 V"
    ], fontsize=13)

    ax2.set_ylabel(
        "Señal referencia a cero",
        color="#27AE60",
        fontsize=17,
        fontweight="bold"
    )

    ax2.set_xlabel(
        "Bit Time",
        fontsize=16,
        fontweight="bold"
    )

    ax2.tick_params(
        axis="both",
        length=7,
        width=2
    )

    ax2.legend(
        loc="upper right",
        fontsize=12,
        frameon=False
    )

    # ========================================================
    # EJE X
    # ========================================================

    ax2.set_xlim(
        0,
        n_bits * BIT_DURATION
    )

    ax2.set_xticks(
        np.arange(n_bits + 1)
    )

    ax2.set_xticklabels(
        [
            str(i)
            for i in range(n_bits + 1)
        ],
        fontsize=11
    )

    # ========================================================
    # ELIMINAR SPINES SUPERIORES
    # ========================================================

    for ax in [ax1, ax2]:

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.spines["left"].set_linewidth(2)

    ax2.spines["bottom"].set_linewidth(2)

    # ========================================================
    # TÍTULO GENERAL
    # ========================================================

    fig.suptitle(
        "CAN Bus — Tren de pulsos diferencial",
        fontsize=25,
        fontweight="bold",
        y=0.98
    )

    # ========================================================
    # GUARDAR
    # ========================================================

    plt.savefig(
        "can_protocol_pulse_train.png",
        dpi=300,
        facecolor="white",
        bbox_inches="tight"
    )

    plt.show()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("Generando tren de pulsos CAN...")

    plot_can_protocol()

    print(
        "✓ Imagen guardada como: "
        "can_protocol_pulse_train.png"
    )