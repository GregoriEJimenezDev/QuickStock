"""BST manual. Clave = codigo del producto. Sin listas/dicts internos."""
from __future__ import annotations
from typing import Callable, Optional
import sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from modelos.producto import Producto

Visitante = Callable[[Producto], None]


class NodoBST:
    """Nodo del árbol binario de búsqueda."""

    # Complejidad: O(1)
    def __init__(self, producto: Producto) -> None:
        """Crea un nodo hoja con el producto dado."""
        self._producto = producto
        self._izquierdo: Optional["NodoBST"] = None
        self._derecho: Optional["NodoBST"] = None

    # Complejidad: O(1)
    @property
    def producto(self) -> Producto:
        """Retorna el producto del nodo."""
        return self._producto

    # Complejidad: O(1)
    @producto.setter
    def producto(self, valor: Producto) -> None:
        """Reemplaza el producto del nodo."""
        self._producto = valor

    # Complejidad: O(1)
    @property
    def izquierdo(self) -> Optional["NodoBST"]:
        """Retorna el hijo izquierdo."""
        return self._izquierdo

    # Complejidad: O(1)
    @izquierdo.setter
    def izquierdo(self, valor: Optional["NodoBST"]) -> None:
        """Fija el hijo izquierdo."""
        self._izquierdo = valor

    # Complejidad: O(1)
    @property
    def derecho(self) -> Optional["NodoBST"]:
        """Retorna el hijo derecho."""
        return self._derecho

    # Complejidad: O(1)
    @derecho.setter
    def derecho(self, valor: Optional["NodoBST"]) -> None:
        """Fija el hijo derecho."""
        self._derecho = valor


