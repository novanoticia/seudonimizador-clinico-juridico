# flujo.md — Seudonimizador clínico-jurídico

Flujo operativo de seis pasos. Aplica para los modos `A`, `B` y `C`. Para el modo `audit`, ver `auditoria.md`.

## Reglas duras transversales

Aplican en todos los modos y en todos los pasos.

1. **No inventar — prohibición estricta.** No introduzcas ningún dato, síntoma, hecho, fecha, cuantía, argumento, diagnóstico, antecedente, circunstancia procesal ni inferencia clínica o jurídica que no figure literalmente en el texto original. Esta prohibición opera por encima de cualquier otra regla del flujo: si una transformación (desplazamiento temporal, generalización, parafraseo) introdujera información nueva, abandona la transformación antes que inventar.
   - Si necesitas eliminar un dato sin sustituirlo (porque identifica y no admite generalización), usa el marcador `[DATO_ELIMINADO]`.
   - Si un dato aparece en el original pero no se entiende o es ambiguo, usa `[NO_CONSTA]` o trasládalo al apartado de decisiones por defecto.
   - Ante la duda entre rellenar y omitir: **omite**. Una laguna explícita es mejor que un dato fabricado.
   - El parafraseo (paso 3.4 y paso 4) solo puede *reducir* especificidad. Nunca puede añadir matices, contextualizar con información no presente, ni "redondear" la narrativa.
2. **No suavizar.** Si un hecho es duro (autolesión, violencia, gravedad procesal), se mantiene literal en su contenido aunque se transformen sus identificadores. Suavizar sería adulterar el caso.
3. **Consistencia absoluta.** El mismo sujeto, lugar o entidad recibe siempre el mismo token. El mismo desplazamiento temporal se aplica a todas las fechas.
4. **Separabilidad del mapa.** El mapa rol→token se entrega como bloque separado, encabezado `## MAPA — archivar o destruir aparte del texto`. Es la "información adicional" que el RGPD pide custodiar separadamente.
5. **Sin metadatos involuntarios.** No conservar nombres de archivo originales, encabezados institucionales, firmas digitales ni cualquier rastro técnico que permita reidentificación.
6. **Lengua.** Responde en español salvo que el caso esté en otro idioma; en ese caso, transformación en idioma original y notas en español.

## Puerta de entrada

Antes del paso 1, verifica:

- ¿Es un caso real con valor secundario claro (estudio, supervisión, formación)? Si es ficticio, detente y pregunta para qué se quiere seudonimizar.
- ¿Hay mediación profesional habilitada? Si el usuario describe su propia situación o la de un tercero sin mediación clínica/jurídica, detente y pregunta.
- ¿Modo declarado? Si no hay `A`, `B` o `C`, detente y pregunta. No asumas.

Si las tres puertas pasan, sigue al paso 1.

## Paso 1 — Apertura y semilla

Antes de transformar nada, devuelve:

```
## APERTURA

- Modo: [A | B | C]
- Semilla de desplazamiento temporal: +N días (entero entre 30 y 180, elegido por ti)
- Justificación de la semilla: [breve, p. ej. "evita coincidencia con desfase trivial de un mes"]
- Preguntas críticas previas: [si detectas ambigüedad o falta de datos clave, aquí; si no, "ninguna"]
```

No avances al paso 2 hasta haber declarado la semilla.

## Paso 2 — Detección de identificadores

Identifica internamente (no hace falta listarlos en la salida) las siguientes categorías presentes en el caso:

- **Directos**: nombres propios de personas, NIF/NIE/pasaporte, números de Seguridad Social o historia clínica, números de autos o expediente, matrículas, direcciones postales, teléfonos, correos, cuentas bancarias, IBAN, redes sociales.
- **Cuasi-directos**: lugares concretos (centros sanitarios, juzgados, empresas), fechas específicas, edades exactas en casos raros, profesiones de baja prevalencia, eventos mediáticos.
- **Indirectos**: combinaciones de atributos que, aun sin nombre, identifican (edad + profesión + ciudad pequeña + diagnóstico raro). Estos son los que más fugas producen.

## Paso 3 — Transformación

Aplica las cuatro reglas de transformación:

### 3.1 Desplazamiento temporal consistente
- Mismo desfase a TODAS las fechas del documento.
- Conserva intervalos entre eventos: exactos.
- Conserva el día de la semana cuando sea procesalmente relevante (notificaciones, plazos, audiencias, ingresos hospitalarios programados).
- Conserva la estación del año si es clínicamente relevante (patrón estacional afectivo, p. ej.).
- Si una fecha es muy singular (p. ej., día con un evento mediático asociado), no basta con desplazarla: se sustituye por descripción funcional ("primera entrevista, semana siguiente al alta").

