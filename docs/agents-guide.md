# Guía de Agentes — Taller de Liquidez

## Resumen del sistema

Este repositorio utiliza 8 agentes especializados que acompañan las fases del producto de datos. Se ejecutan **secuencialmente** durante el laboratorio guiado de 60 minutos, coordinados por un orquestador.

---

## Tabla de agentes

| Agente | Fase | Responsabilidad | Invocación | Inputs principales | Outputs | Tools | Criterio GO | Siguiente | Tiempo |
|--------|------|----------------|------------|-------------------|---------|-------|-------------|-----------|--------|
| workshop-orchestrator | — | Coordinar flujo y gates | `/agent workshop-orchestrator` | Todos los reports | reports/workshop-execution-log.md | read, write, grep, glob | Todas las fases completadas | — | Continuo |
| business-understanding | 1 | Validar problem statement | `/agent business-understanding` | docs/product-brief.md, steering | reports/01-business-gate.md | read, write, grep, glob | KPI medible, decisión explícita | data-understanding | 7 min |
| data-understanding | 2 | Perfilar datos y calidad | `/agent data-understanding` | data/raw/, steering | reports/02-data-understanding.md | read, write, shell, grep, glob | Datos aptos para modelado | data-preparation | 10 min |
| data-preparation | 3 | Features, split, baselines | `/agent data-preparation` | data/raw/, report anterior | data/processed/, reports/03 | read, write, shell, grep, glob, code | Features sin leakage, baselines evaluados | modeling | 12 min |
| modeling | 4 | Entrenar y serializar modelo | `/agent modeling` | data/processed/, baselines | artifacts/model.joblib, reports/04 | read, write, shell, grep, glob, code | Modelo supera baselines | evaluation | 10 min |
| evaluation | 5 | Métricas técnicas y de negocio | `/agent evaluation` | artifacts/, predictions | reports/05-model-evaluation.md | read, write, shell, grep, glob, code | Modelo aporta valor vs política tradicional | decision-product | 10 min |
| decision-product | 6 | Recomendación, dashboard, CSV | `/agent decision-product` | artifacts/, reports/05 | outputs/CSV, app.py, src/decision/ | read, write, shell, grep, glob, code | Usuario puede decidir cuánto reservar | deployment-monitoring | 6 min |
| deployment-monitoring | 7 | Pipeline, monitoreo, docs | `/agent deployment-monitoring` | Todo el proyecto | docs/model-card.md, monitoring-plan.md | read, write, shell, grep, glob, code | Pipeline funciona, monitoreo definido | (cierre) | 4 min |

---

## Conceptos clave

### Steering vs Skills vs Specs vs Agents

| Componente | Ubicación | Contenido | Persistencia |
|------------|-----------|-----------|--------------|
| **Steering** | `.kiro/steering/` | Contexto persistente del proyecto (producto, tech, pedagogía) | Siempre cargado |
| **Skills** | `.kiro/skills/` | Procedimientos reutilizables paso a paso | Cargado bajo demanda |
| **Specs** | `.kiro/specs/` | Requisitos, diseño y tareas del producto | Referencia de implementación |
| **Agents** | `.kiro/agents/` | Responsabilidades, herramientas y criterios de terminación | Un agente activo a la vez |

### Relación entre ellos

- El **steering** da contexto a todos los agentes automáticamente.
- Los **agents** definen QUÉ hace cada rol y CUÁNDO se detiene.
- Las **skills** definen CÓMO hacer una tarea específica (procedimiento).
- Los **specs** definen QUÉ se debe construir (contrato del producto).

---

## Cómo usar los agentes

### Listar agentes disponibles

```bash
kiro agent list
```

O dentro de una sesión de chat:
```
/agent
```

### Invocar un agente manualmente

```bash
# Iniciar sesión con un agente específico
kiro chat --agent business-understanding
```

O dentro de una sesión de chat:
```
/agent business-understanding
```

### Ejecutar el orquestador (flujo completo del taller)

```bash
kiro chat --agent workshop-orchestrator
```

Luego decir:
```
Comienza el laboratorio desde la fase 1.
```

### Continuar desde un checkpoint

```
/agent workshop-orchestrator
Continúa desde la fase 4 (modeling). Las fases 1-3 ya están completas.
```

---

