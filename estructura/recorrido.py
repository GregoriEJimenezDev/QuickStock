"""Recorridos disponibles del árbol."""
from __future__ import annotations
from enum import Enum


class Recorrido(str, Enum):
    INORDEN = "inorden"
    PREORDEN = "preorden"
    POSTORDEN = "postorden"