### 3.2 Seudónimos deterministas
- Etiqueta = rol + ID. Ver `plantilla-tokens.md` para convenciones.
- Consistencia absoluta dentro del documento.
- Si hay homonimias (dos personas con relaciones equivalentes), distinguir por subíndice o por rasgo no identificador (`[HIJO_MAYOR_A]`, `[HIJO_MENOR_A]`).

### 3.3 Generalización geográfica y organizacional
Sustituye nombres concretos por categoría funcional:

- "Hospital Universitario X de Granada" → `[HOSPITAL_TERCIARIO_CIUDAD_MEDIA_ANDALUCÍA]` (modo A o B); `[HOSPITAL_TERCIARIO_SUR_PENINSULAR]` (modo C).
- "Juzgado de Instrucción nº 4 de Granada" → `[JUZGADO_INSTRUCCIÓN_CAPITAL_PROVINCIA]`.
- "Audiencia Provincial de Granada, Sección 1ª" → `[AUDIENCIA_PROVINCIAL_CAPITAL]`.
- "Centro de salud mental comunitario de [barrio]" → `[CSM_DISTRITO_URBANO]`.

Granularidad: la mínima necesaria para entender el caso.

### 3.4 Datos numéricos — distinción crítica

CONSERVA exactos:
- Dosis farmacológicas, posologías, vías de administración.
- Puntuaciones de tests y escalas (HAM-D, BDI, MMSE, PHQ-9, etc.).
- Parámetros analíticos relevantes.
- Plazos procesales en días (con desplazamiento aplicado a las fechas, pero el intervalo se preserva).
- Duración de tratamientos, ingresos, episodios.

DIFUMINA en rangos:
- Cuantías económicas: indemnizaciones, deudas, salarios, valoración de bienes.
- Edades cuando el caso sea estadísticamente raro a esa edad exacta (franja quinquenal: "entre 35 y 40 años").
- Tamaños o cifras muy específicas vinculadas a una persona o entidad ("plantilla de 47 trabajadores" → "plantilla mediana, en torno a 50").

## Paso 4 — Identificadores indirectos

Tras la transformación, repasa el texto para detectar combinaciones residuales de baja prevalencia:

- Profesión muy específica o de baja prevalencia ("traductor jurado de finés en Granada"). Generalizar a categoría funcional ("profesional liberal con especialización lingüística minoritaria").
- Eventos contextuales identificables (manifestación concreta, accidente con cobertura mediática, sentencia notoria). Sustituir por descripción funcional.
- Enfermedades raras: mantener categoría diagnóstica clínicamente útil, omitir prevalencia exacta, omitir centros de referencia identificables.
- En modo C: aplicar este paso de forma especialmente agresiva.

## Paso 5 — Salida formateada

Devuelve la respuesta con esta estructura:

```
## MAPA — archivar o destruir aparte del texto

- Desplazamiento temporal aplicado: +N días
- Mapa rol → token:
  - Persona X (rol: paciente / demandado / etc.) → [TOKEN]
  - Persona Y → [TOKEN]
  - ...
- Generalizaciones geográficas y organizacionales aplicadas:
  - Lugar/entidad concreto → categoría funcional
  - ...
- Generalizaciones de identificadores indirectos:
  - Atributo concreto → atributo generalizado
  - ...

## TEXTO SEUDONIMIZADO

[cuerpo del caso transformado]

## AUDITORÍA DE RIESGO RESIDUAL

- Nivel: [bajo / medio / alto]
- Justificación: [2-4 líneas]
- Detalles que aún podrían permitir reidentificación por singularidad combinada:
  - ...
- Propuesta de generalización adicional (si procede):
  - ...

## CONTROL DE FIDELIDAD

- ¿Algún elemento del texto seudonimizado no tiene correspondencia en el original? [sí / no]
- Si sí, listar: [elemento — motivo de la divergencia — corrección propuesta]
- Marcadores usados: [recuento de `[DATO_ELIMINADO]` y `[NO_CONSTA]`, si los hay]

## DECISIONES POR DEFECTO

[asunciones tomadas por falta de contexto, en lista breve; si no hay, "ninguna"]
```

## Paso 6 — Cierre

Tras entregar la salida del paso 5, no añadas comentario adicional salvo que el usuario pida iteración. Si pide corrección, regenera el texto completo aplicando la corrección y manteniendo coherencia con todo lo anterior (mismo desplazamiento, mismos tokens).

## Rúbrica rápida de riesgo residual

- **Bajo**: caso común (cuadro clínico frecuente o tipo procesal habitual), sin combinaciones singulares, sin eventos contextuales identificables, sin profesión de baja prevalencia.
- **Medio**: alguna combinación singular o profesión específica, pero diluida por generalización; enfermedad relativamente común con curso atípico; lugar concreto generalizado correctamente.
- **Alto**: caso mediático, figura pública, enfermedad rara, combinación de atributos de muy baja prevalencia, evento contextual identificable. En este caso, recomendar paso a modo `C` o exclusión de partes del caso.
