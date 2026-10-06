# i18n-gl — Catálogo (gallego)

<!-- BORRADOR DE IA, SIN REVISIÓN HUMANA. Las entradas con `seguridad: sí` deben revisarlas una persona antes de cambiar el estado a `revisado` (y hay que actualizar docs/estado-traducciones.md). -->
<!-- Registro: tuteo, como el original en español. Ortografía de la RAG (x en lugar de j: xurídico, xustificación, xeneralización). Tipografía: comillas angulares « » sin espacios, sin signo de interrogación de apertura. -->
<!-- Términos: el gallego NO es lengua oficial de la UE, así que el RGPD no tiene versión oficial en gallego en EUR-Lex (hecho conocido, NO comprobado en esta sesión: EUR-Lex sirve un desafío anti-bots). «pseudonimización», «risco residual» y «semente» son elección de la IA, no tomados de una fuente oficial; la RAG admite también la grafía «seudo-». -->

- código: gl
- estado: borrador-ia-sin-revision-humana
- redactado-por: IA
- revisado-por: nadie
- fecha-revision: —

## Glosario

- seudonimización → pseudonimización
- seudonimizado → pseudonimizado
- identificadores indirectos → identificadores indirectos
- riesgo residual → risco residual
- desplazamiento temporal → desprazamento temporal
- semilla → semente
- token → token
- mapa → mapa
- generalización → xeneralización
- control de fidelidad → control de fidelidade
- fuga → fuga
- regenerar → rexenerar

## Frases

### encabezado.apertura
origen: original
fuente: flujo.md
seguridad: no
es: ## APERTURA
gl: ## ABERTURA

### apertura.modo
origen: original
fuente: flujo.md
seguridad: no
es: Modo:
gl: Modo:
invariable: sí

### lista.modos
origen: original
fuente: flujo.md
seguridad: no
es: [A | B | C]
gl: [A | B | C]
invariable: sí

### apertura.semilla
origen: original
fuente: flujo.md
seguridad: no
es: Semilla de desplazamiento temporal:
gl: Semente do desprazamento temporal:

### unidad.dias
origen: original
fuente: flujo.md
seguridad: no
es: +N días
gl: +N días
invariable: sí

### apertura.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación de la semilla:
gl: Xustificación da semente:

### apertura.preguntas
origen: original
fuente: flujo.md
seguridad: no
es: Preguntas críticas previas:
gl: Preguntas críticas previas:
invariable: sí

### valor.ninguna
origen: original
fuente: flujo.md
seguridad: no
es: ninguna
gl: ningunha

### encabezado.mapa
origen: original
fuente: flujo.md
seguridad: sí
es: ## MAPA — archivar o destruir aparte del texto
gl: ## MAPA — arquivar ou destruír por separado do texto

### mapa.desplazamiento
origen: original
fuente: flujo.md
seguridad: no
es: Desplazamiento temporal aplicado:
gl: Desprazamento temporal aplicado:

### mapa.rol_token
origen: original
fuente: flujo.md
seguridad: no
es: Mapa rol → token:
gl: Mapa rol → token:
invariable: sí

### mapa.ejemplo_persona_x
origen: original
fuente: flujo.md
seguridad: no
es: Persona X (rol: paciente / demandado / etc.) → [TOKEN]
gl: Persoa X (rol: paciente / demandado / etc.) → [TOKEN]

### mapa.ejemplo_persona_y
origen: original
fuente: flujo.md
seguridad: no
es: Persona Y → [TOKEN]
gl: Persoa Y → [TOKEN]

### mapa.generalizaciones_geo
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones geográficas y organizacionales aplicadas:
gl: Xeneralizacións xeográficas e organizativas aplicadas:

### mapa.ejemplo_lugar
origen: original
fuente: flujo.md
seguridad: no
es: Lugar/entidad concreto → categoría funcional
gl: Lugar/entidade concreto → categoría funcional

### mapa.generalizaciones_indirectos
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones de identificadores indirectos:
gl: Xeneralizacións de identificadores indirectos:

