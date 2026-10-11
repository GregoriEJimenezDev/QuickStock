# -*- coding: utf-8 -*-
"""QuickStock: punto de entrada de la aplicación de consola."""
from __future__ import annotations
import sys
import os as _os

sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
sys.setrecursionlimit(20000)

from estructure.bst import ArbolBST
from services.inventario import ServicioInventario
from view.consola import VistaConsola
from view.menu import MenuConsola


# Complejidad: O(t) donde t = interacciones del usuario en el menú
def main() -> None:
    """Crea dependencias, las inyecta y ejecuta el menú hasta salir."""
    arbol = None
    servicio = None
    vista = VistaConsola()
    try:
        arbol = ArbolBST()
        servicio = ServicioInventario(arbol)
        menu = MenuConsola(servicio, vista)
        menu.ejecutar()
    except (EOFError, KeyboardInterrupt):
        vista.mostrar_mensaje("Programa terminado.")
    except Exception as error:
        vista.mostrar_error("Error inesperado: %s" % error)
    finally:
        try:
            if servicio is not None:
                total = servicio.total_productos()
                vista.mostrar_mensaje("Resumen final: total de productos = %d." % total)
            else:
                vista.mostrar_mensaje(
                    "Resumen final no disponible (el programa terminó antes de iniciar).")
        except Exception:
            vista.mostrar_mensaje(
                "Resumen final no disponible (el programa terminó antes de iniciar).")


# Complejidad: O(1)
def _es_ejecucion_directa() -> bool:
    """Indica si el archivo se ejecuta como programa principal."""
    return __name__ == "__main__"


if _es_ejecucion_directa():
    main()
