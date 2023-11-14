import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QGridLayout
from PyQt5.QtCore import Qt, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class LorenzSystemApp(QWidget):
    def __init__(self):
        super().__init__()

        self.sigma_label = QLabel("Sigma:")
        self.sigma_slider = QSlider(Qt.Horizontal)
        self.sigma_slider.setMinimum(1)
        self.sigma_slider.setMaximum(50)
        self.sigma_slider.setValue(10)
        self.sigma_value_label = QLabel(str(self.sigma_slider.value()))

        self.rho_label = QLabel("Rho:")
        self.rho_slider = QSlider(Qt.Horizontal)
        self.rho_slider.setMinimum(1)
        self.rho_slider.setMaximum(50)
        self.rho_slider.setValue(28)
        self.rho_value_label = QLabel(str(self.rho_slider.value()))

        self.beta_label = QLabel("Beta:")
        self.beta_slider = QSlider(Qt.Horizontal)
        self.beta_slider.setMinimum(1)
        self.beta_slider.setMaximum(50)
        self.beta_slider.setValue(8)
        self.beta_value_label = QLabel(str(self.beta_slider.value()))

        self.x_label = QLabel("X0:")
        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setMinimum(-50)
        self.x_slider.setMaximum(50)
        self.x_slider.setValue(1)
        self.x_value_label = QLabel(str(self.x_slider.value()))

        self.y_label = QLabel("Y0:")
        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setMinimum(-50)
        self.y_slider.setMaximum(50)
        self.y_slider.setValue(0)
        self.y_value_label = QLabel(str(self.y_slider.value()))

        self.z_label = QLabel("Z0:")
        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setMinimum(-50)
        self.z_slider.setMaximum(50)
        self.z_slider.setValue(20)
        self.z_value_label = QLabel(str(self.z_slider.value()))

        #self.solve_button = QPushButton("Resolver", self)
        #self.solve_button.clicked.connect(self.solve_lorenz)
    

        self.figure, self.ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.canvas = FigureCanvas(self.figure)
        
        # Timer para actualización en tiempo real
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(100)  # Actualiza cada 100 milisegundos

        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()

        layout.addWidget(self.sigma_label, 0, 0)
        layout.addWidget(self.sigma_slider, 0, 1)
        layout.addWidget(self.sigma_value_label, 0, 2)

        layout.addWidget(self.rho_label, 1, 0)
        layout.addWidget(self.rho_slider, 1, 1)
        layout.addWidget(self.rho_value_label, 1, 2)

        layout.addWidget(self.beta_label, 2, 0)
        layout.addWidget(self.beta_slider, 2, 1)
        layout.addWidget(self.beta_value_label, 2, 2)

        layout.addWidget(self.x_label, 3, 0)
        layout.addWidget(self.x_slider, 3, 1)
        layout.addWidget(self.x_value_label, 3, 2)

        layout.addWidget(self.y_label, 4, 0)
        layout.addWidget(self.y_slider, 4, 1)
        layout.addWidget(self.y_value_label, 4, 2)

        layout.addWidget(self.z_label, 5, 0)
        layout.addWidget(self.z_slider, 5, 1)
        layout.addWidget(self.z_value_label, 5, 2)

        #layout.addWidget(self.solve_button, 6, 0, 1, 3)
        layout.addWidget(self.canvas, 7, 0, 1, 3)

        self.setLayout(layout)

        self.sigma_slider.valueChanged.connect(lambda: self.update_value_label(self.sigma_slider, self.sigma_value_label))
        self.rho_slider.valueChanged.connect(lambda: self.update_value_label(self.rho_slider, self.rho_value_label))
        self.beta_slider.valueChanged.connect(lambda: self.update_value_label(self.beta_slider, self.beta_value_label))
        self.x_slider.valueChanged.connect(lambda: self.update_value_label(self.x_slider, self.x_value_label))
        self.y_slider.valueChanged.connect(lambda: self.update_value_label(self.y_slider, self.y_value_label))
        self.z_slider.valueChanged.connect(lambda: self.update_value_label(self.z_slider, self.z_value_label))

        # Conectar sliders a la función de actualización
        self.sigma_slider.valueChanged.connect(self.update_graph)
        self.rho_slider.valueChanged.connect(self.update_graph)
        self.beta_slider.valueChanged.connect(self.update_graph)
        self.x_slider.valueChanged.connect(self.update_graph)
        self.y_slider.valueChanged.connect(self.update_graph)
        self.z_slider.valueChanged.connect(self.update_graph)
        
        self.show()

    def lorenz_system(self, t, y, sigma, rho, beta):
        dydt = [sigma * (y[1] - y[0]),
                y[0] * (rho - y[2]) - y[1],
                y[0] * y[1] - beta * y[2]]
        return dydt

    def solve_lorenz(self):
        sigma = self.sigma_slider.value()
        rho = self.rho_slider.value()
        beta = self.beta_slider.value()

        x0 = self.x_slider.value()
        y0 = self.y_slider.value()
        z0 = self.z_slider.value()

        y0 = [x0, y0, z0]

        t_span = (0, 25)
        t_eval = np.linspace(t_span[0], t_span[1], 10000)

        sol = solve_ivp(self.lorenz_system, t_span, y0, args=(sigma, rho, beta), t_eval=t_eval)

        self.ax.clear()
        self.ax.plot(sol.y[0], sol.y[1], sol.y[2], color='b', lw=0.5)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('Sistema de Lorenz')
        self.canvas.draw()
        
    def update_graph(self):
        # Aquí va el código para calcular y dibujar el mapa de Lorenz
        # Simplemente puedes llamar a solve_lorenz si quieres usar la misma lógica
        self.solve_lorenz()

    def update_value_label(self, slider, label):
        label.setText(str(slider.value()))
        
