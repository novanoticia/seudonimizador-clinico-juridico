# Changelog

Todas las novedades relevantes del skill se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y se ajusta a versionado semántico.

## [1.0] — 2026-05-08

### Añadido
- Descriptor inicial del skill (`SKILL.md`) con frontmatter, cuatro modos (A clínico, B jurídico, C generalización extrema, `audit`) y marco normativo RGPD/LOPDGDD integrado.
- Flujo operativo de seis pasos (`flujo.md`): puerta de entrada, apertura con semilla de desplazamiento temporal, detección de identificadores, transformación, identificadores indirectos, salida formateada y cierre.
- Reglas duras transversales: no inventar, no suavizar, consistencia absoluta, separabilidad del mapa, sin metadatos involuntarios.
- Catálogo de tokens (`plantilla-tokens.md`) para modos A, B y C, con convenciones de etiquetado y errores frecuentes.
- Plantilla de entrada (`plantilla-entrada.md`) con puertas de entrada y comprobación rápida previa al envío.
- Protocolo del modo `audit` (`auditoria.md`) con seis comprobaciones, rúbrica de riesgo residual y criterios de escalada a revisión humana experta.
- Guía profesional en PDF (`docs/`) con filosofía de diseño, marco ético-legal, arquitectura del flujo, modo recomendado de uso, uso en otras IAs, limitaciones conocidas y sesgos identificados.
- Licencia CC BY 4.0.

### Probado
- Caso clínico depresivo con consumo de sustancias (modo A).
- Caso jurídico civil de responsabilidad contractual con cuantías relevantes (modo B).
- Caso jurídico penal con elementos mediáticos para someter el modo C a tensión.

### Pendiente
- Validación con casos reales por profesionales habilitados.
- Pruebas de encadenamiento con `/cie11-formulacion-clinica`, `/dsm-formulacion-clinica` y `/codigo-civil-formulacion-juridica`.
- Calibrado para población infanto-juvenil.
- Catálogo de tokens ampliado para jurisdicción mercantil técnica y casos administrativos complejos.