### mapa.ejemplo_atributo
origen: original
fuente: flujo.md
seguridad: no
es: Atributo concreto → atributo generalizado
gl: Atributo concreto → atributo xeneralizado

### encabezado.texto
origen: original
fuente: flujo.md
seguridad: no
es: ## TEXTO SEUDONIMIZADO
gl: ## TEXTO PSEUDONIMIZADO

### encabezado.riesgo
origen: original
fuente: flujo.md
seguridad: sí
es: ## AUDITORÍA DE RIESGO RESIDUAL
gl: ## AUDITORÍA DO RISCO RESIDUAL

### riesgo.nivel
origen: original
fuente: flujo.md
seguridad: no
es: Nivel:
gl: Nivel:
invariable: sí

### lista.nivel
origen: original
fuente: flujo.md
seguridad: sí
es: [bajo / medio / alto]
gl: [baixo / medio / alto]

### riesgo.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación:
gl: Xustificación:

### riesgo.detalles
origen: original
fuente: flujo.md
seguridad: no
es: Detalles que aún podrían permitir reidentificación por singularidad combinada:
gl: Detalles que aínda poderían permitir a reidentificación por singularidade combinada:

### riesgo.propuesta
origen: original
fuente: flujo.md
seguridad: no
es: Propuesta de generalización adicional (si procede):
gl: Proposta de xeneralización adicional (se procede):

### encabezado.fidelidad
origen: original
fuente: flujo.md
seguridad: sí
es: ## CONTROL DE FIDELIDAD
gl: ## CONTROL DE FIDELIDADE

### fidelidad.pregunta
origen: original
fuente: flujo.md
seguridad: sí
es: ¿Algún elemento del texto seudonimizado no tiene correspondencia en el original?
gl: Hai algún elemento do texto pseudonimizado sen correspondencia no orixinal?

### lista.si_no
origen: original
fuente: flujo.md
seguridad: sí
es: [sí / no]
gl: [si / non]

### fidelidad.si_listar
origen: original
fuente: flujo.md
seguridad: no
es: Si sí, listar:
gl: En caso afirmativo, enumera:

### fidelidad.marcadores
origen: original
fuente: flujo.md
seguridad: no
es: Marcadores usados:
gl: Marcadores empregados:

### encabezado.decisiones
origen: original
fuente: flujo.md
seguridad: no
es: ## DECISIONES POR DEFECTO
gl: ## DECISIÓNS POR DEFECTO

### mapa.formato_entrada
origen: original
fuente: plantilla-tokens.md
seguridad: no
es: Sujeto / lugar / entidad original → [TOKEN]   (rol en el caso: …)
gl: Suxeito / lugar / entidade orixinal → [TOKEN]   (rol no caso: …)

### encabezado.audit
origen: original
fuente: auditoria.md
seguridad: no
es: ## AUDITORÍA — texto ya seudonimizado
gl: ## AUDITORÍA — texto xa pseudonimizado

### encabezado.comprobaciones
origen: original
fuente: auditoria.md
seguridad: no
es: ### Comprobaciones
gl: ### Comprobacións

### audit.comprobacion_1
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores directos:
gl: Identificadores directos:
invariable: sí

### audit.comprobacion_2
origen: original
fuente: auditoria.md
seguridad: no
es: Lugares y entidades:
gl: Lugares e entidades:

### audit.comprobacion_3
origen: original
fuente: auditoria.md
seguridad: no
es: Fechas:
gl: Datas:

### audit.comprobacion_4
origen: original
fuente: auditoria.md
seguridad: no
es: Numéricos identificadores:
gl: Datos numéricos identificadores:

### audit.comprobacion_5
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores indirectos:
gl: Identificadores indirectos:
invariable: sí

### audit.comprobacion_6
origen: original
fuente: auditoria.md
seguridad: no
es: Coherencia interna:
gl: Coherencia interna:
invariable: sí

