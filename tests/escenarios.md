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

**Estado: preparada y todavía sin ejecutar.** Se completará con los resultados, los hallazgos y las decisiones.

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

*(se rellenan al cerrar la ronda)*
