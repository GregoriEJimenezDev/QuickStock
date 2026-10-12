"""Prueba de flujo completo: el resumen final sale una sola vez."""
from __future__ import annotations
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ENTRADA = "1\n50\nManzana\nFrutas\n10\n5\n8\ns\n"


# Complejidad: O(t) donde t = interacciones simuladas con el menú
def ejecutar_flujo() -> str:
    """Corre main.py con entrada simulada y retorna su salida."""
    proceso = subprocess.run([sys.executable, "main.py"], input=ENTRADA,
                             text=True, capture_output=True, cwd=BASE, timeout=60)
    assert proceso.returncode == 0, proceso.stderr
    return proceso.stdout


# Complejidad: O(s) donde s = caracteres de la salida
def comprobar_resumen_unico(salida: str) -> None:
    """Exige un solo resumen con total y altura, sin el duplicado viejo."""
    assert salida.count("Resumen final") == 1, salida.count("Resumen final")
    assert "Total de productos: 1" in salida
    assert "Altura del árbol: 1" in salida
    assert "Resumen final: total de productos" not in salida


if __name__ == "__main__":
    comprobar_resumen_unico(ejecutar_flujo())
    print("Flujo completo: resumen único OK.")
