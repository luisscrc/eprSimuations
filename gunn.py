import matplotlib.pyplot as plt
import numpy as np

# =========================================================
# PARÁMETROS FÍSICOS DEL DIODO GUNN
# =========================================================
V_umbral = 3.0
V_RDN_ini = 3.0
V_RDN_fin = 6.0
I_pico = 1.0
I_valle = 0.4

# =========================================================
# FIGURA CON DOS SUBPLOTS
# =========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# =========================================================
# PANEL 1: CURVA I–V DEL DIODO GUNN
# =========================================================
V = np.linspace(0, 10, 500)

I = np.where(V < V_umbral, 0.3 * V, 0)

mascara_rdn = (V >= V_RDN_ini) & (V <= V_RDN_fin)
V_rdn = V[mascara_rdn]
t = (V_rdn - V_RDN_ini) / (V_RDN_fin - V_RDN_ini)
I_rdn = I_pico - (I_pico - I_valle) * (3*t**2 - 2*t**3)
I[mascara_rdn] = I_rdn

mascara_post = V > V_RDN_fin
I[mascara_post] = I_valle + 0.15 * (V[mascara_post] - V_RDN_fin)

ax1.plot(V, I, color="#6E162E", linewidth=3, zorder=3)

ax1.axvspan(V_RDN_ini, V_RDN_fin, color="#B43C5A", alpha=0.18, zorder=1)
ax1.text((V_RDN_ini + V_RDN_fin)/2, 0.15,
         "Región de\nresistencia\ndiferencial\nnegativa (RDN)",
         ha="center", va="bottom",
         fontsize=14, fontweight="bold", color="#6E162E")

ax1.axvline(V_umbral, color="#333333", linestyle="--", linewidth=1.5)
ax1.text(V_umbral + 0.15, 1.15, "Umbral $V_{th}$",
         fontsize=15, fontweight="bold", color="#333333")

ax1.axhline(I_pico, color="#333333", linestyle=":", linewidth=1.2)
ax1.text(0.2, I_pico + 0.03, "$I_{pico}$",
         fontsize=14, color="#333333")

ax1.axhline(I_valle, color="#333333", linestyle=":", linewidth=1.2)
ax1.text(0.2, I_valle + 0.03, "$I_{valle}$",
         fontsize=14, color="#333333")

ax1.annotate("", xy=(V_RDN_ini + 0.3, I_pico - 0.02),
             xytext=(V_RDN_fin - 0.3, I_valle + 0.02),
             arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#B43C5A"))
ax1.text(4.6, 0.75, r"$\frac{dI}{dV} < 0$",
         fontsize=18, fontweight="bold", color="#B43C5A")

ax1.set_xlabel("Voltaje aplicado  $V$  (V)",
               fontsize=17, fontweight="bold")
ax1.set_ylabel("Corriente  $I$  (u.a.)",
               fontsize=17, fontweight="bold")
# ax1.set_title(...)   ← TÍTULO ELIMINADO
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 1.4)
ax1.grid(True, linestyle="--", alpha=0.4)
ax1.tick_params(axis="both", labelsize=15)

# =========================================================
# PANEL 2: PULSOS DE CORRIENTE — SOLO 5 DOMINIOS
# =========================================================
N_DOMINIOS = 5
f_osc = N_DOMINIOS
t_max = N_DOMINIOS / f_osc
t = np.linspace(0, t_max, 1500)

periodo = 1 / f_osc

t_mod = np.mod(t, periodo) / periodo
I_pulsos = 0.5 + 0.45 * np.exp(-3*t_mod) * np.cos(2*np.pi*t_mod)

I_microondas = 0.05 * np.sin(2*np.pi*20*t)

I_total = I_pulsos + I_microondas

ax2.plot(t, I_total, color="#6E162E", linewidth=2.5, zorder=3)

for k in range(N_DOMINIOS):
    t_pulso = k * periodo
    ax2.axvline(t_pulso, color="#B43C5A", linestyle=":",
                linewidth=1.5, alpha=0.7)
    ax2.text(t_pulso + 0.005, 1.05, f"dominio {k+1}",
             fontsize=14, color="#B43C5A", rotation=90,
             va="bottom")

ax2.text(t_max/2, 0.22,
         r"$f \approx \dfrac{v_d}{L}$" + "\n\n" +
         r"$v_d$: velocidad de deriva" + "\n" +
         r"$L$: longitud del semiconductor",
         fontsize=17, fontweight="bold",
         color="#6E162E",
         ha="center", va="center",
         bbox=dict(boxstyle="round,pad=0.5",
                   facecolor="#F5F5F5",
                   edgecolor="#6E162E",
                   linewidth=2))

ax2.set_xlabel("Tiempo  $t$  (u.a.)",
               fontsize=17, fontweight="bold")
ax2.set_ylabel("Corriente  $I$  (u.a.)",
               fontsize=17, fontweight="bold")
# ax2.set_title(...)   ← TÍTULO ELIMINADO
ax2.set_xlim(0, t_max)
ax2.set_ylim(0, 1.15)
ax2.grid(True, linestyle="--", alpha=0.4)
ax2.tick_params(axis="both", labelsize=15)

# =========================================================
# SIN TÍTULO GENERAL
# =========================================================
# fig.suptitle(...)   ← TÍTULO GENERAL ELIMINADO

plt.tight_layout()
plt.savefig("diodo_gunn.png", dpi=200, bbox_inches="tight")
plt.show()