"""Pruebas de los bloques i18n añadidos al original (tarea 4).

Contrato: son SOLO adiciones delimitadas (la línea base lo vigila aparte), están
en el sitio acordado, dicen lo que se aprobó y no se salen del tamaño previsto.

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import extraer_es as ex  # noqa: E402
import linea_base as lb  # noqa: E402

SKILL = RAIZ / lb.SKILL_DIR
INICIO, FIN = lb.INICIO, lb.FIN

# Nº de bloques por fichero: lista cerrada.
BLOQUES_ESPERADOS = {"SKILL.md": 2, "flujo.md": 1, "auditoria.md": 1,
                     "plantilla-entrada.md": 0, "plantilla-tokens.md": 0}
LIMITE_BYTES_SKILL = 11000          # SKILL.md completo (hoy 7 680 B sin bloques)
LIMITE_CHARS_BLOQUE_SKILL = 2600    # el bloque de «Idioma de la respuesta»

NUEVOS_ESPERADOS = {
    "encabezado.aviso_traduccion": "## AVISO DE TRADUCCIÓN",
    "aviso.traduccion": None,
    "puerta.ficticio": None,
    "puerta.sin_mediacion": None,
    "puerta.modo": None,
}


def texto(nombre):
    return (SKILL / nombre).read_text(encoding="utf-8")


def bloques_de(nombre):
    """[(línea_inicio, línea_fin, cuerpo)] de los bloques i18n (1-based)."""
    res, ini, cuerpo = [], None, []
    for n, l in enumerate(texto(nombre).split("\n"), start=1):
        if l.strip() == INICIO:
            ini, cuerpo = n, []
        elif l.strip() == FIN:
            res.append((ini, n, "\n".join(cuerpo)))
            ini = None
        elif ini is not None:
            cuerpo.append(l)
    return res


def linea_de(nombre, prefijo, desde=1):
    for n, l in enumerate(texto(nombre).split("\n"), start=1):
        if n >= desde and l.startswith(prefijo):
            return n
    raise AssertionError(f"{nombre}: no hay línea que empiece por {prefijo!r}")


class Estructura(unittest.TestCase):
    def test_numero_de_bloques_por_fichero(self):
        for f, n in BLOQUES_ESPERADOS.items():
            with self.subTest(f):
                self.assertEqual(len(bloques_de(f)), n)

    def test_cada_bloque_esta_balanceado_y_no_vacio(self):
        for f in BLOQUES_ESPERADOS:
            for ini, fin, cuerpo in bloques_de(f):
                with self.subTest(f"{f}:{ini}"):
                    self.assertGreater(fin, ini)
                    self.assertTrue(cuerpo.strip())

    def test_los_bloques_van_seguidos_de_una_linea_en_blanco_y_precedidos_de_otra(self):
        # Convención que exige la comparación con la línea base.
        for f in ("SKILL.md", "flujo.md", "auditoria.md"):
            ls = texto(f).split("\n")
            for ini, fin, _ in bloques_de(f):
                with self.subTest(f"{f}:{ini}"):
                    self.assertEqual(ls[ini - 2], "", "falta línea en blanco antes del bloque")
                    self.assertEqual(ls[fin], "", "falta línea en blanco tras el bloque")

    def test_el_frontmatter_queda_intacto_y_fuera_de_los_bloques(self):
        self.assertEqual(lb.comparar_frontmatter(texto("SKILL.md")), [])
        self.assertLess(len(lb.frontmatter(texto("SKILL.md"))["description"]), 500)
        primera = bloques_de("SKILL.md")[0][0]
        fin_fm = texto("SKILL.md").split("\n").index("---", 1) + 1
        self.assertGreater(primera, fin_fm)

    def test_la_comparacion_con_la_linea_base_pasa(self):
        self.assertEqual(lb.comparar_todo(RAIZ), [])


class Posicion(unittest.TestCase):
    def test_skill_bloque_de_idioma_tras_los_modos_y_antes_de_para_que_no_sirve(self):
        ini, fin, _ = bloques_de("SKILL.md")[0]
        self.assertGreater(ini, linea_de("SKILL.md", "Si el usuario no especifica modo"))
        self.assertLess(fin, linea_de("SKILL.md", "## Para qué NO sirve"))

    def test_skill_bloque_de_ficheros_tras_el_ultimo_fichero_listado(self):
        ini, fin, cuerpo = bloques_de("SKILL.md")[1]
        self.assertGreater(ini, linea_de("SKILL.md", "- `auditoria.md`"))
        self.assertLess(fin, linea_de("SKILL.md", "## Limitaciones conocidas"))
        self.assertTrue(cuerpo.lstrip().startswith("- `i18n-<código>.md`"))

    def test_flujo_bloque_entre_el_paso_5_y_el_paso_6(self):
        ini, fin, _ = bloques_de("flujo.md")[0]
        self.assertGreater(ini, linea_de("flujo.md", "## Paso 5"))
        self.assertLess(fin, linea_de("flujo.md", "## Paso 6"))
        # …y fuera del bloque de código de la plantilla del paso 5.
        ls = texto("flujo.md").split("\n")
        valla_cierre = max(i for i, l in enumerate(ls[:ini], start=1) if l.startswith("```"))
        self.assertGreater(ini, valla_cierre)

    def test_auditoria_bloque_tras_la_salida_y_antes_de_las_limitaciones(self):
        ini, fin, _ = bloques_de("auditoria.md")[0]
        self.assertGreater(ini, linea_de("auditoria.md", "## Salida del modo"))
        self.assertLess(fin, linea_de("auditoria.md", "## Limitaciones del modo"))
        ls = texto("auditoria.md").split("\n")
        valla_cierre = max(i for i, l in enumerate(ls[:ini], start=1) if l.startswith("```"))
        self.assertGreater(ini, valla_cierre)


class ContenidoDelBloquePrincipal(unittest.TestCase):
    def setUp(self):
        self.b = bloques_de("SKILL.md")[0][2]

    def test_reglas_de_seleccion_del_idioma(self):
        for fragmento in (
            "exactamente tres elementos",
            "`/seudonimizar A en`",
            "`/seudonimizar en`",
            "Si el caso empieza en esa misma línea, no hay código de idioma",
            "`en-US`", "`ca_ES`", "`fr_FR.UTF-8`",
            "`es` equivale a no poner código",
            "2 o 3 letras",
        ):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.b)

    def test_sin_codigo_no_cambia_nada(self):
        self.assertIn("no cargues ningún catálogo", self.b)

    def test_fallo_seguro_si_no_hay_catalogo(self):
        self.assertRegex(self.b, r"(?i)no inventes la traducción")
        self.assertRegex(self.b, r"(?i)responde en español")

    def test_codigo_desconocido_avisa_en_espanol_y_continua(self):
        self.assertIn("Idioma", self.b)
        self.assertIn("no disponible", self.b)
        self.assertIn("continúa en español", self.b)

    def test_lo_que_no_se_traduce(self):
        for fragmento in ("[DATO_ELIMINADO]", "[NO_CONSTA]", "[PACIENTE_A]",
                          "el texto del caso", "los modos"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.b)

    def test_el_idioma_persiste_en_la_conversacion(self):
        self.assertIn("se mantiene en la conversación", self.b)

    def test_linea_multilingue_de_respaldo_con_los_seis_idiomas(self):
        m = re.search(r"^\s*> (\[es\].*)$", self.b, re.M)
        self.assertIsNotNone(m, "falta la línea de respaldo (cita con `> `)")
        partes = re.findall(r"\[([a-z]{2})\]\s*([^\[·]+)", m.group(1))
        self.assertEqual([c for c, _ in partes], ["es", "en", "fr", "ca", "gl", "eu"])
        for c, t in partes:
            self.assertTrue(t.strip(), c)

    def test_no_se_sale_del_tamano_previsto(self):
        self.assertLessEqual(len(self.b), LIMITE_CHARS_BLOQUE_SKILL)
        self.assertLessEqual(len(texto("SKILL.md").encode("utf-8")), LIMITE_BYTES_SKILL)

    def test_no_define_una_lista_de_idiomas_los_descubre_por_ficheros(self):
        # Añadir un idioma = soltar un fichero; SKILL.md no se edita.
        self.assertIn("`i18n-<código>.md`", self.b)
        self.assertNotRegex(self.b, r"idiomas disponibles: es, en")


class ContenidoDeLosOtrosBloques(unittest.TestCase):
    def test_flujo(self):
        b = bloques_de("flujo.md")[0][2]
        for fragmento in (
            "## AVISO DE TRADUCCIÓN", "aviso.traduccion", "regla 6",
            "paso 6", "no es un comentario adicional",
            "[DATO_ELIMINADO]", "`puerta.", "Sin código", "el idioma del caso",
        ):
            with self.subTest(fragmento):
                self.assertIn(fragmento, b)

    def test_flujo_acota_el_alcance_de_la_regla_nueva(self):
        b = bloques_de("flujo.md")[0][2]
        self.assertRegex(b, r"(solo|únicamente) (si|cuando|con)")

    def test_auditoria(self):
        b = bloques_de("auditoria.md")[0][2]
        for fragmento in (
            "## AVISO DE TRADUCCIÓN", "`regenerar.texto`", "comprobación 6",
            "tokens", "[DATO_ELIMINADO]", "[NO_CONSTA]", "no cuentan",
        ):
            with self.subTest(fragmento):
                self.assertIn(fragmento, b)

    def test_auditoria_no_amplia_la_exencion_mas_alla_del_vocabulario_cerrado(self):
        b = bloques_de("auditoria.md")[0][2]
        self.assertRegex(b, r"(?i)cualquier otro resto en otro idioma sigue contando")

    def test_flujo_mantiene_el_idioma_al_iterar_o_regenerar(self):
        b = bloques_de("flujo.md")[0][2]
        self.assertRegex(b, r"(?i)al iterar o regenerar \(paso 6\), mantén el mismo idioma")

    def test_los_encabezados_de_los_bloques_son_los_que_se_citan_entre_si(self):
        # auditoria.md remite al «bloque «Idioma de la salida»» de flujo.md.
        self.assertIn("### Idioma de la salida", bloques_de("flujo.md")[0][2])
        self.assertIn("«Idioma de la salida»", bloques_de("auditoria.md")[0][2])
        self.assertIn("### Idioma de la respuesta", bloques_de("SKILL.md")[0][2])
        self.assertIn("### Idioma de la salida del modo `audit`", bloques_de("auditoria.md")[0][2])

    def test_auditoria_no_traduce_el_texto_auditado_ni_reproduce_datos_sensibles(self):
        b = bloques_de("auditoria.md")[0][2]
        self.assertRegex(b, r"(?i)el texto auditado no se traduce")
        self.assertRegex(b, r"(?i)sin reproducir el dato sensible, también en el idioma elegido")

    def test_auditoria_sin_codigo_nada_de_esto_aplica(self):
        b = bloques_de("auditoria.md")[0][2]
        self.assertRegex(b, r"(?i)sin código, nada de esto aplica")

    def test_skill_lista_los_catalogos_entre_los_archivos(self):
        b = bloques_de("SKILL.md")[1][2]
        self.assertIn("`i18n-es.md`", b)
        self.assertIn("referencia", b)


class ClavesCitadasExisten(unittest.TestCase):
    """Toda clave del catálogo citada en un bloque debe existir en i18n-es.md."""

    @staticmethod
    def claves_del_catalogo():
        t = (SKILL / "i18n-es.md").read_text(encoding="utf-8")
        return set(re.findall(r"^### (\S+)$", t, re.M))

    def test_las_claves_citadas_existen(self):
        claves = self.claves_del_catalogo()
        citadas = set()
        for f in ("SKILL.md", "flujo.md", "auditoria.md"):
            for _, _, cuerpo in bloques_de(f):
                citadas |= set(re.findall(
                    r"`((?:aviso|puerta|encabezado|regenerar)\.[a-z_]+)`", cuerpo))
        self.assertTrue(citadas)
        self.assertEqual(citadas - claves, set())

    def test_las_puertas_se_citan_con_comodin_o_por_clave_existente(self):
        # «`puerta.*`» es un comodín legítimo en la prosa; las claves concretas existen.
        claves = self.claves_del_catalogo()
        for k in ("puerta.ficticio", "puerta.sin_mediacion", "puerta.modo"):
            self.assertIn(k, claves)


class EntradasNuevasDeLaReferencia(unittest.TestCase):
    def setUp(self):
        self.nuevos = {n[0]: n for n in ex.NUEVOS}

    def test_estan_todas_y_son_de_origen_nuevo_y_de_seguridad(self):
        self.assertEqual(set(self.nuevos), set(NUEVOS_ESPERADOS))
        for k, (_, origen, fuente, seguridad, texto_) in self.nuevos.items():
            with self.subTest(k):
                self.assertEqual(origen, "nuevo")
                self.assertIsNone(fuente)
                self.assertEqual(seguridad, "sí")
                self.assertTrue(texto_.strip())

    def test_el_encabezado_del_aviso_es_el_que_citan_los_bloques(self):
        self.assertEqual(self.nuevos["encabezado.aviso_traduccion"][4], "## AVISO DE TRADUCCIÓN")

    def test_el_aviso_remite_a_la_version_en_espanol(self):
        t = self.nuevos["aviso.traduccion"][4]
        self.assertIn("IA", t)
        self.assertIn("sin revisión humana", t)
        self.assertIn("versión en español", t)

    def test_las_puertas_preguntan(self):
        for k in ("puerta.ficticio", "puerta.sin_mediacion"):
            self.assertIn("?", self.nuevos[k][4], k)
        self.assertIn("audit", self.nuevos["puerta.modo"][4])

    def test_el_catalogo_generado_los_incluye(self):
        t = (SKILL / "i18n-es.md").read_text(encoding="utf-8")
        for k in NUEVOS_ESPERADOS:
            self.assertIn(f"### {k}\norigen: nuevo\nseguridad: sí\nes: ", t)


if __name__ == "__main__":
    unittest.main()
