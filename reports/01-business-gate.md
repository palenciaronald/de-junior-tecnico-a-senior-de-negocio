# 01 — Business Gate

## Estado

**GO** ✅

## Resumen

El product brief define correctamente el problema de negocio, la decisión, el usuario funcional, el KPI principal y el entregable. El proyecto está listo para avanzar a la fase de entendimiento de datos.

## Evidencia revisada

- `docs/product-brief.md`
- `.kiro/steering/product.md`
- `.kiro/steering/data-science-standards.md`

## Hallazgos

| Criterio | Validación | Estado |
|----------|-----------|--------|
| Problema definido | "Determinar cuánto dinero reservar para D+1, reduciendo ocioso sin deteriorar servicio" | ✅ |
| Decisión explícita | Al cierre del día D, decidir cuánto reservar para D+1 | ✅ |
| Usuario funcional | Analista de liquidez y tesorería | ✅ |
| Owner | Área ficticia de Analítica de Liquidez | ✅ |
| Forma de consumo | Streamlit + CSV exportable | ✅ |
| Entregable | Recomendación diaria con 12 componentes específicos | ✅ |
| KPI principal medible | Costo total = c_ociosidad × max(q-y,0) + c_faltante × max(y-q,0) | ✅ |
| Nivel de servicio | 95% default, configurable 80–99% | ✅ |
| Costos definidos | Ociosidad: 0.01%, Faltante: 0.05% (ratio 1:5) | ✅ |
| Política de referencia | max(7 días) × 1.10 | ✅ |
| Predicción ≠ decisión | Explícitamente separados en el documento | ✅ |
| Guardrails | Nivel de servicio mínimo definido | ✅ |

## Supuestos

1. Los costos (0.01% ociosidad, 0.05% faltante) son configurables y no fijos — el tablero permitirá modificarlos.
2. El ratio 1:5 es un punto de partida razonable para un producto financiero donde el faltante es más costoso que el exceso.
3. La política tradicional (max 7 días + 10%) es representativa de una regla manual conservadora.
4. Los datos son 100% educativos — no representan una empresa real.

## Artefactos

- `reports/01-business-gate.md` (este archivo)

## Riesgos pendientes

- Los costos son parámetros arbitrarios para el ejercicio. En un caso real, requerirían validación con tesorería.
- No se ha validado aún si los datos disponibles permiten estimar estos costos empíricamente.

## Siguiente paso

Ejecutar agente **data-understanding** para perfilar el dataset y evaluar si es apto para modelado.
