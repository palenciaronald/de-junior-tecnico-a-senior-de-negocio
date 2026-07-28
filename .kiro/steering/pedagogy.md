# Pedagogy Steering

## Público objetivo

Estudiantes de pregrado de ingeniería, quinto semestre en adelante.

### Conocimientos previos asumidos
- Python básico.
- Estadística descriptiva e inferencial.
- Manipulación de datos (pandas).
- Conceptos básicos de machine learning (train/test, métricas).

### Conocimientos NO asumidos
- Productos de datos.
- MLOps.
- Arquitectura de sistemas.
- Agentes de IA.
- Kiro.

## Duración

- Primera hora: pensamiento de negocio, producto de datos, ML, CRISP-DM, agentes y Kiro.
- Segunda hora: laboratorio práctico guiado individual (60 minutos exactos).

## Formato

Build-along individual (no competencia, no hackathon, no equipos).

El formato pedagógico es:

> Pensar con el instructor → ejecutar con Kiro → inspeccionar el resultado → decidir si se puede avanzar.

## Principios pedagógicos

1. **Explicar antes de ejecutar.** Cada paso del laboratorio comienza con el instructor contextualizando qué se va a hacer y por qué.
2. **No ocultar decisiones detrás del agente.** Cuando el agente produce código, el instructor explica qué decidió el humano antes de pedirlo.
3. **Cada paso tiene un gate.** El estudiante debe poder responder una pregunta de negocio antes de avanzar.
4. **Mantener cada paso dentro del tiempo asignado.** Si un paso se extiende, usar checkpoints de recuperación.
5. **Todos siguen el mismo ejemplo.** No variantes, no personalización durante el taller.
6. **El error es parte del flujo.** Si algo falla, se muestra cómo diagnosticarlo y recuperarse.
7. **El laboratorio no depende de trabajo colaborativo.** Cada participante debe poder completarlo sin depender de otros.
8. **Ejecución secuencial de agentes.** No lanzar múltiples agentes simultáneamente. Observar y discutir cada fase.

## Cronograma del laboratorio (60 minutos)

| Min | Fase | Actividad principal |
|-----|------|-------------------|
| 0–10 | Gate de negocio | Revisar product-brief, confirmar problema y decisión |
| 10–20 | Entendimiento de datos | Ejecutar agente, revisar calidad, GO/NO-GO |
| 20–31 | Preparación y baseline | Features, separación temporal, baselines |
| 31–41 | Modelado y evaluación | Entrenar, comparar, métricas técnicas y de negocio |
| 41–51 | Capa de decisión | Recomendación, costos asimétricos, CSV |
| 51–57 | Producto | Streamlit, simulador, interpretación funcional |
| 57–59 | Operación | Arquitectura, monitoreo, owner |
| 59–60 | Cierre | Pregunta final |

## Frase de cierre

> "El agente construyó mucho, pero ¿quién decidió qué debía construir?"

## Mecanismos de recuperación

- Cada fase tiene un checkpoint en rama Git.
- Si un estudiante se atrasa, puede hacer checkout del checkpoint correspondiente.
- El instructor debe ensayar el flujo completo antes del taller.
- Los prompts del estudiante son cortos, deterministas y acotados.

## Materiales entregados al participante

- Steering preparado.
- Skills preparadas.
- Agentes preparados.
- Specs preparados.
- Datos generados.
- Instrucciones secuenciales.
- Tests para validar cada paso.
