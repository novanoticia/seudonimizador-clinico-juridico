# i18n-eu — Catálogo (euskera)

<!-- EXPERIMENTAL. BORRADOR DE IA, SIN REVISIÓN HUMANA, Y DE RIESGO ELEVADO DE ERRORES. El euskera es el idioma menos fiable de los cinco para un borrador de IA (lengua aglutinante, terminología jurídica y clínica poco estandarizada, y sin vocabulario compartido con el español que permita detectar fallos por heurística). Las entradas con `seguridad: sí` deben revisarlas una persona antes de cambiar el estado a `revisado` (y hay que actualizar docs/estado-traducciones.md). -->
<!-- Advertencia reforzada: `aviso.traduccion` es más fuerte que el de los demás idiomas y es BILINGÜE (euskera + « — AVISO: » + español), para que la advertencia siga siendo inequívoca aunque el euskera fuese defectuoso. Es la única entrada que contiene español a propósito. -->
<!-- Registro: zuka (trato de respeto, «duzu», «baduzu»), el estándar del software; el original en español tutea. Tipografía: comillas angulares « » sin espacios; sin tildes (la ortografía vasca no las usa). -->
<!-- Términos: el euskera NO es lengua oficial de la UE, así que el RGPD no tiene versión oficial en euskera en EUR-Lex (hecho conocido, NO comprobado en esta sesión: EUR-Lex sirve un desafío anti-bots). «pseudonimizazio», «hondar-arriskua», «hazia», «zeharkako identifikatzaileak» y «fideltasun-kontrola» son elección de la IA, no tomados de una fuente oficial. El glosario se aplica por RAÍCES, no por término entero. -->

- código: eu
- estado: experimental-ia-sin-revision-humana
- redactado-por: IA
- revisado-por: nadie
- fecha-revision: —

## Glosario

- seudonimización → pseudonimizazio
- seudonimizado → pseudonimizatu
- identificadores indirectos → zeharkako identifikatzaileak
- riesgo residual → hondar-arriskua
- desplazamiento temporal → denbora-desplazamendua
- semilla → hazia
- token → tokena
- mapa → mapa
- generalización → orokortzea
- control de fidelidad → fideltasun-kontrola
- fuga → ihesa
- regenerar → birsortu

## Frases

### encabezado.apertura
origen: original
fuente: flujo.md
seguridad: no
es: ## APERTURA
eu: ## HASIERA

### apertura.modo
origen: original
fuente: flujo.md
seguridad: no
es: Modo:
eu: Modua:

### lista.modos
origen: original
fuente: flujo.md
seguridad: no
es: [A | B | C]
eu: [A | B | C]
invariable: sí

### apertura.semilla
origen: original
fuente: flujo.md
seguridad: no
es: Semilla de desplazamiento temporal:
eu: Denbora-desplazamenduaren hazia:

### unidad.dias
origen: original
fuente: flujo.md
seguridad: no
es: +N días
eu: +N egun

### apertura.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación de la semilla:
eu: Haziaren justifikazioa:

### apertura.preguntas
origen: original
fuente: flujo.md
seguridad: no
es: Preguntas críticas previas:
eu: Aurretiazko galdera kritikoak:

### valor.ninguna
origen: original
fuente: flujo.md
seguridad: no
es: ninguna
eu: bat ere ez

### encabezado.mapa
origen: original
fuente: flujo.md
seguridad: sí
es: ## MAPA — archivar o destruir aparte del texto
eu: ## MAPA — testutik bereizita artxibatu edo suntsitu

### mapa.desplazamiento
origen: original
fuente: flujo.md
seguridad: no
es: Desplazamiento temporal aplicado:
eu: Aplikatutako denbora-desplazamendua:

### mapa.rol_token
origen: original
fuente: flujo.md
seguridad: no
es: Mapa rol → token:
eu: Rol → token mapa:

### mapa.ejemplo_persona_x
origen: original
fuente: flujo.md
seguridad: no
es: Persona X (rol: paciente / demandado / etc.) → [TOKEN]
eu: X pertsona (rola: paziente / demandatu / etab.) → [TOKEN]

### mapa.ejemplo_persona_y
origen: original
fuente: flujo.md
seguridad: no
es: Persona Y → [TOKEN]
eu: Y pertsona → [TOKEN]

### mapa.generalizaciones_geo
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones geográficas y organizacionales aplicadas:
eu: Aplikatutako orokortze geografikoak eta antolakuntzazkoak:

### mapa.ejemplo_lugar
origen: original
fuente: flujo.md
seguridad: no
es: Lugar/entidad concreto → categoría funcional
eu: Leku/erakunde zehatza → kategoria funtzionala

