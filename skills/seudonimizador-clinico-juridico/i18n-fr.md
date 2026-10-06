# i18n-fr — Catálogo (francés)

<!-- BORRADOR DE IA, SIN REVISIÓN HUMANA. Las entradas con `seguridad: sí` deben revisarlas una persona antes de cambiar el estado a `revisado` (y hay que actualizar docs/estado-traducciones.md). -->
<!-- Registro profesional («vous»). Tipografía francesa: espacio insécable antes de «:», espacio fino insécable antes de «?», comillas « » con espacio insécable, apóstrofo tipográfico. -->
<!-- Términos: «pseudonymisation» consta en el art. 4(5) del RGPD en francés; «table de correspondance» y «risque résiduel» los usa la CNIL. Comprobado solo por búsqueda (resúmenes, no texto literal): EUR-Lex no es accesible desde el entorno de desarrollo. -->

- código: fr
- estado: borrador-ia-sin-revision-humana
- redactado-por: IA
- revisado-por: nadie
- fecha-revision: —

## Glosario

- seudonimización → pseudonymisation
- seudonimizado → pseudonymisé
- identificadores indirectos → identifiants indirects
- riesgo residual → risque résiduel
- desplazamiento temporal → décalage temporel
- semilla → graine
- token → token
- mapa → table de correspondance
- generalización → généralisation
- control de fidelidad → contrôle de fidélité
- fuga → fuite
- regenerar → régénérer

## Frases

### encabezado.apertura
origen: original
fuente: flujo.md
seguridad: no
es: ## APERTURA
fr: ## OUVERTURE

### apertura.modo
origen: original
fuente: flujo.md
seguridad: no
es: Modo:
fr: Mode :

### lista.modos
origen: original
fuente: flujo.md
seguridad: no
es: [A | B | C]
fr: [A | B | C]
invariable: sí

### apertura.semilla
origen: original
fuente: flujo.md
seguridad: no
es: Semilla de desplazamiento temporal:
fr: Graine du décalage temporel :

### unidad.dias
origen: original
fuente: flujo.md
seguridad: no
es: +N días
fr: +N jours

### apertura.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación de la semilla:
fr: Justification de la graine :

### apertura.preguntas
origen: original
fuente: flujo.md
seguridad: no
es: Preguntas críticas previas:
fr: Questions critiques préalables :

### valor.ninguna
origen: original
fuente: flujo.md
seguridad: no
es: ninguna
fr: aucune

### encabezado.mapa
origen: original
fuente: flujo.md
seguridad: sí
es: ## MAPA — archivar o destruir aparte del texto
fr: ## TABLE DE CORRESPONDANCE — à archiver ou détruire séparément du texte

### mapa.desplazamiento
origen: original
fuente: flujo.md
seguridad: no
es: Desplazamiento temporal aplicado:
fr: Décalage temporel appliqué :

### mapa.rol_token
origen: original
fuente: flujo.md
seguridad: no
es: Mapa rol → token:
fr: Table de correspondance rôle → token :

### mapa.ejemplo_persona_x
origen: original
fuente: flujo.md
seguridad: no
es: Persona X (rol: paciente / demandado / etc.) → [TOKEN]
fr: Personne X (rôle : patient / défendeur / etc.) → [TOKEN]

### mapa.ejemplo_persona_y
origen: original
fuente: flujo.md
seguridad: no
es: Persona Y → [TOKEN]
fr: Personne Y → [TOKEN]

### mapa.generalizaciones_geo
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones geográficas y organizacionales aplicadas:
fr: Généralisations géographiques et organisationnelles appliquées :

### mapa.ejemplo_lugar
origen: original
fuente: flujo.md
seguridad: no
es: Lugar/entidad concreto → categoría funcional
fr: Lieu/entité concret → catégorie fonctionnelle

### mapa.generalizaciones_indirectos
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones de identificadores indirectos:
fr: Généralisations des identifiants indirects :

