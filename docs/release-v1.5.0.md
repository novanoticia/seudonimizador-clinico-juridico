# v1.5.0 — Idioma de la respuesta (en, fr, ca, gl, eu): traducciones de IA sin revisar

Seudonimizador clínico-jurídico: skill que seudonimiza casos clínicos (psicología/psiquiatría) y jurídicos para estudio, supervisión o formación, conservando la utilidad analítica y eliminando los identificadores directos. Se invoca con `/seudonimizar` seguido del modo (`A` clínico, `B` jurídico, `C` generalización extrema, `audit`).

> ⚠️ **No sustituye la anonimización formal** que exigen el RGPD y la LOPDGDD para publicación, peritaje o expediente. Úsalo preferentemente en una conversación temporal y nunca con datos reales sin base legal.

## Qué trae esta versión

### Añadido
- **Idioma de la respuesta.** Un código de idioma tras el modo, en la primera línea y con el caso en la línea siguiente: `/seudonimizar A en`. Idiomas: `en`, `fr`, `ca`, `gl` y `eu`. Sin código, todo funciona exactamente como antes, en español.
- **Catálogos de traducción** `i18n-<código>.md` (uno por idioma) y la referencia `i18n-es.md`. Un idioma nuevo es un fichero más: no hay que editar `SKILL.md`.
- **Aviso de traducción** al final de la salida, solo cuando el idioma no es el español.
- Verificación automática (pruebas, validador de catálogos, comparación con la línea base) y un CI en GitHub Actions.

### Cambiado
- Solo **adiciones** delimitadas en `SKILL.md`, `flujo.md` y `auditoria.md`: 40 líneas añadidas y 0 eliminadas. El frontmatter y la `description` no se tocan.
- Los paquetes de esta Release incluyen los catálogos de idioma.

### Sin cambios
- El comportamiento en español: la salida por defecto es idéntica a la de la versión anterior.

## Estado real de las traducciones (léelo antes de usarlas)

**Ninguna de las traducciones ha sido revisada por una persona.** Las ha redactado una IA y contienen frases de seguridad y de contenido clínico y jurídico.

- `en`, `fr`, `ca` y `gl`: **borradores de IA, sin revisión humana**.
- `eu` (euskera): **experimental**. Es el idioma de mayor riesgo de error y ninguna comprobación automática puede detectarlo; su aviso final es más fuerte y bilingüe (euskera y español). Revisión por una persona nativa **imprescindible** antes de usarlo con casos reales.
- **No se ha ejecutado el skill con un idioma distinto del español en ninguna plataforma real.** Lo verificado es automático (pruebas y validadores), no el comportamiento de un modelo.
- Los términos oficiales (RGPD) se comprobaron por búsqueda web, **no** en el texto oficial de EUR-Lex, que no era accesible desde el entorno de desarrollo.
- Si la plataforma carga **solo `SKILL.md`** y no los catálogos, el skill responde en español y lo dice: no inventa la traducción.
- Los tokens (`[PACIENTE_A]`…) y los marcadores `[DATO_ELIMINADO]` y `[NO_CONSTA]` no se traducen: en un caso en otro idioma verás palabras españolas entre corchetes.

El detalle, idioma por idioma, está en [docs/estado-traducciones.md](https://github.com/novanoticia/seudonimizador-clinico-juridico/blob/main/docs/estado-traducciones.md).

## Si ya tienes el paquete antiguo (v1.4.0 o anterior)

El paquete antiguo **no contiene los catálogos**: con él, pedir un idioma no hace nada. **Reinstala** el paquete de esta Release sustituyendo el anterior por completo (no basta con copiar unos pocos ficheros).

## Archivos de esta Release

| Archivo | Para qué sirve |
|---|---|
| `seudonimizador-clinico-juridico.zip` | Claude.ai, Perplexity, Mistral y Claude Code (descomprimir). |
| `seudonimizador-clinico-juridico.skill` | Mismo paquete con extensión alternativa, para marketplaces de terceros. |

Ambos archivos son idénticos en contenido. Instrucciones de instalación por plataforma en el [README](https://github.com/novanoticia/seudonimizador-clinico-juridico#instalación). Detalle completo de los cambios en el [CHANGELOG.md](https://github.com/novanoticia/seudonimizador-clinico-juridico/blob/main/CHANGELOG.md).

---
*Nota ética: este texto ha sido elaborado con asistencia de IA y requiere revisión humana.*