### audit.comprobacion_7
origen: original
fuente: auditoria.md
seguridad: no
es: Fidelidad al original:
gl: Fidelidade ao orixinal:

### lista.veredicto
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda]
gl: [Pasa / Fallo / Dúbida]

### lista.veredicto_fidelidad
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda / No aplicable]
gl: [Pasa / Fallo / Dúbida / Non aplicable]

### encabezado.riesgo_estimado
origen: original
fuente: auditoria.md
seguridad: sí
es: ### Riesgo residual estimado
gl: ### Risco residual estimado

### encabezado.propuestas
origen: original
fuente: auditoria.md
seguridad: no
es: ### Propuestas
gl: ### Propostas

### propuestas.correcciones
origen: original
fuente: auditoria.md
seguridad: no
es: Correcciones necesarias antes de uso secundario:
gl: Correccións necesarias antes do uso secundario:

### propuestas.generalizacion
origen: original
fuente: auditoria.md
seguridad: no
es: Generalización adicional recomendada (si procede):
gl: Xeneralización adicional recomendada (se procede):

### propuestas.recomendacion
origen: original
fuente: auditoria.md
seguridad: no
es: Recomendación global:
gl: Recomendación global:
invariable: sí

### lista.recomendacion
origen: original
fuente: auditoria.md
seguridad: sí
es: [apto para uso secundario interno / requiere corrección antes de uso / pasar a modo C / fragmentar y reseudonimizar partes / no apto sin revisión humana experta]
gl: [apto para uso secundario interno / require corrección antes do uso / pasar ao modo C / fragmentar e pseudonimizar de novo partes / non apto sen revisión humana experta]

### encabezado.regenerar
origen: original
fuente: auditoria.md
seguridad: no
es: ### Si quieres regenerar
gl: ### Se queres rexenerar

### regenerar.texto
origen: original
fuente: auditoria.md
seguridad: no
es: Indica explícitamente "regenerar" y el texto se reprocesa aplicando las correcciones detectadas, manteniendo los tokens y el desplazamiento temporal del original (si son recuperables) o introduciendo nuevos (si no).
gl: Indica explicitamente «rexenerar» e o texto reprocésase aplicando as correccións detectadas, mantendo os tokens e o desprazamento temporal do orixinal (se son recuperables) ou introducindo outros novos (se non).

### encabezado.aviso_traduccion
origen: nuevo
seguridad: sí
es: ## AVISO DE TRADUCCIÓN
gl: ## AVISO DE TRADUCIÓN

### aviso.traduccion
origen: nuevo
seguridad: sí
es: Marco de esta respuesta traducido por IA, sin revisión humana. Ante cualquier duda sobre una advertencia de seguridad, consulta la versión en español, que es la de referencia.
gl: O marco desta resposta foi traducido por unha IA, sen revisión humana. En caso de dúbida sobre calquera advertencia de seguridade, consulta a versión en castelán, que é a de referencia.

### puerta.ficticio
origen: nuevo
seguridad: sí
es: Esto parece un caso ficticio: si ya lo es, no hay nada que seudonimizar. ¿Para qué quieres seudonimizarlo?
gl: Isto parece un caso ficticio: se xa o é, non hai nada que pseudonimizar. Para que queres pseudonimizalo?

### puerta.sin_mediacion
origen: nuevo
seguridad: sí
es: Parece que describes tu propia situación o la de un tercero sin mediación clínica o jurídica. Este skill es para casos ya manejados por un profesional habilitado. ¿Quién interviene profesionalmente en este caso?
gl: Parece que describes a túa propia situación ou a dun terceiro sen mediación clínica ou xurídica. Este skill é para casos xa xestionados por un profesional habilitado. Quen intervén profesionalmente neste caso?

### puerta.modo
origen: nuevo
seguridad: sí
es: Indica el modo: A (clínico), B (jurídico), C (generalización extrema) o audit. No hay modo por defecto.
gl: Indica o modo: A (clínico), B (xurídico), C (xeneralización extrema) ou audit. Non hai modo por defecto.