### mapa.generalizaciones_indirectos
origen: original
fuente: flujo.md
seguridad: no
es: Generalizaciones de identificadores indirectos:
eu: Zeharkako identifikatzaileen orokortzeak:

### mapa.ejemplo_atributo
origen: original
fuente: flujo.md
seguridad: no
es: Atributo concreto → atributo generalizado
eu: Atributu zehatza → atributu orokortua

### encabezado.texto
origen: original
fuente: flujo.md
seguridad: no
es: ## TEXTO SEUDONIMIZADO
eu: ## TESTU PSEUDONIMIZATUA

### encabezado.riesgo
origen: original
fuente: flujo.md
seguridad: sí
es: ## AUDITORÍA DE RIESGO RESIDUAL
eu: ## HONDAR-ARRISKUAREN AUDITORETZA

### riesgo.nivel
origen: original
fuente: flujo.md
seguridad: no
es: Nivel:
eu: Maila:

### lista.nivel
origen: original
fuente: flujo.md
seguridad: sí
es: [bajo / medio / alto]
eu: [baxua / ertaina / altua]

### riesgo.justificacion
origen: original
fuente: flujo.md
seguridad: no
es: Justificación:
eu: Justifikazioa:

### riesgo.detalles
origen: original
fuente: flujo.md
seguridad: no
es: Detalles que aún podrían permitir reidentificación por singularidad combinada:
eu: Berridentifikazioa oraindik ere ahalbidetu lezaketen xehetasunak, singulartasun konbinatuaren ondorioz:

### riesgo.propuesta
origen: original
fuente: flujo.md
seguridad: no
es: Propuesta de generalización adicional (si procede):
eu: Orokortze osagarriaren proposamena (hala dagokionean):

### encabezado.fidelidad
origen: original
fuente: flujo.md
seguridad: sí
es: ## CONTROL DE FIDELIDAD
eu: ## FIDELTASUN-KONTROLA

### fidelidad.pregunta
origen: original
fuente: flujo.md
seguridad: sí
es: ¿Algún elemento del texto seudonimizado no tiene correspondencia en el original?
eu: Testu pseudonimizatuko elementuren batek ez al du baliokiderik jatorrizkoan?

### lista.si_no
origen: original
fuente: flujo.md
seguridad: sí
es: [sí / no]
eu: [bai / ez]

### fidelidad.si_listar
origen: original
fuente: flujo.md
seguridad: no
es: Si sí, listar:
eu: Baiezkoan, zerrendatu:

### fidelidad.marcadores
origen: original
fuente: flujo.md
seguridad: no
es: Marcadores usados:
eu: Erabilitako markatzaileak:

### encabezado.decisiones
origen: original
fuente: flujo.md
seguridad: no
es: ## DECISIONES POR DEFECTO
eu: ## LEHENETSITAKO ERABAKIAK

### mapa.formato_entrada
origen: original
fuente: plantilla-tokens.md
seguridad: no
es: Sujeto / lugar / entidad original → [TOKEN]   (rol en el caso: …)
eu: Jatorrizko subjektua / lekua / erakundea → [TOKEN]   (kasuko rola: …)

### encabezado.audit
origen: original
fuente: auditoria.md
seguridad: no
es: ## AUDITORÍA — texto ya seudonimizado
eu: ## AUDITORETZA — dagoeneko pseudonimizatutako testua

### encabezado.comprobaciones
origen: original
fuente: auditoria.md
seguridad: no
es: ### Comprobaciones
eu: ### Egiaztapenak

### audit.comprobacion_1
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores directos:
eu: Identifikatzaile zuzenak:

### audit.comprobacion_2
origen: original
fuente: auditoria.md
seguridad: no
es: Lugares y entidades:
eu: Lekuak eta erakundeak:

### audit.comprobacion_3
origen: original
fuente: auditoria.md
seguridad: no
es: Fechas:
eu: Datak:

### audit.comprobacion_4
origen: original
fuente: auditoria.md
seguridad: no
es: Numéricos identificadores:
eu: Datu numeriko identifikatzaileak:

### audit.comprobacion_5
origen: original
fuente: auditoria.md
seguridad: no
es: Identificadores indirectos:
eu: Zeharkako identifikatzaileak:

### audit.comprobacion_6
origen: original
fuente: auditoria.md
seguridad: no
es: Coherencia interna:
eu: Barne-koherentzia:

### audit.comprobacion_7
origen: original
fuente: auditoria.md
seguridad: no
es: Fidelidad al original:
eu: Jatorrizkoarekiko fideltasuna:

### lista.veredicto
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda]
eu: [Gainditu / Huts / Zalantza]

