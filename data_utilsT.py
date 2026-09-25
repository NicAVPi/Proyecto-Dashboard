"""Carga y valida los CSV generados por el notebook (Modelo/ModeloL)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).parent / "data"

COLUMNAS_PREDICCIONES = {
    "id", "grupo", "periodo", "internet", "computador", "tipo_colegio",
    "valor_real", "probabilidad",
}
COLUMNAS_METRICAS = {"modelo", "exactitud", "precision", "recall", "f1", "roc_auc"}


@dataclass
class Datos:
    predicciones: pd.DataFrame
    metricas: pd.DataFrame
    importancia: pd.DataFrame


def _leer_csv(nombre: str) -> pd.DataFrame:
    ruta = DATA_DIR / nombre
    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró {ruta}. Ejecuta de nuevo la celda de exportación del "
            f"notebook (Modelo / ModeloL) antes de correr el dashboard."
        )
    return pd.read_csv(ruta)


def cargar_y_validar() -> Datos:
    predicciones = _leer_csv("predicciones.csv")
    metricas = _leer_csv("metricas_modelos.csv")
    importancia = _leer_csv("importancia_variables.csv")

    faltantes = COLUMNAS_PREDICCIONES - set(predicciones.columns)
    if faltantes:
        raise ValueError(f"predicciones.csv no tiene las columnas: {sorted(faltantes)}")

    faltantes = COLUMNAS_METRICAS - set(metricas.columns)
    if faltantes:
        raise ValueError(f"metricas_modelos.csv no tiene las columnas: {sorted(faltantes)}")

    faltantes = {"variable", "importancia"} - set(importancia.columns)
    if faltantes:
        # Compatibilidad con una versión anterior de la celda 97 que usaba 'coeficiente'.
        if faltantes == {"importancia"} and "coeficiente" in importancia.columns:
            importancia = importancia.rename(columns={"coeficiente": "importancia"})
        else:
            raise ValueError(f"importancia_variables.csv no tiene las columnas: {sorted(faltantes)}")

    predicciones = predicciones.copy()
    predicciones["valor_real"] = predicciones["valor_real"].astype(int)
    predicciones["probabilidad"] = predicciones["probabilidad"].astype(float)
    predicciones["grupo"] = predicciones["grupo"].astype(str)
    predicciones["periodo"] = predicciones["periodo"].astype(str)

    return Datos(predicciones=predicciones, metricas=metricas, importancia=importancia)
