# Escenarios de simulación y registro de ejecuciones

## Qué es esto, y qué no

- Es una **simulación** con subagentes de contexto limpio: cada uno recibe solo el paquete instalado y un
  mensaje de usuario, y responde como lo haría un asistente con el skill. **No es una plataforma real.**
  Lo que salga aquí no se puede extrapolar a Claude.ai, ChatGPT, Perplexity, Mistral ni a otro modelo.
- **Límite metodológico:** los simuladores **no están aislados a nivel de sistema**. Compartían máquina con el
  repositorio y podían leer ficheros fuera del paquete. Se les ordenó no hacerlo y cada uno declara los ficheros
  que leyó, pero esa lista es una **autodeclaración, no verificada**.
- Los **criterios de éxito se preregistraron** en `tests/simulacion_escenarios.py` antes de lanzar ningún
  simulador, y cada criterio lleva un ejemplo que debe pasar y otro que debe fallar (lo exige
  `tests/test_simulacion.py`). El evaluador es `tools/evaluar_simulacion.py`. Evalúa solo lo que se pudo
  preregistrar de forma mecánica: **leer las respuestas y las notas de los simuladores sigue siendo necesario**.
- **Todos los casos son ficticios** (nombres, NIF, autos, teléfonos y fechas inventados).
- Una respuesta que cumple los criterios no demuestra que el skill sea correcto, solo que ese simulador, ese día,
  hizo lo previsto. Una respuesta que los incumple es un hallazgo.

## Cómo repetir una ronda

```bash
bash scripts/build-dist.sh                       # genera dist/ (no se versiona)
# descomprimir el .zip en una carpeta limpia y crear, aparte, una copia con SOLO SKILL.md (escenario S7)
# lanzar un subagente por escenario con instrucciones_del_simulador(...) de tests/simulacion_escenarios.py
python3 tools/evaluar_simulacion.py <carpeta con S1.respuesta.md … S10.respuesta.md>
```

## Escenarios

### S1
**Idioma explícito (`en`), modo A.** Caso clínico ficticio en castellano. Se espera el marco en inglés con los
encabezados del catálogo, los tokens sin traducir, el texto seudonimizado **en castellano** sin ningún
identificador original, la dosis y la escala conservadas y el aviso de traducción al final. Mensaje:
`/seudonimizar A en`.

### S2
**Idioma explícito (`ca`), modo B.** Caso jurídico ficticio en castellano. Marco en catalán, tokens jurídicos
sin traducir, cuantías en rangos, aviso en catalán.

### S3
**Idioma explícito (`eu`, experimental), modo A.** Marco en euskera y **advertencia reforzada bilingüe**
(`ESPERIMENTALA`, ` — AVISO: ` y la mitad en español).

### S4
**Código desconocido (`xx`).** Avisa en español de que no está disponible, lista los idiomas disponibles y
continúa en español, sin ningún encabezado ni aviso de otro idioma.

### S5
**Sin código (línea base).** Comportamiento por defecto: marco en español, sin aviso de traducción, sin mención
a idiomas ni catálogos.

### S6
**Falta el modo (`/seudonimizar en`).** Se espera que pregunte el modo **en inglés** y se detenga, sin procesar nada.

### S7
**Solo se cargó `SKILL.md` (sin catálogos), con `fr`.** El fallo seguro: responde en español, dice que la
traducción no está disponible, añade la línea multilingüe de respaldo y **no inventa** el marco en francés.

### S8
**Modo `audit` con idioma explícito (`gl`)** sobre un texto con fugas (nombre y teléfono). Marco en gallego, la
fuga directa detectada (comprobación 1 = Fallo) **sin reproducir** el nombre ni el teléfono, aviso en gallego.

### S9
**El caso empieza en la misma línea** (`/seudonimizar B en 2023 el demandante…`). `en` **no** es un código de
idioma (la primera línea no tiene exactamente tres elementos): comportamiento por defecto en español.

### S10
**Puerta de entrada con idioma (`fr`):** el usuario describe su propia situación sin mediación profesional. Se
espera que pregunte **en francés** por la mediación y se detenga, sin procesar el caso.

## Ronda 1

**Estado: ejecutada** (10 simuladores de contexto limpio, uno por escenario; S7 con un paquete que solo
contiene `SKILL.md`). Es una simulación, **no una plataforma real**.

**Resultado automático (criterios preregistrados):** 191 de 192 criterios pasan; ningún crítico falla. El único
fallo (S5, deseable, «no menciona idiomas ni catálogos») era un **falso positivo del criterio**: la respuesta
decía «el token del catálogo» (el catálogo de tokens del skill, no de idiomas). Se corrigió el criterio
**después de ver el resultado** (cambio posterior, no preregistrado), y su ejemplo OK/KO lo comprueba.

**Hallazgos de los simuladores (leyendo respuestas y notas) y decisión:**

| Hallazgo | Escenarios | Decisión |
|---|---|---|
| Sin salida estructurada (pregunta de puerta) no había dónde poner el aviso de traducción | S6, S10 | Corregido: el aviso se añade también tras una pregunta de puerta. Test añadido antes del cambio. |
| El aviso de código desconocido se colocó como «comentario adicional» al final | S4 | Corregido: va al principio, antes de `## APERTURA`. |
| El texto libre del marco (justificaciones) lo genera el modelo en el momento y no lo ha revisado nadie | S3 y otros | Declarado en flujo.md, README, CHANGELOG, texto de la Release y estado de traducciones. |

