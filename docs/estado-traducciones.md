# Estado de las traducciones

Este registro dice, idioma por idioma, **quién ha escrito y quién ha revisado** cada
traducción del marco del skill. Una prueba automática (`tests/test_catalogos_traducidos.py`)
comprueba que cada fila coincide con la cabecera de su catálogo `i18n-<código>.md`: si
alguien revisa un catálogo y no actualiza esta tabla, el CI lo avisa.

**Ninguna traducción está revisada por una persona.** Las ha redactado una IA. Contienen
texto de seguridad y de contenido clínico y jurídico, y no deben presentarse como
revisadas hasta que lo estén.

## Catálogos

| Idioma | Código | Estado | Redactado por | Revisado por | Fecha de revisión | Notas |
|---|---|---|---|---|---|---|
| Inglés | en | borrador-ia-sin-revision-humana | IA | nadie | — | Ortografía británica. `pseudonymisation` consta en el art. 4(5) del RGPD y en el título de las directrices del CEPD (comprobado por búsqueda; ver «Límites de la verificación»). |
| Francés | fr | borrador-ia-sin-revision-humana | IA | nadie | — | Prioridad clínica. Registro «vous» y tipografía francesa. `pseudonymisation`, `table de correspondance` y `risque résiduel` comprobados por búsqueda (ver «Límites de la verificación»). |
| Catalán | ca | borrador-ia-sin-revision-humana | IA | nadie | — | Prioridad jurídica. Tuteo, como el original. El catalán no es lengua oficial de la UE: no hay RGPD oficial en catalán (hecho conocido, **no comprobado**). `pseudonimització`, `risc residual` y `llavor` son elección de la IA. |
| Gallego | gl | borrador-ia-sin-revision-humana | IA | nadie | — | Prioridad jurídica. Tuteo, como el original. Diez entradas coinciden con el español (`invariable: sí`). No hay RGPD oficial en gallego (hecho conocido, **no comprobado**). `pseudonimización`, `risco residual` y `semente` son elección de la IA; la RAG admite también la grafía con `seudo-`. |
| Euskera | eu | experimental-ia-sin-revision-humana | IA | nadie | — | Prioridad jurídica. **Advertencia reforzada**: el aviso final es bilingüe (euskera + español) y más fuerte que el de los demás idiomas. El de mayor riesgo de error de los cinco. Trato de respeto (zuka). Términos elegidos por la IA, sin fuente oficial (ver «Límites de la verificación»). |

El español (`es`) es la **referencia**: se genera del original con
`python3 tools/extraer_es.py escribir` y no se traduce ni se revisa aquí.

## Límites de la verificación de términos

Los nombres oficiales (RGPD) y los términos de la CNIL se comprobaron **por búsqueda web**,
cuyos resúmenes **no son texto literal**: en una ocasión el buscador escribió «pseudonymization»
(grafía americana) al parafrasear el considerando 26, que no es la oficial. **EUR-Lex no es
accesible desde el entorno de desarrollo** (lo bloquea el proxy de salida), así que ningún
término se ha comprobado abriendo el texto oficial. Quien revise debería contrastar al menos
`pseudonymisation` / `pseudonymisation` (art. 4(5)) y `risque résiduel` / `residual risk`
directamente en EUR-Lex.

**Novedad de la tarea 7 sobre el acceso a EUR-Lex.** Tras permitir `eur-lex.europa.eu` en la
red del entorno, el sitio responde HTTP 202 con la cabecera `x-amzn-waf-action: challenge`: sirve
un **desafío anti-bots** (cuerpo vacío) a clientes que no son un navegador. No se ha intentado
eludirlo. `publications.europa.eu`, `cnil.fr` y `edpb.europa.eu` siguen sin estar permitidos.
Los términos continúan **sin comprobar en el texto oficial**.

## Estados

- `pendiente`: aún no existe el catálogo.
- `borrador-ia-sin-revision-humana`: redactado por una IA; nadie lo ha leído con
  criterio de traductor ni de especialista.
- `experimental-ia-sin-revision-humana`: lo mismo, **más** un riesgo de error alto y difícil de
  detectar por heurística (idioma sin vocabulario compartido con el español, terminología poco
  estandarizada). Va acompañado de una **advertencia reforzada** en la propia salida. No debe
  presentarse como una traducción utilizable sin revisión; es el estado de `eu`.
- `revisado`: una persona lo ha revisado. Exige nombre del revisor y fecha en la
  cabecera del catálogo y en esta tabla.

## Otros textos redactados por IA y sin revisar (fuera de los catálogos)

- La **línea de respaldo multilingüe** de `SKILL.md` (en, fr, ca, gl, eu): traducciones de
  «Traducción no disponible: respondo en español».
- Las cinco entradas `nuevo` de la referencia en español: `aviso.traduccion`,
  `encabezado.aviso_traduccion` y las tres preguntas `puerta.ficticio`,
  `puerta.sin_mediacion` y `puerta.modo`. Están redactadas por IA; con el idioma por
  defecto no se emiten.
- La **selección de las frases marcadas `seguridad: sí`** (diez extraídas del original y las
  cinco `nuevo`) es un criterio de la IA. Conviene que lo confirme una persona.
- La **clasificación** de qué es literal y qué es instrucción en las plantillas
  (`tools/extraer_es.py`).

## Cómo revisar un catálogo

1. Empieza por las entradas con `seguridad: sí`: son las que, mal traducidas, podrían
   degradar una salvaguarda (invertir un nivel de riesgo o un veredicto, aflojar la
   separación del mapa, el control de fidelidad, las preguntas de las puertas).
2. Corrige el catálogo a mano (la columna del idioma; la columna `es` no se toca).
3. Cambia en la cabecera `estado: revisado`, `revisado-por: <nombre>` y
   `fecha-revision: AAAA-MM-DD`.
4. Actualiza la fila de esta tabla con los mismos valores.
5. Ejecuta `python3 -m unittest discover -s tests` y
   `python3 tools/validar_i18n.py`.

## Perfil de revisor necesario

- **en**, **fr**: alguien con inglés o francés clínico (para el marco de la salida basta con
  revisar las frases de seguridad).
- **ca**, **gl**, **eu**: hablante nativo con formación jurídica o sanitaria. Para `eu` es
  **imprescindible** antes de usarlo con casos reales: ninguna prueba automática puede
  detectar un error de traducción en euskera.
- Riesgo señalado por la revisión independiente (no confirmado como error): en `eu`, la pregunta de fidelidad
  (`fidelidad.pregunta`) es una interrogativa negativa con respuesta `bai / ez`, forma que puede ser ambigua en
  euskera; su inversión escondería una invención. No se ha cambiado la polaridad (alteraría el contrato con el
  original en español). Pendiente de revisión nativa.
- Las preguntas de puerta de `auditoria.md` y la de finalidad secundaria de `SKILL.md` no tienen clave de
  catálogo: el modelo las redacta en el momento, sin revisar (ver «texto libre» en el README).

---
*Elaborado con asistencia de IA; requiere revisión humana.*
