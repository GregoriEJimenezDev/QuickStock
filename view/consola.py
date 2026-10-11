"""Vista de consola: única familia de entrada y único formateo (DRY)."""
from __future__ import annotations
import shutil
import sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from models.producto import Producto
from view.constantes import (TITULO_APP, MENU_PRINCIPAL, SUBMENU_LISTAR,
                              SUBMENU_REPORTES, ENCABEZADO_PRODUCTO, SEPARADOR)


class VistaConsola:
    """Entrada/salida y formateo. Todo se muestra centrado. Sin lógica de negocio."""

    # Complejidad: O(1)
    def __init__(self, ancho: int = 80) -> None:
        """Inicializa la vista con el ancho de centrado de respaldo."""
        self._ancho_respaldo = ancho

    # Complejidad: O(1)
    def _ancho(self) -> int:
        """Retorna el ancho actual de la terminal (respaldo si falla)."""
        try:
            return shutil.get_terminal_size().columns
        except Exception:
            return self._ancho_respaldo

    # Complejidad: O(L) donde L = líneas del texto
    def _centrar(self, texto: str) -> str:
        """Centra cada línea del texto al ancho de la terminal."""
        ancho = self._ancho()
        return "\n".join(linea.center(ancho) for linea in str(texto).split("\n"))

    # Complejidad: O(L) donde L = líneas del texto
    def _imprimir(self, texto: str) -> None:
        """Imprime un texto ya centrado."""
        print(self._centrar(texto))

    # Complejidad: O(L) donde L = líneas del mensaje; O(1) por intento
    def _preguntar(self, mensaje: str) -> str:
        """Prompt centrado en su línea; la escritura va en línea propia con '>>>'."""
        self._imprimir(mensaje)
        return input(self._marcador_entrada()).strip()

    # Complejidad: O(1)
    def _marcador_entrada(self) -> str:
        """Retorna el marcador '>>>' con sangría centrada y sin relleno final."""
        ancho = self._ancho()
        prefijo = ">>> "
        sangria = max(0, (ancho - len(prefijo)) // 2)
        return " " * sangria + prefijo

    # Complejidad: O(1)
    def mostrar_titulo(self) -> None:
        """Imprime el título de la aplicación, centrado."""
        self._imprimir(TITULO_APP)

    # Complejidad: O(1)
    def mostrar_menu_principal(self) -> None:
        """Imprime el menú principal de 8 opciones, centrado."""
        self._imprimir(MENU_PRINCIPAL)

    # Complejidad: O(1)
    def mostrar_submenu_listar(self) -> None:
        """Imprime el submenú de listados, centrado."""
        self._imprimir(SUBMENU_LISTAR)

    # Complejidad: O(1)
    def mostrar_submenu_reportes(self) -> None:
        """Imprime el submenú de reportes, centrado."""
        self._imprimir(SUBMENU_REPORTES)

    # Complejidad: O(1)
    def mostrar_mensaje(self, texto: str) -> None:
        """Imprime un mensaje informativo, centrado."""
        self._imprimir(texto)

    # Complejidad: O(1)
    def mostrar_error(self, texto: str) -> None:
        """Imprime un mensaje de error, centrado."""
        self._imprimir("Error: " + texto)

    # Complejidad: O(1)
    def mostrar_encabezado(self, texto: str) -> None:
        """Imprime un encabezado de sección, centrado."""
        self._imprimir("\n" + texto + "\n" + SEPARADOR)

    # Complejidad: O(1)
    def mostrar_producto(self, producto: Producto) -> None:
        """Único método de formateo/impresión de un producto (DRY), centrado."""
        self._imprimir(str(producto))

    # Complejidad: O(1)
    def mostrar_encabezado_tabla(self) -> None:
        """Imprime el encabezado de la tabla de productos, centrado."""
        self._imprimir(ENCABEZADO_PRODUCTO + "\n" + SEPARADOR)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_entero(self, mensaje: str) -> int:
        """Lee un entero con reintento ante texto inválido o vacío."""
        while True:
            crudo = self._preguntar(mensaje)
            if not crudo:
                self.mostrar_error("El valor no puede estar vacío.")
                continue
            try:
                return int(crudo)
            except ValueError:
                self.mostrar_error("Debe ingresar un número entero.")

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_decimal(self, mensaje: str) -> float:
        """Lee un decimal con reintento ante texto inválido o vacío."""
        while True:
            crudo = self._preguntar(mensaje)
            if not crudo:
                self.mostrar_error("El valor no puede estar vacío.")
                continue
            try:
                return float(crudo.replace(",", "."))
            except ValueError:
                self.mostrar_error("Debe ingresar un número.")

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_texto_no_vacio(self, mensaje: str) -> str:
        """Lee texto no vacío (rechaza vacíos y solo-espacios) con reintento."""
        while True:
            crudo = self._preguntar(mensaje)
            if crudo:
                return crudo
            self.mostrar_error("El valor no puede estar vacío.")

    # Complejidad: O(1)
    def leer_texto_libre(self, mensaje: str) -> str:
        """Lee una línea libre (puede ser vacía, p. ej. opción de menú)."""
        return self._preguntar(mensaje)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_confirmacion(self, mensaje: str) -> bool:
        """Lee confirmación s/n con reintento; True si 's'."""
        while True:
            crudo = self._preguntar(mensaje).lower()
            if crudo in ("s", "si", "sí"):
                return True
            if crudo in ("n", "no"):
                return False
            self.mostrar_error("Responda 's' o 'n'.")
