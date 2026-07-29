# Plantilla de Diapositivas — Primera Hora

> Solo mensajes y estructura. Las imágenes se colocan manualmente.

---

## BLOQUE 1: ¿Qué es ciencia de datos? (min 0–8)

### Diapo 1 — Título
```
De junior técnico a senior de negocio
Ciencia de datos con IA agéntica
```

### Diapo 2 — Ciencia de datos en una organización
```
Ciencia de datos no es entrenar modelos.

Es usar datos para mejorar decisiones.
```

### Diapo 3 — Junior técnico vs Senior de negocio
```
El junior pregunta: ¿qué modelo uso?
El senior pregunta: ¿qué decisión cambiará y cuánto cuesta equivocarse?
```

### Diapo 4 — Producto de datos vs modelo de datos
```
Un modelo es un componente.
Un producto de datos es lo que consume el usuario funcional para decidir.

El modelo vive dentro del producto. No es el producto.
```

### Diapo 5 — KPI de negocio vs métrica técnica
```
Al junior le importa: MAPE, RMSE, AUC
Al senior le importa: ¿cuánto dinero ahorramos? ¿se deterioró el servicio?

La métrica técnica mide el ajuste del modelo.
El KPI mide el impacto en el negocio.
```

---

## BLOQUE 2: Tecnologías (min 8–20)

### Diapo 6 — ML, GenAI y agentes no son lo mismo
```
Machine Learning → Aprende patrones de datos históricos.
                   Genera el pronóstico de retiros.

IA Generativa   → Interpreta instrucciones, genera texto y código.
                   No reemplaza al modelo predictivo.

Agentes de IA   → Combinan un modelo generativo con:
                   objetivo + contexto + herramientas + supervisión humana.
                   Ejecutan tareas acotadas.
```

### Diapo 7 — Qué función cumple cada tecnología en el taller
```
El modelo de ML     → pronostica los retiros de mañana.
El agente de IA     → ayuda a construir el producto (documenta, programa, evalúa).
El humano           → define el problema, aprueba cada fase, decide.

El agente construye. El humano decide qué construir.
```

### Diapo 8 — CRISP-DM como mapa del trabajo
```
[IMAGEN: diagrama CRISP-DM clásico]

1. Entendimiento del negocio
2. Entendimiento de datos
3. Preparación de datos
4. Modelado
5. Evaluación
6. Despliegue

Esto no lo inventamos hoy. Es el estándar desde 1996.
```

### Diapo 9 — ¿Cómo acelerar CRISP-DM?
```
¿Y si un equipo de agentes especializados
ejecuta cada fase bajo tu supervisión?

Tú piensas. Ellos construyen. Tú apruebas.
```

---

## BLOQUE 3: Agentes (min 20–35)

### Diapo 10 — Qué es un agente
```
Un agente es un sistema que combina:

• Un objetivo acotado
• Contexto (documentos, datos, reglas)
• Un modelo de lenguaje
• Herramientas (leer, escribir, ejecutar)
• Memoria (artefactos generados)
• Supervisión humana (GO / NO-GO)

No es magia. Es automatización con guardrails.
```

### Diapo 11 — Equipo de agentes en Kiro
```
Steering  → Contexto persistente (reglas, producto, tech)
Specs     → Requisitos, diseño, tareas
Agentes   → Responsabilidades y permisos por fase
Skills    → Procedimientos reutilizables

Todo en Markdown y JSON. Todo versionable. Todo auditable.
```

### Diapo 12 — Nuestro equipo de agentes
```
1. business-understanding    → Valida el problema
2. data-understanding        → Explora los datos
3. data-preparation          → Prepara features
4. modeling-tournament       → Compara modelos
5. evaluation-business       → Traduce a negocio
6. productization-deployment → Construye el producto

Secuencial. Uno a la vez. Tú apruebas cada puerta.
```

---

## BLOQUE 4: El caso de hoy (min 35–50)

### Diapo 13 — Transición
```
Ya entendemos las herramientas.
Ahora tomemos el rol del senior.

Vamos a resolver un problema real con este enfoque.
```

### Diapo 14 — Solicitud inicial
```
"Necesitamos predecir cuánto retirarán mañana."

¿Eso es suficiente para empezar a programar?
```