**Revisión independiente de la rama** (un subagente con instrucciones de solo lectura, mutantes sobre una copia):
0 críticos, 7 importantes, 9 menores. Corregidos con test previo: I1 (forma de la primera línea, también de dos
elementos), I2 (el idioma lo decide cada invocación), I3 (regla 4 y alcance de la precedencia), I4 (listas
`lista.*` y veredictos traducidos), I6 (aviso en puertas, ver arriba), I7 (mutantes no detectados: locale, carga del
catálogo, puertas truncadas). I5 (euskera, interrogativa negativa) **no se cambia**: es un riesgo señalado, no un
error confirmado, y alterar la polaridad cambiaría el contrato con el original; queda anotado como pendiente de
revisión nativa.

**Límites de esta ronda:** el revisor y los simuladores son modelos: no equivalen a una revisión humana.

## Ronda 2

**Estado: ejecutada** sobre el paquete reconstruido con los arreglos de la ronda 1 (`bash scripts/build-dist.sh`,
paquete completo), solo en los escenarios afectados: S1, S4, S6 y S10. Cuatro simuladores nuevos de contexto
limpio; cada uno declara haber leído solo ficheros del paquete (autodeclaración, no verificada). Simulación, **no
plataforma real**. No se cambió ningún criterio entre la ronda 1 y la 2.

**Resultado automático:** S1 23/23, S4 41/41, S6 8/8, S10 8/8; ningún criterio falla.

**Lo que se comprobó leyendo las respuestas:**
- S4: el aviso de código desconocido sale en la primera línea, antes de `## APERTURA`, y el resto continúa en español.
- S6 y S10: la pregunta de puerta sale en el idioma pedido (inglés, francés), la respuesta se detiene ahí y lleva
  al final el aviso de traducción, que en la ronda 1 faltaba.
- S1: marco en inglés, texto del caso en castellano, tokens y marcadores sin traducir, aviso al final.

**Lo que no demuestra:** un solo simulador por escenario, un solo día. Que 4 de 4 hagan lo previsto no mide la
variabilidad entre ejecuciones ni entre modelos.

**Observaciones nuevas de los simuladores (pendientes, no se tocan):**
- S10: `puerta.sin_mediacion` pregunta quién interviene profesionalmente aunque el usuario ya ha dicho que nadie;
  el skill no dice si hay que ofrecer una orientación. Es el comportamiento del original (puerta de entrada),
  traducido; cambiarlo alteraría el español.
- S1: en el control de fidelidad, con respuesta «no», el simulador escribió «not applicable» como texto libre
  (la plantilla no dice si se omite).
- Reiteradas de la ronda 1: fechas solo con mes, token del centro de salud mental en localidad pequeña,
  `[CONVIVIENTE_A]`, orden de APERTURA y MAPA.

## Ejecuciones en plataformas reales

Ninguna se ha hecho. Esta tabla es para que las anotes tú (o quien las haga) cuando ocurran. **Sin una fila con
resultado, el comportamiento con idiomas distintos del español no está comprobado en esa plataforma.**

| Plataforma | Modelo | Fecha | Escenario | Resultado | Notas |
|---|---|---|---|---|---|
| Claude.ai | pendiente | pendiente | S1, S4, S5, S7 | pendiente | |
| ChatGPT (Complementos) | pendiente | pendiente | S1, S4, S5, S7 | pendiente | |
| Perplexity | pendiente | pendiente | S1, S4, S5, S7 | pendiente | |
| Mistral AI | pendiente | pendiente | S1, S4, S5, S7 | pendiente | |
| Claude Code | pendiente | pendiente | S1, S4, S5, S7 | pendiente | |

## Pendientes menores

- Claves de catálogo para las puertas de `auditoria.md` y la de finalidad secundaria de `SKILL.md` (hoy las redacta
  el modelo): añadiría frases de seguridad nuevas, sin revisar, en seis idiomas. (I6, parte restante)
- Euskera: `fidelidad.pregunta` como interrogativa negativa. Revisión nativa. (I5)
- Menores de la revisión: «regenerate» en conversaciones fr/ca (M4); si el aviso se repite al iterar (M5);
  `i18n-es.md` viaja en el paquete aunque no se carga y `build-dist.sh` copia cualquier `.md` nuevo (M6); las
  pruebas dependen de git con historial completo (M7, el CI lo cubre); workflow duplica `push`/`pull_request`,
  acciones fijadas por etiqueta y una prueba tautológica (M8); README «v1.5» y enlaces `releases/latest` hasta que
  haya Release, y CHANGELOG con dos secciones sin publicar (M9); exención de tokens en comprobación 6 solo con
  código (M3); casos como `pt-BR` o código vacío (M2).
- Ambigüedades **ya presentes en el original** que los simuladores señalaron y no se tocan (alteran el skill en
  español): fechas solo con mes, token para pueblos pequeños, dos formatos de línea del mapa, orden APERTURA/MAPA,
  rúbrica de riesgo, amplitud de rangos, `[CONVIVIENTE_A]`, elección de token en derivaciones.
