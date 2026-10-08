"""
simulacion guia de ondas 3D.py

Visualización 3D interactiva de modos electromagnéticos TE/TM
en una guía de onda rectangular y una cavidad resonante.

Requisitos:
    pip install PyQt6 pyqtgraph numpy

Características:
- Guía rectangular / cavidad rectangular.
- Modos TE y TM.
- Vista 3D de las paredes conductoras.
- Flechas/vector field de E y H.
- Animación temporal de los campos.
- Frecuencia de corte y frecuencia resonante.
- Dimensiones configurables.
- Vista transversal o longitudinal.

Nota:
La guía rectangular hueca convencional no soporta TEM.
TEM se muestra solamente como referencia conceptual.
"""

import sys
import numpy as np

from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl


C = 299_792_458.0


# ============================================================
# MODOS
# ============================================================

def parse_mode(mode):
    kind = mode[:2].upper()
    numbers = mode[2:]

    if len(numbers) == 2:
        m = int(numbers[0])
        n = int(numbers[1])
        l = 0
    elif len(numbers) == 3:
        m = int(numbers[0])
        n = int(numbers[1])
        l = int(numbers[2])
    else:
        m = n = l = 0

    return kind, m, n, l


def cutoff_frequency(mode, a, b):
    kind, m, n, _ = parse_mode(mode)

    if kind == "TEM":
        return 0.0

    return C / 2 * np.sqrt(
        (m / a) ** 2 +
        (n / b) ** 2
    )


def cavity_frequency(mode, a, b, d):
    kind, m, n, l = parse_mode(mode)

    if kind == "TEM":
        return 0.0

    return C / 2 * np.sqrt(
        (m / a) ** 2 +
        (n / b) ** 2 +
        (l / d) ** 2
    )


# ============================================================
# VENTANA
# ============================================================