### mapa.ejemplo_atributo
origen: original
fuente: flujo.md
seguridad: no
es: Atributo concreto → atributo generalizado
fr: Attribut concret → attribut généralisé

### encabezado.texto
origen: original
fuente: flujo.md
seguridad: no
es: ## TEXTO SEUDONIMIZADO
fr: ## TEXTE PSEUDONYMISÉ

### encabezado.riesgo
origen: original
fuente: flujo.md
seguridad: sí
es: ## AUDITORÍA DE RIESGO RESIDUAL
fr: ## AUDIT DU RISQUE RÉSIDUEL

### riesgo.nivel
origen: original
fuente: flujo.md
seguridad: no
es: Nivel:
fr: Niveau :

### lista.nivel
origen: original
fuente: flujo.md
seguridad: sí
es: [bajo / medio / alto]
fr: [faible / moyen / élevé]

### riesgo.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación:
fr: Justification :

### riesgo.detalles
origen: original
fuente: flujo.md
seguridad: no
es: Detalles que aún podrían permitir reidentificación por singularidad combinada:
fr: Éléments pouvant encore permettre une réidentification par singularité combinée :

### riesgo.propuesta
origen: original
fuente: flujo.md
seguridad: no
es: Propuesta de generalización adicional (si procede):
fr: Proposition de généralisation supplémentaire (le cas échéant) :

### encabezado.fidelidad
origen: original
fuente: flujo.md
seguridad: sí
es: ## CONTROL DE FIDELIDAD
fr: ## CONTRÔLE DE FIDÉLITÉ

### fidelidad.pregunta
origen: original
fuente: flujo.md
seguridad: sí
es: ¿Algún elemento del texto seudonimizado no tiene correspondencia en el original?
fr: Un élément du texte pseudonymisé est-il sans correspondance dans l’original ?

### lista.si_no
origen: original
fuente: flujo.md
seguridad: sí
es: [sí / no]
fr: [oui / non]

### fidelidad.si_listar
origen: original
fuente: flujo.md
seguridad: no
es: Si sí, listar:
fr: Si oui, lister :

### fidelidad.marcadores
origen: original
fuente: flujo.md
seguridad: no
es: Marcadores usados:
fr: Marqueurs utilisés :

### encabezado.decisiones
origen: original
fuente: flujo.md
seguridad: no
es: ## DECISIONES POR DEFECTO
fr: ## DÉCISIONS PAR DÉFAUT

### mapa.formato_entrada
origen: original
fuente: plantilla-tokens.md
seguridad: no
es: Sujeto / lugar / entidad original → [TOKEN]   (rol en el caso: …)
fr: Sujet / lieu / entité d’origine → [TOKEN]   (rôle dans le cas : …)

### encabezado.audit
origen: original
fuente: auditoria.md
seguridad: no
es: ## AUDITORÍA — texto ya seudonimizado
fr: ## AUDIT — texte déjà pseudonymisé

### encabezado.comprobaciones
origen: original
fuente: auditoria.md
seguridad: no
es: ### Comprobaciones
fr: ### Vérifications

### audit.comprobacion_1
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores directos:
fr: Identifiants directs :

### audit.comprobacion_2
origen: original
fuente: auditoria.md
seguridad: no
es: Lugares y entidades:
fr: Lieux et entités :

### audit.comprobacion_3
origen: original
fuente: auditoria.md
seguridad: no
es: Fechas:
fr: Dates :

### audit.comprobacion_4
origen: original
fuente: auditoria.md
seguridad: no
es: Numéricos identificadores:
fr: Données numériques identifiantes :

### audit.comprobacion_5
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores indirectos:
fr: Identifiants indirects :

### audit.comprobacion_6
origen: original
fuente: auditoria.md
seguridad: no
es: Coherencia interna:
fr: Cohérence interne :

### audit.comprobacion_7
origen: original
fuente: auditoria.md
seguridad: no
es: Fidelidad al original:
fr: Fidélité à l’original :

