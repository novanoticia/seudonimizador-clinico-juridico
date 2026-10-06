# i18n-en — Catálogo (inglés)

<!-- BORRADOR DE IA, SIN REVISIÓN HUMANA. Las entradas con `seguridad: sí` deben revisarlas una persona antes de cambiar el estado a `revisado` (y hay que actualizar docs/estado-traducciones.md). -->
<!-- Ortografía británica, coherente con el inglés oficial del RGPD (pseudonymisation). -->

- código: en
- estado: borrador-ia-sin-revision-humana
- redactado-por: IA
- revisado-por: nadie
- fecha-revision: —

## Glosario

- seudonimización → pseudonymisation
- seudonimizado → pseudonymised
- identificadores indirectos → indirect identifiers
- riesgo residual → residual risk
- desplazamiento temporal → time shift
- semilla → seed
- token → token
- mapa → map
- generalización → generalisation
- control de fidelidad → fidelity check
- fuga → leak
- regenerar → regenerate

## Frases

### encabezado.apertura
origen: original
fuente: flujo.md
seguridad: no
es: ## APERTURA
en: ## OPENING

### apertura.modo
origen: original
fuente: flujo.md
seguridad: no
es: Modo:
en: Mode:

### lista.modos
origen: original
fuente: flujo.md
seguridad: no
es: [A | B | C]
en: [A | B | C]
invariable: sí

### apertura.semilla
origen: original
fuente: flujo.md
seguridad: no
es: Semilla de desplazamiento temporal:
en: Time shift seed:

### unidad.dias
origen: original
fuente: flujo.md
seguridad: no
es: +N días
en: +N days

### apertura.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación de la semilla:
en: Seed justification:

### apertura.preguntas
origen: original
fuente: flujo.md
seguridad: no
es: Preguntas críticas previas:
en: Critical preliminary questions:

### valor.ninguna
origen: original
fuente: flujo.md
seguridad: no
es: ninguna
en: none

### encabezado.mapa
origen: original
fuente: flujo.md
seguridad: sí
es: ## MAPA — archivar o destruir aparte del texto
en: ## MAP — archive or destroy separately from the text

### mapa.desplazamiento
origen: original
fuente: flujo.md
seguridad: no
es: Desplazamiento temporal aplicado:
en: Time shift applied:

### mapa.rol_token
origen: original
fuente: flujo.md
seguridad: no
es: Mapa rol → token:
en: Role → token map:

### mapa.ejemplo_persona_x
origen: original
fuente: flujo.md
seguridad: no
es: Persona X (rol: paciente / demandado / etc.) → [TOKEN]
en: Person X (role: patient / defendant / etc.) → [TOKEN]

### mapa.ejemplo_persona_y
origen: original
fuente: flujo.md
seguridad: no
es: Persona Y → [TOKEN]
en: Person Y → [TOKEN]

### mapa.generalizaciones_geo
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones geográficas y organizacionales aplicadas:
en: Geographic and organisational generalisations applied:

### mapa.ejemplo_lugar
origen: original
fuente: flujo.md
seguridad: no
es: Lugar/entidad concreto → categoría funcional
en: Specific place/entity → functional category

### mapa.generalizaciones_indirectos
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones de identificadores indirectos:
en: Generalisations of indirect identifiers:

### mapa.ejemplo_atributo
origen: original
fuente: flujo.md
seguridad: no
es: Atributo concreto → atributo generalizado
en: Specific attribute → generalised attribute

### encabezado.texto
origen: original
fuente: flujo.md
seguridad: no
es: ## TEXTO SEUDONIMIZADO
en: ## PSEUDONYMISED TEXT

### encabezado.riesgo
origen: original
fuente: flujo.md
seguridad: sí
es: ## AUDITORÍA DE RIESGO RESIDUAL
en: ## RESIDUAL RISK AUDIT

### riesgo.nivel
origen: original
fuente: flujo.md
seguridad: no
es: Nivel:
en: Level:

### lista.nivel
origen: original
fuente: flujo.md
seguridad: sí
es: [bajo / medio / alto]
en: [low / medium / high]

### riesgo.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación:
en: Justification:

### riesgo.detalles
origen: original
fuente: flujo.md
seguridad: no
es: Detalles que aún podrían permitir reidentificación por singularidad combinada:
en: Details that could still allow re-identification through combined uniqueness:

### riesgo.propuesta
origen: original
fuente: flujo.md
seguridad: no
es: Propuesta de generalización adicional (si procede):
en: Proposed additional generalisation (if applicable):

### encabezado.fidelidad
origen: original
fuente: flujo.md
seguridad: sí
es: ## CONTROL DE FIDELIDAD
en: ## FIDELITY CHECK

### fidelidad.pregunta
origen: original
fuente: flujo.md
seguridad: sí
es: ¿Algún elemento del texto seudonimizado no tiene correspondencia en el original?
en: Is any element of the pseudonymised text without a counterpart in the original?

### lista.si_no
origen: original
fuente: flujo.md
seguridad: sí
es: [sí / no]
en: [yes / no]

### fidelidad.si_listar
origen: original
fuente: flujo.md
seguridad: no
es: Si sí, listar:
en: If yes, list:

