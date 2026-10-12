"""Vista de consola: única familia de entrada y único formateo (DRY)."""
from __future__ import annotations
import sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from models.producto import Producto
from view.constantes import (TITULO_APP, MENU_PRINCIPAL, SUBMENU_LISTAR,
                              SUBMENU_REPORTES, ENCABEZADO_PRODUCTO, SEPARADOR)


class VistaConsola:
    """Entrada/salida y formateo. Sin lógica de negocio."""

    # Complejidad: O(1)
    def mostrar_titulo(self) -> None:
        print(TITULO_APP)

    # Complejidad: O(1)
    def mostrar_menu_principal(self) -> None:
        print(MENU_PRINCIPAL)

    # Complejidad: O(1)
    def mostrar_submenu_listar(self) -> None:
        print(SUBMENU_LISTAR)

    # Complejidad: O(1)
    def mostrar_submenu_reportes(self) -> None:
        print(SUBMENU_REPORTES)

    # Complejidad: O(1)
    def mostrar_mensaje(self, texto: str) -> None:
        print(texto)

    # Complejidad: O(1)
    def mostrar_error(self, texto: str) -> None:
        print("Error: " + texto)

    # Complejidad: O(1)
    def mostrar_encabezado(self, texto: str) -> None:
        print("\n" + texto)
        print(SEPARADOR)

    # Complejidad: O(1)
    def mostrar_producto(self, producto: Producto) -> None:
        """Único punto de formateo/impresión de un producto."""
        print(str(producto))

    # Complejidad: O(1)
    def mostrar_encabezado_tabla(self) -> None:
        print(ENCABEZADO_PRODUCTO)
        print(SEPARADOR)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_entero(self, mensaje: str) -> int:
        while True:
            crudo = input(mensaje).strip()
            if not crudo:
                self.mostrar_error("El valor no puede estar vacío.")
                continue
            try:
                return int(crudo)
            except ValueError:
                self.mostrar_error("Debe ingresar un número entero.")

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_decimal(self, mensaje: str) -> float:
        while True:
            crudo = input(mensaje).strip()
            if not crudo:
                self.mostrar_error("El valor no puede estar vacío.")
                continue
            try:
                return float(crudo.replace(",", "."))
            except ValueError:
                self.mostrar_error("Debe ingresar un número.")

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_texto_no_vacio(self, mensaje: str) -> str:
        while True:
            crudo = input(mensaje).strip()
            if crudo:
                return crudo
            self.mostrar_error("El valor no puede estar vacío.")

    # Complejidad: O(1)
    def leer_texto_libre(self, mensaje: str) -> str:
        return input(mensaje).strip()

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_confirmacion(self, mensaje: str) -> bool:
        while True:
            crudo = input(mensaje).strip().lower()
            if crudo in ("s", "si", "sí"):
                return True
            if crudo in ("n", "no"):
                return False
            self.mostrar_error("Responda 's' o 'n'.")
