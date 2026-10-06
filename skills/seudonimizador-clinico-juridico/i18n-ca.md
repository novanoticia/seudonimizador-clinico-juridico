# i18n-ca — Catálogo (catalán)

<!-- BORRADOR DE IA, SIN REVISIÓN HUMANA. Las entradas con `seguridad: sí` deben revisarlas una persona antes de cambiar el estado a `revisado` (y hay que actualizar docs/estado-traducciones.md). -->
<!-- Registro: tuteo, como el original en español (imperativos «Indica…»). Tipografía: apóstrofo tipográfico (’), comillas angulares « » sin espacios, punto volat (l·l), sin signo de interrogación de apertura. -->
<!-- Términos: el catalán NO es lengua oficial de la UE, así que el RGPD no tiene versión oficial en catalán en EUR-Lex (hecho conocido, NO comprobado en esta sesión: EUR-Lex sirve un desafío anti-bots). «pseudonimització», «risc residual» y «llavor» son elección de la IA, no tomados de una fuente oficial. -->

- código: ca
- estado: borrador-ia-sin-revision-humana
- redactado-por: IA
- revisado-por: nadie
- fecha-revision: —

## Glosario

- seudonimización → pseudonimització
- seudonimizado → pseudonimitzat
- identificadores indirectos → identificadors indirectes
- riesgo residual → risc residual
- desplazamiento temporal → desplaçament temporal
- semilla → llavor
- token → token
- mapa → mapa
- generalización → generalització
- control de fidelidad → control de fidelitat
- fuga → fuita
- regenerar → regenerar

## Frases

### encabezado.apertura
origen: original
fuente: flujo.md
seguridad: no
es: ## APERTURA
ca: ## OBERTURA

### apertura.modo
origen: original
fuente: flujo.md
seguridad: no
es: Modo:
ca: Mode:

### lista.modos
origen: original
fuente: flujo.md
seguridad: no
es: [A | B | C]
ca: [A | B | C]
invariable: sí

### apertura.semilla
origen: original
fuente: flujo.md
seguridad: no
es: Semilla de desplazamiento temporal:
ca: Llavor del desplaçament temporal:

### unidad.dias
origen: original
fuente: flujo.md
seguridad: no
es: +N días
ca: +N dies

### apertura.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación de la semilla:
ca: Justificació de la llavor:

### apertura.preguntas
origen: original
fuente: flujo.md
seguridad: no
es: Preguntas críticas previas:
ca: Preguntes crítiques prèvies:

### valor.ninguna
origen: original
fuente: flujo.md
seguridad: no
es: ninguna
ca: cap

### encabezado.mapa
origen: original
fuente: flujo.md
seguridad: sí
es: ## MAPA — archivar o destruir aparte del texto
ca: ## MAPA — arxivar o destruir per separat del text

### mapa.desplazamiento
origen: original
fuente: flujo.md
seguridad: no
es: Desplazamiento temporal aplicado:
ca: Desplaçament temporal aplicat:

### mapa.rol_token
origen: original
fuente: flujo.md
seguridad: no
es: Mapa rol → token:
ca: Mapa rol → token:
invariable: sí

### mapa.ejemplo_persona_x
origen: original
fuente: flujo.md
seguridad: no
es: Persona X (rol: paciente / demandado / etc.) → [TOKEN]
ca: Persona X (rol: pacient / demandat / etc.) → [TOKEN]

### mapa.ejemplo_persona_y
origen: original
fuente: flujo.md
seguridad: no
es: Persona Y → [TOKEN]
ca: Persona Y → [TOKEN]
invariable: sí

### mapa.generalizaciones_geo
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones geográficas y organizacionales aplicadas:
ca: Generalitzacions geogràfiques i organitzatives aplicades:

### mapa.ejemplo_lugar
origen: original
fuente: flujo.md
seguridad: no
es: Lugar/entidad concreto → categoría funcional
ca: Lloc/entitat concret → categoria funcional

