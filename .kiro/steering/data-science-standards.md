# Data Science Standards Steering

## Separación temporal

- Siempre usar separación cronológica (train antes que test en el tiempo).
- Nunca usar random split para series de tiempo.
- El punto de corte debe simular el momento de decisión real.
- El conjunto de test debe representar el periodo de evaluación futura.

## Prevención de leakage

- Solo usar variables disponibles al momento de tomar la decisión (cierre del día D para predecir D+1).
- Los lags deben calcularse con información estrictamente pasada.
- No usar variables que contengan información del futuro (retiros del día que se quiere predecir).
- Validar explícitamente la ausencia de leakage con tests automatizados.
- Documentar qué información está disponible en cada punto temporal.

## Baselines obligatorios

Antes de entrenar cualquier modelo, implementar y evaluar como mínimo:

1. Valor del día anterior (naive lag-1).
2. Valor del mismo día de la semana anterior (lag-7).
3. Promedio móvil (ventana de 7 o 14 días).

Ningún modelo se considera útil si no supera todos los baselines en las métricas relevantes.

## Reproducibilidad

- Semilla fija: 42.
- Todos los comandos deben producir los mismos resultados con la misma semilla.
- Datos generados con script determinista.
- Modelos serializados con metadata (fecha, versión, parámetros, métricas).
- El pipeline completo debe ser re-ejecutable desde cero.

## Métricas técnicas

| Métrica | Propósito |
|---------|-----------|
| MAE | Error absoluto promedio — interpretable en unidades de negocio |
| RMSE | Penaliza errores grandes |
| WAPE | Error porcentual ponderado — comparable entre escalas |
| Pinball loss | Evalúa calidad de cuantiles |
| Cobertura del intervalo | Porcentaje de observaciones dentro del intervalo predicho |
| Error en días de alta demanda | Rendimiento en días críticos (quincena, fin de mes) |

## Métricas de negocio

| Métrica | Propósito |
|---------|-----------|
| Costo total de liquidez | C(q,y) = c_ociosidad * max(q-y, 0) + c_faltante * max(y-q, 0) |
| Reducción de dinero ocioso | Comparado contra política tradicional |
| Porcentaje de días con faltante | Frecuencia de insuficiencia |
| Nivel de servicio alcanzado | % días donde q >= y |
| Monto promedio del faltante | Severidad cuando hay insuficiencia |

## Diferencia entre predicción y decisión

- La **predicción** es el pronóstico de retiros (cuánto se espera que retiren).
- La **decisión** es cuánto reservar (incorpora costos, nivel de servicio, buffer).
- La recomendación ≠ pronóstico promedio.
- La selección del modelo debe considerar tanto métricas técnicas como impacto en el costo de negocio.
- Un modelo con peor MAE puede generar mejor decisión si su distribución de errores es más favorable.

## Documentación de supuestos

Todo modelo y decisión debe documentar explícitamente:

- Periodo de entrenamiento.
- Variables utilizadas y su disponibilidad temporal.
- Hiperparámetros seleccionados.
- Supuestos sobre estacionariedad o distribución.
- Limitaciones conocidas.
- Condiciones bajo las cuales el modelo podría fallar.
- Comparación contra baselines y política tradicional.

## Validación temporal (backtesting)

- Simular la ejecución del modelo día a día en el periodo de test.
- Calcular métricas acumuladas y por ventana.
- Identificar periodos de bajo rendimiento.
- Evaluar estabilidad de la recomendación.

## Principio rector

El KPI de negocio es impactado por el producto completo (predicción + decisión + política + configuración), no exclusivamente por el modelo.
