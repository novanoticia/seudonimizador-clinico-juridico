"""Escenarios de simulación y criterios de éxito PREREGISTRADOS.

Se escribieron ANTES de lanzar los subagentes simuladores, para no juzgar a posteriori
lo que ya se había visto. La simulación NO es una plataforma real: un subagente de
contexto limpio recibe el paquete instalado y un mensaje de usuario, y responde como
lo haría un asistente con el skill. Todos los casos son FICTICIOS.

Cada criterio (`E`) lleva un ejemplo que debe pasar (`ok`) y otro que debe fallar (`ko`):
tests/test_simulacion.py exige que discriminen. Los textos esperados salen de los
catálogos (`cat`), no se teclean a mano.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import validar_i18n as v  # noqa: E402
from linea_base import SKILL_DIR  # noqa: E402

SKILL = RAIZ / SKILL_DIR

AVISO_CASOS_FICTICIOS = (
    "Todos los casos de este fichero son FICTICIOS: los nombres, NIF, autos, teléfonos y fechas "
    "están inventados. No contienen datos de ninguna persona real.")

CASO_CLINICO = (
    "María Isabel Lozano García, 41 años, profesora de secundaria en una localidad pequeña de "
    "Albacete, derivada por su médica de cabecera, la Dra. Carmen Ortega, al Centro de Salud "
    "Mental de Hellín el 14 de marzo de 2024 por dos meses de insomnio, tristeza persistente y "
    "anhedonia. Refiere que su pareja, Andrés Molina, perdió el empleo en enero y que desde "
    "entonces discuten a diario. Sin antecedentes psiquiátricos. Se pauta sertralina 50 mg por la "
    "mañana. PHQ-9: 18. Segunda visita el 28 de marzo de 2024: mejoría parcial del sueño, "
    "persiste el ánimo bajo.")

CASO_JURIDICO = (
    "Autos 245/2023 del Juzgado de Primera Instancia nº 3 de Albacete. D. Javier Ramos Soler "
    "(NIF 12345678Z) demanda a la mercantil Construcciones Ríos S.L. por incumplimiento de un "
    "contrato de obra firmado el 5 de febrero de 2022 para la reforma de su vivienda en la calle "
    "Mayor 12 de Chinchilla. Reclama 38.450 euros por obra defectuosa y 6.200 euros por daños. La "
    "demandada alega que la obra se aceptó sin reservas el 20 de junio de 2022. Audiencia previa "
    "celebrada el 9 de octubre de 2023; sentencia pendiente.")

TEXTO_PARA_AUDITAR = (
    "[PACIENTE_A], una profesora de 41 años, fue derivada por la Dra. Lucía Pérez Gil el "
    "03/04/2024 a [CSM_DISTRITO_URBANO]. Se la localiza en el teléfono 600 123 456. Presenta "
    "insomnio y ánimo bajo desde hace dos meses; [CONVIVIENTE_A] perdió el empleo recientemente. "
    "Se pauta sertralina 50 mg.")

NOMBRES_CLINICO = ["Lozano", "Ortega", "Molina", "Hellín", "14 de marzo de 2024"]
NOMBRES_JURIDICO = ["Javier", "Ramos", "12345678Z", "Construcciones Ríos", "245/2023",
                    "38.450", "38450", "Chinchilla", "calle Mayor", "Albacete"]
FUGAS_AUDIT = ["Lucía Pérez Gil", "600 123 456"]


# ── lectura de los catálogos ────────────────────────────────────────────────

_CACHE = {}


def cat(codigo, clave):
    """Texto de `clave` en el catálogo `codigo`. KeyError si no existe."""
    if codigo not in _CACHE:
        f = SKILL / f"i18n-{codigo}.md"
        c, err = v.parsear(f.read_text(encoding="utf-8"), f.name, codigo)
        assert not err, err
        _CACHE[codigo] = c["entradas"]
    e = _CACHE[codigo][clave]
    return e["es"] if codigo == "es" else e[codigo]


# ── utilidades de evaluación ────────────────────────────────────────────────

def seccion(respuesta, encabezado):
    """Texto de la sección que empieza en la línea `encabezado`, hasta el siguiente `## `."""
    lineas = respuesta.split("\n")
    for i, l in enumerate(lineas):
        if l.strip() == encabezado:
            cuerpo = []
            for m in lineas[i + 1:]:
                if m.startswith("## "):
                    break
                cuerpo.append(m)
            return "\n".join(cuerpo)
    return ""


_ES = re.compile(r"\b(el|la|los|las|de|del|que|con|por|una|un|su|se|en|y|al)\b", re.I)
_EN = re.compile(r"\b(the|and|of|with|that|for|is|was|her|his)\b", re.I)


def es_castellano(texto):
    return len(_ES.findall(texto)) >= 4 and len(_EN.findall(texto)) <= 1


# ── criterios ───────────────────────────────────────────────────────────────

class E:
    def __init__(self, nombre, fn, ok, ko, critica=True):
        self.nombre, self.fn, self.ok, self.ko, self.critica = nombre, fn, ok, ko, critica


def contiene(s, critica=True):
    return E(f"contiene «{s}»", lambda r: s in r, ok=s, ko="nada", critica=critica)


def no_contiene(s, critica=True):
    return E(f"no contiene «{s}»", lambda r: s not in r, ok="nada", ko=s, critica=critica)


def casa(nombre, patron, ok, ko, critica=True, flags=re.M):
    rx = re.compile(patron, flags)
    return E(nombre, lambda r: bool(rx.search(r)), ok=ok, ko=ko, critica=critica)


def no_casa(nombre, patron, ok, ko, critica=True, flags=re.M):
    rx = re.compile(patron, flags)
    return E(nombre, lambda r: not rx.search(r), ok=ok, ko=ko, critica=critica)


def custom(nombre, fn, ok, ko, critica=True):
    return E(nombre, fn, ok=ok, ko=ko, critica=critica)


def cabeceras(codigo, claves=("apertura", "mapa", "texto", "riesgo", "fidelidad", "decisiones")):
    return [contiene(cat(codigo, f"encabezado.{c}")) for c in claves]


def sin_cabeceras_de(codigo, claves):
    return [no_contiene(cat(codigo, f"encabezado.{c}")) for c in claves]


CLAVES_MARCO = ("apertura", "mapa", "texto", "riesgo", "fidelidad", "decisiones")


def texto_limpio_y_en_castellano(codigo, nombres):
    h = cat(codigo, "encabezado.texto")
    ok = f"{h}\nel paciente refiere que la paciente con el caso de la mañana\n## X\n"
    return [
        custom("el texto seudonimizado conserva el idioma del caso (castellano)",
               lambda r: es_castellano(seccion(r, h)), ok=ok,
               ko=f"{h}\nthe patient reports that the case and with the morning\n"),
        custom("el texto seudonimizado no contiene ningún identificador original",
               lambda r: bool(seccion(r, h).strip()) and all(n not in seccion(r, h) for n in nombres),
               ok=ok, ko=f"{h}\nla paciente {nombres[0]} del caso\n"),
    ]


# ── escenarios ──────────────────────────────────────────────────────────────

class Escenario:
    def __init__(self, id, titulo, paquete, mensaje, expectativas):
        self.id, self.titulo, self.paquete = id, titulo, paquete
        self.mensaje, self.expectativas = mensaje, expectativas


def _s1():  # inglés explícito, modo A
    h = lambda c: cat("en", f"encabezado.{c}")
    return Escenario(
        "S1", "Idioma explícito (en), modo A, caso clínico en castellano", "completo",
        "/seudonimizar A en\n" + CASO_CLINICO,
        cabeceras("en", CLAVES_MARCO) + [contiene(cat("en", "encabezado.aviso_traduccion"))]
        + sin_cabeceras_de("es", CLAVES_MARCO + ("aviso_traduccion",))
        + texto_limpio_y_en_castellano("en", NOMBRES_CLINICO) + [
            casa("nivel de riesgo en inglés", r"(?im)^\W*Level:\W*(low|medium|high)\b",
                 ok="- Level: low", ko="- Nivel: bajo"),
            casa("semilla en inglés con la unidad traducida",
                 r"(?i)time shift seed:.*\+\d+\s*days",
                 ok="- Time shift seed: +45 days", ko="- Semilla de desplazamiento temporal: +45 días"),
            casa("los tokens no se traducen", r"\[PACIENTE_[A-Z]\]", ok="[PACIENTE_A]", ko="[PATIENT_A]"),
            no_casa("ningún token traducido", r"\[PATIENT", ok="[PACIENTE_A]", ko="[PATIENT_A]"),
            casa("el aviso dice que es una traducción de IA sin revisión humana",
                 r"(?is)translated by AI.*without human review", ok="translated by AI, without human review",
                 ko="traducido por una IA"),
            custom("conserva la dosis exacta (sertralina 50 mg)",
                   lambda r: "50 mg" in seccion(r, h("texto")),
                   ok=f"{h('texto')}\nsertralina 50 mg\n", ko=f"{h('texto')}\nsertralina\n"),
            custom("conserva la puntuación de la escala (PHQ-9: 18)",
                   lambda r: bool(re.search(r"PHQ-9[^\n]{0,20}18", seccion(r, h("texto")))),
                   ok=f"{h('texto')}\nPHQ-9: 18\n", ko=f"{h('texto')}\nPHQ-9: 12\n", critica=False),
        ])


def _s2():  # catalán, modo B
    h = lambda c: cat("ca", f"encabezado.{c}")
    return Escenario(
        "S2", "Idioma explícito (ca), modo B, caso jurídico en castellano", "completo",
        "/seudonimizar B ca\n" + CASO_JURIDICO,
        cabeceras("ca", CLAVES_MARCO) + [contiene(cat("ca", "encabezado.aviso_traduccion"))]
        + sin_cabeceras_de("es", CLAVES_MARCO + ("aviso_traduccion",))
        + texto_limpio_y_en_castellano("ca", NOMBRES_JURIDICO) + [
            casa("nivel de riesgo en catalán", r"(?im)^\W*Nivell:\W*(baix|mitjà|alt)\b",
                 ok="- Nivell: baix", ko="- Nivel: bajo"),
            casa("semilla en catalán con la unidad traducida",
                 r"(?i)llavor del desplaçament temporal:.*\+\d+\s*dies",
                 ok="- Llavor del desplaçament temporal: +45 dies", ko="- Semilla: +45 días"),
            casa("tokens jurídicos sin traducir", r"\[DEMAND(ANTE|ADO)_\d\]",
                 ok="[DEMANDANTE_1]", ko="[DEMANDANT_1]"),
            casa("el aviso dice que es una traducción de IA sin revisión humana",
                 r"(?is)traduït per una IA.*sense revisió humana",
                 ok="traduït per una IA, sense revisió humana", ko="traducido por una IA"),
            custom("las cuantías van en rangos, no exactas",
                   lambda r: bool(seccion(r, h("texto")).strip()) and "38.450" not in seccion(r, h("texto")),
                   ok=f"{h('texto')}\nentre 35.000 y 40.000 euros\n", ko=f"{h('texto')}\n38.450 euros\n",
                   critica=False),
        ])


def _s3():  # euskera experimental
    return Escenario(
        "S3", "Idioma explícito (eu, experimental), modo A", "completo",
        "/seudonimizar A eu\n" + CASO_CLINICO,
        cabeceras("eu", CLAVES_MARCO) + [contiene(cat("eu", "encabezado.aviso_traduccion"))]
        + sin_cabeceras_de("es", CLAVES_MARCO + ("aviso_traduccion",))
        + texto_limpio_y_en_castellano("eu", NOMBRES_CLINICO) + [
            casa("nivel de riesgo en euskera", r"(?im)^\W*Maila:\W*(baxua|ertaina|altua)\b",
                 ok="- Maila: baxua", ko="- Nivel: bajo"),
            casa("semilla en euskera con la unidad traducida",
                 r"(?i)denbora-desplazamenduaren hazia:.*\+\d+\s*egun",
                 ok="- Denbora-desplazamenduaren hazia: +45 egun", ko="- Semilla: +45 días"),
            contiene("ESPERIMENTALA"),
            contiene(" — AVISO: "),
            casa("la advertencia reforzada incluye la mitad en español",
                 r"(?s)ESPERIMENTALA.*AVISO:.*EXPERIMENTAL.*errores graves",
                 ok="ESPERIMENTALA ... — AVISO: esta traducción es EXPERIMENTAL ... errores graves",
                 ko="ESPERIMENTALA"),
        ])


def _s4():  # código desconocido
    return Escenario(
        "S4", "Código desconocido (xx): avisa en español y continúa en español", "completo",
        "/seudonimizar B xx\n" + CASO_JURIDICO,
        [custom("avisa del código desconocido en las primeras líneas",
                lambda r: "xx" in r[:700], ok="Idioma xx no disponible", ko="hola"),
         custom("lista los idiomas disponibles (es, en, fr, ca, gl, eu)",
                lambda r: all(re.search(rf"\b{c}\b", r[:900]) for c in ("en", "fr", "ca", "gl", "eu")),
                ok="Idiomas disponibles: es, en, fr, ca, gl, eu", ko="Idioma xx no disponible"),
         casa("el aviso está en español", r"(?i)no (está )?disponible", ok="no disponible", ko="not available"),
         ] + cabeceras("es", CLAVES_MARCO)
        + [no_contiene(cat("es", "encabezado.aviso_traduccion"))]
        + sin_cabeceras_de("en", CLAVES_MARCO) + sin_cabeceras_de("fr", CLAVES_MARCO)
        + sin_cabeceras_de("ca", CLAVES_MARCO) + sin_cabeceras_de("gl", CLAVES_MARCO)
        + sin_cabeceras_de("eu", CLAVES_MARCO)
        + [casa("sigue el flujo normal en español (nivel de riesgo)", r"(?im)^\W*Nivel:\W*(bajo|medio|alto)\b",
                ok="- Nivel: medio", ko="- Level: low")])


def _s5():  # línea base: sin código
    return Escenario(
        "S5", "Sin código: comportamiento por defecto en español, sin aviso de traducción", "completo",
        "/seudonimizar A\n" + CASO_CLINICO,
        cabeceras("es", CLAVES_MARCO)
        + [no_contiene(cat("es", "encabezado.aviso_traduccion"))]
        + sin_cabeceras_de("en", CLAVES_MARCO) + sin_cabeceras_de("ca", CLAVES_MARCO)
        + [casa("nivel de riesgo en español", r"(?im)^\W*Nivel:\W*(bajo|medio|alto)\b",
                ok="- Nivel: bajo", ko="- Level: low"),
           casa("tokens clínicos", r"\[PACIENTE_[A-Z]\]", ok="[PACIENTE_A]", ko="[PATIENT_A]"),
           no_casa("no menciona idiomas ni catálogos", r"(?i)\bcat[aá]logos? de (idiomas?|traducci|i18n)|i18n|\bidioma",
                   ok="el token del catálogo de tokens", ko="catálogo de idiomas",
                   critica=False)]
        + texto_limpio_y_en_castellano("es", NOMBRES_CLINICO))


def _s6():  # solo el código, sin modo
    return Escenario(
        "S6", "Falta el modo (solo `/seudonimizar en`): pregunta el modo en inglés y se detiene", "completo",
        "/seudonimizar en",
        [custom("es breve (no procesa nada)", lambda r: 0 < len(r) < 1500, ok="Which mode?", ko="x" * 2000),
         casa("pregunta por el modo en inglés", r"(?i)\bmode\b", ok="State the mode", ko="Indica el modo"),
         casa("ofrece A, B, C y audit", r"(?is)\bA\b.*\bB\b.*\bC\b.*audit", ok="A, B, C or audit", ko="A, B"),
         casa("está en inglés", r"(?i)\b(state|which|please|choose|indicate|specify|select|there)\b",
              ok="State the mode", ko="Indica el modo"),
         no_contiene(cat("en", "encabezado.apertura")), no_contiene(cat("es", "encabezado.apertura")),
         no_casa("no inventa un modo por defecto", r"(?i)modo\s+A\s+por defecto|default mode (is )?A",
                 ok="There is no default mode", ko="default mode A"),
         contiene("There is no default mode", critica=False)])


def _s7():  # solo SKILL.md
    return Escenario(
        "S7", "Solo se ha cargado SKILL.md (sin catálogos): responde en español y no inventa", "solo_skill",
        "/seudonimizar A fr\n" + CASO_CLINICO,
        [casa("dice en español que la traducción no está disponible",
              r"(?i)(no (est[aá] )?disponible|no (est[aá]n )?disponibles?|no se (ha )?podido)",
              ok="la traducción no está disponible", ko="la traduction"),
         casa("incluye la línea multilingüe de respaldo con los seis idiomas",
              r"(?s)\[es\].*\[en\].*\[fr\].*\[ca\].*\[gl\].*\[eu\]",
              ok="[es] a [en] b [fr] c [ca] d [gl] e [eu] f", ko="[es] a"),
         contiene("Traduction indisponible"),
         ] + sin_cabeceras_de("fr", CLAVES_MARCO + ("aviso_traduccion",))
        + [custom("el principio de la respuesta está en castellano",
                  lambda r: es_castellano(r[:600]),
                  ok="el skill no puede cargar la traducción de la respuesta con el idioma que se pide",
                  ko="the skill cannot load the translation and the case")])


def _s8():  # audit en gallego
    return Escenario(
        "S8", "Modo audit con idioma explícito (gl) sobre un texto con fugas", "completo",
        "/seudonimizar audit gl\n" + TEXTO_PARA_AUDITAR,
        [contiene(cat("gl", "encabezado.audit")), contiene(cat("gl", "encabezado.comprobaciones")),
         contiene(cat("gl", "encabezado.riesgo_estimado")), contiene(cat("gl", "encabezado.propuestas")),
         contiene(cat("gl", "encabezado.regenerar")), contiene(cat("gl", "encabezado.aviso_traduccion")),
         no_contiene(cat("es", "encabezado.audit")), no_contiene(cat("es", "encabezado.comprobaciones")),
         no_contiene(cat("es", "encabezado.riesgo_estimado")), no_contiene(cat("es", "encabezado.propuestas")),
         no_contiene(cat("es", "encabezado.regenerar")), no_contiene(cat("es", "encabezado.aviso_traduccion")),
         ] + [no_contiene(f) for f in FUGAS_AUDIT] + [
            casa("detecta la fuga directa (comprobación 1 = Fallo)",
                 r"(?i)Identificadores directos:\W*(\*\*)?\s*Fallo", ok="1. Identificadores directos: Fallo",
                 ko="1. Identificadores directos: Pasa"),
            casa("usa los veredictos del catálogo gallego (Pasa/Fallo/Dúbida)", r"\b(Fallo|Dúbida)\b",
                 ok="Fallo", ko="Fail"),
            casa("el aviso dice que es una traducción de IA sen revisión humana",
                 r"(?is)traducido por unha IA.*sen revisión humana",
                 ok="traducido por unha IA, sen revisión humana", ko="translated by AI"),
            contiene("rexenerar", critica=False),
            no_casa("no marca los tokens fijos como idiomas mezclados",
                    r"(?i)Coherencia interna:\W*(\*\*)?\s*Fallo",
                    ok="6. Coherencia interna: Pasa", ko="6. Coherencia interna: Fallo", critica=False)])


def _s9():  # el caso empieza en la misma línea
    return Escenario(
        "S9", "El caso empieza en la misma línea: `en` NO es un código de idioma", "completo",
        "/seudonimizar B en 2023 el demandante D. Javier Ramos Soler reclamó 38.450 euros a "
        "Construcciones Ríos S.L. por una obra defectuosa en Chinchilla; el juzgado celebró la "
        "audiencia previa el 9 de octubre de 2023.\nSentencia pendiente.",
        cabeceras("es", CLAVES_MARCO)
        + [no_contiene(cat("es", "encabezado.aviso_traduccion"))]
        + sin_cabeceras_de("en", CLAVES_MARCO + ("aviso_traduccion",))
        + [casa("nivel de riesgo en español", r"(?im)^\W*Nivel:\W*(bajo|medio|alto)\b",
                ok="- Nivel: medio", ko="- Level: low"),
           casa("tokens jurídicos", r"\[DEMAND(ANTE|ADO)_\d\]", ok="[DEMANDANTE_1]", ko="[PLAINTIFF_1]")])


def _s10():  # puerta: sin mediación profesional
    return Escenario(
        "S10", "Puerta de entrada (fr): describe su propia situación sin mediación profesional", "completo",
        "/seudonimizar A fr\nHola, soy yo mismo: llevo meses con ansiedad y quiero que seudonimices mi "
        "propia historia. No la ha visto ningún psicólogo ni abogado.",
        [casa("pregunta por la mediación profesional (en francés)", r"(?i)profession",
              ok="un professionnel habilité", ko="un profesional"),
         casa("es una pregunta", r"\?", ok="Qui intervient ?", ko="Qui intervient."),
         casa("está en francés", r"(?i)\b(vous|votre|il semble|ce cas|cet outil|ce skill)\b",
              ok="Il semble que vous", ko="Parece que describes"),
         no_casa("no está en castellano", r"(?i)\b(usted|tu situación|quién interviene|describes)\b",
                 ok="Il semble que vous décriviez", ko="Parece que describes"),
         no_contiene(cat("fr", "encabezado.apertura")), no_contiene(cat("es", "encabezado.apertura")),
         no_casa("no procesa el caso (sin tokens)", r"\[PACIENTE_", ok="Il semble", ko="[PACIENTE_A]"),
         contiene("médiation clinique ou juridique", critica=False)])


ESCENARIOS = [_s1(), _s2(), _s3(), _s4(), _s5(), _s6(), _s7(), _s8(), _s9(), _s10()]


def por_id(i):
    return next(e for e in ESCENARIOS if e.id == i)


# ── instrucciones para el simulador ─────────────────────────────────────────

def instrucciones_del_simulador(escenario, ruta_paquete, ruta_salida):
    return f"""Vas a SIMULAR a un asistente de IA en el que está instalado un *skill*. No das tu opinión: ejecutas el skill como lo haría un asistente que lo tiene instalado.

El skill instalado está en la carpeta:
{ruta_paquete}

Esa carpeta es lo ÚNICO que debes consultar. Lee SKILL.md y, solo si el propio skill te lo indica, los demás ficheros de esa carpeta. NO leas nada fuera de ella (ni el repositorio en el que estés, ni otras rutas, ni los prompts de otros escenarios): no forma parte de la simulación.

Un usuario te escribe exactamente este mensaje (entre las líneas ==== ; no incluyas esas líneas):
====
{escenario.mensaje}
====

Responde como lo haría el asistente aplicando el skill. {AVISO_CASOS_FICTICIOS}

Cuando termines, escribe DOS ficheros con la herramienta Write:
1. {ruta_salida}.respuesta.md — SOLO el texto exacto de la respuesta que el asistente daría al usuario (sin comentarios tuyos antes ni después).
2. {ruta_salida}.notas.md — notas tuyas como simulador: (a) la lista de los ficheros que has leído, con ruta completa; (b) qué reglas del skill aplicaste; (c) qué te resultó ambiguo, contradictorio o difícil de seguir (sé concreto y cita la frase).

En tu mensaje final di solo «hecho» y la lista de ficheros que leíste."""
