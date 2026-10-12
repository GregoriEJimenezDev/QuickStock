"""Menú de consola: flujo controlado de las 8 opciones en orden."""
from __future__ import annotations
import sys
import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
from services.inventario import ServicioInventario
from services.validador import Validador
from view.consola import VistaConsola
from view.constantes import (MSG_SIN_PRODUCTOS, MSG_NO_ENCONTRADO,
                              MSG_DUPLICADO, MSG_RANGO_INVALIDO,
                              MSG_SIN_RESULTADOS, MSG_CANCELADO,
                              MSG_CONFIRMAR_SALIR, MSG_CONFIRMAR_ELIMINAR,
                              MSG_DESPEDIDA)


class MenuConsola:
    """Controla el bucle principal. Recibe servicio y vista inyectados."""

    # Complejidad: O(1)
    def __init__(self, servicio: ServicioInventario, vista: VistaConsola) -> None:
        self._servicio = servicio
        self._vista = vista

    # Complejidad: O(t) donde t = interacciones del usuario
    def ejecutar(self) -> None:
        self._vista.mostrar_titulo()
        while True:
            self._vista.mostrar_menu_principal()
            opcion = self._vista.leer_texto_libre("Seleccione una opción (1-8): ")
            if opcion == "1":
                self._opcion_registrar()
            elif opcion == "2":
                self._opcion_buscar()
            elif opcion == "3":
                self._opcion_editar()
            elif opcion == "4":
                self._opcion_eliminar()
            elif opcion == "5":
                self._opcion_listar()
            elif opcion == "6":
                self._opcion_reportes()
            elif opcion == "7":
                self._opcion_estado()
            elif opcion == "8":
                if self._opcion_salir():
                    break
            else:
                self._vista.mostrar_error("Opción inválida. Elija del 1 al 8.")

    # Complejidad: O(h) promedio, O(n) peor caso (inserción BST)
    def _opcion_registrar(self) -> None:
        self._vista.mostrar_encabezado("1. Registrar producto")
        codigo = self._vista.leer_entero("Código (entero > 0): ")
        if self._servicio.buscar_por_codigo(codigo) is not None:
            self._vista.mostrar_error(MSG_DUPLICADO)
            return
        nombre = self._vista.leer_texto_no_vacio("Nombre: ")
        categoria = self._vista.leer_texto_no_vacio("Categoría: ")
        precio = self._vista.leer_decimal("Precio (> 0): ")
        stock = self._vista.leer_entero("Stock (>= 0): ")
        try:
            ok = self._servicio.registrar(codigo, nombre, categoria, precio, stock)
        except ValueError as error:
            self._vista.mostrar_error(str(error))
            return
        if ok:
            self._vista.mostrar_mensaje("Producto registrado correctamente.")
        else:
            self._vista.mostrar_error(MSG_DUPLICADO)

    # Complejidad: O(h) promedio, O(n) peor caso (búsqueda BST)
    def _opcion_buscar(self) -> None:
        self._vista.mostrar_encabezado("2. Buscar producto")
        codigo = self._vista.leer_entero("Código a buscar: ")
        producto = self._servicio.buscar_por_codigo(codigo)
        if producto is None:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)
            return
        self._vista.mostrar_encabezado_tabla()
        self._vista.mostrar_producto(producto)

    # Complejidad: O(h) promedio, O(n) peor caso (búsqueda BST)
    def _opcion_editar(self) -> None:
        self._vista.mostrar_encabezado("3. Editar producto")
        codigo = self._vista.leer_entero("Código a editar: ")
        if self._servicio.buscar_por_codigo(codigo) is None:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)
            return
        nombre = self._vista.leer_texto_no_vacio("Nuevo nombre: ")
        categoria = self._vista.leer_texto_no_vacio("Nueva categoría: ")
        precio = self._vista.leer_decimal("Nuevo precio (> 0): ")
        stock = self._vista.leer_entero("Nuevo stock (>= 0): ")
        try:
            ok = self._servicio.editar(codigo, nombre, categoria, precio, stock)
        except ValueError as error:
            self._vista.mostrar_error(str(error))
            return
        if ok:
            self._vista.mostrar_mensaje("Producto actualizado correctamente.")
        else:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)

    # Complejidad: O(h) promedio, O(n) peor caso (eliminación BST)
    def _opcion_eliminar(self) -> None:
        self._vista.mostrar_encabezado("4. Eliminar producto")
        codigo = self._vista.leer_entero("Código a eliminar: ")
        producto = self._servicio.buscar_por_codigo(codigo)
        if producto is None:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)
            return
        self._vista.mostrar_encabezado_tabla()
        self._vista.mostrar_producto(producto)
        if not self._vista.leer_confirmacion(MSG_CONFIRMAR_ELIMINAR):
            self._vista.mostrar_mensaje(MSG_CANCELADO)
            return
        if self._servicio.eliminar(codigo):
            self._vista.mostrar_mensaje("Producto eliminado correctamente.")
        else:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)

    # Complejidad: O(n)
    def _opcion_listar(self) -> None:
        self._vista.mostrar_encabezado("5. Listar productos")
        self._vista.mostrar_submenu_listar()
        opcion = self._vista.leer_texto_libre("Elija (A/B/C/V): ").upper()
        if opcion == "V":
            return
        modos = {"A": "inorden", "B": "preorden", "C": "postorden"}
        if opcion not in modos:
            self._vista.mostrar_error("Opción inválida del submenú.")
            return
        self._vista.mostrar_encabezado_tabla()
        hay = self._servicio.listar(modos[opcion], self._vista.mostrar_producto)
        if not hay:
            self._vista.mostrar_mensaje(MSG_SIN_PRODUCTOS)

    # Complejidad: O(n) peor caso (reportes sobre el BST)
    def _opcion_reportes(self) -> None:
        self._vista.mostrar_encabezado("6. Generar reportes")
        self._vista.mostrar_submenu_reportes()
        opcion = self._vista.leer_texto_libre("Elija (A/B/C/D/V): ").upper()
        if opcion == "V":
            return
        elif opcion == "A":
            self._reporte_stock_bajo()
        elif opcion == "B":
            self._reporte_rango()
        elif opcion == "C":
            self._vista.mostrar_mensaje(
                "Total de productos registrados: %d" % self._servicio.total_productos())
        elif opcion == "D":
            self._vista.mostrar_mensaje(
                "Valor total del inventario: %.2f" % self._servicio.valor_total())
        else:
            self._vista.mostrar_error("Opción inválida del submenú.")

    # Complejidad: O(n)
    def _reporte_stock_bajo(self) -> None:
        limite = self._vista.leer_entero("Umbral X de stock (>= 0): ")
        try:
            Validador.limite_stock(limite)
        except ValueError as error:
            self._vista.mostrar_error(str(error))
            return
        self._vista.mostrar_encabezado_tabla()
        hallados = self._servicio.reporte_stock_bajo(limite, self._vista.mostrar_producto)
        if hallados == 0:
            self._vista.mostrar_mensaje(MSG_SIN_RESULTADOS)

    # Complejidad: O(k + h) donde k = nodos en rango, O(n) peor caso
    def _reporte_rango(self) -> None:
        while True:
            minimo = self._vista.leer_entero("Código mínimo: ")
            maximo = self._vista.leer_entero("Código máximo: ")
            if Validador.rango_valido(minimo, maximo):
                break
            self._vista.mostrar_error(MSG_RANGO_INVALIDO)
        self._vista.mostrar_encabezado_tabla()
        hallados = self._servicio.reporte_rango(minimo, maximo, self._vista.mostrar_producto)
        if hallados == 0:
            self._vista.mostrar_mensaje(MSG_SIN_RESULTADOS)

    # Complejidad: O(n) por la altura; resto O(h)
    def _opcion_estado(self) -> None:
        self._vista.mostrar_encabezado("7. Estado del árbol")
        total, altura, minimo, maximo = self._servicio.estado()
        self._vista.mostrar_mensaje("Cantidad total de productos: %d" % total)
        self._vista.mostrar_mensaje("Altura del árbol: %d" % altura)
        if minimo is None or maximo is None:
            self._vista.mostrar_mensaje(MSG_SIN_PRODUCTOS)
            return
        self._vista.mostrar_mensaje("Producto con código mínimo:")
        self._vista.mostrar_producto(minimo)
        self._vista.mostrar_mensaje("Producto con código máximo:")
        self._vista.mostrar_producto(maximo)

    # Complejidad: O(n) por el resumen (conteo + altura)
    def _opcion_salir(self) -> bool:
        if not self._vista.leer_confirmacion(MSG_CONFIRMAR_SALIR):
            self._vista.mostrar_mensaje(MSG_CANCELADO)
            return False
        total, altura, _, _ = self._servicio.estado()
        self._vista.mostrar_encabezado("Resumen final")
        self._vista.mostrar_mensaje("Total de productos: %d" % total)
        self._vista.mostrar_mensaje("Altura del árbol: %d" % altura)
        self._vista.mostrar_mensaje(MSG_DESPEDIDA)
        return True
