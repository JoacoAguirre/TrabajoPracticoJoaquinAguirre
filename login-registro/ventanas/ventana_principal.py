from PyQt6.QtWidgets import QStackedWidget

from controladores.autenticacion import ServicioAutenticacion
from ventanas.ventana_login import VentanaLogin
from ventanas.ventana_registro import VentanaRegistro


class VentanaPrincipal(QStackedWidget):
    """La ventana de la aplicación: muestra una pantalla por vez."""

    def __init__(self):
        super().__init__()
        # Un solo servicio, compartido: si cada pantalla creara el suyo,
        # el login no vería a los usuarios que se registraron.
        servicio = ServicioAutenticacion()
        self.login = VentanaLogin(servicio)
        self.registro = VentanaRegistro(servicio)
        self.addWidget(self.login)
        self.addWidget(self.registro)

        self.login.btn_ir_registro.clicked.connect(self.mostrar_registro)
        self.registro.btn_volver_login.clicked.connect(self.mostrar_login)

        self.resize(900, 780)
        self.mostrar_login()

    def mostrar_login(self):
        self.login.limpiar()
        self.setWindowTitle("Iniciar sesión")
        self.setCurrentWidget(self.login)
        self.login.input_usuario.setFocus()

    def mostrar_registro(self):
        self.registro.limpiar()
        self.setWindowTitle("Crear cuenta")
        self.setCurrentWidget(self.registro)
        self.registro.input_nombre.setFocus()