## Cómo recuperar el flujo después de un NO-GO

1. El orquestador se detiene y muestra el problema.
2. El humano decide:
   - **Corregir**: ejecutar el agente de nuevo después de ajustar el input.
   - **Continuar de todas formas**: indicar explícitamente al orquestador que continúe (solo si es pedagógicamente justificado).
   - **Usar checkpoint**: `git checkout checkpoint-XX-name` y retomar.
3. El orquestador registra la decisión en el log.

---

## Permisos por agente

### Agentes revisores (mínimo privilegio)

| Agente | tools | allowedTools (auto-aprobados) |
|--------|-------|-------------------------------|
| workshop-orchestrator | read, write, grep, glob | read, grep, glob |
| business-understanding | read, write, grep, glob | read, grep, glob |
| data-understanding | read, write, shell, grep, glob | read, grep, glob |
| evaluation | read, write, shell, grep, glob, code | read, grep, glob, code |
| deployment-monitoring | read, write, shell, grep, glob, code | read, grep, glob |

### Agentes implementadores

| Agente | tools | allowedTools (auto-aprobados) |
|--------|-------|-------------------------------|
| data-preparation | read, write, shell, grep, glob, code | read, grep, glob, code |
| modeling | read, write, shell, grep, glob, code | read, grep, glob, code |
| decision-product | read, write, shell, grep, glob, code | read, grep, glob, code |

**Principio**: lectura y búsqueda auto-aprobadas. Escritura, terminal e instalaciones requieren aprobación humana.

---

## Inspeccionar permisos de un agente

```bash
# Ver la configuración completa
cat .kiro/agents/business-understanding.json | python3 -m json.tool
```

O:
```bash
kiro agent validate --path .kiro/agents/business-understanding.json
```

---

## Evitar ejecución paralela

- El orquestador invoca UN agente a la vez.
- Espera resultado + aprobación humana antes del siguiente.
- NO usar `/spawn` durante el taller.
- NO ejecutar múltiples sesiones de Kiro simultáneamente sobre el mismo proyecto.

---

## Comprobar qué contexto recibió un agente

Dentro de una sesión con el agente activo:
```
/context
```

Esto muestra los archivos cargados como recursos y el espacio utilizado.

---

## Flujo visual

```
┌─────────────────────────────────────────────────────────┐
│                 workshop-orchestrator                     │
│                                                         │
│  ┌─────────────┐    Aprobación    ┌─────────────────┐  │
│  │  business-  │ ──── GO? ────→   │     data-       │  │
│  │understanding│                  │ understanding   │  │
│  └─────────────┘                  └────────┬────────┘  │
│                                            │ GO?       │
│                                            ▼           │
│  ┌─────────────┐    Aprobación    ┌─────────────────┐  │
│  │  modeling   │ ←── GO? ─────    │     data-       │  │
│  │             │                  │  preparation    │  │
│  └──────┬──────┘                  └─────────────────┘  │
│         │ GO?                                          │
│         ▼                                              │
│  ┌─────────────┐    Aprobación    ┌─────────────────┐  │
│  │ evaluation  │ ──── GO? ────→   │   decision-     │  │
│  │             │                  │    product      │  │
│  └─────────────┘                  └────────┬────────┘  │
│                                            │ GO?       │
│                                            ▼           │
│                                   ┌─────────────────┐  │
│                                   │  deployment-    │  │
│                                   │  monitoring     │  │
│                                   └────────┬────────┘  │
│                                            │           │
│                                            ▼           │
│         "El agente construyó mucho,                    │
│          pero ¿quién decidió qué debía construir?"     │
└─────────────────────────────────────────────────────────┘
```

---

## Contrato de respuesta (todos los agentes)

Cada agente termina con esta estructura:

```markdown
## Estado
GO | REVISAR | NO-GO

## Resumen
...

## Evidencia revisada
...

## Hallazgos
...

## Supuestos
...

## Artefactos
...

## Riesgos pendientes
...

## Siguiente paso
...
```

---

## Recurso faltante

| Recurso | Estado | Cuándo se crea |
|---------|--------|----------------|
| docs/product-brief.md | ❌ Pendiente | Antes de ejecutar el primer agente (Fase 3 de implementación) |

Todos los demás recursos referenciados por los agentes ya existen en el repositorio.
