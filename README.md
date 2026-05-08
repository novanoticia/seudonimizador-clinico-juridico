# seudonimizador-clinico-juridico

Skill para asistentes conversacionales (Claude, Anthropic) de **seudonimización con generalización dirigida** de casos clínicos (psicología/psiquiatría) y jurídicos para uso secundario: estudio, supervisión, formación o redacción didáctica. Conserva utilidad analítica (cronología exacta, secuencia procesal, evolución sintomatológica, lógica argumental) eliminando identificadores directos y reduciendo identificadores indirectos. **No anonimiza en sentido jurídico fuerte.**

> **Autor:** Pablo · [mindandhealth.org](https://mindandhealth.org) · [github.com/novanoticia](https://github.com/novanoticia)
> **Licencia:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.es)
> **Versión actual:** v1.0

---

## Antes de empezar: lee la guía

Antes de probar el skill, conviene leer la guía profesional. Explica filosofía de diseño, marco ético-legal (RGPD, LOPDGDD, MDR 2017/745, copyright), arquitectura del flujo, modos de invocación, modo recomendado de uso, uso en otras IAs, limitaciones conocidas y sesgos identificados:

📄 **[Guía para profesionales (PDF, v1.0)](./docs/seudonimizador-clinico-juridico-guia-profesional-v1.0.pdf)**

Es un documento pensado para leer una vez antes del primer uso. Sin esa lectura, hay riesgo de tratar la herramienta como caja negra, lo que en este caso significa creer que produce anonimización conforme cuando solo produce seudonimización razonada.

---

## Estado del proyecto

Versión **1.0**. Probado únicamente con casos sintéticos (clínico depresivo con consumo, jurídico civil de responsabilidad contractual, jurídico penal con elementos mediáticos para someter el modo C a tensión).

> **No validado con casos reales por profesionales habilitados.** Pendiente de prueba en supervisión y formación reales antes de cualquier uso institucional.

---

## Audiencia esperada

Profesionales habilitados en psiquiatría, psicología clínica, derecho o disciplinas afines que quieran un andamio metodológico para preparar casos reales destinados a uso secundario interno (supervisión, formación, redacción didáctica).

**No es para autodescripción del propio usuario, no es para uso por personas no cualificadas profesionalmente, no sustituye revisión humana experta, no es producto sanitario en el sentido del MDR 2017/745, no es asesoramiento jurídico.**

---

## Sobre el autor

