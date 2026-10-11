"""Validador centralizado (DRY: única implementación de reglas)."""
from __future__ import annotations


class Validador:
    """Reglas de negocio reutilizadas por Registrar y Editar."""

    # Complejidad: O(1)
    def __init__(self) -> None:
        """Inicializa el validador (sin estado)."""
        pass

    # Complejidad: O(1)
    @staticmethod
    def texto_no_vacio(valor: str, campo: str) -> str:
        """Valida texto no vacío (sin solo-espacios) y lo retorna limpio."""
        limpio = (valor or "").strip()
        if not limpio:
            raise ValueError("%s no puede estar vacío." % campo)
        return limpio

    # Complejidad: O(1)
    @staticmethod
    def codigo(valor: int) -> int:
        """Valida que el código sea entero positivo."""
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError("El código debe ser un número entero.")
        if valor <= 0:
            raise ValueError("El código debe ser mayor que 0.")
        return valor

    # Complejidad: O(1)
    @staticmethod
    def precio(valor: float) -> float:
        """Valida que el precio sea > 0."""
        if not isinstance(valor, (int, float)) or isinstance(valor, bool):
            raise ValueError("El precio debe ser numérico.")
        if float(valor) <= 0:
            raise ValueError("El precio debe ser mayor que 0.")
        return float(valor)

    # Complejidad: O(1)
    @staticmethod
    def stock(valor: int) -> int:
        """Valida que el stock sea entero >= 0."""
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError("El stock debe ser un número entero.")
        if valor < 0:
            raise ValueError("El stock no puede ser negativo.")
        return valor

    # Complejidad: O(1)
    @staticmethod
    def limite_stock(valor: int) -> int:
        """Valida el umbral X de stock bajo (>= 0)."""
        return Validador.stock(valor)

    # Complejidad: O(1)
    @staticmethod
    def rango_valido(minimo: int, maximo: int) -> bool:
        """Indica si el rango mínimo <= máximo es válido."""
        return minimo <= maximo