### mapa.generalizaciones_indirectos
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones de identificadores indirectos:
ca: Generalitzacions d’identificadors indirectes:

### mapa.ejemplo_atributo
origen: original
fuente: flujo.md
seguridad: no
es: Atributo concreto → atributo generalizado
ca: Atribut concret → atribut generalitzat

### encabezado.texto
origen: original
fuente: flujo.md
seguridad: no
es: ## TEXTO SEUDONIMIZADO
ca: ## TEXT PSEUDONIMITZAT

### encabezado.riesgo
origen: original
fuente: flujo.md
seguridad: sí
es: ## AUDITORÍA DE RIESGO RESIDUAL
ca: ## AUDITORIA DEL RISC RESIDUAL

### riesgo.nivel
origen: original
fuente: flujo.md
seguridad: no
es: Nivel:
ca: Nivell:

### lista.nivel
origen: original
fuente: flujo.md
seguridad: sí
es: [bajo / medio / alto]
ca: [baix / mitjà / alt]

### riesgo.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación:
ca: Justificació:

### riesgo.detalles
origen: original
fuente: flujo.md
seguridad: no
es: Detalles que aún podrían permitir reidentificación por singularidad combinada:
ca: Detalls que encara podrien permetre la reidentificació per singularitat combinada:

### riesgo.propuesta
origen: original
fuente: flujo.md
seguridad: no
es: Propuesta de generalización adicional (si procede):
ca: Proposta de generalització addicional (si escau):

### encabezado.fidelidad
origen: original
fuente: flujo.md
seguridad: sí
es: ## CONTROL DE FIDELIDAD
ca: ## CONTROL DE FIDELITAT

### fidelidad.pregunta
origen: original
fuente: flujo.md
seguridad: sí
es: ¿Algún elemento del texto seudonimizado no tiene correspondencia en el original?
ca: Hi ha algun element del text pseudonimitzat sense correspondència a l’original?

### lista.si_no
origen: original
fuente: flujo.md
seguridad: sí
es: [sí / no]
ca: [sí / no]
invariable: sí

### fidelidad.si_listar
origen: original
fuente: flujo.md
seguridad: no
es: Si sí, listar:
ca: En cas afirmatiu, enumera:

### fidelidad.marcadores
origen: original
fuente: flujo.md
seguridad: no
es: Marcadores usados:
ca: Marcadors utilitzats:

### encabezado.decisiones
origen: original
fuente: flujo.md
seguridad: no
es: ## DECISIONES POR DEFECTO
ca: ## DECISIONS PER DEFECTE

### mapa.formato_entrada
origen: original
fuente: plantilla-tokens.md
seguridad: no
es: Sujeto / lugar / entidad original → [TOKEN]   (rol en el caso: …)
ca: Subjecte / lloc / entitat original → [TOKEN]   (rol en el cas: …)

### encabezado.audit
origen: original
fuente: auditoria.md
seguridad: no
es: ## AUDITORÍA — texto ya seudonimizado
ca: ## AUDITORIA — text ja pseudonimitzat

### encabezado.comprobaciones
origen: original
fuente: auditoria.md
seguridad: no
es: ### Comprobaciones
ca: ### Comprovacions

### audit.comprobacion_1
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores directos:
ca: Identificadors directes:

### audit.comprobacion_2
origen: original
fuente: auditoria.md
seguridad: no
es: Lugares y entidades:
ca: Llocs i entitats:

### audit.comprobacion_3
origen: original
fuente: auditoria.md
seguridad: no
es: Fechas:
ca: Dates:

### audit.comprobacion_4
origen: original
fuente: auditoria.md
seguridad: no
es: Numéricos identificadores:
ca: Dades numèriques identificadores:

### audit.comprobacion_5
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores indirectos:
ca: Identificadors indirectes:

### audit.comprobacion_6
origen: original
fuente: auditoria.md
seguridad: no
es: Coherencia interna:
ca: Coherència interna:

