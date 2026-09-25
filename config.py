"""Configuracion que el estudiante puede personalizar sin tocar app.py."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

PREDICCIONES_CSV = DATA_DIR / "predicciones.csv"
METRICAS_CSV = DATA_DIR / "metricas_modelos.csv"
IMPORTANCIA_CSV = DATA_DIR / "importancia_variables.csv"
 
TITULO = "Desempeño en Saber 11 (ICFES)"
SUBTITULO = "Estudiantes que superan el puntaje global promedio, según el modelo de regresión logística"
 
# Paleta
COLOR_PRIMARIO = "#1B3A4B"   # azul oscuro (encabezado, header de tabla)
COLOR_SECUNDARIO = "#2E86AB"  # azul medio (clase 0 / matriz de confusion)
COLOR_ACENTO = "#F4B942"      # amarillo (barras destacadas)
COLOR_ALERTA = "#D6604D"      # rojo (clase 1 / riesgo)
 
# Nombres de negocio usados en los filtros y tarjetas KPI
NOMBRE_GRUPO = "Estrato de vivienda"
NOMBRE_PERIODO = "Periodo histórico"
NOMBRE_REGISTRO = "Estudiantes"
NOMBRE_CLASE_POSITIVA = "Supera el promedio"
NOMBRE_INTERNET = "Internet"
NOMBRE_COMPUTADOR = "Computador"
NOMBRE_TIPO_COLEGIO = "Tipo de colegio"
