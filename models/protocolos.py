"""Contratos mínimos para inyección de dependencias."""
from __future__ import annotations
from typing import Callable, Optional, Protocol

from models.producto import Producto

Visitante = Callable[[Producto], None]


class RepositorioProductos(Protocol):
    """Lo que el servicio necesita del árbol, sin la clase concreta."""

    # Complejidad: O(1)
    def esta_vacio(self) -> bool:
        ...

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def insertar(self, producto: Producto) -> bool:
        ...

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def buscar(self, codigo: int) -> Optional[Producto]:
        ...

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def eliminar(self, codigo: int) -> bool:
        ...

    # Complejidad: O(n)
    def inorden(self, visitante: Visitante) -> None:
        ...

    # Complejidad: O(n)
    def preorden(self, visitante: Visitante) -> None:
        ...

    # Complejidad: O(n)
    def postorden(self, visitante: Visitante) -> None:
        ...

    # Complejidad: O(k + h) donde k = nodos en rango, O(n) peor caso
    def rango(self, minimo: int, maximo: int, visitante: Visitante) -> None:
        ...

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def minimo(self) -> Optional[Producto]:
        ...

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def maximo(self) -> Optional[Producto]:
        ...

    # Complejidad: O(n)
    def contar(self) -> int:
        ...

    # Complejidad: O(n)
    def altura(self) -> int:
        ...

    # Complejidad: O(n)
    def valor_total(self) -> float:
        ...


class VistaEntrada(Protocol):
    """Lo que el menú necesita para leer datos, sin la consola concreta."""

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_codigo(self, mensaje: str) -> int:
        ...

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_precio(self, mensaje: str) -> float:
        ...

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_stock(self, mensaje: str) -> int:
        ...

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_umbral(self, mensaje: str) -> int:
        ...

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_texto_no_vacio(self, mensaje: str) -> str:
        ...

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_entero(self, mensaje: str) -> int:
        ...

    # Complejidad: O(1)
    def leer_texto_libre(self, mensaje: str) -> str:
        ...

    # Complejidad: O(m) donde m = intentos del usuario; O(1) por intento
    def leer_confirmacion(self, mensaje: str) -> bool:
        ...


class VistaSalida(Protocol):
    """Lo que el menú necesita para mostrar datos, sin la consola concreta."""

    # Complejidad: O(1)
    def mostrar_titulo(self) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_menu_principal(self) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_submenu_listar(self) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_submenu_reportes(self) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_mensaje(self, texto: str) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_error(self, texto: str) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_encabezado(self, texto: str) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_producto(self, producto: Producto) -> None:
        ...

    # Complejidad: O(1)
    def mostrar_encabezado_tabla(self) -> None:
        ...


class Vista(VistaEntrada, VistaSalida, Protocol):
    """Vista completa que implementa la consola."""
