# -*- coding: utf-8 -*-
"""QuickStock: punto de entrada de la aplicación de consola."""
from __future__ import annotations
import sys

sys.setrecursionlimit(20000)

from estructura.bst import ArbolBST
from services.inventario import ServicioInventario
from view.consola import VistaConsola
from view.menu import MenuConsola
from view.constantes import MSG_ERROR_INESPERADO, MSG_NO_INICIO, MSG_SALIDA_ANORMAL


# Complejidad: O(1)
def build_app() -> MenuConsola:
    """Instancia y cablea árbol, servicio, vista y menú."""
    arbol = ArbolBST()
    servicio = ServicioInventario(arbol)
    vista = VistaConsola()
    return MenuConsola(servicio, vista)


# Complejidad: O(t) donde t = interacciones del usuario en el menú
def main() -> None:
    """Arranca el menú; el resumen final se muestra una sola vez."""
    try:
        menu = build_app()
    except Exception:
        print(MSG_NO_INICIO)
        return
    try:
        menu.ejecutar()
    except (EOFError, KeyboardInterrupt):
        menu.error_y_resumen(MSG_SALIDA_ANORMAL)
    except Exception as error:
        menu.error_y_resumen(MSG_ERROR_INESPERADO % error)


if __name__ == "__main__":
    main()
