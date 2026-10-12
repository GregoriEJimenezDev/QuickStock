"""Textos de menús y mensajes."""

TITULO_APP = "=== QuickStock - Gestión de Inventario (BST) ==="

MENU_PRINCIPAL = """--- MENÚ PRINCIPAL ---
1. Registrar producto
2. Buscar producto
3. Editar producto
4. Eliminar producto
5. Listar productos
6. Generar reportes
7. Ver estado del árbol
8. Salir"""

SUBMENU_LISTAR = """--- LISTAR PRODUCTOS ---
A. In-order (ordenado por código)
B. Pre-order (Raíz -> Izq -> Der)
C. Post-order (Izq -> Der -> Raíz)
V. Volver"""

SUBMENU_REPORTES = """--- GENERAR REPORTES ---
A. Stock bajo
B. Rango de códigos
C. Total de productos registrados
D. Valor total del inventario
V. Volver"""

MSG_DESPEDIDA = "Gracias por usar QuickStock."
MSG_SIN_PRODUCTOS = "No hay productos registrados."
MSG_NO_ENCONTRADO = "No existe un producto con ese código."
MSG_DUPLICADO = "Ya existe un producto con ese código."
MSG_RANGO_INVALIDO = "El mínimo no puede ser mayor que el máximo."
MSG_SIN_RESULTADOS = "Sin resultados para la búsqueda."
MSG_CANCELADO = "Operación cancelada."
MSG_CONFIRMAR_SALIR = "¿Desea salir del programa? (s/n): "
MSG_CONFIRMAR_ELIMINAR = "¿Confirma la eliminación? (s/n): "
MSG_OPCION_INVALIDA = "Opción inválida. Elija del 1 al 8."
MSG_SUBMENU_INVALIDO = "Opción inválida del submenú."
MSG_SALIDA_ANORMAL = "Programa interrumpido."
MSG_NO_INICIO = "No se pudo iniciar QuickStock."
MSG_ERROR_INESPERADO = "Error inesperado: %s"

MSG_REGISTRO_OK = "Producto registrado correctamente."
MSG_EDICION_OK = "Producto actualizado correctamente."
MSG_ELIMINACION_OK = "Producto eliminado correctamente."

ENC_REGISTRAR = "1. Registrar producto"
ENC_BUSCAR = "2. Buscar producto"
ENC_EDITAR = "3. Editar producto"
ENC_ELIMINAR = "4. Eliminar producto"
ENC_LISTAR = "5. Listar productos"
ENC_REPORTES = "6. Generar reportes"
ENC_ESTADO = "7. Estado del árbol"
TITULO_RESUMEN = "Resumen final"

MSG_TOTAL_FINAL = "Total de productos: %d"
MSG_ALTURA_FINAL = "Altura del árbol: %d"
MSG_TOTAL_REPORTE = "Total de productos registrados: %d"
MSG_VALOR_REPORTE = "Valor total del inventario: %.2f"
MSG_CANTIDAD = "Cantidad total de productos: %d"
MSG_ALTURA = "Altura del árbol: %d"
MSG_MINIMO_TITULO = "Producto con código mínimo:"
MSG_MAXIMO_TITULO = "Producto con código máximo:"

PROMPT_OPCION = "Seleccione una opción (1-8): "
PROMPT_SUBMENU_LISTAR = "Elija (A/B/C/V): "
PROMPT_SUBMENU_REPORTES = "Elija (A/B/C/D/V): "
PROMPT_CODIGO = "Código (entero > 0): "
PROMPT_NOMBRE = "Nombre: "
PROMPT_CATEGORIA = "Categoría: "
PROMPT_PRECIO = "Precio (> 0): "
PROMPT_STOCK = "Stock (>= 0): "
PROMPT_NUEVO_NOMBRE = "Nuevo nombre: "
PROMPT_NUEVA_CATEGORIA = "Nueva categoría: "
PROMPT_NUEVO_PRECIO = "Nuevo precio (> 0): "
PROMPT_NUEVO_STOCK = "Nuevo stock (>= 0): "
PROMPT_BUSCAR = "Código a buscar: "
PROMPT_EDITAR = "Código a editar: "
PROMPT_ELIMINAR = "Código a eliminar: "
PROMPT_UMBRAL = "Umbral X de stock (>= 0): "
PROMPT_MINIMO = "Código mínimo: "
PROMPT_MAXIMO = "Código máximo: "

ENCABEZADO_PRODUCTO = "Código | Nombre | Categoría | Precio | Stock"
SEPARADOR = "-" * 60
