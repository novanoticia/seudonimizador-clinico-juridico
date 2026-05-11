# auditoria.md — Protocolo del modo `audit`

El modo `audit` se invoca cuando el usuario pasa un texto **ya seudonimizado** (por este skill, por otra IA, por un humano) y quiere comprobar si está limpio.

No regenera el texto. Solo audita y, si el usuario lo pide después, regenera.

## Cuándo usar este modo

- Texto procesado anteriormente que se va a reutilizar en otro contexto.
- Texto seudonimizado por una herramienta distinta y se duda de su solidez.
- Antes de incorporar un caso a una sesión de supervisión, taller o material formativo.
- Tras una iteración de corrección, para verificar que no han quedado fugas.

## Cuándo NO usar este modo

- Para validar conformidad con RGPD para publicación. Eso requiere revisión humana experta y, en su caso, asesoría jurídica.
- Para "garantizar" que un texto está anónimo. La auditoría es estimación cualitativa, no certificación.

## Puerta de entrada

Antes de auditar:

- ¿El texto entregado dice ser ya seudonimizado, o el usuario está confundiendo este modo con `A`/`B`/`C`? Si es lo segundo, redirigir.
- ¿Hay finalidad clara para la auditoría (estudio, supervisión, formación)?

## Protocolo de seis comprobaciones

Para cada categoría, indicar: **Pasa / Fallo / Duda**, con localización de la fuga si la hay.

### 1. Identificadores directos
Buscar restos de:
- Nombres propios de personas.
- NIF/NIE/pasaporte, números de historia clínica, autos o expediente, Seguridad Social.
- Direcciones postales, teléfonos, correos, redes sociales.
- Matrículas, IBAN, números de cuenta.

### 2. Lugares y entidades
Buscar nombres concretos no generalizados:
- Hospitales, centros de salud, clínicas privadas.
- Juzgados, tribunales, fiscalías, comisarías.
- Empresas, centros educativos, asociaciones.
- Barrios, calles, ciudades pequeñas (las grandes capitales pueden mantenerse según el caso, pero un pueblo concreto rara vez).

### 3. Fechas
Buscar:
- Fechas que no encajen en un desplazamiento consistente con el resto del texto (síntoma de transformación incompleta).
- Fechas singulares por su contenido público (día de un evento mediático, jornada electoral, etc.).
- Edades exactas en casos raros (pediátrico avanzado, geriátrico extremo, edad atípica para un cuadro o para un puesto).

### 4. Numéricos identificadores
Buscar cuantías exactas (indemnizaciones, deudas, salarios) que no estén en rango. Distinguir de los numéricos clínicos (dosis, escalas) que deben mantenerse exactos: el fallo es cuantía económica exacta, no escala diagnóstica exacta.

### 5. Identificadores indirectos
Buscar combinaciones singulares:
- Profesión + ciudad + edad cuando la combinación sea de baja prevalencia.
- Enfermedad rara + centro de referencia identificable.
- Cargo público o profesión muy visible.
- Eventos contextuales narrados con detalle suficiente para identificarlos.

### 6. Coherencia interna
Buscar:
- Tokens inconsistentes (el mismo sujeto con dos tokens distintos, o dos sujetos con el mismo token).
- Restos de citas textuales sin seudonimizar.
- Metadatos visibles (encabezados institucionales, firmas, números de página identificables, nombres de archivo originales).
- Idiomas mezclados sin justificación (a veces los nombres propios sobreviven en una cita en otro idioma).

### 7. Fidelidad al original (condicional)
Solo si el usuario aporta también el texto original junto al seudonimizado. Si no lo aporta, marcar esta comprobación como **No aplicable** y avisar de la limitación.

Buscar elementos del texto seudonimizado que **no tengan correspondencia en el original**:
- Síntomas, diagnósticos, hallazgos exploratorios o antecedentes clínicos añadidos.
- Hechos, plazos, cuantías o fundamentos jurídicos no presentes en el original.
- Matices narrativos, inferencias causales o contextualizaciones introducidas durante el parafraseo.
- "Redondeo" de la narrativa: frases puente o transiciones que aportan información implícita ausente del original.

Este es el control específico contra alucinaciones del paso de transformación. Una sola fuga aquí degrada el caso silenciosamente y debe escalar el nivel de riesgo a **alto** independientemente del resto de comprobaciones.

## Salida del modo `audit`

```
## AUDITORÍA — texto ya seudonimizado

### Comprobaciones
1. Identificadores directos: [Pasa / Fallo / Duda]
   - Si hay fugas: localización y contenido (sin reproducir el dato sensible literal; describirlo: "nombre propio en línea 14, segunda mención").
2. Lugares y entidades: [...]
3. Fechas: [...]
4. Numéricos identificadores: [...]
5. Identificadores indirectos: [...]
6. Coherencia interna: [...]
7. Fidelidad al original: [Pasa / Fallo / Duda / No aplicable]
   - Si el original no se aportó: marcar No aplicable y recordar la limitación.
   - Si hay divergencias: listarlas con localización y motivo probable.

### Riesgo residual estimado
- Nivel: [bajo / medio / alto]
- Justificación: [3-5 líneas]

### Propuestas
- Correcciones necesarias antes de uso secundario:
  - ...
- Generalización adicional recomendada (si procede):
  - ...
- Recomendación global: [apto para uso secundario interno / requiere corrección antes de uso / pasar a modo C / fragmentar y reseudonimizar partes / no apto sin revisión humana experta]

### Si quieres regenerar
Indica explícitamente "regenerar" y el texto se reprocesa aplicando las correcciones detectadas, manteniendo los tokens y el desplazamiento temporal del original (si son recuperables) o introduciendo nuevos (si no).
```

## Limitaciones del modo `audit`

- No puede detectar identificadores que no aparezcan en el texto pero sí en metadatos no visibles del archivo (propiedades del documento, marcas de agua, autoría incrustada). El usuario debe limpiar el archivo aparte.
- Puede no detectar combinaciones singulares que solo serían identificables para alguien con conocimiento del contexto local específico (compañero de un servicio, vecino de una localidad). La auditoría se limita a lo razonablemente identificable por un tercero externo medio.
- En casos muy especializados (medicina forense, derecho mercantil técnico), el conocimiento experto del campo amplía el riesgo de reidentificación más allá de lo que la auditoría general detecta.

## Cuándo escalar a revisión humana

Recomendar revisión humana experta y, si procede, asesoría jurídica si:

- El texto se va a publicar (científica, divulgativa, jurídicamente).
- El caso afecta a una figura pública o tiene cobertura mediática.
- Hay datos de menores, datos genéticos, datos biométricos o categorías especiales del Art. 9 RGPD con riesgo elevado.
- El uso secundario implica cesión a terceros fuera del entorno de supervisión o formación cerrada.