Desarrollado por **Pablo** ([mindandhealth.org](https://mindandhealth.org), GitHub: [novanoticia](https://github.com/novanoticia)) — **no profesional sanitario ni jurista en ejercicio**. Es un proyecto personal con interés autodidacta en marcos clínicos contextuales, razonamiento clínico y jurídico, y crítica de la mediación algorítmica de la información sensible.

El skill se ha construido con **asistencia de Claude (Anthropic)**. Las decisiones de diseño, la dirección y la responsabilidad del contenido corresponden al autor humano. Requiere validación profesional antes de cualquier uso real.

---

## Qué hace

Recibe un caso real ya manejado por un profesional habilitado y devuelve, en este orden:

1. Apertura con semilla de desplazamiento temporal y eventuales preguntas críticas previas.
2. Mapa rol→token (separable, pensado para archivar o destruir aparte).
3. Texto seudonimizado con cronología consistente.
4. Auditoría de riesgo residual (bajo / medio / alto) con justificación.
5. Decisiones por defecto y lagunas.

**Modos disponibles:**

- `A` — caso clínico (psicología/psiquiatría).
- `B` — caso jurídico (civil, penal, laboral, contencioso, mercantil).
- `C` — generalización extrema, para casos mediáticos, figuras públicas o de muy baja prevalencia.
- `audit` — auditoría de un texto ya seudonimizado, con rúbrica de riesgo y propuesta de generalización adicional.

Detalle completo en [`SKILL.md`](./SKILL.md), lógica de transformación en [`flujo.md`](./flujo.md), formato de entrada en [`plantilla-entrada.md`](./plantilla-entrada.md), catálogo de tokens en [`plantilla-tokens.md`](./plantilla-tokens.md), protocolo del modo `audit` en [`auditoria.md`](./auditoria.md), y discusión exhaustiva en la guía PDF.

---

## Qué NO hace

- No produce **anonimización** en el sentido del Considerando 26 RGPD. Lo que entrega es **seudonimización con generalización dirigida** (Art. 4.5 RGPD).
- No sustituye los procedimientos formales de anonimización exigibles para publicación científica, peritaje formal, expediente oficial o cesión a terceros.
- No emite juicio clínico ni jurídico sobre el caso. Solo lo transforma.
- No detecta identificadores en imágenes, audio, vídeo, ni metadatos no visibles de archivos. Solo texto.
- No es un producto sanitario en el sentido del Reglamento (UE) 2017/745.
- No es asesoramiento jurídico.

---

## Modo recomendado de uso

El skill está diseñado para minimizar la huella de los datos sensibles en la sesión y en la cuenta del usuario. Sigue este orden:

1. **Activa Conversación Temporal** (Incognito) en la app de Claude para macOS antes de pegar nada. La Conversación Temporal no usa memoria, no se guarda en el historial visible y no entra en la búsqueda de chats pasados. Es la capa mínima razonable.
2. **Limpia el archivo en origen** si vas a adjuntar PDF/DOCX: revisa metadatos (autoría incrustada, marcas de agua, propiedades del documento) con herramientas externas (`exiftool`, propiedades del documento) antes de subirlo.
3. **Invoca el skill** con `/seudonimizar A`, `B`, `C` o `audit` seguido del caso o adjuntando archivo.
4. **Verifica el mapa de tokens y la auditoría de riesgo residual** antes de aceptar el resultado. Si detectas fuga, pide corrección concreta y deja que el skill regenere manteniendo coherencia.
5. **Archiva o destruye el mapa rol→token aparte del texto transformado.** Es la "información adicional" que el RGPD pide custodiar separadamente para que la seudonimización sea efectiva (Art. 4.5).
6. **Cierra la conversación** una vez tengas el resultado en disco local.

> Aviso: la Conversación Temporal es una capa de privacidad de interfaz, no una bóveda criptográfica. Reduce la exposición pero no la elimina. Para usos que requieran cumplimiento RGPD pleno (publicación, peritaje, expediente), considera procesamiento local (LLM en máquina propia) y revisión humana experta como capas adicionales.

---

## Uso en otras IAs

El skill es un conjunto de archivos Markdown. Cualquier asistente conversacional capaz de leer instrucciones extensas puede aplicarlo, con matices según la plataforma.

- **Claude (app, web, API)**: uso nativo. Coloca el directorio en la carpeta de skills personales y se activa con `/seudonimizar`. Recomendado: Opus 4.7 por capacidad de razonamiento sostenido. Funciona también en Sonnet con resultados algo más mecánicos en el modo `C`.
- **ChatGPT (Temporary Chat)**: usa el equivalente "chat temporal". Pega `SKILL.md` + `flujo.md` + `plantilla-tokens.md` (concatenados) como primer mensaje, indicando: "Sigue este protocolo. Espera mi caso." Activa el chat temporal antes de pegar nada.
- **Mistral LeChat**: equivalente. Pegar el bloque del skill como prompt inicial. Modelos grandes (Large) recomendados.
- **Google Gemini**: usa el modo de chat temporal cuando esté disponible. Pega el skill y procede.
- **Meta AI en WhatsApp**: no recomendado para casos sensibles por la integración con la cuenta del usuario y la falta de un modo temporal verificable.
- **LLM local (Ollama, llama.cpp, LM Studio, etc.)**: opción más segura para casos con datos especialmente delicados. Requiere modelo de razonamiento suficientemente grande (≥ 30B parámetros para resultados aceptables en modos B y C). El procesamiento local elimina la transmisión a terceros, que es la principal preocupación RGPD.

En todos los casos, la salida hay que auditarla. Cuanto más pequeño o menos capaz sea el modelo, más probable es que omita identificadores indirectos. El modo `audit` puede aplicarse a textos producidos por cualquier IA para revisar su solidez.

---

## Cómo usarlo (instalación)

1. Clona o descarga este repositorio.
2. Coloca el directorio en la carpeta de skills personales según la documentación oficial de Anthropic.
3. Invoca con `/seudonimizar [modo]` seguido del caso, en una **Conversación Temporal**.

Plantilla orientativa de entrada en [`plantilla-entrada.md`](./plantilla-entrada.md). Buenas prácticas detalladas en la guía PDF.

---

## Estructura del repositorio

```
seudonimizador-clinico-juridico/
├── SKILL.md               # Descriptor del skill: trigger y resumen
├── flujo.md               # Flujo operativo de seis pasos
├── plantilla-entrada.md   # Formato de entrada para el usuario
├── plantilla-tokens.md    # Catálogo de roles y convenciones
├── auditoria.md           # Protocolo del modo audit
├── LICENSE                # CC BY 4.0
├── README.md              # Este archivo
├── CHANGELOG.md           # Historial de versiones
├── .gitignore
└── docs/
    └── seudonimizador-clinico-juridico-guia-profesional-v1.0.pdf
```

---

## Disclaimer

Este skill es una **herramienta metodológica experimental sin validación formal**. Lo que produce es seudonimización con generalización dirigida; no es anonimización en sentido jurídico. El uso real con datos sensibles es responsabilidad exclusiva del profesional habilitado que lo emplee y debe ajustarse al marco normativo aplicable (RGPD, LOPDGDD, secreto profesional, deber de sigilo).

Ni el autor ni la herramienta ofrecen garantía alguna sobre la exactitud, idoneidad o consecuencias derivadas de su uso. Cualquier uso por personas no cualificadas profesionalmente queda fuera del alcance previsto del proyecto y bajo entera responsabilidad de quien lo realice.

---

## Referencias y atribuciones

Este skill referencia, sin reproducir literalmente, las siguientes obras y marcos:

- **RGPD** — Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales. Artículos 4.5 (seudonimización), 9 (categorías especiales), 25 (privacidad desde el diseño), Considerando 26 (anonimización).
- **LOPDGDD** — Ley Orgánica 3/2018, de Protección de Datos Personales y garantía de los derechos digitales (España).
- **MDR 2017/745** — Reglamento (UE) 2017/745 sobre productos sanitarios. Citado para delimitar lo que el skill no es.
- **Directrices del Grupo de Trabajo del Artículo 29 (WP29) sobre técnicas de anonimización** (Opinion 05/2014). Marco de referencia técnica.

Toda referencia es nominativa y conceptual. El usuario es responsable de cumplir las condiciones de licencia o derechos de autor de cualquier material consultado a partir de estas referencias.

---

## Asistencia de IA

Este skill ha sido elaborado con asistencia de **Claude (Anthropic)**. Su contenido refleja decisiones, criterios y revisión del autor humano, pero requiere revisión profesional adicional antes de cualquier uso real con datos sensibles.

---

## Licencia

[Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.es). Texto resumido en [`LICENSE`](./LICENSE).

Eres libre de:

- **Compartir** — copiar y redistribuir el material en cualquier medio o formato.
- **Adaptar** — remezclar, transformar y construir a partir del material para cualquier propósito, incluso comercialmente.

Bajo el siguiente término:

- **Atribución** — Debes dar crédito de manera adecuada, proporcionar un enlace a la licencia, e indicar si se han realizado cambios. Puedes hacerlo en cualquier forma razonable, pero no de forma tal que sugiera que tienes el apoyo del licenciante o lo recibes por el uso que haces.

---

## Cómo citarlo

Si lo referencias en un trabajo o adaptación:

> Pablo (2026). *seudonimizador-clinico-juridico* (v1.0). Skill de seudonimización con generalización dirigida para casos clínicos y jurídicos. mindandhealth.org · github.com/novanoticia/seudonimizador-clinico-juridico

---

## Feedback y contribuciones

Cualquier feedback profesional es valioso, especialmente sobre: identificadores indirectos no detectados, comportamiento inesperado en modo `C`, fallos en la consistencia de tokens, casos jurídicos donde el desplazamiento temporal rompe la lógica procesal, sugerencias de modos adicionales.

El autor puede ser contactado a través de [mindandhealth.org](https://mindandhealth.org). Issues y pull requests en GitHub también son bienvenidos. Las contribuciones de **clínicos y juristas habilitados** que quieran probar el skill con casos reales son especialmente valoradas.

Más detalles sobre cómo dar feedback en la guía PDF.
