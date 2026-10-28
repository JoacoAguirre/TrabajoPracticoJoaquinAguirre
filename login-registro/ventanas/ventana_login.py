from pathlib import Path

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QWidget

RUTA_UI = Path(__file__).parent / "login.ui"


class VentanaLogin(QWidget):
    """Controla la pantalla de inicio de sesión. El diseño vive en login.ui."""

    def __init__(self, servicio):
        super().__init__()
        uic.loadUi(RUTA_UI, self)
        # Una subclase de QWidget necesita esto para que el QSS pinte su fondo.
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.servicio = servicio
        self._conectar_eventos()

    def _conectar_eventos(self):
        self.btn_login.clicked.connect(self.iniciar_sesion)
        self.input_password.returnPressed.connect(self.iniciar_sesion)
        self.chk_mostrar_password.toggled.connect(self.alternar_password)

    def iniciar_sesion(self):
        usuario = self.input_usuario.text().strip()
        password = self.input_password.text()

        error = self._validar(usuario, password)
        if error:
            self._mostrar_mensaje(error, "error")
            return

        if self.servicio.autenticar(usuario, password):
            nombre = self.servicio.obtener_nombre(usuario)
            self._mostrar_mensaje(f"Sesión iniciada como {nombre}", "exito")
        else:

            self._mostrar_mensaje("Usuario o contraseña incorrectos.", "error")

    def alternar_password(self, visible):
        if visible:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

    def limpiar(self):
        """Deja la pantalla como recién abierta (la usa VentanaPrincipal)."""
        self.input_password.clear()
        self.chk_mostrar_password.setChecked(False)
        self._mostrar_mensaje("")
        self.input_usuario.setFocus()

    def _validar(self, usuario, password):
        if not usuario:
            return "Ingresá tu usuario o correo electrónico."
        if not password:
            return "Ingresá tu contraseña."
        return None

    def _mostrar_mensaje(self, texto, tipo="info"):
        self.label_mensaje.setText(texto)
        self.label_mensaje.setProperty("tipo", tipo)
        # Le pedimos a Qt que vuelva a leer los estilos con la propiedad nueva.
        self.label_mensaje.style().unpolish(self.label_mensaje)
        self.label_mensaje.style().polish(self.label_mensaje)
