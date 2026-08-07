# plantilla-entrada.md — Formato de entrada para el skill

Esta plantilla es **orientativa**, no obligatoria. El skill puede procesar casos redactados en prosa libre. Cuanto más se acerque la entrada a esta estructura, más limpios serán el mapa de tokens y la auditoría de riesgo residual.

La plantilla está pensada para que el material que entra al skill sea trazable por ti antes de que el skill lo transforme.

## Antes de pegar nada: tres puertas mínimas

Antes de invocar `/seudonimizar`, comprueba lo siguiente. Son las "puertas de entrada" que el flujo verifica internamente, pero hacerlo a mano antes ahorra fricciones.

- [ ] El caso es **real** y proviene de tu actividad profesional o supervisión.
- [ ] La finalidad es **secundaria**: estudio, supervisión, formación, redacción didáctica. No publicación, no peritaje formal, no expediente oficial.
- [ ] Has decidido el **modo**: A (clínico), B (jurídico), C (generalización extrema), `audit` (auditar texto ya transformado).
- [ ] Tienes claro que vas a **archivar o destruir el mapa rol→token aparte** del texto transformado.

Si alguna falla, detente. No sirve para esto.

## Encabezado de la entrada

Recomendado, no obligatorio:

```
Modo: [A | B | C | audit]
Identificador interno del caso: [referencia tuya, no identificable]
Fecha aproximada de invocación: [solo para tu archivo]
```

El identificador interno te sirve a ti para localizar el caso en tu sistema. No debe contener nombres, ni iniciales muy específicas, ni fechas exactas que faciliten reidentificación.

## Cuerpo del caso

### Modo A (clínico)

Información útil de incluir, en el orden que sea:

- **Datos generales mínimos**: edad o franja, sexo si es relevante, situación de convivencia, ocupación o categoría profesional, vía de derivación.
- **Motivo de consulta**: en palabras del paciente cuando esté disponible.
- **Cronología del cuadro actual**: inicio, curso, momentos de cambio, duración total.
- **Síntomas**: diferenciando lo referido del paciente y lo observado por el clínico.
- **Antecedentes psiquiátricos personales y familiares**.
- **Antecedentes médicos y medicación**: con dosis exactas (el skill las preserva).
- **Consumo de sustancias** cuando proceda.
- **Situación psicosocial**: red de apoyo, vivienda, trabajo, estresores recientes.
- **Exploración psicopatológica**: el resumen del clínico tras la entrevista.
- **Hipótesis diagnósticas o formulación previa** si la hay.
- **Intervenciones realizadas y respuesta**.

### Modo B (jurídico)

Información útil de incluir, en el orden que sea:

- **Tipo procesal**: civil, penal, contencioso-administrativo, laboral, mercantil.
- **Hechos**: relato cronológico de los hechos relevantes con fechas exactas (el skill las desplaza).
- **Partes y representación**: quién interviene, en qué condición procesal, con qué representación letrada.
- **Órgano judicial y fase**: juzgado, sala, fase del procedimiento.
- **Pretensiones y fundamentos**: qué se pide, sobre qué base jurídica.
- **Resoluciones previas**: autos, sentencias, recursos, plazos.
- **Cuantías económicas** cuando proceda (el skill las pasa a rangos).
- **Pruebas relevantes**: documentales, periciales, testificales.
- **Cuestiones a analizar**: lo que quieres que el caso permita estudiar.

### Modo C (generalización extrema)

Cualquiera de los dos cuerpos anteriores, pero indicando arriba el motivo por el que se elige modo C:

- Caso mediático.
- Figura pública o cargo institucional.
- Enfermedad rara, evento singular o combinación de muy baja prevalencia.
- Otro motivo de alto riesgo de reidentificación.

### Modo `audit`

En este modo, la entrada es un **texto ya seudonimizado** (por este skill u otra vía). No hay encabezado de caso: simplemente el texto a auditar.

Opcionalmente, indica:
- Quién lo seudonimizó (este skill v1.0, otra IA, manual).
- Si conoces el desplazamiento temporal aplicado y el mapa rol→token.
- Para qué uso secundario está pensado.

## Lo que NO debe incluir la entrada

Aunque el skill seudonimiza, conviene reducir la exposición desde el origen.

- **No incluyas** capturas de pantalla, fotos, escaneos de DNI o documentos identificables.
- **No incluyas** archivos con metadatos no limpiados (autoría incrustada, marcas de agua, ruta de origen). Si pasas un PDF o DOCX, límpialo antes con herramientas externas (`exiftool`, propiedades del documento).
- **No incluyas** nombres reales en cita textual entre comillas pensando que "como están entrecomillados, los respetará". El skill seudonimiza también las citas, pero el material en bruto no debería pasar por el chat si es evitable.
- **No incluyas** información de terceros sin relación con el caso ("el primo del paciente, que es jugador del Madrid"). Si no aporta, fuera.
- **No incluyas** el mapa de seudónimos de un caso anterior si vas a procesar uno nuevo. Cada caso, su mapa.

## Comprobación rápida antes de enviar

- [ ] El caso está mínimamente desidentificado en origen (sin DNI, dirección postal, teléfono, IBAN, matrícula).
- [ ] He elegido el modo (`A`, `B`, `C`, `audit`).
- [ ] Si es A o B, sé qué quiero conservar como aprendizaje del caso (eso me indica qué debe sobrevivir a la transformación).
- [ ] Si es `audit`, tengo el texto ya seudonimizado disponible.
- [ ] Voy a archivar o destruir el mapa rol→token por separado del texto.
- [ ] Estoy en una **Conversación Temporal** (Incognito) o equivalente en la IA que esté usando. No en una conversación que vaya a quedarse en el historial.

## Si dudas

Si dudas sobre si el caso es procesable por el skill:

- **Caso ficticio o ya desidentificado al máximo**: no hace falta usar el skill. Procésalo directamente con el skill clínico o jurídico que toque.
- **Caso real para publicación o peritaje**: este skill no es suficiente. Requiere revisión humana experta y, si procede, asesoría jurídica.
- **Caso con datos de menores, datos genéticos, biométricos u otras categorías especiales del Art. 9 RGPD**: piensa dos veces antes de pasarlo a un LLM en la nube. Considera procesamiento local.
- **Caso muy mediático**: usa modo C, y aun así audita el resultado con `audit` antes de cualquier uso.

Cuando en duda, menos.
