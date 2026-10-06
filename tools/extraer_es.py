#!/usr/bin/env python3
"""Extrae del ORIGINAL los literales visibles en español y genera i18n-es.md.

El catálogo de referencia nunca se escribe a mano: cada literal se LEE de la
línea real del original con una expresión regular de un solo grupo y se
comprueba con aserciones (nº de coincidencias exacto, literal único, sin
espacios en los extremos). Si el original cambia de forma, la extracción falla.

También comprueba la COBERTURA: todo texto de las plantillas de salida (bloques
de código clasificados como `salida`) es un literal con clave o una instrucción
declarada. Una etiqueta nueva sin clave, o un bloque de código nuevo sin
clasificar, rompe la comprobación.

Uso:
    python3 tools/extraer_es.py escribir     # regenera i18n-es.md
    python3 tools/extraer_es.py comprobar    # sale con 1 si está desfasado o hay huecos

Solo biblioteca estándar.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linea_base import FICHEROS_MD, RAIZ, SKILL_DIR  # noqa: E402
from validar_i18n import fuentes_reales  # noqa: E402

CATALOGO_ES = RAIZ / SKILL_DIR / "i18n-es.md"


class ErrorExtraccion(Exception):
    pass


# ── especificación ──────────────────────────────────────────────────────────
# (clave, fichero fuente, regex con UN grupo = el literal, seguridad[, nº de coincidencias])
#
# `seguridad: sí` marca las frases cuya traducción defectuosa podría degradar una
# salvaguarda (invertir un veredicto o un nivel de riesgo, aflojar la separación del
# mapa, el control de fidelidad). Es un criterio mío, DEBE revisarlo una persona: la
# lista queda fijada en tests/test_extractor_es.py para que cualquier cambio sea un diff.

ESPECIFICACION = [
    # ── flujo.md · Paso 1 (APERTURA)
    ("encabezado.apertura", "flujo.md", r"^(## APERTURA)$", "no"),
    ("apertura.modo", "flujo.md", r"^- (Modo:) \[A \| B \| C\]$", "no"),
    ("lista.modos", "flujo.md", r"^- Modo: (\[A \| B \| C\])$", "no"),
    ("apertura.semilla", "flujo.md", r"^- (Semilla de desplazamiento temporal:) ", "no"),
    ("unidad.dias", "flujo.md", r"(\+N días)", "no", 2),
    ("apertura.justificacion", "flujo.md", r"^- (Justificación de la semilla:) ", "no"),
    ("apertura.preguntas", "flujo.md", r"^- (Preguntas críticas previas:) ", "no"),
    ("valor.ninguna", "flujo.md", r'"(ninguna)"', "no", 2),
    # ── flujo.md · Paso 5 (salida formateada)
    ("encabezado.mapa", "flujo.md", r"^(## MAPA — archivar o destruir aparte del texto)$", "sí"),
    ("mapa.desplazamiento", "flujo.md", r"^- (Desplazamiento temporal aplicado:) ", "no"),
    ("mapa.rol_token", "flujo.md", r"^- (Mapa rol → token:)$", "no"),
    ("mapa.ejemplo_persona_x", "flujo.md",
     r"^  - (Persona X \(rol: paciente / demandado / etc\.\) → \[TOKEN\])$", "no"),
    ("mapa.ejemplo_persona_y", "flujo.md", r"^  - (Persona Y → \[TOKEN\])$", "no"),
    ("mapa.generalizaciones_geo", "flujo.md",
     r"^- (Generalizaciones geográficas y organizacionales aplicadas:)$", "no"),
    ("mapa.ejemplo_lugar", "flujo.md", r"^  - (Lugar/entidad concreto → categoría funcional)$", "no"),
    ("mapa.generalizaciones_indirectos", "flujo.md",
     r"^- (Generalizaciones de identificadores indirectos:)$", "no"),
    ("mapa.ejemplo_atributo", "flujo.md", r"^  - (Atributo concreto → atributo generalizado)$", "no"),
    ("encabezado.texto", "flujo.md", r"^(## TEXTO SEUDONIMIZADO)$", "no"),
    ("encabezado.riesgo", "flujo.md", r"^(## AUDITORÍA DE RIESGO RESIDUAL)$", "sí"),
    ("riesgo.nivel", "flujo.md", r"^- (Nivel:) \[bajo / medio / alto\]$", "no"),
    ("lista.nivel", "flujo.md", r"^- Nivel: (\[bajo / medio / alto\])$", "sí"),
    ("riesgo.justificacion", "flujo.md", r"^- (Justificación:) \[2-4 líneas\]$", "no"),
    ("riesgo.detalles", "flujo.md",
     r"^- (Detalles que aún podrían permitir reidentificación por singularidad combinada:)$", "no"),
    ("riesgo.propuesta", "flujo.md",
     r"^- (Propuesta de generalización adicional \(si procede\):)$", "no"),
    ("encabezado.fidelidad", "flujo.md", r"^(## CONTROL DE FIDELIDAD)$", "sí"),
    ("fidelidad.pregunta", "flujo.md",
     r"^- (¿Algún elemento del texto seudonimizado no tiene correspondencia en el original\?) \[sí / no\]$",
     "sí"),
    ("lista.si_no", "flujo.md", r"^- ¿Algún elemento .*\? (\[sí / no\])$", "sí"),
    ("fidelidad.si_listar", "flujo.md", r"^- (Si sí, listar:) ", "no"),
    ("fidelidad.marcadores", "flujo.md", r"^- (Marcadores usados:) ", "no"),
    ("encabezado.decisiones", "flujo.md", r"^(## DECISIONES POR DEFECTO)$", "no"),
    # ── plantilla-tokens.md · formato de las entradas del mapa
    ("mapa.formato_entrada", "plantilla-tokens.md",
     r"^- (Sujeto / lugar / entidad original → \[TOKEN\]   \(rol en el caso: …\))$", "no"),
    # ── auditoria.md · salida del modo audit
    ("encabezado.audit", "auditoria.md", r"^(## AUDITORÍA — texto ya seudonimizado)$", "no"),
    ("encabezado.comprobaciones", "auditoria.md", r"^(### Comprobaciones)$", "no"),
    ("audit.comprobacion_1", "auditoria.md", r"^1\. (Identificadores directos:) ", "no"),
    ("audit.comprobacion_2", "auditoria.md", r"^2\. (Lugares y entidades:) ", "no"),
    ("audit.comprobacion_3", "auditoria.md", r"^3\. (Fechas:) ", "no"),
    ("audit.comprobacion_4", "auditoria.md", r"^4\. (Numéricos identificadores:) ", "no"),
    ("audit.comprobacion_5", "auditoria.md", r"^5\. (Identificadores indirectos:) ", "no"),
    ("audit.comprobacion_6", "auditoria.md", r"^6\. (Coherencia interna:) ", "no"),
    ("audit.comprobacion_7", "auditoria.md", r"^7\. (Fidelidad al original:) ", "no"),
    ("lista.veredicto", "auditoria.md",
     r"^1\. Identificadores directos: (\[Pasa / Fallo / Duda\])$", "sí"),
    ("lista.veredicto_fidelidad", "auditoria.md",
     r"^7\. Fidelidad al original: (\[Pasa / Fallo / Duda / No aplicable\])$", "sí"),
    ("encabezado.riesgo_estimado", "auditoria.md", r"^(### Riesgo residual estimado)$", "sí"),
    ("encabezado.propuestas", "auditoria.md", r"^(### Propuestas)$", "no"),
    ("propuestas.correcciones", "auditoria.md",
     r"^- (Correcciones necesarias antes de uso secundario:)$", "no"),
    ("propuestas.generalizacion", "auditoria.md",
     r"^- (Generalización adicional recomendada \(si procede\):)$", "no"),
    ("propuestas.recomendacion", "auditoria.md", r"^- (Recomendación global:) \[", "no"),
    ("lista.recomendacion", "auditoria.md", r"^- Recomendación global: (\[.*\])$", "sí"),
    ("encabezado.regenerar", "auditoria.md", r"^(### Si quieres regenerar)$", "no"),
    ("regenerar.texto", "auditoria.md", r'^(Indica explícitamente "regenerar" y .*)$', "no"),
]

# Entradas `nuevo` de la referencia (texto redactado para los catálogos, no extraído).
# (clave, "nuevo", None, seguridad, texto). Se rellena en las tareas 4 y 5.
NUEVOS = []

# Términos del glosario (propuesta inicial; se cierra en la Fase 5).
GLOSARIO_ES = [
    "seudonimización", "seudonimizado", "identificadores indirectos", "riesgo residual",
    "desplazamiento temporal", "semilla", "token", "mapa", "generalización",
    "control de fidelidad", "fuga", "regenerar",
]

# ── clasificación de bloques de código ──────────────────────────────────────
# (fichero, nº de bloque) -> ("salida", motivo) | ("excluido", motivo)
BLOQUES = {
    ("flujo.md", 1): ("salida", "Paso 1: plantilla de la apertura"),
    ("flujo.md", 2): ("salida", "Paso 5: plantilla de la salida formateada"),
    ("auditoria.md", 1): ("salida", "plantilla de la salida del modo audit"),
    ("plantilla-tokens.md", 1): ("salida", "formato de las entradas del mapa"),
    ("plantilla-entrada.md", 1): ("excluido", "formato de ENTRADA del usuario: documentación (categoría D), fuera de alcance"),
}

# Texto de las plantillas que NO es un literal de salida sino una INSTRUCCIÓN al
# modelo (él redacta el contenido en el idioma elegido). Cadenas exactas.
INSTRUCCIONES = {
    "flujo.md": [
        "(entero entre 30 y 180, elegido por ti)",
        '[breve, p. ej. "evita coincidencia con desfase trivial de un mes"]',
        '[si detectas ambigüedad o falta de datos clave, aquí; si no, "ninguna"]',
        "[cuerpo del caso transformado]",
        "[2-4 líneas]",
        "[elemento — motivo de la divergencia — corrección propuesta]",
        "[recuento de `[DATO_ELIMINADO]` y `[NO_CONSTA]`, si los hay]",
        '[asunciones tomadas por falta de contexto, en lista breve; si no hay, "ninguna"]',
    ],
    "auditoria.md": [
        "[...]",
        '- Si hay fugas: localización y contenido (sin reproducir el dato sensible literal; '
        'describirlo: "nombre propio en línea 14, segunda mención").',
        "- Si el original no se aportó: marcar No aplicable y recordar la limitación.",
        "- Si hay divergencias: listarlas con localización y motivo probable.",
        "[3-5 líneas]",
    ],
}


# ── extracción ──────────────────────────────────────────────────────────────

def extraer(fuentes, especificacion=None):
    """Lee los literales del original. Lanza ErrorExtraccion ante cualquier duda."""
    resultado = []
    for item in (ESPECIFICACION if especificacion is None else especificacion):
        clave, fichero, patron, seguridad = item[:4]
        esperadas = item[4] if len(item) > 4 else 1
        if fichero not in fuentes:
            raise ErrorExtraccion(f"{clave}: no hay texto de la fuente `{fichero}`")
        rx = re.compile(patron)
        coincidencias = []
        for n, linea in enumerate(fuentes[fichero].split("\n"), start=1):
            m = rx.search(linea)
            if m:
                coincidencias.append((n, m.group(1)))
        if len(coincidencias) != esperadas:
            raise ErrorExtraccion(
                f"{clave}: se esperaban {esperadas} coincidencia(s) en {fichero} y hay "
                f"{len(coincidencias)} (líneas {[n for n, _ in coincidencias]})")
        literales = {lit for _, lit in coincidencias}
        if len(literales) != 1:
            raise ErrorExtraccion(
                f"{clave}: las coincidencias dan literales distintos: {sorted(literales)}")
        literal = literales.pop()
        if not literal.strip():
            raise ErrorExtraccion(f"{clave}: literal vacío")
        if literal != literal.strip():
            raise ErrorExtraccion(f"{clave}: el literal tiene espacios en los extremos: {literal!r}")
        resultado.append({"clave": clave, "origen": "original", "fuente": fichero,
                          "seguridad": seguridad, "es": literal})
    return resultado


def generar(fuentes, especificacion=None, nuevos=None):
    """Texto de i18n-es.md (formato definido en tools/validar_i18n.py)."""
    entradas = extraer(fuentes, especificacion)
    for clave, origen, fuente, seguridad, texto in (NUEVOS if nuevos is None else nuevos):
        entradas.append({"clave": clave, "origen": origen, "fuente": fuente,
                         "seguridad": seguridad, "es": texto})
    out = ["# i18n-es — Catálogo de referencia (español)",
           "",
           "<!-- Generado por tools/extraer_es.py a partir del original. No editar a mano: "
           "`python3 tools/extraer_es.py escribir`. -->",
           "",
           "- código: es",
           "- estado: referencia",
           "",
           "## Glosario",
           ""]
    out += [f"- {t} → {t}" for t in GLOSARIO_ES]
    out += ["", "## Frases", ""]
    for e in entradas:
        out.append(f"### {e['clave']}")
        out.append(f"origen: {e['origen']}")
        if e["fuente"]:
            out.append(f"fuente: {e['fuente']}")
        out.append(f"seguridad: {e['seguridad']}")
        out.append(f"es: {e['es']}")
        out.append("")
    return "\n".join(out)


# ── cobertura ───────────────────────────────────────────────────────────────

def bloques(texto):
    """Bloques de código (``` … ```) con la línea (1-based) de la valla de apertura."""
    res, abierto = [], None
    for n, linea in enumerate(texto.split("\n"), start=1):
        if linea.startswith("```"):
            if abierto is None:
                abierto = {"inicio": n, "lineas": []}
            else:
                res.append(abierto)
                abierto = None
        elif abierto is not None:
            abierto["lineas"].append(linea)
    if abierto is not None:
        raise ErrorExtraccion(f"bloque de código sin cerrar (abre en la línea {abierto['inicio']})")
    return res


def cobertura(fuentes, entradas=None, clasificacion=None, instrucciones=None):
    """Lista de problemas: texto visible sin clave, bloques sin clasificar, etc."""
    entradas = extraer(fuentes) if entradas is None else entradas
    clasificacion = BLOQUES if clasificacion is None else clasificacion
    instrucciones = INSTRUCCIONES if instrucciones is None else instrucciones
    informe, lineas_salida = [], []   # (fichero, nº, texto)

    encontrados = set()
    for fichero in FICHEROS_MD:
        if fichero not in fuentes:
            continue
        for i, b in enumerate(bloques(fuentes[fichero]), start=1):
            encontrados.add((fichero, i))
            tipo = clasificacion.get((fichero, i))
            if tipo is None:
                informe.append(f"{fichero}: bloque de código nº {i} (línea {b['inicio']}) "
                               f"sin clasificar: añádelo a BLOQUES como `salida` o `excluido`")
            elif tipo[0] == "salida":
                for k, l in enumerate(b["lineas"], start=b["inicio"] + 1):
                    lineas_salida.append((fichero, k, l))
    for (fichero, i), tipo in sorted(clasificacion.items()):
        if (fichero, i) not in encontrados:
            informe.append(f"{fichero}: la clasificación del bloque nº {i} está obsoleta "
                           f"(ya no existe ese bloque)")

    for fichero, lista in instrucciones.items():
        for s in lista:
            if not any(s in l for f, _, l in lineas_salida if f == fichero):
                informe.append(f"{fichero}: la instrucción declarada no figura en ninguna "
                               f"plantilla de salida: {s!r}")

    literales = [e["es"] for e in entradas]
    for fichero, n, linea in lineas_salida:
        if not linea.strip():
            continue
        trabajo = linea
        piezas = sorted(literales + instrucciones.get(fichero, []), key=len, reverse=True)
        for p in piezas:
            trabajo = trabajo.replace(p, " ")
        for lista in re.findall(r"\[[^\[\]]*(?: / | \| )[^\[\]]*\]", trabajo):
            informe.append(f"{fichero}:{n}: lista de opciones sin clave: {lista!r}")
        palabras = re.findall(r"[^\W\d_]+", trabajo)
        if palabras:
            informe.append(f"{fichero}:{n}: texto visible sin clave: {' '.join(palabras)!r} "
                           f"(línea: {linea.strip()!r})")

    for e in entradas:
        if not any(e["es"] in l for _, _, l in lineas_salida):
            informe.append(f"literal huérfano `{e['clave']}`: ya no figura en ninguna plantilla de salida")
    return informe


# ── CLI ─────────────────────────────────────────────────────────────────────

def main(argv):
    if len(argv) != 2 or argv[1] not in ("escribir", "comprobar"):
        print(__doc__)
        return 2
    fuentes = fuentes_reales()
    try:
        texto = generar(fuentes)
        problemas = cobertura(fuentes)
    except ErrorExtraccion as e:
        print("✗", e)
        return 1
    if argv[1] == "escribir":
        CATALOGO_ES.write_text(texto, encoding="utf-8")
        print(f"escrito {CATALOGO_ES.relative_to(RAIZ)}")
        for p in problemas:
            print("✗", p)
        return 1 if problemas else 0
    desfasado = (not CATALOGO_ES.is_file()
                 or CATALOGO_ES.read_text(encoding="utf-8") != texto)
    if desfasado:
        problemas.insert(0, "i18n-es.md falta o está desfasado: `python3 tools/extraer_es.py escribir`")
    for p in problemas:
        print("✗", p)
    print("OK: i18n-es.md está en sincronía y todos los literales tienen clave"
          if not problemas else f"{len(problemas)} problema(s)")
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
