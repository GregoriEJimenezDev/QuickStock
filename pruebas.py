"""Pruebas de QuickStock con assert, sin librerías externas ni consola interactiva."""
from __future__ import annotations
import ast
import glob
import math
import os
import random
import sys

sys.setrecursionlimit(20000)

from estructura.bst import ArbolBST
from estructura.recorrido import Recorrido
from models.producto import ProductoFactory
from models.validador import Validador
from services.inventario import ServicioInventario

BASE = os.path.dirname(os.path.abspath(__file__))
DATOS_9 = ((50, 5), (30, 3), (70, 7), (20, 2), (40, 4),
           (60, 6), (80, 8), (35, 0), (45, 1))


# Complejidad: O(n) donde n = códigos esperados
def afirmar_orden(arbol: ArbolBST, esperado: tuple, recorrido: Recorrido) -> None:
    """Comprueba un recorrido sin guardar productos en listas."""
    pasos = {Recorrido.INORDEN: arbol.inorden,
             Recorrido.PREORDEN: arbol.preorden,
             Recorrido.POSTORDEN: arbol.postorden}
    indice = 0

    # Complejidad: O(1) por visita, O(n) total
    def _revisar(producto) -> None:
        nonlocal indice
        assert producto.codigo == esperado[indice], (recorrido, indice)
        indice += 1

    pasos[recorrido](_revisar)
    assert indice == len(esperado), (recorrido, indice, len(esperado))


# Complejidad: O(1)
def _servicio_nuevo() -> tuple:
    """Crea un árbol vacío con su servicio."""
    arbol = ArbolBST()
    return arbol, ServicioInventario(arbol)


# Complejidad: O(n) donde n = nodos del árbol de prueba
def prueba_arbol_9_nodos() -> None:
    arbol, servicio = _servicio_nuevo()
    for codigo, stock in DATOS_9:
        assert servicio.registrar(codigo, "N%d" % codigo, "C", 10.0, stock) is True
    afirmar_orden(arbol, (20, 30, 35, 40, 45, 50, 60, 70, 80), Recorrido.INORDEN)
    afirmar_orden(arbol, (50, 30, 20, 40, 35, 45, 70, 60, 80), Recorrido.PREORDEN)
    afirmar_orden(arbol, (20, 35, 45, 40, 30, 60, 80, 70, 50), Recorrido.POSTORDEN)
    assert arbol.altura() == 4
    assert arbol.minimo().codigo == 20
    assert arbol.maximo().codigo == 80
    assert servicio.total_productos() == 9
    print("OK arbol de 9 nodos")


# Complejidad: O(n) donde n = nodos del árbol de prueba
def prueba_reportes_9_nodos() -> None:
    arbol, servicio = _servicio_nuevo()
    for codigo, stock in DATOS_9:
        assert servicio.registrar(codigo, "N%d" % codigo, "C", 10.0, stock) is True
    assert servicio.valor_total() == 360.0
    afirmar_reporte(servicio, 2, (20, 35, 45))
    afirmar_rango(servicio, 30, 45, (30, 35, 40, 45))
    afirmar_rango(servicio, 61, 69, ())
    print("OK reportes de 9 nodos")


# Complejidad: O(k) donde k = productos esperados
def afirmar_reporte(servicio: ServicioInventario, limite: int, esperado: tuple) -> None:
    """Comprueba el reporte de stock bajo sin guardar productos en listas."""
    indice = 0

    # Complejidad: O(1) por visita, O(n) total
    def _revisar(producto) -> None:
        nonlocal indice
        assert producto.codigo == esperado[indice], (limite, indice)
        indice += 1

    hallados = servicio.reporte_stock_bajo(limite, _revisar)
    assert hallados == len(esperado) and indice == len(esperado)


# Complejidad: O(k) donde k = productos esperados
def afirmar_rango(servicio: ServicioInventario, minimo: int,
                  maximo: int, esperado: tuple) -> None:
    """Comprueba el reporte por rango sin guardar productos en listas."""
    indice = 0

    # Complejidad: O(1) por visita, O(k + h) total
    def _revisar(producto) -> None:
        nonlocal indice
        assert producto.codigo == esperado[indice], (minimo, maximo, indice)
        indice += 1

    hallados = servicio.reporte_rango(minimo, maximo, _revisar)
    assert hallados == len(esperado) and indice == len(esperado)


# Complejidad: O(n) donde n = nodos tras cada eliminación
def prueba_eliminaciones() -> None:
    arbol, servicio = _servicio_nuevo()
    for codigo, stock in DATOS_9:
        assert servicio.registrar(codigo, "N%d" % codigo, "C", 10.0, stock) is True
    assert servicio.eliminar(20) is True
    afirmar_orden(arbol, (30, 35, 40, 45, 50, 60, 70, 80), Recorrido.INORDEN)
    assert servicio.eliminar(30) is True
    afirmar_orden(arbol, (35, 40, 45, 50, 60, 70, 80), Recorrido.INORDEN)
    assert servicio.eliminar(70) is True
    afirmar_orden(arbol, (35, 40, 45, 50, 60, 80), Recorrido.INORDEN)
    assert servicio.eliminar(50) is True
    afirmar_orden(arbol, (35, 40, 45, 60, 80), Recorrido.INORDEN)
    assert servicio.total_productos() == 5
    print("OK eliminaciones hoja, un hijo, dos hijos y raiz")