### lista.veredicto_fidelidad
origen: original
fuente: auditoria.md
seguridad: sí
es: [Pasa / Fallo / Duda / No aplicable]
eu: [Gainditu / Huts / Zalantza / Ez aplikagarria]

### encabezado.riesgo_estimado
origen: original
fuente: auditoria.md
seguridad: sí
es: ### Riesgo residual estimado
eu: ### Kalkulatutako hondar-arriskua

### encabezado.propuestas
origen: original
fuente: auditoria.md
seguridad: no
es: ### Propuestas
eu: ### Proposamenak

### propuestas.correcciones
origen: original
fuente: auditoria.md
seguridad: no
es: Correcciones necesarias antes de uso secundario:
eu: Bigarren mailako erabilera baino lehen egin beharreko zuzenketak:

### propuestas.generalizacion
origen: original
fuente: auditoria.md
seguridad: no
es: Generalización adicional recomendada (si procede):
eu: Gomendatutako orokortze osagarria (hala dagokionean):

### propuestas.recomendacion
origen: original
fuente: auditoria.md
seguridad: no
es: Recomendación global:
eu: Gomendio orokorra:

### lista.recomendacion
origen: original
fuente: auditoria.md
seguridad: sí
es: [apto para uso secundario interno / requiere corrección antes de uso / pasar a modo C / fragmentar y reseudonimizar partes / no apto sin revisión humana experta]
eu: [barne-erabilera sekundariorako egokia / erabili aurretik zuzenketa behar du / C modura pasatu / zatiak banatu eta berriro pseudonimizatu / aditu baten giza berrikuspenik gabe ez da egokia]

### encabezado.regenerar
origen: original
fuente: auditoria.md
seguridad: no
es: ### Si quieres regenerar
eu: ### Birsortu nahi baduzu

### regenerar.texto
origen: original
fuente: auditoria.md
seguridad: no
es: Indica explícitamente "regenerar" y el texto se reprocesa aplicando las correcciones detectadas, manteniendo los tokens y el desplazamiento temporal del original (si son recuperables) o introduciendo nuevos (si no).
eu: Esplizituki adierazi «birsortu», eta testua berriz prozesatuko da detektatutako zuzenketak aplikatuz, jatorrizkoaren tokenak eta denbora-desplazamendua mantenduz (berreskuragarriak badira) edo berriak sartuz (ez bada hala).

### encabezado.aviso_traduccion
origen: nuevo
seguridad: sí
es: ## AVISO DE TRADUCCIÓN
eu: ## ITZULPEN-OHARRA (ESPERIMENTALA)

### aviso.traduccion
origen: nuevo
seguridad: sí
es: Marco de esta respuesta traducido por IA, sin revisión humana. Ante cualquier duda sobre una advertencia de seguridad, consulta la versión en español, que es la de referencia.
eu: ADI: euskarazko itzulpen hau ESPERIMENTALA da. Erantzun honen markoa adimen artifizial batek itzuli du, giza berrikuspenik gabe, eta akats larriak izan ditzake. Zalantzarik izanez gero, batez ere segurtasun-oharrei dagokienez, kontsultatu gaztelaniazko bertsioa, hori baita erreferentzia. — AVISO: esta traducción al euskera es EXPERIMENTAL, la ha redactado una IA sin revisión humana y puede contener errores graves. Ante cualquier duda, en especial sobre advertencias de seguridad, consulta la versión en español, que es la de referencia.

### puerta.ficticio
origen: nuevo
seguridad: sí
es: Esto parece un caso ficticio: si ya lo es, no hay nada que seudonimizar. ¿Para qué quieres seudonimizarlo?
eu: Kasu fikziozkoa dirudi: hala bada, ez dago ezer pseudonimizatzeko. Zertarako pseudonimizatu nahi duzu?

### puerta.sin_mediacion
origen: nuevo
seguridad: sí
es: Parece que describes tu propia situación o la de un tercero sin mediación clínica o jurídica. Este skill es para casos ya manejados por un profesional habilitado. ¿Quién interviene profesionalmente en este caso?
eu: Badirudi zure egoera propioa edo hirugarren batena deskribatzen ari zarela, bitartekaritza kliniko edo juridikorik gabe. Skill hau profesional gaitu batek jada kudeatutako kasuetarako da. Nork esku hartzen du profesionalki kasu honetan?

### puerta.modo
origen: nuevo
seguridad: sí
es: Indica el modo: A (clínico), B (jurídico), C (generalización extrema) o audit. No hay modo por defecto.
eu: Adierazi modua: A (kliniko), B (juridiko), C (muturreko orokortzea) edo audit. Ez dago modu lehenetsirik.
