---
name: seudonimizador-clinico-juridico
description: >-
  Seudonimiza casos clínicos (psicología/psiquiatría) y jurídicos para estudio, supervisión o formación, conservando la utilidad analítica y eliminando identificadores directos e indirectos. Trigger obligatorio: "/seudonimizar"; actívalo con ese comando o con "seudonimiza este caso". Modos: A (clínico), B (jurídico), C (generalización extrema) y audit. NO sustituye la anonimización formal exigida por RGPD/LOPDGDD para publicación, peritaje o expediente.
---

# Seudonimizador Clínico-Jurídico

Skill de transformación de casos reales en versiones aptas para uso secundario (estudio, supervisión, formación, redacción didáctica). **No anonimiza en sentido fuerte.** Produce textos seudonimizados con generalización dirigida, marcando explícitamente el riesgo residual.

## Por qué este skill

El uso real de un LLM con material clínico o jurídico se mueve siempre entre dos extremos malos:

- Pasar el caso crudo (riesgo legal y ético claro).
- Reducirlo tanto que pierde utilidad para razonar sobre él.

Este skill ocupa el medio razonado: conserva intervalos temporales, secuencias procesales, sintomatología, hallazgos exploratorios y dinámicas relevantes; elimina identificadores directos y reduce identificadores indirectos hasta un nivel auditado.

No transcribe nombres, no inventa hechos, no rellena lagunas. La fidelidad al original es regla dura: ningún dato, síntoma, hecho, cuantía o inferencia que no figure en el texto de entrada puede aparecer en la salida. Cuando un dato debe eliminarse sin sustituirlo, se marca como `[DATO_ELIMINADO]`; cuando un dato del original es ambiguo, se marca como `[NO_CONSTA]` o se traslada a decisiones por defecto. Ante la duda, omitir prevalece sobre rellenar.

## Marco normativo (lectura obligada antes de usarlo)

El RGPD distingue dos figuras:

- **Seudonimización (Art. 4.5 RGPD).** El dato no puede atribuirse a un interesado sin información adicional, conservada por separado. Sigue siendo dato personal. Requiere medidas técnicas y organizativas.
- **Anonimización (Considerando 26 RGPD).** El dato no puede vincularse a un interesado por ningún medio razonable. Deja de ser dato personal.

Lo que produce este skill es **seudonimización con generalización dirigida**. Aproxima la anonimización funcional para uso secundario interno (supervisión, formación), pero **no es anonimización en sentido jurídico** y **no autoriza por sí solo** a publicar el caso, incorporarlo a un peritaje, ni difundirlo.

Para que la seudonimización sea efectiva, el RGPD exige que la información que permitiría reidentificar (en este skill, el "mapa de tokens") **se conserve separada** y bajo medidas adicionales. Por eso este skill entrega el mapa en una sección destacada, pensada para ser archivada o destruida aparte del texto transformado.

## Para qué sirve

Recibe un caso real ya manejado por un profesional habilitado y devuelve, en este orden:

1. Confirmación con semilla de desplazamiento temporal y mapa rol→token.
2. Texto seudonimizado del caso, en bloque separable.
3. Auditoría de riesgo residual (bajo / medio / alto) con justificación.
4. Control de fidelidad: comprobación explícita de que ningún elemento de la salida carece de correspondencia en el original.
5. Decisiones por defecto (asunciones tomadas por falta de contexto).

## Modos de invocación

Sintaxis: `/seudonimizar [modo]` seguido del caso o adjuntando archivo.

- **`A`** (clínico). Caso de psicología o psiquiatría. Conserva sintomatología, exploración, hipótesis diagnósticas, formulación, dinámica transferencial, intervenciones y respuesta. Anonimiza identidad y vínculos del paciente y allegados, centros concretos, eventos traumáticos identificables por singularidad.
- **`B`** (jurídico). Caso jurídico (civil, penal, laboral, administrativo). Conserva hechos probados (parafraseados si son muy específicos), fundamentos de derecho, plazos procesales desplazados, tipos delictivos o civiles, lógica argumentativa. Anonimiza partes, procuradores, peritos nominados, números de autos y expediente, matrículas, direcciones, registros catastrales.
- **`C`** (generalización extrema). Para casos mediáticos, figuras públicas, enfermedades raras, eventos de prensa o combinaciones de baja prevalencia donde A o B dejarían riesgo residual alto. Aplica generalización adicional en profesión, ubicación, edad, eventos contextuales y hechos singulares.
- **`audit`**. Audita un texto ya seudonimizado (por este skill o por otra vía). Devuelve únicamente fugas detectadas, riesgo residual estimado y propuesta de generalización adicional. No regenera el texto salvo petición expresa.

Si el usuario no especifica modo, se pide aclaración. No hay modo por defecto: confundir A y B degrada el resultado.

## Para qué NO sirve

- Anonimización conforme al Cdo. 26 RGPD para publicación científica, peritaje formal, expediente oficial o cesión a terceros.
- Casos ficticios sin valor formativo: si ya es ficticio, no hay nada que seudonimizar.
- Procesamiento de datos identificables sin valor secundario claro (estudio, supervisión, formación).
- Sustitución del juicio profesional sobre qué partes del caso son sensibles y por qué.
- Ofuscación intencional de hechos relevantes para una causa o un cuadro clínico.

## Cómo usarlo

1. Lee `flujo.md` antes de procesar cualquier caso.
2. Detecta el modo (`A`, `B`, `C`, `audit`); si no se ha indicado, pide al usuario que lo aclare.
3. Verifica las puertas de entrada: caso real, mediación profesional, finalidad secundaria, separación posterior del mapa de tokens.
4. Sigue el flujo de seis pasos descrito en `flujo.md`, en orden, sin saltar ninguno.
5. Devuelve la salida con el formato y los encabezados especificados, incluida la auditoría de riesgo residual.
6. Si el modo es `audit`, sigue el protocolo de `auditoria.md` en lugar del flujo general.

## Archivos del skill

- `SKILL.md` — este descriptor.
- `flujo.md` — flujo operativo de seis pasos con reglas duras transversales.
- `plantilla-entrada.md` — guía de formato de entrada para el usuario.
- `plantilla-tokens.md` — catálogo de roles y convenciones de etiquetado consistente.
- `auditoria.md` — protocolo del modo `audit` y rúbrica de riesgo residual.

## Limitaciones conocidas

- Ámbito calibrado para España (RGPD, LOPDGDD, terminología procesal y sanitaria). Otros marcos jurídicos requieren ajustes.
- No detecta automáticamente identificadores en imágenes, audio o vídeo. Solo texto.
- La auditoría de riesgo residual es una estimación cualitativa, no una garantía formal.
- El mapa rol→token se entrega en la misma respuesta que el texto transformado. La separación efectiva (RGPD Art. 4.5) depende de que el usuario archive o destruya el mapa aparte; el skill no puede forzar esa separación.
- Pendiente de validación con casos reales de distinto tipo. Iterar tras pruebas.

## Versión

v1.1 — refuerzo de la regla de no-invención tras detectarse alucinaciones en uso real (adiciones de matiz no presentes en el original durante el parafraseo). La regla 1 transversal de `flujo.md` se ha reescrito como prohibición estricta y prioritaria sobre cualquier otra transformación. Se introduce el marcador `[DATO_ELIMINADO]` y un bloque obligatorio de **Control de fidelidad** en la salida del paso 5.

v1.0 — descriptor inicial con cuatro modos (A clínico, B jurídico, C generalización extrema, audit), flujo de seis pasos, plantilla de tokens y protocolo de auditoría. Probado únicamente con casos sintéticos. Iterar tras uso real.