### audit.comprobacion_7
origen: original
fuente: auditoria.md
seguridad: no
es: Fidelidad al original:
ca: Fidelitat a l’original:

### lista.veredicto
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda]
ca: [Passa / Falla / Dubte]

### lista.veredicto_fidelidad
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda / No aplicable]
ca: [Passa / Falla / Dubte / No aplicable]

### encabezado.riesgo_estimado
origen: original
fuente: auditoria.md
seguridad: sí
es: ### Riesgo residual estimado
ca: ### Risc residual estimat

### encabezado.propuestas
origen: original
fuente: auditoria.md
seguridad: no
es: ### Propuestas
ca: ### Propostes

### propuestas.correcciones
origen: original
fuente: auditoria.md
seguridad: no
es: Correcciones necesarias antes de uso secundario:
ca: Correccions necessàries abans de l’ús secundari:

### propuestas.generalizacion
origen: original
fuente: auditoria.md
seguridad: no
es: Generalización adicional recomendada (si procede):
ca: Generalització addicional recomanada (si escau):

### propuestas.recomendacion
origen: original
fuente: auditoria.md
seguridad: no
es: Recomendación global:
ca: Recomanació global:

### lista.recomendacion
origen: original
fuente: auditoria.md
seguridad: sí
es: [apto para uso secundario interno / requiere corrección antes de uso / pasar a modo C / fragmentar y reseudonimizar partes / no apto sin revisión humana experta]
ca: [apte per a ús secundari intern / requereix correcció abans de l’ús / passar al mode C / fragmentar i tornar a pseudonimitzar parts / no apte sense revisió humana experta]

### encabezado.regenerar
origen: original
fuente: auditoria.md
seguridad: no
es: ### Si quieres regenerar
ca: ### Si vols regenerar

### regenerar.texto
origen: original
fuente: auditoria.md
seguridad: no
es: Indica explícitamente "regenerar" y el texto se reprocesa aplicando las correcciones detectadas, manteniendo los tokens y el desplazamiento temporal del original (si son recuperables) o introduciendo nuevos (si no).
ca: Indica explícitament «regenerar» i el text es reprocessa aplicant les correccions detectades, mantenint els tokens i el desplaçament temporal de l’original (si són recuperables) o introduint-ne de nous (si no).

### encabezado.aviso_traduccion
origen: nuevo
seguridad: sí
es: ## AVISO DE TRADUCCIÓN
ca: ## AVÍS DE TRADUCCIÓ

### aviso.traduccion
origen: nuevo
seguridad: sí
es: Marco de esta respuesta traducido por IA, sin revisión humana. Ante cualquier duda sobre una advertencia de seguridad, consulta la versión en español, que es la de referencia.
ca: El marc d’aquesta resposta ha estat traduït per una IA, sense revisió humana. En cas de dubte sobre qualsevol advertiment de seguretat, consulta la versió en castellà, que és la de referència.

### puerta.ficticio
origen: nuevo
seguridad: sí
es: Esto parece un caso ficticio: si ya lo es, no hay nada que seudonimizar. ¿Para qué quieres seudonimizarlo?
ca: Això sembla un cas fictici: si ja ho és, no hi ha res a pseudonimitzar. Per a què vols pseudonimitzar-lo?

### puerta.sin_mediacion
origen: nuevo
seguridad: sí
es: Parece que describes tu propia situación o la de un tercero sin mediación clínica o jurídica. Este skill es para casos ya manejados por un profesional habilitado. ¿Quién interviene profesionalmente en este caso?
ca: Sembla que descrius la teva pròpia situació o la d’un tercer sense mediació clínica o jurídica. Aquest skill és per a casos ja gestionats per un professional habilitat. Qui hi intervé professionalment en aquest cas?

### puerta.modo
origen: nuevo
seguridad: sí
es: Indica el modo: A (clínico), B (jurídico), C (generalización extrema) o audit. No hay modo por defecto.
ca: Indica el mode: A (clínic), B (jurídic), C (generalització extrema) o audit. No hi ha mode per defecte.
