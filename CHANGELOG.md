# Changelog

Todos los cambios relevantes del skill `seudonimizador-clinico-juridico` se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y la numeración aplica [Semantic Versioning](https://semver.org/lang/es/) en su lectura adaptada para skills (mayor = ruptura de comportamiento, menor = ampliación o refuerzo de reglas, parche = correcciones puntuales).

## [1.2] — 2026-05-31

### Motivación

El paquete no se importaba como skill en Perplexity: devolvía `description exceeds maximum length of 1024 characters`. La causa no era el número de caracteres (1006, por debajo del límite) sino que Perplexity mide ese límite **en bytes UTF-8**. Al estar la descripción en español, los caracteres acentuados y la `ñ` ocupan 2 bytes cada uno, elevando el total a 1027 bytes. Claude.ai cuenta caracteres (o aplica un margen mayor), por lo que la importación allí nunca falló y el problema pasó desapercibido.

### Cambiado

- **`SKILL.md` — descripción del frontmatter condensada de 1027 a 912 bytes UTF-8.** Se mantienen el trigger `/seudonimizar`, los cuatro modos (A, B, C, audit), las frases de activación en lenguaje natural y la advertencia RGPD/LOPDGDD. Se reduce el número de ejemplos redundantes y se elimina el marcado Markdown del frontmatter. La lógica del skill no se toca.

### Añadido

- **`README.md` — Opción 2: Perplexity (Skills).** Instalación nativa por `.zip`, paralela a la de Claude.ai, con renumeración de las opciones siguientes (Claude Code → 3, Otras IA → 4) y una nota técnica sobre el límite en bytes UTF-8 para evitar la recaída al editar la descripción.

### Notas

- **No hay cambios de comportamiento.** Una instalación previa en Claude.ai produce salidas idénticas; el salto de versión refleja la ampliación de plataformas soportadas y la documentación nueva, no un cambio de reglas.
- Paquetes `dist/*.zip` y `dist/*.skill` regenerados con el `SKILL.md` corregido.

## [1.1] — 2026-05-11

### Motivación

Tras pruebas en uso real se detectó que el skill, durante la fase de transformación, introducía ocasionalmente matices narrativos, contextualizaciones o inferencias clínicas/jurídicas que no figuraban en el texto original. El parafraseo previsto para *reducir* especificidad estaba *añadiendo* contenido. Una alucinación silenciosa en este skill contamina el razonamiento posterior (clínico, jurídico, didáctico) sin dejar rastro detectable, lo que la hace más grave que la fuga de un identificador residual.

La v1.1 endurece la regla de fidelidad al original como prioridad operativa por encima de cualquier otra transformación.

### Cambiado

- **`flujo.md` — Regla 1 transversal reescrita como prohibición estricta y prioritaria.**
  - Prohíbe explícitamente introducir cualquier dato, síntoma, hecho, fecha, cuantía, argumento, diagnóstico, antecedente, circunstancia procesal o inferencia que no figure literalmente en el texto original.
  - Acota el parafraseo de los pasos 3.4 y 4: solo puede *reducir* especificidad, nunca añadir matices ni "redondear" la narrativa.
  - Regla operativa explícita: ante la duda entre rellenar y omitir, omitir prevalece.
- **`SKILL.md` — Preámbulo reforzado y bump a v1.1.**
  - La sección "Por qué este skill" detalla los marcadores y la regla de omisión preferente.
  - "Para qué sirve" añade el **Control de fidelidad** como cuarto entregable obligatorio de la salida.

### Añadido

- **Marcador `[DATO_ELIMINADO]`** como convención formal para eliminar un dato del original sin sustituirlo (distinto de `[NO_CONSTA]`, que se reserva para datos del original cuya lectura es ambigua).
- **Bloque obligatorio "Control de fidelidad" en el paso 5 de `flujo.md`.** Tras la auditoría de riesgo residual y antes de las decisiones por defecto. Fuerza al modelo a declarar si hay elementos sin correspondencia en el original y a listarlos si los hay. Actúa como auto-control explícito.
- **Comprobación 7 en `auditoria.md` (modo `audit`): fidelidad al original.** Condicional al aporte del texto original junto al seudonimizado. Si no se aporta, se marca `No aplicable` honestamente. Una fuga en esta comprobación escala el nivel de riesgo a `alto` automáticamente.

### Notas

- La instalación del paquete `.skill` queda inalterada: misma estructura, mismo trigger `/seudonimizar`, mismos cuatro modos (`A`, `B`, `C`, `audit`).
- Los marcadores `[DATO_ELIMINADO]` y `[NO_CONSTA]` no aparecen en `plantilla-tokens.md` (que cataloga seudónimos de personas, lugares y entidades) sino que son convenciones del flujo. No requieren actualización del catálogo de tokens.
- Pendiente: validar empíricamente con casos reales si la nueva instrucción reduce las alucinaciones detectadas. Si persisten, considerar añadir un paso 0 de extracción literal de hechos antes de transformar.

## [1.0] — 2026-05-09

### Añadido

- Descriptor inicial del skill con cuatro modos: `A` (clínico), `B` (jurídico), `C` (generalización extrema), `audit` (auditoría de texto ya seudonimizado).
- Flujo operativo de seis pasos con reglas duras transversales.
- Catálogo de tokens con convenciones de etiquetado consistente.
- Protocolo de auditoría con seis comprobaciones y rúbrica de riesgo residual.
- Plantilla de entrada para el usuario.
- Marco normativo en `SKILL.md`: distinción RGPD entre seudonimización (Art. 4.5) y anonimización (Considerando 26).
- Documentación pública: README con tres opciones de instalación (Claude.ai, Claude Code, otras IAs) y guía profesional en PDF.
- Licencia CC BY 4.0.

### Probado

- Caso clínico depresivo con consumo de sustancias (modo A).
- Caso jurídico civil de responsabilidad contractual con cuantías relevantes (modo B).
- Caso jurídico penal con elementos mediáticos para someter el modo C a tensión.

### Pendiente

- Validación con casos reales por profesionales habilitados.
- Pruebas de encadenamiento con `/cie11-formulacion-clinica`, `/dsm-formulacion-clinica` y `/codigo-civil-formulacion-juridica`.
- Calibrado para población infanto-juvenil.
- Catálogo de tokens ampliado para jurisdicción mercantil técnica y casos administrativos complejos.
