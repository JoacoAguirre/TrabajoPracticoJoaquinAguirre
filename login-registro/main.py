import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from ventanas.ventana_principal import VentanaPrincipal

RUTA_VENTANAS = Path(__file__).parent / "ventanas"
RUTA_ESTILOS = RUTA_VENTANAS / "estilos.qss"
RUTA_RECURSOS = RUTA_VENTANAS / "recursos"


def cargar_estilos(app):
    try:
        qss = RUTA_ESTILOS.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Aviso: no encontré {RUTA_ESTILOS}. Sigo con el estilo por defecto.")
        return
    # El QSS necesita rutas absolutas para las imágenes (ej. el tilde del checkbox).
    app.setStyleSheet(qss.replace("{{RECURSOS}}", RUTA_RECURSOS.as_posix()))


def main():
    app = QApplication(sys.argv)
    cargar_estilos(app)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