class Waveguide3D(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Simulación 3D - Modos TE/TM en guía y cavidad"
        )

        self.resize(1500, 950)

        # Dimensiones normalizadas para la visualización
        self.a = 22.86
        self.b = 10.16
        self.d = 45.72

        self.frequency = 10.0e9

        self.phase = 0.0

        self.Nx = 7
        self.Ny = 5
        self.Nz = 9

        # ====================================================
        # CENTRAL
        # ====================================================

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)

        main = QtWidgets.QHBoxLayout(central)

        # ====================================================
        # CONTROLES
        # ====================================================

        panel = QtWidgets.QVBoxLayout()

        panel.addWidget(
            QtWidgets.QLabel("<b>GEOMETRÍA</b>")
        )

        self.geometry = QtWidgets.QComboBox()

        self.geometry.addItems([
            "Guía de onda rectangular",
            "Cavidad resonante rectangular"
        ])

        panel.addWidget(self.geometry)

        # ----------------------------------------------------

        panel.addWidget(
            QtWidgets.QLabel("<b>MODO</b>")
        )

        self.mode = QtWidgets.QComboBox()

        self.mode.addItems([
            "TE10",
            "TE20",
            "TE01",
            "TE11",
            "TE21",
            "TM11",
            "TM21"
        ])

        panel.addWidget(self.mode)

        # ----------------------------------------------------

        panel.addWidget(
            QtWidgets.QLabel("<b>CAMPO A MOSTRAR</b>")
        )

        self.field = QtWidgets.QComboBox()

        self.field.addItems([
            "E y H",
            "E",
            "H"
        ])

        panel.addWidget(self.field)

        # ----------------------------------------------------

        panel.addWidget(
            QtWidgets.QLabel("<b>FRECUENCIA</b>")
        )

        self.freq = QtWidgets.QDoubleSpinBox()

        self.freq.setRange(
            0.1,
            100.0
        )

        self.freq.setDecimals(3)
        self.freq.setSingleStep(0.1)
        self.freq.setValue(10.0)
        self.freq.setSuffix(" GHz")

        panel.addWidget(self.freq)

        # ----------------------------------------------------
        # DIMENSIONES
        # ----------------------------------------------------

        panel.addWidget(
            QtWidgets.QLabel("<b>DIMENSIONES</b>")
        )

        self.a_spin = self.dimension_spin(
            self.a
        )

        self.b_spin = self.dimension_spin(
            self.b
        )

        self.d_spin = self.dimension_spin(
            self.d
        )

        grid = QtWidgets.QGridLayout()

        grid.addWidget(
            QtWidgets.QLabel("a"),
            0,
            0
        )

        grid.addWidget(
            self.a_spin,
            0,
            1
        )

        grid.addWidget(
            QtWidgets.QLabel("b"),
            1,
            0
        )

        grid.addWidget(
            self.b_spin,
            1,
            1
        )

        grid.addWidget(
            QtWidgets.QLabel("d"),
            2,
            0
        )

        grid.addWidget(
            self.d_spin,
            2,
            1
        )

        panel.addLayout(grid)

        # ----------------------------------------------------

        self.animation = QtWidgets.QCheckBox(
            "Animar campos"
        )

        self.animation.setChecked(True)

        panel.addWidget(
            self.animation
        )

        # ----------------------------------------------------

        self.show_walls = QtWidgets.QCheckBox(
            "Mostrar paredes conductoras"
        )

        self.show_walls.setChecked(True)

        panel.addWidget(
            self.show_walls
        )

        # ----------------------------------------------------

        self.info = QtWidgets.QTextEdit()

        self.info.setReadOnly(True)

        self.info.setMinimumHeight(
            250
        )

        panel.addWidget(
            self.info
        )

        panel.addStretch()

        main.addLayout(
            panel,
            1
        )

        # ====================================================
        # VISTA 3D
        # ====================================================

        self.view = gl.GLViewWidget()

        self.view.setCameraPosition(
            distance=85,
            elevation=25,
            azimuth=45
        )

        self.view.setBackgroundColor(
            (15, 15, 20)
        )

        main.addWidget(
            self.view,
            4
        )

        # ====================================================
        # EJES
        # ====================================================

        self.axis = gl.GLAxisItem()

        self.axis.setSize(
            x=40,
            y=40,
            z=40
        )

        self.view.addItem(
            self.axis
        )

        # ====================================================
        # OBJETOS 3D
        # ====================================================

        self.wall_items = []
        self.e_items = []
        self.h_items = []

        # ====================================================
        # TIMER
        # ====================================================

        self.timer = QtCore.QTimer()

        self.timer.timeout.connect(
            self.animate
        )

        self.timer.start(
            80
        )

        # ====================================================
        # SEÑALES
        # ====================================================

        self.geometry.currentIndexChanged.connect(
            self.geometry_changed
        )

        self.mode.currentIndexChanged.connect(
            self.update_scene
        )

        self.field.currentIndexChanged.connect(
            self.update_scene
        )

        self.freq.valueChanged.connect(
            self.frequency_changed
        )

        self.a_spin.valueChanged.connect(
            self.dimension_changed
        )

        self.b_spin.valueChanged.connect(
            self.dimension_changed
        )

        self.d_spin.valueChanged.connect(
            self.dimension_changed
        )

        self.show_walls.stateChanged.connect(
            self.update_scene
        )

        # ====================================================
        # INICIO
        # ====================================================

        self.geometry_changed()

    # ========================================================
    # WIDGET
    # ========================================================

    @staticmethod
    def dimension_spin(value):

        spin = QtWidgets.QDoubleSpinBox()

        spin.setRange(
            1,
            500
        )

        spin.setDecimals(
            2
        )

        spin.setValue(
            value
        )

        spin.setSuffix(
            " mm"
        )

        return spin

    # ========================================================
    # GEOMETRÍA
    # ========================================================

    def geometry_changed(self):

        if self.geometry.currentIndex() == 0:

            self.mode.clear()

            self.mode.addItems([
                "TE10",
                "TE20",
                "TE01",
                "TE11",
                "TE21",
                "TM11",
                "TM21"
            ])

        else:

            self.mode.clear()

            self.mode.addItems([
                "TE101",
                "TE102",
                "TE111",
                "TE201",
                "TM110",
                "TM111",
                "TM211"
            ])

        self.update_scene()

    # ========================================================
    # PARÁMETROS
    # ========================================================

    def update_parameters(self):

        self.a = self.a_spin.value()
        self.b = self.b_spin.value()
        self.d = self.d_spin.value()

        self.frequency = (
            self.freq.value() * 1e9
        )

    def frequency_changed(self):

        self.update_parameters()
        self.update_scene()

    def dimension_changed(self):

        self.update_parameters()
        self.update_scene()

    # ========================================================
    # CAMPOS
    # ========================================================

    def field_vectors(self):

        self.update_parameters()

        mode = self.mode.currentText()

        kind, m, n, l = parse_mode(
            mode
        )

        # Coordenadas normalizadas

        x = np.linspace(
            0.05,
            0.95,
            self.Nx
        )

        y = np.linspace(
            0.05,
            0.95,
            self.Ny
        )

        z = np.linspace(
            0.05,
            0.95,
            self.Nz
        )

        # Para visualización se utilizan planos
        # estratégicos en el volumen.

        points = []

        E = []
        H = []

        if self.geometry.currentIndex() == 0:

            # =================================================
            # GUÍA DE ONDA
            # =================================================

            for zz in z:

                for yy in y:

                    for xx in x:

                        X = xx
                        Y = yy

                        # -------------------------------------
                        # TEM
                        # -------------------------------------

                        if kind == "TEM":

                            ex = 1.0
                            ey = 0.0
                            ez = 0.0

                            hx = 0.0
                            hy = 1.0
                            hz = 0.0

                        # -------------------------------------
                        # TE
                        # -------------------------------------

                        elif kind == "TE":

                            hz = (
                                np.cos(
                                    m*np.pi*X
                                )
                                *
                                np.cos(
                                    n*np.pi*Y
                                )
                            )

                            ex = (
                                np.cos(
                                    m*np.pi*X
                                )
                                *
                                np.sin(
                                    n*np.pi*Y
                                )
                            )

                            ey = (
                                -np.sin(
                                    m*np.pi*X
                                )
                                *
                                np.cos(
                                    n*np.pi*Y
                                )
                            )

                            ez = 0.0

                            hx = (
                                np.sin(
                                    m*np.pi*X
                                )
                                *
                                np.cos(
                                    n*np.pi*Y
                                )
                            )

                            hy = (
                                np.cos(
                                    m*np.pi*X
                                )
                                *
                                np.sin(
                                    n*np.pi*Y
                                )
                            )

                        # -------------------------------------
                        # TM
                        # -------------------------------------

                        else:

                            ez = (
                                np.sin(
                                    m*np.pi*X
                                )
                                *
                                np.sin(
                                    n*np.pi*Y
                                )
                            )

                            ex = (
                                np.cos(
                                    m*np.pi*X
                                )
                                *
                                np.sin(
                                    n*np.pi*Y
                                )
                            )

                            ey = (
                                np.sin(
                                    m*np.pi*X
                                )
                                *
                                np.cos(
                                    n*np.pi*Y
                                )
                            )

                            hx = (
                                -np.sin(
                                    m*np.pi*X
                                )
                                *
                                np.cos(
                                    n*np.pi*Y
                                )
                            )

                            hy = (
                                np.cos(
                                    m*np.pi*X
                                )
                                *
                                np.sin(
                                    n*np.pi*Y
                                )
                            )

                            hz = 0.0

                        points.append([
                            X*self.a,
                            Y*self.b,
                            (zz-0.5)*self.d
                        ])

                        E.append([
                            ex,
                            ey,
                            ez
                        ])

                        H.append([
                            hx,
                            hy,
                            hz
                        ])

        else:

            # =================================================
            # CAVIDAD
            # =================================================

            for zz in z:

                for yy in y:

                    for xx in x:

                        X = xx
                        Y = yy
                        Z = zz

                        # ------------------------------------------------
                        # TE
                        # ------------------------------------------------

                        if kind == "TE":

                            hz = (
                                np.cos(m*np.pi*X)
                                *
                                np.cos(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            ex = (
                                np.cos(m*np.pi*X)
                                *
                                np.sin(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            ey = (
                                -np.sin(m*np.pi*X)
                                *
                                np.cos(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            ez = 0.0

                            hx = (
                                np.sin(m*np.pi*X)
                                *
                                np.cos(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            hy = (
                                np.cos(m*np.pi*X)
                                *
                                np.sin(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                        # ------------------------------------------------
                        # TM
                        # ------------------------------------------------

                        else:

                            ez = (
                                np.sin(m*np.pi*X)
                                *
                                np.sin(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            ex = (
                                np.cos(m*np.pi*X)
                                *
                                np.sin(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            ey = (
                                np.sin(m*np.pi*X)
                                *
                                np.cos(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            hx = (
                                -np.sin(m*np.pi*X)
                                *
                                np.cos(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            hy = (
                                np.cos(m*np.pi*X)
                                *
                                np.sin(n*np.pi*Y)
                                *
                                np.cos(l*np.pi*Z)
                            )

                            hz = 0.0

                        points.append([
                            X*self.a,
                            Y*self.b,
                            Z*self.d
                        ])

                        E.append([
                            ex,
                            ey,
                            ez
                        ])

                        H.append([
                            hx,
                            hy,
                            hz
                        ])

        return (
            np.array(points),
            np.array(E),
            np.array(H)
        )

    # ========================================================
    # PAREDES
    # ========================================================

    def create_walls(self):

        self.clear_walls()

        if not self.show_walls.isChecked():
            return

        a = self.a
        b = self.b
        d = self.d

        # ----------------------------------------------------
        # Para no bloquear completamente la visualización,
        # las paredes se dibujan como bordes transparentes.
        # ----------------------------------------------------

        corners = np.array([
            [0, 0, 0],
            [a, 0, 0],
            [a, b, 0],
            [0, b, 0],
            [0, 0, d],
            [a, 0, d],
            [a, b, d],
            [0, b, d]
        ])

        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),

            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),

            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7)
        ]

        for i, j in edges:

            pts = np.array([
                corners[i],
                corners[j]
            ])

            item = gl.GLLinePlotItem(
                pos=pts,
                width=3,
                antialias=True
            )

            self.view.addItem(
                item
            )

            self.wall_items.append(
                item
            )

    def clear_walls(self):

        for item in self.wall_items:

            self.view.removeItem(
                item
            )

        self.wall_items.clear()

    # ========================================================
    # VECTORES
    # ========================================================

    def create_vectors(self):

        self.clear_vectors()

        points, E, H = self.field_vectors()

        # Normalización independiente
        # para que ambos campos puedan verse.

        emax = np.max(
            np.linalg.norm(
                E,
                axis=1
            )
        )

        hmax = np.max(
            np.linalg.norm(
                H,
                axis=1
            )
        )

        if emax > 0:
            E = E / emax

        if hmax > 0:
            H = H / hmax

        phase = np.cos(
            self.phase
        )

        E *= phase
        H *= phase

        # Escala visual
        arrow_scale = min(
            self.a,
            self.b,
            self.d
        ) * 0.55

        show = self.field.currentText()

         # ----------------------------------------------------
        # Campo E (AZUL)
        # ----------------------------------------------------

        if show in ("E", "E y H"):

            for p, v in zip(
                points,
                E
            ):

                magnitude = np.linalg.norm(
                    v
                )

                if magnitude < 0.08:
                    continue

                direction = (
                    v / magnitude
                )

                length = (
                    magnitude *
                    arrow_scale
                )

                end = (
                    p +
                    direction *
                    length
                )

                line = gl.GLLinePlotItem(
                    pos=np.array([
                        p,
                        end
                    ]),
                    color=(0.2, 0.5, 1.0, 1.0),  # ← AZUL
                    width=2.5,
                    antialias=True
                )

                self.view.addItem(
                    line
                )

                self.e_items.append(
                    line
                )

        # ----------------------------------------------------
        # Campo H (ROJO)
        # ----------------------------------------------------

        if show in ("H", "E y H"):

            for p, v in zip(
                points,
                H
            ):

                magnitude = np.linalg.norm(
                    v
                )

                if magnitude < 0.08:
                    continue

                direction = (
                    v / magnitude
                )

                length = (
                    magnitude *
                    arrow_scale
                )

                end = (
                    p +
                    direction *
                    length
                )

                line = gl.GLLinePlotItem(
                    pos=np.array([
                        p,
                        end
                    ]),
                    color=(1.0, 0.2, 0.2, 1.0),  # ← ROJO
                    width=2.0,
                    antialias=True
                )

                self.view.addItem(
                    line
                )

                self.h_items.append(
                    line
                )

    # ========================================================
    # LIMPIAR VECTORES
    # ========================================================

    def clear_vectors(self):

        for item in self.e_items:

            self.view.removeItem(
                item
            )

        for item in self.h_items:

            self.view.removeItem(
                item
            )

        self.e_items.clear()
        self.h_items.clear()

    # ========================================================
    # ACTUALIZAR ESCENA
    # ========================================================

    def update_scene(self):

        self.update_parameters()

        self.create_walls()

        self.create_vectors()

        self.update_information()

    # ========================================================
    # INFORMACIÓN
    # ========================================================

    def update_information(self):

        mode = self.mode.currentText()

        kind, m, n, l = parse_mode(
            mode
        )

        if self.geometry.currentIndex() == 0:

            fc = cutoff_frequency(
                mode,
                self.a / 1000,
                self.b / 1000
            )

            fc_ghz = fc / 1e9

            text = f"""
            <b>GUÍA DE ONDA RECTANGULAR</b><br><br>

            <b>Modo:</b> {mode}<br>
            m = {m}, n = {n}<br><br>

            <b>Dimensiones:</b><br>
            a = {self.a:.2f} mm<br>
            b = {self.b:.2f} mm<br>
            longitud visual = {self.d:.2f} mm<br><br>

            <b>Frecuencia:</b><br>
            f = {self.frequency/1e9:.4f} GHz<br><br>

            <b>Frecuencia de corte:</b><br>
            fc = {fc_ghz:.4f} GHz<br><br>

            """

            if self.frequency > fc:

                text += (
                    "<b>Estado:</b> "
                    "PROPAGACIÓN"
                )

            else:

                text += (
                    "<b>Estado:</b> "
                    "POR DEBAJO DE CORTE"
                )

        else:

            fr = cavity_frequency(
                mode,
                self.a / 1000,
                self.b / 1000,
                self.d / 1000
            )

            text = f"""
            <b>CAVIDAD RESONANTE RECTANGULAR</b><br><br>

            <b>Modo:</b> {mode}<br>
            m = {m}, n = {n}, l = {l}<br><br>

            <b>Dimensiones:</b><br>
            a = {self.a:.2f} mm<br>
            b = {self.b:.2f} mm<br>
            d = {self.d:.2f} mm<br><br>

            <b>Frecuencia:</b><br>
            f = {self.frequency/1e9:.4f} GHz<br><br>

            <b>Frecuencia resonante:</b><br>
            fr = {fr/1e9:.4f} GHz<br><br>

            <b>Diferencia:</b><br>
            Δf = {abs(self.frequency-fr)/1e6:.3f} MHz
            """

        self.info.setHtml(
            text
        )

    # ========================================================
    # ANIMACIÓN
    # ========================================================

    def animate(self):

        if not self.animation.isChecked():
            return

        self.phase += 0.20

        # Evita que crezca indefinidamente
        if self.phase > 2*np.pi:
            self.phase -= 2*np.pi

        self.create_vectors()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    app = QtWidgets.QApplication(
        sys.argv
    )

    window = Waveguide3D()

    window.show()

    sys.exit(
        app.exec()
    )
