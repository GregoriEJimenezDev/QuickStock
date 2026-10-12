"""Servicio de inventario: reglas de negocio sobre el BST."""
from __future__ import annotations
from typing import Callable, Optional
from estructura.recorrido import Recorrido
from models.producto import Producto, ProductoFactory
from models.protocolos import RepositorioProductos
from models.validador import Validador


class ServicioInventario:
    """Orquesta CRUD y reportes. Depende de abstracciones inyectadas."""

    # Complejidad: O(1)
    def __init__(self, arbol: RepositorioProductos) -> None:
        self._arbol = arbol
        self._recorridos = {
            Recorrido.INORDEN: arbol.inorden,
            Recorrido.PREORDEN: arbol.preorden,
            Recorrido.POSTORDEN: arbol.postorden,
        }

    # Complejidad: O(h) promedio, O(n) peor caso (delega en BST)
    def registrar(self, codigo: int, nombre: str, categoria: str,
                  precio: float, stock: int) -> bool:
        """Crea con Factory y lo inserta; False si el código está duplicado."""
        producto = ProductoFactory.crear(codigo, nombre, categoria, precio, stock)
        return self._arbol.insertar(producto)

    # Complejidad: O(h) promedio, O(n) peor caso (delega en BST)
    def buscar_por_codigo(self, codigo: int) -> Optional[Producto]:
        return self._arbol.buscar(codigo)

    # Complejidad: O(h) promedio, O(n) peor caso (búsqueda del BST)
    def editar(self, codigo: int, nombre: str, categoria: str,
               precio: float, stock: int) -> bool:
        """Valida los 4 valores antes de asignar; lo fallido no cambia nada."""
        producto = self._arbol.buscar(codigo)
        if producto is None:
            return False
        nombre_ok = Validador.texto_no_vacio(nombre, "El nombre")
        categoria_ok = Validador.texto_no_vacio(categoria, "La categoría")
        precio_ok = Validador.precio(precio)
        stock_ok = Validador.stock(stock)
        producto.nombre = nombre_ok
        producto.categoria = categoria_ok
        producto.precio = precio_ok
        producto.stock = stock_ok
        return True

    # Complejidad: O(h) promedio, O(n) peor caso (delega en BST)
    def eliminar(self, codigo: int) -> bool:
        """Elimina por código; False si no existe (árbol intacto)."""
        return self._arbol.eliminar(codigo)

    # Complejidad: O(n)
    def listar(self, recorrido: Recorrido, visitante: Callable[[Producto], None]) -> bool:
        if self._arbol.esta_vacio():
            return False
        self._recorridos[recorrido](visitante)
        return True

    # Complejidad: O(n)
    def reporte_stock_bajo(self, limite: int,
                            visitante: Callable[[Producto], None]) -> int:
        """Visita in-order y notifica solo stock <= límite; retorna hallados."""
        hallados = 0

        # Complejidad: O(1) por visita, O(n) total
        def _filtro(producto: Producto) -> None:
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
            nonlocal hallados
            hallados += 1
            visitante(producto)

        self._arbol.rango(minimo, maximo, _contador)
        return hallados

    # Complejidad: O(n)
    def total_productos(self) -> int:
        return self._arbol.contar()

    # Complejidad: O(n)
    def valor_total(self) -> float:
        return self._arbol.valor_total()

    # Complejidad: O(n) por la altura; resto O(h)
    def estado(self) -> tuple:
        """Retorna (total, altura, mínimo, máximo) del árbol."""
        total = self._arbol.contar()
        altura = self._arbol.altura()
        minimo = self._arbol.minimo()
        maximo = self._arbol.maximo()
        return (total, altura, minimo, maximo)
