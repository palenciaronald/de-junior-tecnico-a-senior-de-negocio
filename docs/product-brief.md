# Product Brief — Recomendación Diaria de Liquidez

## Problema

Una billetera digital atiende diariamente cientos de miles de retiros a través de su red de cajeros. Si reserva menos dinero del necesario, puede quedarse corta de liquidez, afectar el nivel de servicio y generar costos operativos. Si reserva demasiado, mantiene recursos ociosos y pierde costo de oportunidad.

La solicitud inicial fue: *"Necesitamos predecir los retiros de mañana"*.

Pero predecir no es suficiente. El problema completo es:

> **Determinar diariamente cuánto dinero debe reservar la billetera para atender los retiros esperados del día siguiente, reduciendo el dinero ocioso sin deteriorar el nivel de servicio.**

## Decisión

Cada día, al cierre del día D, el responsable de liquidez debe decidir:

**¿Cuánto dinero reservar para atender los retiros del día D+1?**

## Usuario funcional

Analista o responsable de liquidez y tesorería.

## Owner

Área ficticia de Analítica de Liquidez.

## Producto de datos

Una recomendación diaria que incluye:

- Fecha para la cual aplica (D+1).
- Pronóstico central de retiros.
- Intervalo o cuantiles de predicción (cuantil 95).
- Monto recomendado para reservar.
- Buffer de seguridad.
- Nivel de servicio seleccionado.
- Riesgo estimado de insuficiencia.
- Costo esperado del dinero ocioso.
- Costo esperado del faltante.
- Fecha de actualización del modelo.
- Versión del modelo.
- Posibilidad de exportar la recomendación a CSV.

## Frecuencia

Ejecución diaria, al cierre del día D.

## Forma de consumo

- Minitablero en Streamlit.
- Archivo CSV exportable.
- Diseño preparado para consumo posterior vía API o batch.

## KPI principal

Reducción del costo total de liquidez frente a una regla tradicional, manteniendo un nivel de servicio definido.

**Función de costo:**

```
C(q, y) = costo_ociosidad × max(q − y, 0) + costo_faltante × max(y − q, 0)
```

Donde:
- `q` = dinero reservado (decisión).
- `y` = retiros reales (observación).
- `costo_ociosidad` = 0.0001 (0.01% del exceso por día).
- `costo_faltante` = 0.0005 (0.05% del faltante por día).

El ratio 1:5 refleja que quedarse corto es más costoso que tener exceso.

## KPIs de resultado

| KPI | Descripción |
|-----|-------------|
| Reducción de dinero ocioso | Promedio diario de dinero reservado de más vs. política tradicional |
| Reducción del costo total | Costo modelo vs. costo política tradicional |
| Porcentaje de días con faltante | Frecuencia de insuficiencia |
| Monto promedio del faltante | Severidad cuando hay insuficiencia |
| Nivel de servicio alcanzado | % días donde la reserva cubre los retiros |

## Métricas técnicas

| Métrica | Propósito |
|---------|-----------|
| MAE | Error absoluto promedio en COP |
| RMSE | Penaliza errores grandes |
| WAPE | Error porcentual ponderado |
| Pinball loss | Calidad del cuantil 95 |
| Cobertura del intervalo | % observaciones dentro del cuantil |
| Error en días de alta demanda | Rendimiento en quincena/fin de mes |

## Nivel de servicio

- Default: **95%** (el 95% de los días la reserva debe cubrir los retiros reales).
- Configurable desde el tablero (rango 80%–99%).

## Política tradicional de referencia

```
reserva = max(retiros últimos 7 días) × 1.10
```

Representa una regla conservadora manual sin modelo.

## Datos disponibles

Dataset de retiros diarios por cajeros:
- Periodo: julio 2024 – junio 2026 (2 años).
- Granularidad: diaria.
- Variables: fecha, total transacciones, valor total (COP).
- 100% sintético / educativo. No contiene información personal ni confidencial.

## Principio rector

El KPI de negocio es impactado por el **producto completo** (predicción + decisión + política + configuración), **no exclusivamente por el modelo**.

La predicción no es la decisión.
