# Contrato de datos

## 1. data/predicciones.csv

Una fila por observacion evaluada.

| Columna | Tipo | Significado |
|---|---|---|
| id | texto | Identificador unico sin datos sensibles. |
| grupo | texto | Categoria para filtrar y comparar. Ejemplo: programa, sede o producto. |
| periodo | texto | Periodo o cohorte. |
| valor_real | entero | Resultado conocido: 0 o 1. |
| probabilidad | decimal | Probabilidad estimada de la clase positiva, entre 0 y 1. |

Se permiten columnas adicionales. La tabla del dashboard tambien las mostrara.

## 2. data/metricas_modelos.csv

Una fila por modelo o iteracion.

Columnas obligatorias: `modelo`, `exactitud`, `precision`, `recall`, `f1`, `roc_auc`.
Todas las metricas deben escribirse como decimales entre 0 y 1.

## 3. data/importancia_variables.csv

Una fila por variable. Columnas obligatorias: `variable`, `importancia`.
La importancia puede proceder de coeficientes absolutos, importancia por permutacion, SHAP agregado u otra tecnica explicada en el informe del estudiante.

## Ejemplo de exportacion desde un notebook

```python
predicciones = X_prueba.copy()
predicciones["id"] = ids_prueba
predicciones["grupo"] = grupo_prueba
predicciones["periodo"] = periodo_prueba
predicciones["valor_real"] = y_prueba
predicciones["probabilidad"] = modelo.predict_proba(X_prueba)[:, 1]
predicciones.to_csv("data/predicciones.csv", index=False)
```