class ArbolBST:
    """Árbol de búsqueda binaria manual (estructura principal)."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        """Inicializa un árbol vacío."""
        self._raiz: Optional[NodoBST] = None

    # Complejidad: O(1)
    def esta_vacio(self) -> bool:
        """Indica si el árbol no tiene nodos."""
        return self._raiz is None

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def insertar(self, producto: Producto) -> bool:
        """Inserta iterativamente; False si el código ya existe."""
        nuevo = NodoBST(producto)
        if self._raiz is None:
            self._raiz = nuevo
            return True
        actual = self._raiz
        while True:
            if producto.codigo == actual.producto.codigo:
                return False
            elif producto.codigo < actual.producto.codigo:
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    return True
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    return True
                actual = actual.derecho

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def buscar(self, codigo: int) -> Optional[Producto]:
        """Busca iterativamente por código; None si no existe."""
        actual = self._raiz
        while actual is not None:
            if codigo == actual.producto.codigo:
                return actual.producto
            elif codigo < actual.producto.codigo:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def eliminar(self, codigo: int) -> bool:
        """Elimina iterativamente (hoja, un hijo, dos hijos con sucesor)."""
        padre = None
        actual = self._raiz
        while actual is not None and actual.producto.codigo != codigo:
            padre = actual
            if codigo < actual.producto.codigo:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        if actual is None:
            return False
        reemplazo = self._resolver_reemplazo(actual)
        if padre is None:
            self._raiz = reemplazo
        elif padre.izquierdo is actual:
            padre.izquierdo = reemplazo
        else:
            padre.derecho = reemplazo
        return True

    # Complejidad: O(h) promedio, O(n) peor caso (baja hasta el sucesor)
    def _resolver_reemplazo(self, nodo: NodoBST) -> Optional[NodoBST]:
        """Resuelve el subárbol de reemplazo según los 3 casos."""
        if nodo.izquierdo is None:
            return nodo.derecho
        if nodo.derecho is None:
            return nodo.izquierdo
        sucesor_padre = nodo
        sucesor = nodo.derecho
        while sucesor.izquierdo is not None:
            sucesor_padre = sucesor
            sucesor = sucesor.izquierdo
        nodo.producto = sucesor.producto
        if sucesor_padre.izquierdo is sucesor:
            sucesor_padre.izquierdo = sucesor.derecho
        else:
            sucesor_padre.derecho = sucesor.derecho
        return nodo

    # Complejidad: O(n)
    def inorden(self, visitante: Visitante) -> None:
        """Recorre Izq->Raíz->Der aplicando el visitante (callback)."""
        self._inorden_rec(self._raiz, visitante)

    # Complejidad: O(n)
    def _inorden_rec(self, nodo: Optional[NodoBST], visitante: Visitante) -> None:
        """Ayudante recursivo del recorrido in-order."""
        if nodo is None:
            return
        self._inorden_rec(nodo.izquierdo, visitante)
        visitante(nodo.producto)
        self._inorden_rec(nodo.derecho, visitante)

    # Complejidad: O(n)
    def preorden(self, visitante: Visitante) -> None:
        """Recorre Raíz->Izq->Der aplicando el visitante (callback)."""
        self._preorden_rec(self._raiz, visitante)

    # Complejidad: O(n)
    def _preorden_rec(self, nodo: Optional[NodoBST], visitante: Visitante) -> None:
        """Ayudante recursivo del recorrido pre-order."""
        if nodo is None:
            return
        visitante(nodo.producto)
        self._preorden_rec(nodo.izquierdo, visitante)
        self._preorden_rec(nodo.derecho, visitante)

    # Complejidad: O(n)
    def postorden(self, visitante: Visitante) -> None:
        """Recorre Izq->Der->Raíz aplicando el visitante (callback)."""
        self._postorden_rec(self._raiz, visitante)

    # Complejidad: O(n)
    def _postorden_rec(self, nodo: Optional[NodoBST], visitante: Visitante) -> None:
        """Ayudante recursivo del recorrido post-order."""
        if nodo is None:
            return
        self._postorden_rec(nodo.izquierdo, visitante)
        self._postorden_rec(nodo.derecho, visitante)
        visitante(nodo.producto)

    # Complejidad: O(k + h) donde k = nodos en rango, O(n) peor caso
    def rango(self, minimo: int, maximo: int, visitante: Visitante) -> None:
        """In-order con PODA real: no entra a ramas fuera del rango."""
        self._rango_rec(self._raiz, minimo, maximo, visitante)

    # Complejidad: O(k + h) donde k = nodos en rango, O(n) peor caso
    def _rango_rec(self, nodo: Optional[NodoBST], minimo: int,
                   maximo: int, visitante: Visitante) -> None:
        """Ayudante recursivo podado del reporte por rango."""
        if nodo is None:
            return
        codigo = nodo.producto.codigo
        if codigo > minimo:
            self._rango_rec(nodo.izquierdo, minimo, maximo, visitante)
        if minimo <= codigo <= maximo:
            visitante(nodo.producto)
        if codigo < maximo:
            self._rango_rec(nodo.derecho, minimo, maximo, visitante)

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def minimo(self) -> Optional[Producto]:
        """Retorna el producto de código mínimo (iterativo)."""
        if self._raiz is None:
            return None
        return self._minimo_nodo(self._raiz).producto

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def maximo(self) -> Optional[Producto]:
        """Retorna el producto de código máximo (iterativo)."""
        actual = self._raiz
        if actual is None:
            return None
        while actual.derecho is not None:
            actual = actual.derecho
        return actual.producto

    # Complejidad: O(h) promedio, O(n) peor caso (árbol degenerado)
    def _minimo_nodo(self, nodo: NodoBST) -> NodoBST:
        """Baja iterativamente a la izquierda hasta el mínimo."""
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    # Complejidad: O(n)
    def contar(self) -> int:
        """Cuenta los nodos reutilizando el recorrido in-order."""
        total = 0

        # Complejidad: O(1) por visita, O(n) total
        def _visitar(producto: Producto) -> None:
            """Incrementa el contador por cada nodo visitado."""
            nonlocal total
            total += 1

        self.inorden(_visitar)
        return total

    # Complejidad: O(n)
    def altura(self) -> int:
        """Altura del árbol (raíz = 1; vacío = 0)."""
        return self._altura_rec(self._raiz)

    # Complejidad: O(n)
    def _altura_rec(self, nodo: Optional[NodoBST]) -> int:
        """Ayudante recursivo que calcula la altura."""
        if nodo is None:
            return 0
        izq = self._altura_rec(nodo.izquierdo)
        der = self._altura_rec(nodo.derecho)
        return 1 + (izq if izq > der else der)

    # Complejidad: O(n)
    def valor_total(self) -> float:
        """Suma precio*stock reutilizando el recorrido in-order."""
        total = 0.0

        # Complejidad: O(1) por visita, O(n) total
        def _visitar(producto: Producto) -> None:
            """Acumula precio*stock de cada nodo visitado."""
            nonlocal total
            total += producto.precio * producto.stock

        self.inorden(_visitar)
        return total
