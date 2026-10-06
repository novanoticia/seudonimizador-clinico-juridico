#!/usr/bin/env python3
"""Validador de catálogos i18n del skill.

Un catálogo es un fichero `i18n-<código>.md` junto al SKILL.md. `i18n-es.md` es la
REFERENCIA: sus literales se extraen del original y no se reescriben. Cada otro
idioma debe tener exactamente las mismas claves.

Formato (valores siempre en UNA línea):

    # i18n-en — Catálogo
    - código: en
    - estado: borrador-ia-sin-revision-humana | revisado     (es: referencia)
    - redactado-por: IA
    - revisado-por: nadie
    - fecha-revision: —

    ## Glosario
    - término → traducción

    ## Frases
    ### encabezado.apertura
    origen: original | nuevo
    fuente: flujo.md            (solo `original`)
    seguridad: sí | no
    es: ## APERTURA
    en: ## OPENING
    invariable: sí              (solo si la traducción es igual a propósito)

Uso:  python3 tools/validar_i18n.py [directorio]    (sale con 1 si hay errores)
Solo biblioteca estándar.
"""
import datetime
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from linea_base import FICHEROS_MD, RAIZ, SKILL_DIR, quitar_bloques  # noqa: E402

FICHERO_RE = re.compile(r"^i18n-([a-z]{2,3})\.md$")
CLAVE_RE = re.compile(r"^[a-z0-9_]+(\.[a-z0-9_]+)+$")
CAMPO_RE = re.compile(r"^([a-z][a-z-]*): ?(.*)$")
CABECERA_RE = re.compile(r"^- ([\wáéíóúñ-]+): ?(.*)$")
GLOSARIO_RE = re.compile(r"^- (.+?) → (.*)$")
FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MARCADOR_RE = re.compile(r"\{[^{}]*\}")
MARCADOR_VALIDO_RE = re.compile(r"^\{[a-z_][a-z0-9_]*\}$")
PENDIENTE_RE = re.compile(r"\b(TODO|XXX|FIXME)\b|\?\?\?")
ESTADOS = {"borrador-ia-sin-revision-humana", "revisado"}


# ── texto contractual ───────────────────────────────────────────────────────

def contrato(texto):
    """Lo que NO puede cambiar al traducir, extraído de un literal."""
    sin_ticks = re.sub(r"`[^`]*`", "", texto)
    return {
        "codigo": sorted(re.findall(r"`[^`]*`", texto)),
        "tokens": sorted(re.findall(r"\[[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9_]+\]", texto)),
        "modos": [[x.strip() for x in g.split("|")]
                  for g in re.findall(r"\[([^\[\]`]*\|[^\[\]`]*)\]", sin_ticks)],
        "opciones": [len(g.split("/")) for g in
                     re.findall(r"\[([^\[\]`|]*/[^\[\]`|]*)\]", sin_ticks)],
        "marcadores": sorted(m for m in MARCADOR_RE.findall(texto)
                             if MARCADOR_VALIDO_RE.match(m)),
    }


def errores_de_llaves(texto):
    """Las llaves solo valen como marcadores con nombre: {nombre}."""
    informe = []
    for m in MARCADOR_RE.findall(texto):
        if not MARCADOR_VALIDO_RE.match(m):
            informe.append(f"marcador inválido `{m}` (solo `{{nombre}}`)")
    resto = MARCADOR_RE.sub("", texto)
    if "{" in resto or "}" in resto:
        informe.append("llave suelta")
    return informe


# ── lectura de un catálogo ──────────────────────────────────────────────────

def parsear(texto, fichero, codigo):
    """Devuelve (catalogo, errores). `codigo` es el del nombre del fichero."""
    cab, glosario, entradas, errores = {}, {}, {}, []
    seccion, actual = "cabecera", None
    campos_ok = {"origen", "fuente", "seguridad", "es", codigo, "invariable"}

    for n, linea in enumerate(texto.split("\n"), start=1):
        if linea.startswith("# ") and n == 1:
            continue
        if linea.startswith("## "):
            nombre = linea[3:].strip()
            if nombre == "Glosario":
                seccion = "glosario"
            elif nombre == "Frases":
                seccion = "frases"
            else:
                errores.append(f"{fichero}:{n}: sección desconocida `{nombre}`")
            actual = None
            continue
        if linea.strip() == "":
            continue
        if seccion == "cabecera":
            m = CABECERA_RE.match(linea)
            if m:
                cab[m.group(1)] = m.group(2).strip()
            else:
                errores.append(f"{fichero}:{n}: línea no reconocida en la cabecera")
        elif seccion == "glosario":
            m = GLOSARIO_RE.match(linea)
            if not m:
                errores.append(f"{fichero}:{n}: glosario: línea no reconocida")
            elif not m.group(2).strip():
                errores.append(f"{fichero}:{n}: glosario: traducción vacía de `{m.group(1)}`")
                glosario[m.group(1)] = ""
            else:
                glosario[m.group(1)] = m.group(2).strip()
        else:  # frases
            if linea.startswith("### "):
                clave = linea[4:].strip()
                if not CLAVE_RE.match(clave):
                    errores.append(f"{fichero}:{n}: clave inválida `{clave}`")
                if clave in entradas:
                    errores.append(f"{fichero}:{n}: clave duplicada `{clave}`")
                actual = entradas.setdefault(clave, {"_linea": n})
                continue
            m = CAMPO_RE.match(linea)
            if actual is None or not m:
                errores.append(f"{fichero}:{n}: línea no reconocida "
                               f"(cada valor va en una sola línea)")
                continue
            campo, valor = m.group(1), m.group(2)
            if campo not in campos_ok:
                errores.append(f"{fichero}:{n}: campo desconocido `{campo}`")
            actual[campo] = valor
    return {"cabecera": cab, "glosario": glosario, "entradas": entradas}, errores


