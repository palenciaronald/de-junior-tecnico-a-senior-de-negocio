# Product Steering

## Propósito

Producto de datos que genera una recomendación diaria de liquidez para una billetera digital ficticia. Determina cuánto dinero reservar para atender retiros esperados del día siguiente, minimizando el costo total (dinero ocioso + faltante) sin deteriorar el nivel de servicio.

## Usuario funcional

Analista o responsable de liquidez y tesorería.

## Decisión que soporta

Al cierre del día D, decidir cuánto dinero reservar para atender los retiros del día D+1.

## Entregable

Recomendación diaria que incluye:
- Pronóstico central de retiros.
- Intervalo de predicción (cuantiles).
- Monto recomendado para reservar.
- Buffer de seguridad.
- Nivel de servicio aplicado.
- Riesgo estimado de insuficiencia.
- Costos esperados (ociosidad y faltante).
- Metadata del modelo (versión, fecha de actualización).

## KPIs

### Negocio
- Reducción del costo total de liquidez vs. regla tradicional.
- Reducción promedio de dinero ocioso.
- Porcentaje de días con faltante.
- Nivel de servicio alcanzado.

### Técnicos
- MAE, RMSE, WAPE.
- Pinball loss (cuantiles).
- Cobertura del intervalo de predicción.
- Error en días de alta demanda.

## Restricciones

- Datos 100% sintéticos. No usar datos reales ni confidenciales.
- Funciona offline después de instalar dependencias.
- No requiere API keys, servicios cloud ni GPU.
- El modelo es un componente; la decisión es el producto.
- El KPI de negocio es impactado por el producto completo, no solo por el modelo.

## Principios de producto

1. La predicción no es la decisión.
2. El producto debe ser consumible por una persona no técnica.
3. Los costos y nivel de servicio deben ser configurables.
4. Comparar siempre contra una política tradicional de referencia.
5. Transparencia: mostrar supuestos, versión y fecha del modelo.
6. El agente construye, pero el humano define y aprueba.