### lista.veredicto
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda]
fr: [Réussi / Échec / Incertain]

### lista.veredicto_fidelidad
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda / No aplicable]
fr: [Réussi / Échec / Incertain / Non applicable]

### encabezado.riesgo_estimado
origen: original
fuente: auditoria.md
seguridad: sí
es: ### Riesgo residual estimado
fr: ### Risque résiduel estimé

### encabezado.propuestas
origen: original
fuente: auditoria.md
seguridad: no
es: ### Propuestas
fr: ### Propositions

### propuestas.correcciones
origen: original
fuente: auditoria.md
seguridad: no
es: Correcciones necesarias antes de uso secundario:
fr: Corrections nécessaires avant tout usage secondaire :

### propuestas.generalizacion
origen: original
fuente: auditoria.md
seguridad: no
es: Generalización adicional recomendada (si procede):
fr: Généralisation supplémentaire recommandée (le cas échéant) :

### propuestas.recomendacion
origen: original
fuente: auditoria.md
seguridad: no
es: Recomendación global:
fr: Recommandation globale :

### lista.recomendacion
origen: original
fuente: auditoria.md
seguridad: sí
es: [apto para uso secundario interno / requiere corrección antes de uso / pasar a modo C / fragmentar y reseudonimizar partes / no apto sin revisión humana experta]
fr: [apte à un usage secondaire interne / nécessite une correction avant usage / passer au mode C / fragmenter et pseudonymiser de nouveau certaines parties / inapte sans révision humaine experte]

### encabezado.regenerar
origen: original
fuente: auditoria.md
seguridad: no
es: ### Si quieres regenerar
fr: ### Si vous souhaitez régénérer

### regenerar.texto
origen: original
fuente: auditoria.md
seguridad: no
es: Indica explícitamente "regenerar" y el texto se reprocesa aplicando las correcciones detectadas, manteniendo los tokens y el desplazamiento temporal del original (si son recuperables) o introduciendo nuevos (si no).
fr: Indiquez explicitement « régénérer » et le texte sera retraité en appliquant les corrections détectées, en conservant les tokens et le décalage temporel de l’original (s’ils sont récupérables) ou en en introduisant de nouveaux (sinon).

### encabezado.aviso_traduccion
origen: nuevo
seguridad: sí
es: ## AVISO DE TRADUCCIÓN
fr: ## AVIS DE TRADUCTION

### aviso.traduccion
origen: nuevo
seguridad: sí
es: Marco de esta respuesta traducido por IA, sin revisión humana. Ante cualquier duda sobre una advertencia de seguridad, consulta la versión en español, que es la de referencia.
fr: Le cadre de cette réponse a été traduit par une IA, sans révision humaine. En cas de doute sur un avertissement de sécurité, consultez la version espagnole, qui sert de référence.

### puerta.ficticio
origen: nuevo
seguridad: sí
es: Esto parece un caso ficticio: si ya lo es, no hay nada que seudonimizar. ¿Para qué quieres seudonimizarlo?
fr: Il semble s’agir d’un cas fictif : s’il l’est déjà, il n’y a rien à pseudonymiser. Dans quel but souhaitez-vous le pseudonymiser ?

### puerta.sin_mediacion
origen: nuevo
seguridad: sí
es: Parece que describes tu propia situación o la de un tercero sin mediación clínica o jurídica. Este skill es para casos ya manejados por un profesional habilitado. ¿Quién interviene profesionalmente en este caso?
fr: Il semble que vous décriviez votre propre situation ou celle d’un tiers sans médiation clinique ou juridique. Ce skill est destiné à des cas déjà traités par un professionnel habilité. Qui intervient professionnellement dans ce cas ?

### puerta.modo
origen: nuevo
seguridad: sí
es: Indica el modo: A (clínico), B (jurídico), C (generalización extrema) o audit. No hay modo por defecto.
fr: Indiquez le mode : A (clinique), B (juridique), C (généralisation extrême) ou audit. Il n’y a pas de mode par défaut.
