
import hashlib
import hmac
import os

LONGITUD_MINIMA_PASSWORD = 8
ITERACIONES = 600_000


class ServicioAutenticacion:

    def __init__(self):
        self._usuarios = {}

    def registrar(self, nombre, apellido, usuario, password):
        clave = self._normalizar(usuario)
        minimo = LONGITUD_MINIMA_PASSWORD
        if not nombre.strip() or not apellido.strip():
            raise ValueError("Completá tu nombre y tu apellido.")
        if not clave:
            raise ValueError("Completá tu usuario o correo electrónico.")
        if len(password) < minimo:
            raise ValueError(f"La contraseña necesita al menos {minimo} caracteres.")
        if clave in self._usuarios:
            raise ValueError("Ese usuario ya está registrado.")

        sal = os.urandom(16)
        self._usuarios[clave] = {
            "nombre": nombre.strip(),
            "apellido": apellido.strip(),
            "sal": sal,
            "hash": self._calcular_hash(password, sal),
        }

    def autenticar(self, usuario, password):
        datos = self._usuarios.get(self._normalizar(usuario))
        if datos is None:
            return False
        calculado = self._calcular_hash(password, datos["sal"])
        return hmac.compare_digest(calculado, datos["hash"])

    def obtener_nombre(self, usuario):
        datos = self._usuarios.get(self._normalizar(usuario))
        return datos["nombre"] if datos else None

    @staticmethod
    def _normalizar(usuario):
        return usuario.strip().lower()

    @staticmethod
    def _calcular_hash(password, sal):
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), sal, ITERACIONES
        )
