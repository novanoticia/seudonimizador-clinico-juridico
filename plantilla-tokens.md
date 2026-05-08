# plantilla-tokens.md — Convenciones de etiquetado

Catálogo de tokens para mantener consistencia entre casos. No es exhaustivo: ante un rol no listado, crear token nuevo siguiendo el mismo patrón (rol en mayúsculas + sufijo identificador).

## Principios

1. **Rol antes que nombre**. El token informa de la función en el caso, no de la persona.
2. **Una sola dimensión por token**. Si un sujeto cumple varios roles (p. ej. testigo y víctima), usar el rol procesalmente más relevante y mencionar el segundo en el mapa.
3. **Sufijos**:
   - Letras (`_A`, `_B`, `_C`...) para sujetos del mismo rol distinguibles por relación con el caso principal.
   - Números (`_1`, `_2`...) para roles profesionales o institucionales replicables.
4. **Granularidad**: solo añadir información relacional cuando sea relevante. `[HIJO_MAYOR_A]` solo si la edad relativa importa.

## Modo A — Casos clínicos

### Sujeto principal y allegados
- `[PACIENTE_A]` — paciente del caso. Si hay varios, `[PACIENTE_A]`, `[PACIENTE_B]`...
- `[CONVIVIENTE_A]` — pareja, cónyuge o conviviente actual.
- `[EXCONVIVIENTE_A]` — pareja anterior relevante en el caso.
- `[PROGENITOR_MADRE_A]`, `[PROGENITOR_PADRE_A]`.
- `[HIJO_A]` (con `_MAYOR_`, `_MENOR_` o `_INTERMEDIO_` solo si la edad relativa es relevante).
- `[HERMANO_A]`, `[HERMANA_A]`.
- `[ALLEGADO_A]` — amistad, vecindad u otro vínculo no familiar relevante.

### Profesionales y centros
- `[PSIQUIATRA_REFERENTE]`, `[PSICÓLOGA_REFERENTE]` — clínico responsable habitual.
- `[CLÍNICO_DERIVADOR]` — quien deriva al caso actual.
- `[PROFESIONAL_URGENCIAS]`, `[PROFESIONAL_ATENCIÓN_PRIMARIA]`.
- `[CSM_DISTRITO_URBANO]` — centro de salud mental ambulatorio.
- `[USM_HOSPITALARIA]` — unidad hospitalaria de salud mental.
- `[HOSPITAL_TERCIARIO_CIUDAD_MEDIA]` o `[HOSPITAL_COMARCAL]` según corresponda.
- `[UNIDAD_AGUDOS]`, `[UNIDAD_REHABILITACIÓN]`, `[HOSPITAL_DE_DÍA]`.

### Eventos clínicos relevantes
Los eventos no se convierten en tokens; se mantienen descritos pero generalizados si son singulares. Ejemplos:
- "Ingreso involuntario tras intento autolítico en mayo de 2023" se mantiene como descripción, con la fecha desplazada según la semilla.
- "Atentado de [lugar][fecha]" → "evento traumático colectivo con cobertura mediática".

## Modo B — Casos jurídicos

### Partes
- `[DEMANDANTE_1]`, `[DEMANDADO_1]`, `[ACTOR_1]`, `[INVESTIGADO_1]`, `[ACUSADO_1]`, `[VÍCTIMA_1]`, `[PERJUDICADO_1]`, `[TESTIGO_1]`.
- Sufijo numérico cuando hay varios sujetos del mismo rol procesal.
- Si un sujeto cambia de condición procesal (investigado → acusado), mantener el mismo número y reflejar el cambio en el mapa.

### Representación letrada
- `[LETRADO_DEFENSA_1]`, `[LETRADO_ACUSACIÓN_PARTICULAR_1]`, `[FISCAL_1]`, `[PROCURADOR_1]`.
- `[ABOGADO_DEMANDANTE_1]`, `[ABOGADO_DEMANDADO_1]` para jurisdicción civil.
- `[GRADUADO_SOCIAL_1]` para jurisdicción social.

### Órgano judicial y administración
- `[JUZGADO_INSTRUCCIÓN_CAPITAL_PROVINCIA]`, `[JUZGADO_PRIMERA_INSTANCIA_LOCALIDAD_MEDIA]`.
- `[JUZGADO_PENAL_1]`, `[AUDIENCIA_PROVINCIAL_CAPITAL]`, `[TSJ_AUTONÓMICO]`.
- `[MAGISTRADO_INSTRUCTOR_1]`, `[MAGISTRADO_PONENTE_1]`.
- `[LETRADO_ADMINISTRACIÓN_JUSTICIA_1]`.
- `[POLICÍA_JUDICIAL_1]`, `[GUARDIA_CIVIL_1]`.

### Identificadores procesales y económicos
- Números de autos: `[AUTOS_2023_NNN]` (preservando el año desplazado solo si es procesalmente relevante; en general, mejor `[AUTOS_X]`).
- Cuantías: rangos. `[INDEMNIZACIÓN_15K_20K_EUR]` o "entre 15.000 y 20.000 €".
- Matrículas, IBAN, NIE, número de Seguridad Social, dirección registral: nunca aparecen en el texto transformado. Sustituir por descripción funcional ("vehículo del [INVESTIGADO_1]", "cuenta corriente del [DEMANDADO_1]").

## Modo C — Generalización extrema

Sobre los tokens de A o B, aplicar reducción adicional:

- **Localización**: pasar a nivel de comunidad autónoma o región amplia (`[HOSPITAL_TERCIARIO_SUR_PENINSULAR]`).
- **Profesión**: categoría funcional amplia (en lugar de "investigador en filología semítica", `[ACADÉMICO_HUMANIDADES]`).
- **Edad**: franja decenal en lugar de quinquenal ("en torno a los 40").
- **Eventos contextuales**: descritos por función, nunca por referencia identificable.
- **Cuantías**: orden de magnitud en lugar de rango.

Si tras la generalización extrema el caso queda demasiado vacío para ser útil, indicarlo en el apartado de auditoría: a veces no se puede tener ambas cosas.

## Convenciones de mapa

El mapa rol→token entregado en la salida sigue este formato:

```
- Sujeto / lugar / entidad original → [TOKEN]   (rol en el caso: …)
```

El "original" en el mapa es lo que el usuario pasó como entrada. El usuario es responsable de archivar o destruir el mapa por separado del texto transformado.

## Errores frecuentes a evitar

- Mezclar rol y nombre: nunca `[MARÍA_PACIENTE]`. Solo rol.
- Cambiar el token del mismo sujeto a mitad del texto.
- Dejar el nombre original en una cita textual entre comillas. Las citas también se seudonimizan.
- Usar tokens muy genéricos cuando hay varios sujetos del mismo rol: si hay tres hijos, no pueden ser todos `[HIJO_A]`.
- Olvidar la generalización del lugar y dejar la ciudad concreta en una sola mención del texto. La consistencia se rompe por descuido, no por intención.
