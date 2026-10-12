"""Menú de consola: flujo controlado de las 8 opciones en orden."""
from __future__ import annotations
from estructura.recorrido import Recorrido
from models.protocolos import Vista
from services.inventario import ServicioInventario
from models.validador import Validador
from view.constantes import (
    ENC_BUSCAR, ENC_EDITAR, ENC_ELIMINAR, ENC_ESTADO, ENC_LISTAR,
    ENC_REGISTRAR, ENC_REPORTES, MSG_ALTURA, MSG_ALTURA_FINAL,
    MSG_CANCELADO, MSG_CANTIDAD, MSG_CONFIRMAR_ELIMINAR,
    MSG_CONFIRMAR_SALIR, MSG_DESPEDIDA, MSG_DUPLICADO,
    MSG_EDICION_OK, MSG_ELIMINACION_OK, MSG_MAXIMO_TITULO,
    MSG_MINIMO_TITULO, MSG_NO_ENCONTRADO, MSG_OPCION_INVALIDA,
    MSG_RANGO_INVALIDO, MSG_REGISTRO_OK, MSG_SIN_PRODUCTOS,
    MSG_SIN_RESULTADOS, MSG_SUBMENU_INVALIDO, MSG_TOTAL_FINAL,
    MSG_TOTAL_REPORTE, MSG_VALOR_REPORTE,
    PROMPT_BUSCAR, PROMPT_CATEGORIA, PROMPT_CODIGO, PROMPT_EDITAR,
    PROMPT_ELIMINAR, PROMPT_MAXIMO, PROMPT_MINIMO, PROMPT_NOMBRE,
    PROMPT_NUEVA_CATEGORIA, PROMPT_NUEVO_NOMBRE, PROMPT_NUEVO_PRECIO,
    PROMPT_NUEVO_STOCK, PROMPT_OPCION, PROMPT_PRECIO, PROMPT_STOCK,
    PROMPT_SUBMENU_LISTAR, PROMPT_SUBMENU_REPORTES, PROMPT_UMBRAL,
    TITULO_RESUMEN,
)