# ── validación por catálogo ─────────────────────────────────────────────────

def validar_cabecera(fichero, codigo, cab):
    informe = []
    if cab.get("código") != codigo:
        informe.append(f"{fichero}: el `código` ({cab.get('código')!r}) no coincide "
                       f"con el del nombre del fichero ({codigo!r})")
    estado = cab.get("estado")
    if codigo == "es":
        if estado != "referencia":
            informe.append(f"{fichero}: el estado de la referencia debe ser `referencia`")
        return informe
    for campo in ("redactado-por", "revisado-por", "fecha-revision"):
        if not cab.get(campo):
            informe.append(f"{fichero}: falta `{campo}` en la cabecera")
    if estado not in ESTADOS:
        informe.append(f"{fichero}: estado desconocido {estado!r} (válidos: {sorted(ESTADOS)})")
        return informe
    revisor = cab.get("revisado-por", "")
    if estado == "borrador-ia-sin-revision-humana" and revisor not in ("nadie", ""):
        informe.append(f"{fichero}: estado borrador con revisor `{revisor}`: "
                       f"si alguien lo revisó, el estado es `revisado`")
    if estado == "revisado":
        if revisor in ("nadie", "—", ""):
            informe.append(f"{fichero}: estado revisado sin revisor (`revisado-por`)")
        fecha = cab.get("fecha-revision", "")
        try:
            if not FECHA_RE.match(fecha):
                raise ValueError
            datetime.date.fromisoformat(fecha)
        except ValueError:
            informe.append(f"{fichero}: estado revisado sin fecha válida (AAAA-MM-DD)")
    return informe


def validar_entradas_referencia(fichero, entradas, fuentes):
    informe, vistos = [], {}
    for clave, e in entradas.items():
        pref = f"{fichero}: {clave}"
        origen, seg = e.get("origen"), e.get("seguridad")
        if origen not in ("original", "nuevo"):
            informe.append(f"{pref}: origen inválido {origen!r} (`original` o `nuevo`)")
        if seg not in ("sí", "no"):
            informe.append(f"{pref}: seguridad inválida {seg!r} (`sí` o `no`)")
        literal = e.get("es", "")
        if not literal.strip():
            informe.append(f"{pref}: literal es vacío")
            continue
        if literal in vistos:
            informe.append(f"{pref}: un literal, una clave: el mismo texto está en `{vistos[literal]}`")
        vistos[literal] = clave
        fuente = e.get("fuente")
        if origen == "original":
            if not fuente:
                informe.append(f"{pref}: un literal `original` necesita `fuente`")
            elif fuente not in fuentes:
                informe.append(f"{pref}: fuente `{fuente}` inexistente")
            elif literal not in fuentes[fuente]:
                informe.append(f"{pref}: el literal no figura en la fuente `{fuente}`")
        elif origen == "nuevo" and fuente:
            informe.append(f"{pref}: un literal `nuevo` no lleva `fuente`")
        informe += [f"{pref}: {x}" for x in errores_de_llaves(literal)]
    return informe


