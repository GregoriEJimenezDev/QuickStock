"""Servicio de inventario: reglas de negocio sobre el BST (DIP por constructor)."""
from __future__ import annotations
from typing import Callable, Optional
import sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from models.producto import Producto, ProductoFactory
from estructure.bst import ArbolBST


class ServicioInventario:
    """Orquesta CRUD y reportes. Depende de abstracciones inyectadas."""

    # Complejidad: O(1)
    def __init__(self, arbol: ArbolBST) -> None:
        """Recibe el árbol por inyección (no lo instancia internamente)."""
        self._arbol = arbol

    # Complejidad: O(h) promedio, O(n) peor caso (delega en BST)
    def registrar(self, codigo: int, nombre: str, categoria: str,
                  precio: float, stock: int) -> bool:
        """Crea con Factory y lo inserta; False si el código está duplicado."""
        producto = ProductoFactory.crear(codigo, nombre, categoria, precio, stock)
        return self._arbol.insertar(producto)

    # Complejidad: O(h) promedio, O(n) peor caso (delega en BST)
    def buscar_por_codigo(self, codigo: int) -> Optional[Producto]:
        """Busca un producto por su código."""
        return self._arbol.buscar(codigo)

    # Complejidad: O(h) promedio, O(n) peor caso (búsqueda del BST)
    def editar(self, codigo: int, nombre: str, categoria: str,
               precio: float, stock: int) -> bool:
        """Edita campos (código inmutable); False si no existe."""
        producto = self._arbol.buscar(codigo)
        if producto is None:
            return False
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock
        return True

    # Complejidad: O(h) promedio, O(n) peor caso (delega en BST)
    def eliminar(self, codigo: int) -> bool:
        """Elimina por código; False si no existe (árbol intacto)."""
        return self._arbol.eliminar(codigo)

    # Complejidad: O(n)
    def listar(self, modo: str, visitante: Callable[[Producto], None]) -> bool:
        """Lista con el recorrido pedido ('inorden'/'preorden'/'postorden')."""
        if self._arbol.esta_vacio():
            return False
        if modo == "preorden":
            self._arbol.preorden(visitante)
        elif modo == "postorden":
            self._arbol.postorden(visitante)
        else:
            self._arbol.inorden(visitante)
        return True

    # Complejidad: O(n)
    def reporte_stock_bajo(self, limite: int,
                            visitante: Callable[[Producto], None]) -> int:
        """Visita in-order y notifica solo stock <= límite; retorna hallados."""
        hallados = 0

        # Complejidad: O(1) por visita, O(n) total
        def _filtro(producto: Producto) -> None:
            """Filtra por stock y reenvía al visitante real."""
            nonlocal hallados
            if producto.stock <= limite:
                hallados += 1
                visitante(producto)

        self._arbol.inorden(_filtro)
        return hallados

    # Complejidad: O(k + h) donde k = nodos en rango, O(n) peor caso
    def reporte_rango(self, minimo: int, maximo: int,
                      visitante: Callable[[Producto], None]) -> int:
        """Rango con poda real del BST; retorna cantidad hallada."""
        hallados = 0

        # Complejidad: O(1) por visita, O(k + h) total
        def _contador(producto: Producto) -> None:
            """Cuenta y reenvía cada producto dentro del rango."""
            nonlocal hallados
            hallados += 1
            visitante(producto)

        self._arbol.rango(minimo, maximo, _contador)
        return hallados

    # Complejidad: O(n)
    def total_productos(self) -> int:
        """Retorna la cantidad de nodos del árbol."""
        return self._arbol.contar()

    # Complejidad: O(n)
    def valor_total(self) -> float:
        """Retorna la suma de precio*stock del inventario."""
        return self._arbol.valor_total()

    # Complejidad: O(n) por la altura; resto O(h)
    def estado(self) -> tuple:
        """Retorna (total, altura, mínimo, máximo) del árbol."""
        total = self._arbol.contar()
        altura = self._arbol.altura()
        minimo = self._arbol.minimo()
        maximo = self._arbol.maximo()
        return (total, altura, minimo, maximo)
