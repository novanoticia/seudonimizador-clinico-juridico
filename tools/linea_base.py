#!/usr/bin/env python3
"""Línea base del idioma por defecto (español).

Criterio de éxito principal del proyecto multiidioma: el español no cambia.
Esta herramienta captura una huella del original en un commit concreto y
comprueba después que el árbol de trabajo solo difiere en lo permitido:

  * ADICIONES dentro de bloques delimitados por <!-- i18n:inicio --> y
    <!-- i18n:fin --> (más UNA línea en blanco inmediatamente posterior, si la
    hay y no es el salto final del fichero).
  * Las líneas listadas, una a una, en tests/baseline/reemplazos.txt.
  * La clave `version` de los manifiestos.
  * Ficheros nuevos `i18n-<código>.md` en el paquete.

Solo biblioteca estándar. Uso:

    python3 tools/linea_base.py capturar <commit>   # escribe tests/baseline/
    python3 tools/linea_base.py comparar            # sale con 1 si hay diferencias
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_BASE = RAIZ / "tests" / "baseline"
NOMBRE = "seudonimizador-clinico-juridico"
SKILL_DIR = f"skills/{NOMBRE}"
FICHEROS_MD = ["SKILL.md", "flujo.md", "auditoria.md",
               "plantilla-entrada.md", "plantilla-tokens.md"]
MANIFIESTOS = ["plugin.json", ".claude-plugin/plugin.json",
               ".claude-plugin/marketplace.json"]
INICIO = "<!-- i18n:inicio -->"
FIN = "<!-- i18n:fin -->"
PAQUETE_EXTRA_PERMITIDO = re.compile(rf"^{re.escape(NOMBRE)}/i18n-[a-z]{{2,3}}\.md$")


# ── utilidades ──────────────────────────────────────────────────────────────

def sha(texto):
    if isinstance(texto, str):
        texto = texto.encode("utf-8")
    return hashlib.sha256(texto).hexdigest()


def cargar(nombre):
    return json.loads((DIR_BASE / nombre).read_text(encoding="utf-8"))


def commit_base():
    return (DIR_BASE / "commit_base.txt").read_text().strip()


def git(*args, raiz=RAIZ):
    r = subprocess.run(["git", *args], cwd=raiz, capture_output=True, check=True)
    return r.stdout


def leer_reemplazos():
    """{fichero: {nº de línea del ORIGINAL (1-based) que puede cambiar}}."""
    res = {}
    f = DIR_BASE / "reemplazos.txt"
    if not f.is_file():
        return res
    for linea in f.read_text(encoding="utf-8").splitlines():
        linea = linea.split("#", 1)[0].strip()
        if not linea:
            continue
        fichero, n = linea.rsplit(":", 1)
        res.setdefault(fichero.strip(), set()).add(int(n))
    return res


# ── bloques delimitados ─────────────────────────────────────────────────────

def quitar_bloques(lineas):
    """Elimina los bloques i18n. `lineas` es texto.split("\\n").

    Devuelve (resto, errores). Tras el marcador de cierre se descarta una línea
    en blanco si la hay y no es el elemento final (el salto de línea del EOF).
    """
    resto, errores = [], []
    dentro, saltar_blanca = False, False
    ultimo = len(lineas) - 1
    for i, l in enumerate(lineas):
        marca = l.strip()
        if marca == INICIO:
            if dentro:
                errores.append(f"línea {i + 1}: marcador de inicio anidado")
            dentro = True
        elif marca == FIN:
            if not dentro:
                errores.append(f"línea {i + 1}: marcador de cierre sin inicio")
            dentro = False
            saltar_blanca = True
        elif dentro:
            continue
        else:
            if saltar_blanca and l == "" and i != ultimo:
                saltar_blanca = False
                continue
            saltar_blanca = False
            resto.append(l)
    if dentro:
        errores.append("bloque i18n sin cerrar")
    return resto, errores


# ── comparación de los .md ──────────────────────────────────────────────────

def comparar_md(nombre, texto, reemplazos=()):
    """Compara `texto` con la huella del original de `nombre`. [] si coincide."""
    base = cargar("lineas.json")[nombre]["sha256_lineas"]
    permitidas = set(reemplazos)
    resto, errores = quitar_bloques(texto.split("\n"))
    informe = [f"{nombre}: {e}" for e in errores]
    if len(resto) != len(base):
        informe.append(f"{nombre}: fuera de los bloques i18n hay {len(resto)} "
                       f"líneas y el original tiene {len(base)}")
        # Localiza la primera divergencia para que el mensaje sirva.
        for i, (a, b) in enumerate(zip(resto, base)):
            if sha(a) != b:
                informe.append(f"{nombre}: primera divergencia en la línea {i + 1} del original")
                break
        return informe
    for i, (l, h) in enumerate(zip(resto, base), start=1):
        if sha(l) != h and i not in permitidas:
            informe.append(f"{nombre}: la línea {i} del original ha cambiado "
                           f"y no está en reemplazos.txt")
    return informe


def comparar_con_git(nombre, texto):
    """Segunda vía: texto íntegro de `git show <commit_base>:<fichero>`."""
    original = git("show", f"{commit_base()}:{SKILL_DIR}/{nombre}").decode("utf-8")
    resto, errores = quitar_bloques(texto.split("\n"))
    informe = [f"{nombre}: {e}" for e in errores]
    permitidas = leer_reemplazos().get(nombre, set())
    base = original.split("\n")
    if len(resto) != len(base):
        informe.append(f"{nombre}: difiere de git show (nº de líneas)")
    else:
        for i, (a, b) in enumerate(zip(resto, base), start=1):
            if a != b and i not in permitidas:
                informe.append(f"{nombre}: la línea {i} difiere de git show")
    return informe


# ── frontmatter ─────────────────────────────────────────────────────────────

def frontmatter(texto):
    """Extrae claves, name y description (plegada) del frontmatter de SKILL.md."""
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    if not m:
        raise ValueError("SKILL.md sin frontmatter")
    claves, desc, en_desc, name = [], [], False, None
    for l in m.group(1).split("\n"):
        mk = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", l)
        if mk and not l.startswith(" "):
            en_desc = False
            claves.append(mk.group(1))
            if mk.group(1) == "name":
                name = mk.group(2).strip()
            if mk.group(1) == "description":
                en_desc = True
                resto = mk.group(2).strip()
                if resto and resto not in (">-", ">", "|", "|-"):
                    desc.append(resto)
        elif en_desc:
            desc.append(l.strip())
    return {"claves": claves, "name": name, "description": " ".join(desc).strip()}


def limites_description(desc):
    """Límites de plataforma, independientes de la línea base."""
    informe = []
    if len(desc) >= 500:
        informe.append(f"frontmatter: description de {len(desc)} "
                       f"caracteres (límite de Mistral: < 500)")
    if len(desc.encode("utf-8")) >= 1024:
        informe.append("frontmatter: description >= 1024 bytes (límite de Perplexity)")
    return informe


def comparar_frontmatter(texto):
    base = cargar("frontmatter.json")
    fm = frontmatter(texto)
    informe = []
    if fm["claves"] != base["claves"]:
        informe.append(f"frontmatter: claves {fm['claves']} != {base['claves']}")
    if fm["name"] != base["name"]:
        informe.append("frontmatter: `name` ha cambiado")
    if sha(fm["description"]) != base["description_sha256"]:
        informe.append("frontmatter: `description` ha cambiado")
    return informe + limites_description(fm["description"])


# ── manifiestos ─────────────────────────────────────────────────────────────

def normalizar_manifiesto(dato):
    """Quita `version` (raíz y plugins[]), el único campo que puede cambiar."""
    d = json.loads(json.dumps(dato))
    d.pop("version", None)
    for p in d.get("plugins", []):
        p.pop("version", None)
    return d


def comparar_manifiesto_dato(nombre, dato):
    base = cargar("manifiestos.json")[nombre]
    if normalizar_manifiesto(dato) != base:
        return [f"{nombre}: ha cambiado algo distinto de `version`"]
    return []


def comparar_manifiestos(raiz=RAIZ):
    informe = []
    for f in MANIFIESTOS:
        dato = json.loads((Path(raiz) / f).read_text(encoding="utf-8"))
        informe += comparar_manifiesto_dato(f, dato)
    return informe


# ── paquete (zip) ───────────────────────────────────────────────────────────

def construir_paquete(raiz):
    """Copia `raiz` a un temporal, ejecuta scripts/build-dist.sh y devuelve
    {"miembros": {ruta: texto|sha}, "skill_igual_zip": bool}."""
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp) / "r"
        shutil.copytree(raiz, copia, ignore=shutil.ignore_patterns(
            ".git", "dist", "__pycache__"))
        subprocess.run(["bash", "scripts/build-dist.sh"], cwd=copia,
                       capture_output=True, check=True)
        z, s = copia / "dist" / f"{NOMBRE}.zip", copia / "dist" / f"{NOMBRE}.skill"
        miembros = {}
        with zipfile.ZipFile(z) as zf:
            for n in sorted(zf.namelist()):
                if n.endswith("/"):
                    continue
                datos = zf.read(n)
                miembros[n] = {"sha256": sha(datos),
                               "texto": datos.decode("utf-8") if n.endswith(".md") else None}
        return {"miembros": miembros,
                "skill_igual_zip": z.read_bytes() == s.read_bytes()}


def exportar_commit(commit, destino):
    tar = subprocess.run(["git", "archive", commit], cwd=RAIZ,
                         capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(destino)], input=tar, check=True)


def comparar_paquete(raiz=RAIZ):
    base = cargar("paquete.json")
    actual = construir_paquete(raiz)
    informe = []
    if not actual["skill_igual_zip"]:
        informe.append("paquete: el .skill no es copia exacta del .zip")
    miembros = actual["miembros"]
    for ruta, h in base["miembros"].items():
        if ruta not in miembros:
            informe.append(f"paquete: falta {ruta}")
            continue
        if ruta.endswith(".md"):
            nombre = ruta.rsplit("/", 1)[1]
            informe += [f"paquete/{e}" for e in
                        comparar_md(nombre, miembros[ruta]["texto"],
                                    leer_reemplazos().get(nombre, set()))]
        elif miembros[ruta]["sha256"] != h:
            informe.append(f"paquete: {ruta} ha cambiado")
    for ruta in miembros:
        if ruta not in base["miembros"] and not PAQUETE_EXTRA_PERMITIDO.match(ruta):
            informe.append(f"paquete: fichero inesperado {ruta}")
    return informe


# ── todo junto ──────────────────────────────────────────────────────────────

def comparar_todo(raiz=RAIZ):
    raiz = Path(raiz)
    informe = []
    reemplazos = leer_reemplazos()
    for f in FICHEROS_MD:
        texto = (raiz / SKILL_DIR / f).read_text(encoding="utf-8")
        informe += comparar_md(f, texto, reemplazos.get(f, set()))
    informe += comparar_frontmatter(
        (raiz / SKILL_DIR / "SKILL.md").read_text(encoding="utf-8"))
    informe += comparar_manifiestos(raiz)
    informe += comparar_paquete(raiz)
    return informe


# ── captura ─────────────────────────────────────────────────────────────────

def capturar(commit):
    """Escribe tests/baseline/ a partir de `commit` (NO del árbol de trabajo)."""
    commit = git("rev-parse", "--verify", commit + "^{commit}").decode().strip()
    DIR_BASE.mkdir(parents=True, exist_ok=True)
    (DIR_BASE / "commit_base.txt").write_text(commit + "\n")

    lineas = {}
    for f in FICHEROS_MD:
        texto = git("show", f"{commit}:{SKILL_DIR}/{f}").decode("utf-8")
        ls = texto.split("\n")
        lineas[f] = {"lineas": len(ls), "sha256_fichero": sha(texto),
                     "sha256_lineas": [sha(l) for l in ls]}
        if f == "SKILL.md":
            fm = frontmatter(texto)
            (DIR_BASE / "frontmatter.json").write_text(json.dumps({
                "claves": fm["claves"], "name": fm["name"],
                "description_sha256": sha(fm["description"]),
                "description_caracteres": len(fm["description"]),
                "description_bytes": len(fm["description"].encode("utf-8")),
            }, indent=1, ensure_ascii=False) + "\n")
    (DIR_BASE / "lineas.json").write_text(
        json.dumps(lineas, indent=1, sort_keys=True) + "\n")

    manifiestos = {}
    for f in MANIFIESTOS:
        manifiestos[f] = normalizar_manifiesto(
            json.loads(git("show", f"{commit}:{f}").decode("utf-8")))
    (DIR_BASE / "manifiestos.json").write_text(
        json.dumps(manifiestos, indent=1, sort_keys=True, ensure_ascii=False) + "\n")

    with tempfile.TemporaryDirectory() as tmp:
        exportar_commit(commit, tmp)
        paq = construir_paquete(tmp)
    (DIR_BASE / "paquete.json").write_text(json.dumps({
        "skill_igual_zip": paq["skill_igual_zip"],
        "miembros": {n: m["sha256"] for n, m in paq["miembros"].items()},
    }, indent=1, sort_keys=True) + "\n")

    if not (DIR_BASE / "reemplazos.txt").exists():
        (DIR_BASE / "reemplazos.txt").write_text(
            "# Lista cerrada de líneas del ORIGINAL que pueden cambiar.\n"
            "# Formato: fichero.md:nº_de_línea_del_original   # justificación\n"
            "# Vacía a propósito: la Fase 1.4 aprobó solo ADICIONES.\n")
    print(f"línea base capturada desde {commit}")


def main(argv):
    if len(argv) >= 3 and argv[1] == "capturar":
        capturar(argv[2])
        return 0
    if len(argv) == 2 and argv[1] == "comparar":
        informe = comparar_todo()
        for l in informe:
            print("✗", l)
        print("OK: el español coincide con la línea base" if not informe
              else f"{len(informe)} diferencia(s)")
        return 1 if informe else 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