def validar_traduccion(fichero, codigo, ref, cat):
    informe = []
    for clave, e in cat["entradas"].items():
        r = ref["entradas"].get(clave)
        if r is None:
            continue
        pref = f"{fichero}: {clave}"
        for campo in ("origen", "seguridad", "fuente"):
            if e.get(campo) != r.get(campo):
                informe.append(f"{pref}: `{campo}` distinto del de la referencia "
                               f"({e.get(campo)!r} frente a {r.get(campo)!r})")
        if e.get("es") != r.get("es"):
            informe.append(f"{pref}: el literal `es` difiere de la referencia i18n-es.md")
        tr = e.get(codigo)
        if tr is None:
            informe.append(f"{pref}: falta el campo `{codigo}`")
            continue
        if not tr.strip():
            informe.append(f"{pref}: traducción vacía")
            continue
        if tr != tr.strip():
            informe.append(f"{pref}: espacios sobrantes al principio o al final")
        if PENDIENTE_RE.search(tr):
            informe.append(f"{pref}: marca de pendiente en la traducción")
        informe += [f"{pref}: {x}" for x in errores_de_llaves(tr)]
        original = r.get("es", "")
        a, b = contrato(original), contrato(tr)
        for clave_c, etiqueta in (("codigo", "código entre comillas invertidas"),
                                  ("tokens", "token entre corchetes"),
                                  ("modos", "lista con `|`")):
            if a[clave_c] != b[clave_c]:
                informe.append(f"{pref}: texto contractual distinto ({etiqueta})")
        if a["marcadores"] != b["marcadores"]:
            informe.append(f"{pref}: marcador `{{nombre}}` distinto del original")
        if a["opciones"] != b["opciones"]:
            informe.append(f"{pref}: listas de opciones con distinto número de entradas "
                           f"({a['opciones']} frente a {b['opciones']})")
        invariable = e.get("invariable") == "sí"
        if tr == original and not invariable:
            informe.append(f"{pref}: traducción idéntica al español "
                           f"(si es a propósito, añade `invariable: sí`)")
        if invariable and tr != original:
            informe.append(f"{pref}: `invariable: sí` pero la traducción difiere del español")
    return informe


# ── validación del directorio ───────────────────────────────────────────────

def validar_directorio(directorio, fuentes):
    directorio = Path(directorio)
    informe, catalogos = [], {}
    for f in sorted(directorio.glob("i18n-*.md")):
        m = FICHERO_RE.match(f.name)
        if not m:
            informe.append(f"{f.name}: nombre de fichero no válido (esperado i18n-<código>.md, "
                           f"código de 2–3 letras en minúscula)")
            continue
        codigo = m.group(1)
        cat, errores = parsear(f.read_text(encoding="utf-8"), f.name, codigo)
        informe += errores + validar_cabecera(f.name, codigo, cat["cabecera"])
        catalogos[codigo] = (f.name, cat)

    if not catalogos:
        return informe
    if "es" not in catalogos:
        informe.append("falta la referencia i18n-es.md (los demás catálogos se validan contra ella)")
        return informe

    nombre_es, ref = catalogos["es"]
    informe += validar_entradas_referencia(nombre_es, ref["entradas"], fuentes)
    claves_es = set(ref["entradas"])
    for codigo, (nombre, cat) in sorted(catalogos.items()):
        if codigo == "es":
            continue
        claves = set(cat["entradas"])
        if claves_es - claves:
            informe.append(f"{nombre}: faltan {len(claves_es - claves)} clave(s): "
                           + ", ".join(sorted(claves_es - claves)))
        if claves - claves_es:
            informe.append(f"{nombre}: sobran {len(claves - claves_es)} clave(s) "
                           f"que no están en la referencia: " + ", ".join(sorted(claves - claves_es)))
        informe += validar_traduccion(nombre, codigo, ref, cat)
        for t in sorted(set(ref["glosario"]) - set(cat["glosario"])):
            informe.append(f"{nombre}: glosario: falta el término `{t}`")
        for t in sorted(set(cat["glosario"]) - set(ref["glosario"])):
            informe.append(f"{nombre}: glosario: sobra el término `{t}` (no está en la referencia)")
    return informe


# ── fuentes reales ──────────────────────────────────────────────────────────

def fuentes_desde_textos(textos):
    """{fichero: texto} sin los bloques i18n: lo que cuenta como 'original'."""
    res = {}
    for nombre, t in textos.items():
        resto, _ = quitar_bloques(t.split("\n"))
        res[nombre] = "\n".join(resto)
    return res


def fuentes_reales(raiz=RAIZ):
    base = Path(raiz) / SKILL_DIR
    return fuentes_desde_textos(
        {f: (base / f).read_text(encoding="utf-8") for f in FICHEROS_MD})


def validar_arbol_real(raiz=RAIZ):
    return validar_directorio(Path(raiz) / SKILL_DIR, fuentes_reales(raiz))


def main(argv):
    directorio = Path(argv[1]) if len(argv) > 1 else RAIZ / SKILL_DIR
    informe = validar_directorio(directorio, fuentes_reales())
    for l in informe:
        print("✗", l)
    idiomas = sorted(p.stem.removeprefix("i18n-") for p in directorio.glob("i18n-*.md"))
    if informe:
        print(f"{len(informe)} problema(s). Idiomas encontrados: {', '.join(idiomas) or 'ninguno'}")
        return 1
    print("OK: " + (f"catálogos válidos ({', '.join(idiomas)})" if idiomas
                    else "no hay catálogos que validar"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
