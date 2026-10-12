"""Vista de consola: entrada, salida y formateo."""
from __future__ import annotations
import shutil
from typing import Callable, TypeVar
from models.producto import Producto
from models.protocolos import Vista
from models.validador import Validador
from view.constantes import (TITULO_APP, MENU_PRINCIPAL, SUBMENU_LISTAR,
                              SUBMENU_REPORTES, ENCABEZADO_PRODUCTO, SEPARADOR)

T = TypeVar("T")


class VistaConsola(Vista):
    """Entrada/salida y formateo. Todo se muestra centrado. Sin lógica de negocio."""

    # Complejidad: O(1)
    def _ancho(self) -> int:
        try:
            return shutil.get_terminal_size().columns
        except Exception:
            return 80

    # Complejidad: O(L) donde L = líneas del texto
    def _centrar(self, texto: str) -> str:
        ancho = self._ancho()
        return "\n".join(linea.center(ancho) for linea in str(texto).split("\n"))

    # Complejidad: O(1)
    def _marcador(self) -> str:
        prefijo = ">>> "
        return " " * max(0, (self._ancho() - len(prefijo)) // 2) + prefijo

    # Complejidad: O(L) donde L = líneas del texto
    def _imprimir(self, texto: str) -> None:
        print(self._centrar(texto))

    # Complejidad: O(L) donde L = líneas del mensaje
    def _preguntar(self, mensaje: str) -> str:
        return input(self._centrar(mensaje) + "\n" + self._marcador()).strip()

    # Complejidad: O(1)
    def mostrar_titulo(self) -> None:
        self._imprimir(TITULO_APP)

    # Complejidad: O(1)
    def mostrar_menu_principal(self) -> None:
        self._imprimir(MENU_PRINCIPAL)

    # Complejidad: O(1)
    def mostrar_submenu_listar(self) -> None:
        self._imprimir(SUBMENU_LISTAR)

    # Complejidad: O(1)
    def mostrar_submenu_reportes(self) -> None:
        self._imprimir(SUBMENU_REPORTES)

    # Complejidad: O(1)
    def mostrar_mensaje(self, texto: str) -> None:
        self._imprimir(texto)

    # Complejidad: O(1)
    def mostrar_error(self, texto: str) -> None:
        self._imprimir("Error: " + texto)

    # Complejidad: O(1)
    def mostrar_encabezado(self, texto: str) -> None:
        self._imprimir("\n" + texto + "\n" + SEPARADOR)

    # Complejidad: O(1)
    def mostrar_producto(self, producto: Producto) -> None:
        self._imprimir(str(producto))

    # Complejidad: O(1)
    def mostrar_encabezado_tabla(self) -> None:
        self._imprimir(ENCABEZADO_PRODUCTO + "\n" + SEPARADOR)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_entero(self, mensaje: str) -> int:
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
        while True:
            crudo = self._preguntar(mensaje)
            if crudo:
                return crudo
            self.mostrar_error("El valor no puede estar vacío.")

    # Complejidad: O(1)
    def leer_texto_libre(self, mensaje: str) -> str:
        return self._preguntar(mensaje)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def _leer_validado(self, mensaje: str, lector: Callable[[str], T],
                       regla: Callable[[T], T]) -> T:
        while True:
            try:
                return regla(lector(mensaje))
            except ValueError as error:
                self.mostrar_error(str(error))

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_codigo(self, mensaje: str) -> int:
        return self._leer_validado(mensaje, self.leer_entero, Validador.codigo)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_precio(self, mensaje: str) -> float:
        return self._leer_validado(mensaje, self.leer_decimal, Validador.precio)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_stock(self, mensaje: str) -> int:
        return self._leer_validado(mensaje, self.leer_entero, Validador.stock)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_umbral(self, mensaje: str) -> int:
        return self._leer_validado(mensaje, self.leer_entero, Validador.umbral_stock)

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_confirmacion(self, mensaje: str) -> bool:
        while True:
            crudo = self._preguntar(mensaje).lower()
            if crudo in ("s", "si", "sí"):
                return True
            if crudo in ("n", "no"):
                return False
            self.mostrar_error("Responda 's' o 'n'.")