# Complejidad: O(1)
def prueba_limites() -> None:
    arbol, servicio = _servicio_nuevo()
    assert servicio.registrar(50, "A", "C", 10.0, 5) is True
    assert servicio.registrar(50, "B", "C", 10.0, 5) is False
    assert servicio.eliminar(999) is False
    assert servicio.buscar_por_codigo(999) is None
    assert servicio.editar(999, "X", "Y", 1.0, 0) is False
    vacio, servicio_vacio = _servicio_nuevo()
    assert servicio_vacio.listar(Recorrido.INORDEN, lambda p: None) is False
    assert servicio_vacio.estado() == (0, 0, None, None)
    assert servicio_vacio.reporte_stock_bajo(10, lambda p: None) == 0
    assert servicio_vacio.reporte_rango(1, 100, lambda p: None) == 0
    assert servicio_vacio.buscar_por_codigo(1) is None
    assert vacio.esta_vacio() is True
    print("OK limites")


# Complejidad: O(h) promedio, O(n) peor caso (búsqueda del BST)
def prueba_edicion_atomica() -> None:
    _, servicio = _servicio_nuevo()
    assert servicio.registrar(7, "Orig", "Cat", 5.0, 4) is True
    try:
        servicio.editar(7, "Nuevo", "Nueva", 0, 9)
        raise AssertionError("editar con precio 0 debió fallar")
    except ValueError:
        pass
    producto = servicio.buscar_por_codigo(7)
    assert (producto.nombre, producto.categoria, producto.precio, producto.stock) == (
        "Orig", "Cat", 5.0, 4)
    try:
        servicio.editar(7, "Nuevo", "Nueva", float("nan"), 9)
        raise AssertionError("editar con nan debió fallar")
    except ValueError:
        pass
    assert servicio.buscar_por_codigo(7).nombre == "Orig"
    print("OK edicion atomica")


# Complejidad: O(1)
def prueba_nan_inf() -> None:
    for malo in (float("nan"), float("inf"), float("-inf")):
        try:
            Validador.precio(malo)
            raise AssertionError("precio debió rechazar %r" % (malo,))
        except ValueError:
            pass
    _, servicio = _servicio_nuevo()
    try:
        servicio.registrar(1, "A", "C", float("nan"), 1)
        raise AssertionError("registrar con nan debió fallar")
    except ValueError:
        pass
    assert servicio.buscar_por_codigo(1) is None
    print("OK nan e inf rechazados")


# Complejidad: O(m * h) donde m = operaciones y h = altura del árbol
def prueba_fuzz() -> None:
    azar = random.Random(20261012)
    arbol = ArbolBST()
    referencia = set()
    for _ in range(4000):
        codigo = azar.randint(1, 500)
        if azar.random() < 0.5:
            nuevo = codigo not in referencia
            assert arbol.insertar(
                ProductoFactory.crear(codigo, "N", "C", 1.0, 1)) is nuevo
            referencia.add(codigo)
        else:
            existe = codigo in referencia
            assert arbol.eliminar(codigo) is existe
            referencia.discard(codigo)
    assert arbol.contar() == len(referencia)
    afirmar_orden(arbol, tuple(sorted(referencia)), Recorrido.INORDEN)
    print("OK fuzz 4000 operaciones")


# Complejidad: O(n) donde n = códigos insertados
def prueba_5000_ascendentes() -> None:
    arbol = ArbolBST()
    for codigo in range(1, 5001):
        assert arbol.insertar(
            ProductoFactory.crear(codigo, "N", "C", 1.0, 1)) is True
    assert arbol.buscar(5000).codigo == 5000
    assert arbol.eliminar(2500) is True
    assert arbol.buscar(2500) is None
    print("OK 5000 ascendentes sin RecursionError")


# Complejidad: O(f) donde f = funciones del proyecto
def prueba_big_o() -> None:
    faltantes = []
    patrones = [os.path.join(BASE, "*.py"),
                os.path.join(BASE, "*", "*.py")]
    archivos = []
    for patron in patrones:
        archivos.extend(glob.glob(patron))
    for ruta in sorted(archivos):
        if "__pycache__" in ruta:
            continue
        lineas = open(ruta, encoding="utf-8").read().splitlines()
        arbol_ast = ast.parse(open(ruta, encoding="utf-8").read())
        for nodo in ast.walk(arbol_ast):
            if isinstance(nodo, (ast.FunctionDef, ast.AsyncFunctionDef)):
                ventana = lineas[max(0, nodo.lineno - 3):nodo.lineno - 1]
                if not any("Complejidad" in previa and "O(" in previa
                           for previa in ventana):
                    faltantes.append("%s:%s" % (os.path.basename(ruta), nodo.name))
    for faltante in faltantes:
        print("Sin Big-O: %s" % faltante)
    assert not faltantes, faltantes
    print("OK 100% Big-O")


# Complejidad: O(m * h + n + f) donde m = operaciones fuzz, n = inserciones y f = funciones
def ejecutar_todo() -> None:
    prueba_arbol_9_nodos()
    prueba_reportes_9_nodos()
    prueba_eliminaciones()
    prueba_limites()
    prueba_edicion_atomica()
    prueba_nan_inf()
    prueba_fuzz()
    prueba_5000_ascendentes()
    prueba_big_o()
    print("QuickStock: todas las pruebas pasaron.")


if __name__ == "__main__":
    ejecutar_todo()
