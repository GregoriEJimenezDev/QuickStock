"""Entidad Producto + Builder + Factory."""
from __future__ import annotations
import sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from services.validador import Validador


class Producto:
    """Entidad del inventario. Clave comparable: codigo (entero único)."""

    # Complejidad: O(1)
    def __init__(self, codigo: int, nombre: str, categoria: str,
                 precio: float, stock: int) -> None:
        """Crea un producto ya validado."""
        self._codigo = codigo
        self._nombre = nombre
        self._categoria = categoria
        self._precio = precio
        self._stock = stock

    # Complejidad: O(1)
    @property
    def codigo(self) -> int:
        """Retorna el código (inmutable, clave del BST)."""
        return self._codigo

    # Complejidad: O(1)
    @property
    def nombre(self) -> str:
        """Retorna el nombre."""
        return self._nombre

    # Complejidad: O(1)
    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Actualiza el nombre validando no vacío."""
        self._nombre = Validador.texto_no_vacio(valor, "El nombre")

    # Complejidad: O(1)
    @property
    def categoria(self) -> str:
        """Retorna la categoría."""
        return self._categoria

    # Complejidad: O(1)
    @categoria.setter
    def categoria(self, valor: str) -> None:
        """Actualiza la categoría validando no vacío."""
        self._categoria = Validador.texto_no_vacio(valor, "La categoría")

    # Complejidad: O(1)
    @property
    def precio(self) -> float:
        """Retorna el precio."""
        return self._precio

    # Complejidad: O(1)
    @precio.setter
    def precio(self, valor: float) -> None:
        """Actualiza el precio validando que sea > 0."""
        self._precio = Validador.precio(valor)

    # Complejidad: O(1)
    @property
    def stock(self) -> int:
        """Retorna el stock."""
        return self._stock

    # Complejidad: O(1)
    @stock.setter
    def stock(self, valor: int) -> None:
        """Actualiza el stock validando que sea >= 0."""
        self._stock = Validador.stock(valor)

    # Complejidad: O(1)
    def __str__(self) -> str:
        """Representación en una línea para listados."""
        return "%d | %s | %s | %.2f | %d" % (
            self._codigo, self._nombre, self._categoria,
            self._precio, self._stock)


class ProductoBuilder:
    """Builder fluido. Valida en build()."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        """Inicializa el builder sin datos."""
        self._codigo = None
        self._nombre = None
        self._categoria = None
        self._precio = None
        self._stock = None

    # Complejidad: O(1)
    def con_codigo(self, codigo: int) -> "ProductoBuilder":
        """Fija el código y retorna self para encadenar."""
        self._codigo = codigo
        return self

    # Complejidad: O(1)
    def con_nombre(self, nombre: str) -> "ProductoBuilder":
        """Fija el nombre y retorna self para encadenar."""
        self._nombre = nombre
        return self

    # Complejidad: O(1)
    def con_categoria(self, categoria: str) -> "ProductoBuilder":
        """Fija la categoría y retorna self para encadenar."""
        self._categoria = categoria
        return self

    # Complejidad: O(1)
    def con_precio(self, precio: float) -> "ProductoBuilder":
        """Fija el precio y retorna self para encadenar."""
        self._precio = precio
        return self

    # Complejidad: O(1)
    def con_stock(self, stock: int) -> "ProductoBuilder":
        """Fija el stock y retorna self para encadenar."""
        self._stock = stock
        return self

    # Complejidad: O(1)
    def build(self) -> Producto:
        """Valida todo y construye el Producto."""
        codigo = Validador.codigo(self._codigo) if isinstance(
            self._codigo, int) and not isinstance(self._codigo, bool) else Validador.codigo(self._codigo)
        nombre = Validador.texto_no_vacio(self._nombre or "", "El nombre")
        categoria = Validador.texto_no_vacio(self._categoria or "", "La categoría")
        precio = Validador.precio(self._precio)
        stock = Validador.stock(self._stock)
        return Producto(codigo, nombre, categoria, precio, stock)


class ProductoFactory:
    """Factory que crea Productos usando el Builder internamente."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        """Inicializa la factory (sin estado)."""
        pass

    # Complejidad: O(1)
    @staticmethod
    def crear(codigo: int, nombre: str, categoria: str,
              precio: float, stock: int) -> Producto:
        """Crea un Producto delegando en ProductoBuilder."""
        return (ProductoBuilder()
                .con_codigo(codigo)
                .con_nombre(nombre)
                .con_categoria(categoria)
                .con_precio(precio)
                .con_stock(stock)
                .build())
