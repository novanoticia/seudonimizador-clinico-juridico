"""Pruebas del validador de catálogos i18n.

Se escriben ANTES que los catálogos reales. Casi todas son sintéticas: fabrican
catálogos rotos a propósito y exigen que el validador falle (un validador que
nunca falla no valida nada).

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import validar_i18n as v  # noqa: E402

# Texto "original" ficticio contra el que se comprueban los literales `original`.
FUENTE = {
    "flujo.md": (
        "## APERTURA\n"
        "- Modo: [A | B | C]\n"
        "- Nivel: [bajo / medio / alto]\n"
        "Usa `[DATO_ELIMINADO]` cuando proceda.\n"
        "Marcadores usados: {n} en total\n"
    ),
}

# (clave, origen, fuente, seguridad, es, en, invariable)
ENTRADAS = [
    ("encabezado.apertura", "original", "flujo.md", "no",
     "## APERTURA", "## OPENING", False),
    ("campo.modo", "original", "flujo.md", "no",
     "- Modo: [A | B | C]", "- Mode: [A | B | C]", False),
    ("campo.nivel", "original", "flujo.md", "no",
     "- Nivel: [bajo / medio / alto]", "- Level: [low / medium / high]", False),
    ("marcador.eliminado", "original", "flujo.md", "sí",
     "Usa `[DATO_ELIMINADO]` cuando proceda.",
     "Use `[DATO_ELIMINADO]` when appropriate.", False),
    ("aviso.traduccion", "nuevo", None, "sí",
     "Marco traducido por IA, sin revisión humana.",
     "Frame translated by AI, without human review.", False),
]


def render(codigo, entradas, *, estado=None, revisado_por="nadie",
           fecha="—", glosario=None, redactado_por="IA"):
    es = codigo == "es"
    estado = estado or ("referencia" if es else "borrador-ia-sin-revision-humana")
    out = [f"# i18n-{codigo} — Catálogo", "",
           f"- código: {codigo}", f"- estado: {estado}"]
    if not es:
        out += [f"- redactado-por: {redactado_por}",
                f"- revisado-por: {revisado_por}",
                f"- fecha-revision: {fecha}"]
    out += ["", "## Glosario", ""]
    for t, tr in (glosario if glosario is not None else [("seudonimización", "pseudonymisation")]):
        out.append(f"- {t} → {t if es else tr}")
    out += ["", "## Frases", ""]
    for clave, origen, fuente, seg, e_es, e_en, inv in entradas:
        out.append(f"### {clave}")
        out.append(f"origen: {origen}")
        if fuente:
            out.append(f"fuente: {fuente}")
        out.append(f"seguridad: {seg}")
        out.append(f"es: {e_es}")
        if not es:
            out.append(f"{codigo}: {e_en}")
            if inv:
                out.append("invariable: sí")
        out.append("")
    return "\n".join(out)


class Directorio:
    """Directorio temporal con catálogos; se limpia solo."""

    def __init__(self, testcase, idiomas=("es", "en")):
        self.dir = Path(tempfile.mkdtemp())
        testcase.addCleanup(shutil.rmtree, self.dir, True)
        for c in idiomas:
            self.escribir(c, render(c, ENTRADAS))

    def escribir(self, codigo, texto, nombre=None):
        (self.dir / (nombre or f"i18n-{codigo}.md")).write_text(texto, encoding="utf-8")

    def validar(self):
        return v.validar_directorio(self.dir, FUENTE)


def reemplazar(entradas, cual, **cambios):
    """Devuelve una copia de ENTRADAS con campos cambiados en una clave."""
    campos = ["clave", "origen", "fuente", "seguridad", "es", "en", "invariable"]
    res = []
    for e in entradas:
        e = list(e)
        if e[0] == cual:
            for k, val in cambios.items():
                e[campos.index(k)] = val
        res.append(tuple(e))
    return res


class CaminoFeliz(unittest.TestCase):
    def test_catalogos_correctos_pasan(self):
        self.assertEqual(Directorio(self).validar(), [])

    def test_varios_idiomas_correctos_pasan(self):
        d = Directorio(self, ("es", "en"))
        d.escribir("fr", render("fr", ENTRADAS))
        self.assertEqual(d.validar(), [])

    def test_sin_catalogos_no_hay_nada_que_validar(self):
        d = Directorio(self, ())
        self.assertEqual(d.validar(), [])

    def test_el_arbol_real_valida(self):
        # Hoy no hay catálogos; cuando los haya, esta prueba los vigilará.
        self.assertEqual(v.validar_arbol_real(), [])


class EstructuraDeFicheros(unittest.TestCase):
    def test_falta_la_referencia_es(self):
        d = Directorio(self, ("en",))
        self.assertTrue(any("i18n-es.md" in e for e in d.validar()))

    def test_nombre_de_fichero_mal_formado(self):
        d = Directorio(self)
        d.escribir("EN", render("en", ENTRADAS), nombre="i18n-EN.md")
        self.assertTrue(any("i18n-EN.md" in e and "nombre" in e for e in d.validar()))

    def test_codigo_interno_distinto_del_del_fichero(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS).replace("- código: en", "- código: fr"))
        self.assertTrue(any("código" in e for e in d.validar()))


class Claves(unittest.TestCase):
    def test_falta_una_clave_y_dice_cual(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS[:-1]))
        errores = d.validar()
        self.assertTrue(any("aviso.traduccion" in e and "falta" in e for e in errores), errores)

    def test_clave_de_mas(self):
        d = Directorio(self)
        extra = ENTRADAS + [("campo.nuevo", "nuevo", None, "no", "x", "y", False)]
        d.escribir("en", render("en", extra))
        self.assertTrue(any("campo.nuevo" in e for e in d.validar()))

    def test_clave_duplicada(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS + [ENTRADAS[0]]))
        self.assertTrue(any("duplicada" in e for e in d.validar()))

    def test_literal_es_duplicado_con_otra_clave(self):
        d = Directorio(self)
        dup = reemplazar(ENTRADAS, "campo.modo", es="## APERTURA", en="## OPENING")
        d.escribir("es", render("es", dup))
        d.escribir("en", render("en", dup))
        self.assertTrue(any("un literal, una clave" in e for e in d.validar()))

    def test_clave_con_formato_invalido(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "campo.modo", clave="Campo Modo")
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("Campo Modo" in e for e in d.validar()))


class ValoresVacios(unittest.TestCase):
    def test_traduccion_vacia(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(ENTRADAS, "campo.modo", en="")))
        self.assertTrue(any("campo.modo" in e and "vací" in e for e in d.validar()))

    def test_literal_es_vacio(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "campo.modo", es="")
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("campo.modo" in e and "vací" in e for e in d.validar()))

    def test_solo_espacios_cuenta_como_vacio(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(ENTRADAS, "campo.modo", en="   ")))
        self.assertTrue(any("vací" in e for e in d.validar()))

    def test_marca_de_pendiente(self):
        for marca in ("TODO", "XXX", "???", "FIXME"):
            with self.subTest(marca):
                d = Directorio(self)
                d.escribir("en", render("en", reemplazar(
                    ENTRADAS, "campo.modo", en=f"- Mode: [A | B | C] {marca}")))
                self.assertTrue(any("pendiente" in e for e in d.validar()))

    def test_valor_en_varias_lineas(self):
        d = Directorio(self)
        t = render("en", ENTRADAS).replace("en: ## OPENING", "en: ## OPENING\ncontinúa aquí")
        d.escribir("en", t)
        self.assertTrue(any("línea" in e for e in d.validar()))


class Marcadores(unittest.TestCase):
    """Las llaves solo valen con nombre; los datos interpolados no se reinterpretan."""

    def _con_llaves(self, es, en):
        d = Directorio(self)
        for c, val in (("es", es), ("en", en)):
            d.escribir(c, render(c, reemplazar(ENTRADAS, "aviso.traduccion", es=es, en=en)))
        return d

    def test_marcador_con_nombre_ok(self):
        d = self._con_llaves("Hay {n} marcadores", "There are {n} markers")
        self.assertEqual(d.validar(), [])

    def test_marcador_vacio(self):
        d = self._con_llaves("Hay {} marcadores", "There are {} markers")
        self.assertTrue(any("marcador" in e for e in d.validar()))

    def test_marcador_numerico(self):
        d = self._con_llaves("Hay {0} marcadores", "There are {0} markers")
        self.assertTrue(any("marcador" in e for e in d.validar()))

    def test_llave_suelta(self):
        d = self._con_llaves("Hay { marcadores", "There are { markers")
        self.assertTrue(any("llave" in e for e in d.validar()))

    def test_marcador_distinto_entre_idiomas(self):
        d = self._con_llaves("Hay {n} marcadores", "There are {m} markers")
        self.assertTrue(any("marcador" in e for e in d.validar()))

    def test_marcador_que_falta_en_la_traduccion(self):
        d = self._con_llaves("Hay {n} marcadores", "There are markers")
        self.assertTrue(any("marcador" in e for e in d.validar()))


class TextosContractuales(unittest.TestCase):
    def test_codigo_entre_comillas_invertidas_traducido(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "marcador.eliminado",
            en="Use `[DELETED_DATA]` when appropriate.")))
        self.assertTrue(any("marcador.eliminado" in e and "contractual" in e
                            for e in d.validar()))

    def test_falta_el_codigo_entre_comillas_en_la_traduccion(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "marcador.eliminado", en="Use the marker when appropriate.")))
        self.assertTrue(any("contractual" in e for e in d.validar()))

    def test_token_entre_corchetes_traducido(self):
        d = Directorio(self)
        es = reemplazar(ENTRADAS, "aviso.traduccion", es="Usa [PACIENTE_A] siempre.",
                        en="Use [PATIENT_A] always.")
        d.escribir("es", render("es", es))
        d.escribir("en", render("en", es))
        self.assertTrue(any("contractual" in e for e in d.validar()))

    def test_modos_de_una_lista_con_barra_vertical_deben_ser_identicos(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "campo.modo", en="- Mode: [A | B | X]")))
        self.assertTrue(any("campo.modo" in e for e in d.validar()))

    def test_lista_con_barra_vertical_con_menos_entradas(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "campo.modo", en="- Mode: [A | B]")))
        self.assertTrue(any("campo.modo" in e for e in d.validar()))

    def test_lista_de_opciones_con_distinto_numero_de_entradas(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "campo.nivel", en="- Level: [low / high]")))
        self.assertTrue(any("campo.nivel" in e and "entradas" in e for e in d.validar()))

    def test_lista_de_opciones_que_pierde_los_corchetes(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "campo.nivel", en="- Level: low / medium / high")))
        self.assertTrue(any("campo.nivel" in e for e in d.validar()))

    def test_las_opciones_traducidas_si_pueden_cambiar_de_palabra(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "campo.nivel", en="- Level: [low / mid / high]")))
        self.assertEqual(d.validar(), [])


class SeguridadYOrigen(unittest.TestCase):
    def test_marca_de_seguridad_distinta(self):
        d = Directorio(self)
        t = render("en", ENTRADAS).replace("seguridad: sí", "seguridad: no")
        d.escribir("en", t)
        self.assertTrue(any("seguridad" in e for e in d.validar()))

    def test_valor_de_seguridad_invalido(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "campo.modo", seguridad="quizá")
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("seguridad" in e for e in d.validar()))

    def test_origen_distinto_entre_idiomas(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(ENTRADAS, "campo.modo", origen="nuevo", fuente=None)))
        self.assertTrue(any("origen" in e for e in d.validar()))

    def test_literal_es_distinto_entre_catalogos(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(ENTRADAS, "campo.modo", es="- Modo: [A | B]")))
        self.assertTrue(any("campo.modo" in e and "referencia" in e for e in d.validar()))

    def test_literal_original_que_no_existe_en_la_fuente(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "campo.modo", es="- Modo: [A | B | C | D]",
                         en="- Mode: [A | B | C | D]")
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("campo.modo" in e and "fuente" in e for e in d.validar()))

    def test_fuente_inexistente(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "campo.modo", fuente="otro.md")
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("otro.md" in e for e in d.validar()))

    def test_original_sin_fuente(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "campo.modo", fuente=None)
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("necesita `fuente`" in e for e in d.validar()))

    def test_nuevo_no_se_busca_en_la_fuente(self):
        # aviso.traduccion es `nuevo` y su literal no está en FUENTE: debe pasar.
        self.assertEqual(Directorio(self).validar(), [])


class TraduccionSinHacer(unittest.TestCase):
    def test_traduccion_identica_al_espanol_sin_declararlo(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "aviso.traduccion", en="Marco traducido por IA, sin revisión humana.")))
        self.assertTrue(any("idéntica" in e for e in d.validar()))

    def test_identica_pero_declarada_invariable_pasa(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "aviso.traduccion", en="Marco traducido por IA, sin revisión humana.",
            invariable=True)))
        self.assertEqual(d.validar(), [])

    def test_invariable_declarada_pero_distinta(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "aviso.traduccion", invariable=True)))
        self.assertTrue(any("invariable" in e for e in d.validar()))


class EstadoDeRevision(unittest.TestCase):
    """Honestidad de estado: un borrador de IA nunca se presenta como revisado."""

    def test_borrador_con_revisor_es_incoherente(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, revisado_por="Ana"))
        self.assertTrue(any("estado" in e for e in d.validar()))

    def test_revisado_sin_revisor(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, estado="revisado",
                                revisado_por="nadie", fecha="2026-11-02"))
        self.assertTrue(any("sin revisor" in e for e in d.validar()))

    def test_revisado_sin_fecha_valida(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, estado="revisado",
                                revisado_por="Ana", fecha="pronto"))
        self.assertTrue(any("fecha" in e for e in d.validar()))

    def test_revisado_completo_pasa(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, estado="revisado",
                                revisado_por="Ana", fecha="2026-11-02"))
        self.assertEqual(d.validar(), [])

    def test_experimental_pasa_si_nadie_lo_ha_revisado(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, estado="experimental-ia-sin-revision-humana"))
        self.assertEqual(d.validar(), [])

    def test_experimental_con_revisor_es_incoherente(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, estado="experimental-ia-sin-revision-humana",
                                revisado_por="Ana"))
        self.assertTrue(any("experimental con revisor" in e for e in d.validar()))

    def test_un_experimental_revisado_pasa_a_revisado_con_nombre_y_fecha(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, estado="revisado",
                                revisado_por="Ana", fecha="2026-11-02"))
        self.assertEqual(d.validar(), [])

    def test_estado_desconocido(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, estado="casi-listo"))
        self.assertTrue(any("estado" in e for e in d.validar()))

    def test_falta_el_redactor(self):
        d = Directorio(self)
        t = render("en", ENTRADAS).replace("- redactado-por: IA\n", "")
        d.escribir("en", t)
        self.assertTrue(any("redactado-por" in e for e in d.validar()))


class Glosario(unittest.TestCase):
    def test_termino_que_falta(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, glosario=[]))
        self.assertTrue(any("glosario" in e for e in d.validar()))

    def test_termino_de_mas(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, glosario=[
            ("seudonimización", "pseudonymisation"), ("riesgo", "risk")]))
        self.assertTrue(any("glosario" in e for e in d.validar()))

    def test_traduccion_vacia_en_el_glosario(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS, glosario=[("seudonimización", "")]))
        self.assertTrue(any("glosario" in e for e in d.validar()))


class FormatoDelFichero(unittest.TestCase):
    def test_seccion_desconocida(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS) + "\n## Otra cosa\n")
        self.assertTrue(any("sección desconocida" in e for e in d.validar()))

    def test_campo_desconocido(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS).replace(
            "seguridad: sí\nes: Usa", "seguridad: sí\ncomentario: hola\nes: Usa"))
        self.assertTrue(any("campo desconocido" in e for e in d.validar()))

    def test_los_comentarios_html_de_una_linea_se_ignoran_en_todas_las_secciones(self):
        d = Directorio(self)
        t = render("en", ENTRADAS)
        t = t.replace("- código: en", "<!-- nota -->\n- código: en")
        t = t.replace("## Glosario\n", "## Glosario\n<!-- otra nota -->\n")
        t = t.replace("### campo.modo\n", "### campo.modo\n<!-- y otra -->\n")
        d.escribir("en", t)
        self.assertEqual(d.validar(), [])

    def test_un_comentario_html_abierto_pero_no_cerrado_no_se_ignora(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS).replace(
            "- código: en", "<!-- sin cerrar\n- código: en"))
        self.assertTrue(d.validar())

    def test_linea_suelta_en_la_cabecera(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS).replace(
            "- redactado-por: IA", "- redactado-por: IA\ntexto suelto"))
        self.assertTrue(any("cabecera" in e for e in d.validar()))

    def test_espacios_sobrantes_en_la_traduccion(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "campo.modo", en="- Mode: [A | B | C]  ")))
        self.assertTrue(any("espacios" in e for e in d.validar()))

    def test_literal_nuevo_con_fuente_es_incoherente(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "aviso.traduccion", fuente="flujo.md")
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("`nuevo` no lleva `fuente`" in e for e in d.validar()))

    def test_referencia_con_estado_que_no_es_referencia(self):
        d = Directorio(self)
        d.escribir("es", render("es", ENTRADAS, estado="revisado"))
        self.assertTrue(any("referencia" in e and "estado" in e for e in d.validar()))

    def test_falta_el_campo_de_la_traduccion(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS).replace("en: ## OPENING\n", ""))
        self.assertTrue(any("falta el campo `en`" in e for e in d.validar()))

    def test_fechas_imposibles_o_con_otro_formato(self):
        for fecha in ("2026-13-45", "20261102", "2-11-2026"):
            with self.subTest(fecha):
                d = Directorio(self)
                d.escribir("en", render("en", ENTRADAS, estado="revisado",
                                        revisado_por="Ana", fecha=fecha))
                self.assertTrue(any("fecha" in e for e in d.validar()))

    def test_token_anadido_solo_en_la_traduccion(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "encabezado.apertura", en="## OPENING [PATIENT_A]")))
        self.assertTrue(any("contractual" in e for e in d.validar()))

    def test_marcador_invalido_solo_en_la_traduccion(self):
        d = Directorio(self)
        d.escribir("en", render("en", reemplazar(
            ENTRADAS, "encabezado.apertura", en="## OPENING {0}")))
        self.assertTrue(any("marcador" in e for e in d.validar()))


class CasosQueFaltaban(unittest.TestCase):
    def test_origen_invalido(self):
        d = Directorio(self)
        mal = reemplazar(ENTRADAS, "aviso.traduccion", origen="dudoso")
        d.escribir("es", render("es", mal))
        d.escribir("en", render("en", mal))
        self.assertTrue(any("origen inválido" in e for e in d.validar()))

    def test_linea_malformada_en_el_glosario(self):
        d = Directorio(self)
        d.escribir("en", render("en", ENTRADAS).replace(
            "## Glosario\n", "## Glosario\n\nesto no es una entrada\n"))
        self.assertTrue(any("glosario: línea no reconocida" in e for e in d.validar()))


class LineaDeComandos(unittest.TestCase):
    """La CLI es lo que ejecutará el CI: su código de salida importa."""

    def _ejecutar(self, directorio):
        import subprocess
        return subprocess.run([sys.executable, str(RAIZ / "tools" / "validar_i18n.py"),
                               str(directorio)], capture_output=True, text=True)

    def _solo_nuevos(self):
        # La CLI valida contra las fuentes REALES, así que el directorio de
        # prueba usa únicamente literales `nuevo` (no se buscan en ninguna fuente).
        nuevos = [e for e in ENTRADAS if e[1] == "nuevo"]
        d = Directorio(self, ())
        d.escribir("es", render("es", nuevos))
        d.escribir("en", render("en", nuevos))
        return d

    def test_sale_con_0_si_todo_es_valido(self):
        r = self._ejecutar(self._solo_nuevos().dir)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("OK", r.stdout)
        self.assertIn("en", r.stdout)

    def test_sale_con_1_y_dice_que_falta(self):
        d = self._solo_nuevos()
        d.escribir("en", render("en", []))
        r = self._ejecutar(d.dir)
        self.assertEqual(r.returncode, 1)
        self.assertIn("aviso.traduccion", r.stdout)
        self.assertIn("faltan", r.stdout)

    def test_sin_catalogos_sale_con_0(self):
        r = self._ejecutar(Directorio(self, ()).dir)
        self.assertEqual(r.returncode, 0)
        self.assertIn("no hay catálogos", r.stdout)


class FuentesReales(unittest.TestCase):
    def test_las_fuentes_se_leen_sin_los_bloques_i18n(self):
        # Un literal solo presente DENTRO de un bloque i18n no cuenta como original.
        texto = "linea original\n<!-- i18n:inicio -->\nsolo en el bloque\n<!-- i18n:fin -->\n"
        fuentes = v.fuentes_desde_textos({"x.md": texto})
        self.assertIn("linea original", fuentes["x.md"])
        self.assertNotIn("solo en el bloque", fuentes["x.md"])


if __name__ == "__main__":
    unittest.main()
