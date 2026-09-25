"""Carga y validacion del contrato de datos de la plantilla."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from config import IMPORTANCIA_CSV, METRICAS_CSV, PREDICCIONES_CSV


PREDICCIONES_REQUERIDAS = {
    "id", "grupo", "periodo", "valor_real", "probabilidad"
}
METRICAS_REQUERIDAS = {
    "modelo", "exactitud", "precision", "recall", "f1", "roc_auc"
}
IMPORTANCIA_REQUERIDAS = {"variable", "importancia"}


@dataclass
class DatosDashboard:
    predicciones: pd.DataFrame
    metricas: pd.DataFrame
    importancia: pd.DataFrame


def _columnas_faltantes(df: pd.DataFrame, requeridas: set[str]) -> list[str]:
    return sorted(requeridas.difference(df.columns))


def cargar_y_validar() -> DatosDashboard:
    """Lee los tres CSV y detiene la ejecucion si el contrato no se cumple."""
    faltan_archivos = [
        str(ruta) for ruta in (PREDICCIONES_CSV, METRICAS_CSV, IMPORTANCIA_CSV)
        if not ruta.exists()
    ]
    if faltan_archivos:
        raise FileNotFoundError("No se encontraron: " + ", ".join(faltan_archivos))

    pred = pd.read_csv(PREDICCIONES_CSV)
    metricas = pd.read_csv(METRICAS_CSV)
    importancia = pd.read_csv(IMPORTANCIA_CSV)

    problemas = []
    for nombre, df, requeridas in [
        ("predicciones.csv", pred, PREDICCIONES_REQUERIDAS),
        ("metricas_modelos.csv", metricas, METRICAS_REQUERIDAS),
        ("importancia_variables.csv", importancia, IMPORTANCIA_REQUERIDAS),
    ]:
        faltantes = _columnas_faltantes(df, requeridas)
        if faltantes:
            problemas.append(f"{nombre}: faltan columnas {faltantes}")
        if df.empty:
            problemas.append(f"{nombre}: no contiene filas")

    if problemas:
        raise ValueError("\n".join(problemas))

    pred["valor_real"] = pd.to_numeric(pred["valor_real"], errors="coerce")
    pred["probabilidad"] = pd.to_numeric(pred["probabilidad"], errors="coerce")
    columnas_metricas = ["exactitud", "precision", "recall", "f1", "roc_auc"]
    metricas[columnas_metricas] = metricas[columnas_metricas].apply(
        pd.to_numeric, errors="coerce"
    )
    importancia["importancia"] = pd.to_numeric(
        importancia["importancia"], errors="coerce"
    )

    if pred[["id", "grupo", "periodo", "valor_real", "probabilidad"]].isna().any().any():
        raise ValueError("predicciones.csv contiene valores vacios o no numericos en columnas requeridas")
    if not set(pred["valor_real"].unique()).issubset({0, 1}):
        raise ValueError("valor_real solo puede contener 0 y 1")
    if not pred["probabilidad"].between(0, 1).all():
        raise ValueError("probabilidad debe estar entre 0 y 1")
    if metricas[columnas_metricas].isna().any().any():
        raise ValueError("metricas_modelos.csv contiene metricas vacias o no numericas")
    if not metricas[columnas_metricas].apply(lambda col: col.between(0, 1).all()).all():
        raise ValueError("Todas las metricas deben estar entre 0 y 1")
    if importancia["importancia"].isna().any():
        raise ValueError("importancia_variables.csv contiene importancias no numericas")

    pred["grupo"] = pred["grupo"].astype(str)
    pred["periodo"] = pred["periodo"].astype(str)
    return DatosDashboard(pred, metricas, importancia)