### Diapo 15 — Del pedido al problema (4 preguntas)
```
1. ¿La necesidad real es predecir o decidir cuánto reservar?
2. ¿Cuándo se toma esa decisión? (cierre del día D)
3. ¿Qué pasa si falta dinero? (costo operativo, servicio afectado)
4. ¿Qué pasa si sobra dinero? (costo de oportunidad, recursos ociosos)

→ La predicción es un insumo. La decisión es el producto.
```

### Diapo 16 — Éxito del negocio (3 tarjetas)
```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  DINERO OCIOSO  │  │     FALTANTE    │  │ NIVEL SERVICIO  │
│                 │  │                 │  │                 │
│  Exceso que no  │  │  Insuficiencia  │  │  % de días que  │
│  genera valor   │  │  que afecta la  │  │  cubrimos los   │
│                 │  │  operación      │  │  retiros        │
│  Costo: 0.01%  │  │  Costo: 0.05%  │  │  Target: 95%    │
└─────────────────┘  └─────────────────┘  └─────────────────┘

El KPI: reducir costo total sin deteriorar servicio.
```

### Diapo 17 — El producto de datos
```
Una recomendación diaria que incluye:

• Pronóstico central de retiros
• Intervalo de seguridad (cuantil 95)
• Monto recomendado para reservar
• Buffer de seguridad
• Nivel de servicio seleccionado
• Riesgo estimado de insuficiencia
• Costo esperado

Consumidor: analista de liquidez
Owner: área de Analítica de Liquidez
```

### Diapo 18 — Esto es un product brief
```
Todo lo anterior vive en un archivo:

    docs/product-brief.md

Aquí es donde un senior se sienta a pensar horas.
Sin esto, el modelo más sofisticado no sirve.

Esto es lo primero. El código es lo último.
```

---

## BLOQUE 5: Del brief al repo (min 50–57)

### Diapo 19 — El repositorio preparado
```
Ya tenemos preparado:

✅ Steering (reglas y contexto para los agentes)
✅ Agentes (6 especialistas + 1 orquestador)
✅ Specs (requisitos técnicos del producto)
✅ Datos (2 años de retiros diarios)
✅ Product brief (la definición de negocio)
✅ Templates de notebooks (estructura para cada fase)

¿Qué NO tenemos todavía?
❌ Código del modelo
❌ Features
❌ Dashboard
❌ Recomendación
```

### Diapo 20 — Noten algo importante
```
Llevamos 50 minutos.

No hemos escrito una sola línea de código.

Y ya tenemos:
• Problema definido
• Decisión explícita
• KPI medible
• Usuario identificado
• Producto especificado
• Equipo de agentes listo

Eso es pensar como senior.
```

---

## BLOQUE 6: Transición al taller (min 57–60)

### Diapo 21 — Ahora sí
```
Ya tomamos las decisiones senior.
Ahora vamos a acelerar la construcción con agentes.

Vamos a ejecutar todo a punta de prompts.
Hasta llegar a un dashboard funcional.

El agente construye. Ustedes supervisan.
```

### Diapo 22 — Setup
```
1. Abrir terminal
2. cd de-junior-tecnico-a-senior-de-negocio
3. source .venv/bin/activate
4. kiro chat

¿Todos listos? Empezamos.
```

---

## BLOQUE 7: Ejecución del taller (min 60–118)

> Aquí el instructor ejecuta en vivo.
> Los participantes copian los prompts de la guía.
> No hay diapositivas — es live coding con agentes.

---

## BLOQUE 8: Cierre (min 118–120)

### Diapo 23 — Cierre
```
En 60 minutos, con agentes de IA, construimos:

• Un análisis exploratorio completo
• Un torneo de modelos
• Una evaluación de negocio
• Un producto con dashboard y simulador

Pero la pregunta es...
```

### Diapo 24 — Pregunta final
```
"El agente construyó mucho,
 pero ¿quién decidió qué debía construir?"
```

### Diapo 25 — Contacto
```
[Tu nombre]
[Tu correo]
[Link al repo]

github.com/palenciaronald/de-junior-tecnico-a-senior-de-negocio
```
