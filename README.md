# Seudonimizador Clínico-Jurídico

Skill de transformación de casos reales clínicos y jurídicos en versiones aptas para uso secundario (estudio, supervisión, formación, redacción didáctica), conservando utilidad analítica y eliminando identificadores directos e indirectos.

**Versión actual: v1.4** ([changelog](CHANGELOG.md))

> **Compatible con [Agent Plugins 1.0.0](https://agent-plugins.org/specification)** — el
> formato portátil de empaquetado de la Agentic AI Foundation (OpenAI, Amazon, Microsoft,
> Cursor y Vercel, con Google como *core maintainer*). El paquete lleva el manifiesto
> portable `plugin.json` en la raíz y el skill en
> `skills/seudonimizador-clinico-juridico/`, así que cualquier cliente conformante lo
> descubre.
>
> **Funciona en ChatGPT.** El skill es texto —protocolo, criterios y plantillas, sin
> ejecución local—, así que se instala desde **Complementos** con **Work** activado y
> funciona igual que en Claude. Su
> frontmatter valida contra el conjunto cerrado de
> [Agent Skills](https://agentskills.io/specification), que es lo que ChatGPT, claude.ai
> y la Skills API exigen para aceptar la subida: una clave de más ahí no se ignora,
> falla con error duro. Están también en el **plan gratuito**, con límites de uso.

> **No anonimiza en sentido fuerte.** Produce textos seudonimizados con generalización dirigida, marcando explícitamente el riesgo residual. No sustituye los procedimientos formales de anonimización exigidos por el RGPD/LOPDGDD para publicación científica, peritaje formal, expediente oficial ni cesión a terceros.

## Qué hace

Recibe un caso real ya manejado por un profesional habilitado y devuelve, en este orden:

1. Apertura con semilla de desplazamiento temporal y mapa rol → token.
2. Texto seudonimizado del caso, en bloque separable.
3. Auditoría de riesgo residual (bajo / medio / alto) con justificación.
4. **Control de fidelidad**: comprobación explícita de que ningún elemento de la salida carece de correspondencia en el original (nuevo en v1.1).
5. Decisiones por defecto (asunciones tomadas por falta de contexto).

## Modos

Sintaxis: `/seudonimizar [modo]` seguido del caso o adjuntando archivo.

- **`A`** (clínico). Psicología o psiquiatría. Conserva sintomatología, exploración, hipótesis diagnósticas, formulación, dinámica transferencial, intervenciones, respuesta.
- **`B`** (jurídico). Civil, penal, laboral o administrativo. Conserva hechos probados, fundamentos de derecho, plazos procesales (desplazados con semilla), tipos delictivos o civiles, lógica argumentativa.
- **`C`** (generalización extrema). Casos mediáticos, figuras públicas, enfermedades raras o combinaciones de muy baja prevalencia donde A o B dejarían riesgo residual alto.
- **`audit`**. Audita un texto ya seudonimizado (por este skill o por otra vía). Devuelve fugas detectadas, riesgo estimado y propuesta de generalización adicional. Desde v1.1 audita también la **fidelidad al original** si se aporta el texto original junto al seudonimizado.

Si no se indica modo, el skill pregunta. No hay modo por defecto: confundir A y B degrada el resultado.

## Novedades v1.1 — refuerzo anti-alucinación

Tras pruebas en uso real, el skill incorporaba ocasionalmente matices o inferencias no presentes en el original durante el parafraseo. Una alucinación silenciosa en este contexto es más grave que un identificador residual: contamina el razonamiento clínico o jurídico sin dejar rastro detectable. La v1.1 endurece tres puntos:

- **Regla 1 transversal reescrita como prohibición estricta y prioritaria** sobre cualquier otra transformación. Si una generalización o parafraseo introdujera información nueva, se abandona la transformación antes que inventar.
- **Nuevo marcador `[DATO_ELIMINADO]`** para eliminar un dato sin sustituirlo. Convive con `[NO_CONSTA]`, que se reserva para datos del original cuya lectura es ambigua.
- **Bloque "Control de fidelidad"** obligatorio en la salida y **comprobación 7** en el modo `audit`.

Detalle completo en [CHANGELOG.md](CHANGELOG.md).

## Instalación

### Opción 1 — Claude.ai (recomendada para uso conversacional)

1. Descarga **[`seudonimizador-clinico-juridico.zip`](https://github.com/novanoticia/seudonimizador-clinico-juridico/releases/latest/download/seudonimizador-clinico-juridico.zip)**.
2. En Claude.ai, ve a **Ajustes → Capacidades → Skills**.
3. Asegúrate de que **Code execution and file creation** está activado.
4. Pulsa **Subir skill** (o *Upload skill*).
5. Selecciona el archivo `.zip` descargado.
6. El skill aparece en tu lista de Skills, activado por defecto.

A partir de ese momento, el skill se invoca con `/seudonimizar` seguido del modo (`A`, `B`, `C`, `audit`) en cualquier conversación. **Recomendado**: hazlo en una **Conversación Temporal** para minimizar la huella de los datos sensibles.

> El archivo equivalente **[`seudonimizador-clinico-juridico.skill`](https://github.com/novanoticia/seudonimizador-clinico-juridico/releases/latest/download/seudonimizador-clinico-juridico.skill)** es el mismo paquete con extensión alternativa, presente para compatibilidad con marketplaces de terceros. Ambos están en la página de [Releases](https://github.com/novanoticia/seudonimizador-clinico-juridico/releases/latest). Para Claude.ai usa directamente el `.zip`.

### Opción 2 — ChatGPT (Complementos)

ChatGPT instala este repositorio como **complemento**, sin descargar nada ni
reempaquetar.

1. Abre ChatGPT y **activa `Work` en el selector**.
2. Ve a **Complementos** (*Plugins*).
3. Busca el complemento por nombre, o **añádelo desde URL** con la de este
   repositorio:
   ```
   https://github.com/novanoticia/seudonimizador-clinico-juridico
   ```

Se invoca igual que en Claude: `/seudonimizar` seguido del modo (`A`, `B`, `C`, `audit`).

> Funciona también en el **plan gratuito**, con límites de uso.
>
> Que la instalación sea desde la URL del repositorio, y no subiendo un zip, es
> posible porque el repo es un plugin conforme a
> [Agent Plugins 1.0.0](https://agent-plugins.org/specification): lleva el
> `plugin.json` portable en la raíz y el skill en `skills/seudonimizador-clinico-juridico/`. El paquete de
> Para las plataformas que sí piden un zip, el paquete se descarga desde la
> sección [Releases](https://github.com/novanoticia/seudonimizador-clinico-juridico/releases/latest)
> (no se versiona dentro del repositorio).

### Opción 3 — Perplexity (Skills)

Perplexity admite el mismo paquete de skill que Claude.ai, sin necesidad de pegar texto.

1. Descarga **[`seudonimizador-clinico-juridico.zip`](https://github.com/novanoticia/seudonimizador-clinico-juridico/releases/latest/download/seudonimizador-clinico-juridico.zip)**.
2. En Perplexity, entra en la gestión de **Skills** y elige **subir / importar skill**.
3. Selecciona el archivo `.zip` descargado.
4. El skill se invoca igual que en Claude: `/seudonimizar` seguido del modo (`A`, `B`, `C`, `audit`).

> **Nota técnica:** el límite de longitud del campo `description` depende de la plataforma: Perplexity valida **en bytes UTF-8** (límite 1024) y Mistral **en caracteres** (límite 500). En español, las vocales acentuadas y la `ñ` ocupan 2 bytes cada una. La descripción de este skill mide **455 caracteres / 468 bytes**, dentro de ambos umbrales. Si la editas, no superes los **500 caracteres** para conservar la compatibilidad con Mistral.

### Opción 4 — Mistral AI (Skills)

Mistral admite Skills en su espacio **Work**, a partir de la carpeta del skill descomprimida.

1. Descarga **[`seudonimizador-clinico-juridico.zip`](https://github.com/novanoticia/seudonimizador-clinico-juridico/releases/latest/download/seudonimizador-clinico-juridico.zip)** y **descomprímelo**.
2. En Mistral AI, dentro del espacio **Work**, abre la sección de **Skills**.
3. Selecciona la **carpeta** resultante (`seudonimizador-clinico-juridico/`, la que contiene `SKILL.md`).
4. Se invoca igual que en las demás plataformas: `/seudonimizar` seguido del modo (`A`, `B`, `C`, `audit`).

### Opción 5 — Claude Code (línea de comandos)

```bash
# Skills personales (disponibles en cualquier proyecto)
mkdir -p ~/.claude/skills
cd ~/.claude/skills
unzip /ruta/a/seudonimizador-clinico-juridico.zip

# O bien, skills del proyecto actual
mkdir -p .claude/skills
cd .claude/skills
unzip /ruta/a/seudonimizador-clinico-juridico.zip
```

Claude Code lo detecta automáticamente; se invoca igual que en la app: `/seudonimizar [modo]`.

### Opción 6 — Como plugin (Claude Code y Cowork)

Desde la v1.4 el repositorio también es un **plugin** conforme a
[Agent Plugins 1.0.0](https://agent-plugins.org/specification), el formato
portátil de la Agentic AI Foundation. Eso permite instalarlo entero en vez de
copiar la carpeta del skill:

```bash
# Probarlo sin instalar
claude --plugin-dir /ruta/al/repo

# O clonar e instalar desde el repositorio
git clone https://github.com/novanoticia/seudonimizador-clinico-juridico
claude --plugin-dir ./seudonimizador-clinico-juridico
```

En Cowork: comprime la **raíz del repositorio** (donde están `plugin.json`,
`.claude-plugin/` y `skills/`) y súbela en *Customize → Plugins → Upload*.

Invocado como plugin, el comando queda namespaced:
`/seudonimizador-clinico-juridico:seudonimizador-clinico-juridico`. Si prefieres
el `/seudonimizar` corto, usa la Opción 5.

### Opción 7 — Otras inteligencias artificiales

El skill es texto Markdown. Cualquier asistente conversacional capaz de seguir instrucciones extensas puede aplicarlo, pegándolo como prompt inicial.

1. Abre una conversación efímera o temporal:
   - **ChatGPT**: *Temporary Chat*.
   - **Mistral LeChat**: conversación efímera.
   - **Google Gemini**: chat temporal cuando esté disponible.
   - **LLM local** (Ollama, LM Studio): cualquier sesión nueva.
2. Pega como primer mensaje el contenido concatenado de:
   - `SKILL.md`
   - `flujo.md`
   - `plantilla-tokens.md`
   - `auditoria.md` (si vas a usar el modo `audit`)
3. Añade al final: *«Sigue este protocolo. Espera mi caso.»*
4. Invoca con `/seudonimizar [modo]` o describe el modo en lenguaje natural si la IA no soporta comandos de barra.

> **Avisos por plataforma:**
> - **Meta AI en WhatsApp**: no recomendado para casos sensibles por la integración con la cuenta del usuario y la falta de modo temporal verificable.
> - **Modelos pequeños** (≤ 7B parámetros): tienden a omitir identificadores indirectos y a inventar más durante el parafraseo. Prefiere modelos de razonamiento de tamaño medio o grande.
> - **El modo `audit`** puede aplicarse a textos producidos por cualquier IA, idealmente con un modelo distinto del que generó la seudonimización original.

## Modo recomendado de uso

Independientemente de cómo lo instales:

1. **Activa Conversación Temporal o equivalente** antes de pegar nada sensible.
2. **Pasa un caso por vez**. Mezclar casos en una sola sesión aumenta el riesgo de fugas cruzadas entre tokens.
3. **Verifica el mapa rol → token** antes de aceptar el resultado. Es la fase donde más se cuela algún nombre o entidad real.
4. **Comprueba el bloque "Control de fidelidad"** (nuevo en v1.1). Si el skill declara divergencias, regenera el texto antes de usarlo.
5. **Archiva o destruye el mapa de tokens aparte** del texto transformado. El RGPD Art. 4.5 exige que la información que permite reidentificar se conserve separadamente. El skill entrega el mapa en bloque separable; la separación efectiva depende del usuario.
6. **No publiques, no peritries ni incorpores a expediente oficial** un texto seudonimizado por este skill sin revisión humana experta adicional. La auditoría de riesgo residual es estimación cualitativa, no certificación.

## Encadenamiento con otros skills

El seudonimizador es la primera etapa natural de un flujo profesional con LLM:

- `/seudonimizar A` → `/cie11-formulacion-clinica`: caso clínico transformado y formulado.
- `/seudonimizar A` → `/dsm-formulacion-clinica`: misma cadena con el otro nomenclador.
- `/seudonimizar B` → `/codigo-civil-formulacion-juridica`: caso jurídico civil transformado y formulado.

La separación del mapa rol → token debe hacerse **antes** de pasar el texto seudonimizado al siguiente skill.

## Marco normativo

El RGPD distingue dos figuras:

- **Seudonimización (Art. 4.5 RGPD).** El dato no puede atribuirse a un interesado sin información adicional, conservada por separado. Sigue siendo dato personal. Requiere medidas técnicas y organizativas.
- **Anonimización (Considerando 26 RGPD).** El dato no puede vincularse a un interesado por ningún medio razonable. Deja de ser dato personal.

Lo que produce este skill es **seudonimización con generalización dirigida**. Aproxima la anonimización funcional para uso secundario interno (supervisión, formación), pero **no es anonimización en sentido jurídico** y **no autoriza por sí solo** a publicar el caso, incorporarlo a un peritaje, ni difundirlo.

## Para qué NO sirve

- Anonimización conforme al Considerando 26 RGPD para publicación científica, peritaje formal, expediente oficial o cesión a terceros.
- Casos ficticios sin valor formativo: si ya es ficticio, no hay nada que seudonimizar.
- Procesamiento de datos identificables sin valor secundario claro.
- Sustitución del juicio profesional sobre qué partes del caso son sensibles y por qué.
- Ofuscación intencional de hechos relevantes para una causa o un cuadro clínico.

## Documentación

El skill vive en `skills/seudonimizador-clinico-juridico/`, siguiendo la
estructura de [Agent Plugins 1.0.0](https://agent-plugins.org/specification).

- **[SKILL.md](skills/seudonimizador-clinico-juridico/SKILL.md)** — descriptor formal del skill.
- **[flujo.md](skills/seudonimizador-clinico-juridico/flujo.md)** — flujo operativo de seis pasos con reglas duras transversales.
- **[plantilla-entrada.md](skills/seudonimizador-clinico-juridico/plantilla-entrada.md)** — guía de formato de entrada para el usuario.
- **[plantilla-tokens.md](skills/seudonimizador-clinico-juridico/plantilla-tokens.md)** — catálogo de roles y convenciones de etiquetado.
- **[auditoria.md](skills/seudonimizador-clinico-juridico/auditoria.md)** — protocolo del modo `audit` y rúbrica de riesgo residual.
- **[CHANGELOG.md](CHANGELOG.md)** — historial de versiones.
- **[docs/](docs/)** — guía profesional en PDF (si está disponible).

## Limitaciones conocidas

- Ámbito calibrado para España (RGPD, LOPDGDD, terminología procesal y sanitaria). Otros marcos jurídicos requieren ajustes.
- No detecta automáticamente identificadores en imágenes, audio o vídeo. Solo texto.
- La auditoría de riesgo residual es estimación cualitativa, no garantía formal.
- La regla anti-alucinación de v1.1 reduce el riesgo de invención durante el parafraseo, pero no lo elimina por completo: las instrucciones explícitas en prompts tienden a funcionar, pero no son blindaje absoluto contra la alucinación en LLMs. Conviene auditar la salida con el modo `audit` cuando el caso es delicado.
- El mapa rol → token se entrega en la misma respuesta que el texto transformado. La separación efectiva (RGPD Art. 4.5) depende de que el usuario archive o destruya el mapa aparte.

## Licencia

[CC BY 4.0](LICENSE) — Creative Commons Attribution 4.0 International.

Puedes usar, modificar y redistribuir el skill, incluso comercialmente, siempre que cites la autoría y enlaces a este repositorio.

## Atribución y nota ética

Este skill ha sido desarrollado con asistencia de IA (Claude, de Anthropic) en iteración con un usuario profesional. La estructura, las reglas duras, el catálogo de tokens y el protocolo de auditoría reflejan decisiones humanas tomadas en respuesta a casos de prueba reales. El uso del skill **requiere revisión humana experta** en cada aplicación, y no sustituye los procedimientos formales de anonimización exigidos por el marco normativo vigente.
