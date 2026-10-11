"""Constantes de textos y menús (evita textos mágicos, apoya DRY)."""

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
MSG_RANGO_INVALIDO = "Error: el mínimo no puede ser mayor que el máximo."
MSG_SIN_RESULTADOS = "Sin resultados para la búsqueda."
MSG_CANCELADO = "Operación cancelada."
MSG_CONFIRMAR_SALIR = "¿Desea salir del programa? (s/n): "
MSG_CONFIRMAR_ELIMINAR = "¿Confirma la eliminación? (s/n): "

ENCABEZADO_PRODUCTO = "Código | Nombre | Categoría | Precio | Stock"
SEPARADOR = "-" * 60