### fidelidad.marcadores
origen: original
fuente: flujo.md
seguridad: no
es: Marcadores usados:
en: Markers used:

### encabezado.decisiones
origen: original
fuente: flujo.md
seguridad: no
es: ## DECISIONES POR DEFECTO
en: ## DEFAULT DECISIONS

### mapa.formato_entrada
origen: original
fuente: plantilla-tokens.md
seguridad: no
es: Sujeto / lugar / entidad original → [TOKEN]   (rol en el caso: …)
en: Original subject / place / entity → [TOKEN]   (role in the case: …)

### encabezado.audit
origen: original
fuente: auditoria.md
seguridad: no
es: ## AUDITORÍA — texto ya seudonimizado
en: ## AUDIT — already pseudonymised text

### encabezado.comprobaciones
origen: original
fuente: auditoria.md
seguridad: no
es: ### Comprobaciones
en: ### Checks

### audit.comprobacion_1
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores directos:
en: Direct identifiers:

### audit.comprobacion_2
origen: original
fuente: auditoria.md
seguridad: no
es: Lugares y entidades:
en: Places and entities:

### audit.comprobacion_3
origen: original
fuente: auditoria.md
seguridad: no
es: Fechas:
en: Dates:

### audit.comprobacion_4
origen: original
fuente: auditoria.md
seguridad: no
es: Numéricos identificadores:
en: Identifying numerical data:

### audit.comprobacion_5
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores indirectos:
en: Indirect identifiers:

### audit.comprobacion_6
origen: original
fuente: auditoria.md
seguridad: no
es: Coherencia interna:
en: Internal consistency:

### audit.comprobacion_7
origen: original
fuente: auditoria.md
seguridad: no
es: Fidelidad al original:
en: Fidelity to the original:

### lista.veredicto
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda]
en: [Pass / Fail / Uncertain]

### lista.veredicto_fidelidad
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda / No aplicable]
en: [Pass / Fail / Uncertain / Not applicable]

### encabezado.riesgo_estimado
origen: original
fuente: auditoria.md
seguridad: sí
es: ### Riesgo residual estimado
en: ### Estimated residual risk

### encabezado.propuestas
origen: original
fuente: auditoria.md
seguridad: no
es: ### Propuestas
en: ### Proposals

### propuestas.correcciones
origen: original
fuente: auditoria.md
seguridad: no
es: Correcciones necesarias antes de uso secundario:
en: Corrections needed before secondary use:

### propuestas.generalizacion
origen: original
fuente: auditoria.md
seguridad: no
es: Generalización adicional recomendada (si procede):
en: Recommended additional generalisation (if applicable):

### propuestas.recomendacion
origen: original
fuente: auditoria.md
seguridad: no
es: Recomendación global:
en: Overall recommendation:

### lista.recomendacion
origen: original
fuente: auditoria.md
seguridad: sí
es: [apto para uso secundario interno / requiere corrección antes de uso / pasar a modo C / fragmentar y reseudonimizar partes / no apto sin revisión humana experta]
en: [suitable for internal secondary use / requires correction before use / switch to mode C / split and re-pseudonymise parts / not suitable without expert human review]

### encabezado.regenerar
origen: original
fuente: auditoria.md
seguridad: no
es: ### Si quieres regenerar
en: ### If you want to regenerate

### regenerar.texto
origen: original
fuente: auditoria.md
seguridad: no
es: Indica explícitamente "regenerar" y el texto se reprocesa aplicando las correcciones detectadas, manteniendo los tokens y el desplazamiento temporal del original (si son recuperables) o introduciendo nuevos (si no).
en: Say "regenerate" explicitly and the text will be reprocessed applying the corrections detected, keeping the tokens and the time shift of the original (if recoverable) or introducing new ones (if not).

### encabezado.aviso_traduccion
origen: nuevo
seguridad: sí
es: ## AVISO DE TRADUCCIÓN
en: ## TRANSLATION NOTICE

### aviso.traduccion
origen: nuevo
seguridad: sí
es: Marco de esta respuesta traducido por IA, sin revisión humana. Ante cualquier duda sobre una advertencia de seguridad, consulta la versión en español, que es la de referencia.
en: The framing of this response was translated by AI, without human review. If in doubt about any safety warning, consult the Spanish version, which is the reference.

### puerta.ficticio
origen: nuevo
seguridad: sí
es: Esto parece un caso ficticio: si ya lo es, no hay nada que seudonimizar. ¿Para qué quieres seudonimizarlo?
en: This looks like a fictional case: if it already is, there is nothing to pseudonymise. What do you want to pseudonymise it for?

### puerta.sin_mediacion
origen: nuevo
seguridad: sí
es: Parece que describes tu propia situación o la de un tercero sin mediación clínica o jurídica. Este skill es para casos ya manejados por un profesional habilitado. ¿Quién interviene profesionalmente en este caso?
en: It seems you are describing your own situation or that of a third party without clinical or legal mediation. This skill is for cases already handled by a qualified professional. Who is professionally involved in this case?

### puerta.modo
origen: nuevo
seguridad: sí
es: Indica el modo: A (clínico), B (jurídico), C (generalización extrema) o audit. No hay modo por defecto.
en: State the mode: A (clinical), B (legal), C (extreme generalisation) or audit. There is no default mode.