class MenuConsola:
    """Controla el bucle principal. Recibe servicio y vista inyectados."""

    # Complejidad: O(1)
    def __init__(self, servicio: ServicioInventario, vista: Vista) -> None:
        self._servicio = servicio
        self._vista = vista
        self._acciones = {
            "1": self._opcion_registrar,
            "2": self._opcion_buscar,
            "3": self._opcion_editar,
            "4": self._opcion_eliminar,
            "5": self._opcion_listar,
            "6": self._opcion_reportes,
            "7": self._opcion_estado,
            "8": self._opcion_salir,
        }
        self._listados = {
            "A": Recorrido.INORDEN,
            "B": Recorrido.PREORDEN,
            "C": Recorrido.POSTORDEN,
        }
        self._reportes = {
            "A": self._reporte_stock_bajo,
            "B": self._reporte_rango,
            "C": self._reporte_total,
            "D": self._reporte_valor,
        }

    # Complejidad: O(t) donde t = interacciones del usuario
    def ejecutar(self) -> None:
        self._vista.mostrar_titulo()
        while True:
            self._vista.mostrar_menu_principal()
            accion = self._acciones.get(self._vista.leer_texto_libre(PROMPT_OPCION))
            if accion is None:
                self._vista.mostrar_error(MSG_OPCION_INVALIDA)
                continue
            if accion() is True:
                break

    # Complejidad: O(n) por el estado del árbol
    def resumen_final(self) -> None:
        total, altura, _, _ = self._servicio.estado()
        self._vista.mostrar_encabezado(TITULO_RESUMEN)
        self._vista.mostrar_mensaje(MSG_TOTAL_FINAL % total)
        self._vista.mostrar_mensaje(MSG_ALTURA_FINAL % altura)

    # Complejidad: O(n) por el resumen final
    def error_y_resumen(self, mensaje: str) -> None:
        self._vista.mostrar_error(mensaje)
        self.resumen_final()

    # Complejidad: O(h) promedio, O(n) peor caso (inserción BST)
    def _opcion_registrar(self) -> None:
        self._vista.mostrar_encabezado(ENC_REGISTRAR)
        codigo = self._vista.leer_codigo(PROMPT_CODIGO)
        if self._servicio.buscar_por_codigo(codigo) is not None:
            self._vista.mostrar_error(MSG_DUPLICADO)
            return
        nombre = self._vista.leer_texto_no_vacio(PROMPT_NOMBRE)
        categoria = self._vista.leer_texto_no_vacio(PROMPT_CATEGORIA)
        precio = self._vista.leer_precio(PROMPT_PRECIO)
        stock = self._vista.leer_stock(PROMPT_STOCK)
        if self._servicio.registrar(codigo, nombre, categoria, precio, stock):
            self._vista.mostrar_mensaje(MSG_REGISTRO_OK)
        else:
            self._vista.mostrar_error(MSG_DUPLICADO)

    # Complejidad: O(h) promedio, O(n) peor caso (búsqueda BST)
    def _opcion_buscar(self) -> None:
        self._vista.mostrar_encabezado(ENC_BUSCAR)
        producto = self._servicio.buscar_por_codigo(self._vista.leer_codigo(PROMPT_BUSCAR))
        if producto is None:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)
            return
        self._vista.mostrar_encabezado_tabla()
        self._vista.mostrar_producto(producto)

    # Complejidad: O(h) promedio, O(n) peor caso (búsqueda BST)
    def _opcion_editar(self) -> None:
        self._vista.mostrar_encabezado(ENC_EDITAR)
        codigo = self._vista.leer_codigo(PROMPT_EDITAR)
        if self._servicio.buscar_por_codigo(codigo) is None:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)
            return
        nombre = self._vista.leer_texto_no_vacio(PROMPT_NUEVO_NOMBRE)
        categoria = self._vista.leer_texto_no_vacio(PROMPT_NUEVA_CATEGORIA)
        precio = self._vista.leer_precio(PROMPT_NUEVO_PRECIO)
        stock = self._vista.leer_stock(PROMPT_NUEVO_STOCK)
        try:
            editado = self._servicio.editar(codigo, nombre, categoria, precio, stock)
        except ValueError as error:
            self._vista.mostrar_error(str(error))
            return
        if editado:
            self._vista.mostrar_mensaje(MSG_EDICION_OK)
        else:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)

    # Complejidad: O(h) promedio, O(n) peor caso (eliminación BST)
    def _opcion_eliminar(self) -> None:
        self._vista.mostrar_encabezado(ENC_ELIMINAR)
        producto = self._servicio.buscar_por_codigo(self._vista.leer_codigo(PROMPT_ELIMINAR))
        if producto is None:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)
            return
        self._vista.mostrar_encabezado_tabla()
        self._vista.mostrar_producto(producto)
        if not self._vista.leer_confirmacion(MSG_CONFIRMAR_ELIMINAR):
            self._vista.mostrar_mensaje(MSG_CANCELADO)
            return
        if self._servicio.eliminar(producto.codigo):
            self._vista.mostrar_mensaje(MSG_ELIMINACION_OK)
        else:
            self._vista.mostrar_mensaje(MSG_NO_ENCONTRADO)

    # Complejidad: O(n)
    def _opcion_listar(self) -> None:
        self._vista.mostrar_encabezado(ENC_LISTAR)
        self._vista.mostrar_submenu_listar()
        opcion = self._vista.leer_texto_libre(PROMPT_SUBMENU_LISTAR).upper()
        if opcion == "V":
            return
        recorrido = self._listados.get(opcion)
        if recorrido is None:
            self._vista.mostrar_error(MSG_SUBMENU_INVALIDO)
            return
        self._vista.mostrar_encabezado_tabla()
        if not self._servicio.listar(recorrido, self._vista.mostrar_producto):
            self._vista.mostrar_mensaje(MSG_SIN_PRODUCTOS)

    # Complejidad: O(n) peor caso (reportes sobre el BST)
    def _opcion_reportes(self) -> None:
        self._vista.mostrar_encabezado(ENC_REPORTES)
        self._vista.mostrar_submenu_reportes()
        opcion = self._vista.leer_texto_libre(PROMPT_SUBMENU_REPORTES).upper()
        if opcion == "V":
            return
        reporte = self._reportes.get(opcion)
        if reporte is None:
            self._vista.mostrar_error(MSG_SUBMENU_INVALIDO)
            return
        reporte()

    # Complejidad: O(n)
    def _reporte_stock_bajo(self) -> None:
        limite = self._vista.leer_umbral(PROMPT_UMBRAL)
        self._vista.mostrar_encabezado_tabla()
        hallados = self._servicio.reporte_stock_bajo(limite, self._vista.mostrar_producto)
        if hallados == 0:
            self._vista.mostrar_mensaje(MSG_SIN_RESULTADOS)

    # Complejidad: O(k + h) donde k = nodos en rango, O(n) peor caso
    def _reporte_rango(self) -> None:
        while True:
            minimo = self._vista.leer_entero(PROMPT_MINIMO)
            maximo = self._vista.leer_entero(PROMPT_MAXIMO)
            if Validador.rango_valido(minimo, maximo):
                break
            self._vista.mostrar_error(MSG_RANGO_INVALIDO)
        self._vista.mostrar_encabezado_tabla()
        hallados = self._servicio.reporte_rango(minimo, maximo, self._vista.mostrar_producto)
        if hallados == 0:
            self._vista.mostrar_mensaje(MSG_SIN_RESULTADOS)

    # Complejidad: O(n) por el conteo de nodos
    def _reporte_total(self) -> None:
        self._vista.mostrar_mensaje(MSG_TOTAL_REPORTE % self._servicio.total_productos())

    # Complejidad: O(n)
    def _reporte_valor(self) -> None:
        self._vista.mostrar_mensaje(MSG_VALOR_REPORTE % self._servicio.valor_total())

    # Complejidad: O(n) por la altura; resto O(h)
    def _opcion_estado(self) -> None:
        self._vista.mostrar_encabezado(ENC_ESTADO)
        total, altura, minimo, maximo = self._servicio.estado()
        self._vista.mostrar_mensaje(MSG_CANTIDAD % total)
        self._vista.mostrar_mensaje(MSG_ALTURA % altura)
        if minimo is None or maximo is None:
            self._vista.mostrar_mensaje(MSG_SIN_PRODUCTOS)
            return
        self._vista.mostrar_mensaje(MSG_MINIMO_TITULO)
        self._vista.mostrar_producto(minimo)
        self._vista.mostrar_mensaje(MSG_MAXIMO_TITULO)
        self._vista.mostrar_producto(maximo)

    # Complejidad: O(n) por el resumen (conteo + altura)
    def _opcion_salir(self) -> bool:
        if not self._vista.leer_confirmacion(MSG_CONFIRMAR_SALIR):
            self._vista.mostrar_mensaje(MSG_CANCELADO)
            return False
        self.resumen_final()
        self._vista.mostrar_mensaje(MSG_DESPEDIDA)
        return True
