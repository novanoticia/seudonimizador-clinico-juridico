"""Pruebas del extractor de literales en español y de la cobertura de literales.

Se escriben ANTES que el extractor. Dos garantías:

1. El catálogo de referencia i18n-es.md se GENERA leyendo el original (nunca a
   mano) y falla ruidosamente si el original cambia de forma inesperada.
2. NINGÚN texto visible de las plantillas de salida queda fuera del catálogo:
   cada fragmento es un literal con clave o una instrucción declarada. Una
   plantilla nueva o una etiqueta nueva sin clave rompe la prueba.

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import extraer_es as x  # noqa: E402
import validar_i18n as v  # noqa: E402
from linea_base import SKILL_DIR  # noqa: E402

CATALOGO = RAIZ / SKILL_DIR / "i18n-es.md"

# Marcas de seguridad: lista fijada A PROPÓSITO en la prueba. Cambiarla exige
# editar este fichero, y por tanto un diff que un humano revisa.
SEGURIDAD_ESPERADA = {
    "encabezado.mapa", "encabezado.riesgo", "encabezado.riesgo_estimado",
    "lista.nivel", "encabezado.fidelidad", "fidelidad.pregunta", "lista.si_no",
    "lista.veredicto", "lista.veredicto_fidelidad", "lista.recomendacion",
}


def reales():
    return v.fuentes_reales()


def copia(fuentes):
    return {k: t for k, t in fuentes.items()}


class Especificacion(unittest.TestCase):
    def test_claves_unicas_y_con_formato_valido(self):
        claves = [e[0] for e in x.ESPECIFICACION]
        self.assertEqual(len(claves), len(set(claves)))
        for c in claves:
            self.assertRegex(c, r"^[a-z0-9_]+(\.[a-z0-9_]+)+$")

    def test_cada_patron_tiene_un_unico_grupo_de_captura(self):
        import re
        for e in x.ESPECIFICACION:
            self.assertEqual(re.compile(e[2]).groups, 1, e[0])

    def test_marcas_de_seguridad_valen_si_o_no(self):
        for e in x.ESPECIFICACION:
            self.assertIn(e[3], ("sí", "no"), e[0])

    def test_las_marcas_de_seguridad_son_las_revisadas(self):
        marcadas = {e[0] for e in x.ESPECIFICACION if e[3] == "sí"}
        self.assertEqual(marcadas, SEGURIDAD_ESPERADA)

    def test_los_ficheros_fuente_son_del_skill(self):
        from linea_base import FICHEROS_MD
        for e in x.ESPECIFICACION:
            self.assertIn(e[1], FICHEROS_MD, e[0])


class Extraccion(unittest.TestCase):
    def test_extrae_una_entrada_por_especificacion(self):
        entradas = x.extraer(reales())
        self.assertEqual([e["clave"] for e in entradas],
                         [e[0] for e in x.ESPECIFICACION])

    def test_cada_literal_existe_verbatim_en_su_fuente(self):
        fuentes = reales()
        for e in x.extraer(fuentes):
            self.assertIn(e["es"], fuentes[e["fuente"]], e["clave"])
            self.assertEqual(e["origen"], "original")

    def test_es_determinista(self):
        self.assertEqual(x.generar(reales()), x.generar(reales()))

    def test_literal_con_espacios_internos_se_conserva(self):
        d = {e["clave"]: e["es"] for e in x.extraer(reales())}
        self.assertEqual(d["mapa.formato_entrada"],
                         "Sujeto / lugar / entidad original → [TOKEN]   (rol en el caso: …)")

    def test_literales_compartidos_tienen_una_sola_clave(self):
        literales = [e["es"] for e in x.extraer(reales())]
        self.assertEqual(len(literales), len(set(literales)))


class ExtraccionFallaRuidosamente(unittest.TestCase):
    """Si el original cambia de forma, la extracción debe romperse, no adaptarse."""

    ESPEC = [("a.uno", "f.md", r"^- (Modo:) ", "no")]

    def test_patron_sin_coincidencias(self):
        with self.assertRaises(x.ErrorExtraccion) as c:
            x.extraer({"f.md": "nada que ver\n"}, self.ESPEC)
        self.assertIn("a.uno", str(c.exception))

    def test_fichero_fuente_ausente(self):
        with self.assertRaises(x.ErrorExtraccion):
            x.extraer({}, self.ESPEC)

    def test_demasiadas_coincidencias(self):
        with self.assertRaises(x.ErrorExtraccion) as c:
            x.extraer({"f.md": "- Modo: A\n- Modo: B\n"}, self.ESPEC)
        self.assertIn("a.uno", str(c.exception))

    def test_menos_coincidencias_de_las_esperadas(self):
        espec = [("a.uno", "f.md", r"^- (Modo:) ", "no", 2)]
        with self.assertRaises(x.ErrorExtraccion):
            x.extraer({"f.md": "- Modo: A\n"}, espec)

    def test_coincidencias_con_literales_distintos(self):
        espec = [("a.uno", "f.md", r"(Modo[:;])", "no", 2)]
        with self.assertRaises(x.ErrorExtraccion) as c:
            x.extraer({"f.md": "Modo: A\nModo; B\n"}, espec)
        self.assertIn("distintos", str(c.exception))

    def test_varias_coincidencias_iguales_si_se_esperaban(self):
        espec = [("a.uno", "f.md", r"(Modo:)", "no", 2)]
        r = x.extraer({"f.md": "Modo: A\nModo: B\n"}, espec)
        self.assertEqual(r[0]["es"], "Modo:")

    def test_literal_vacio(self):
        espec = [("a.uno", "f.md", r"^(x*)$", "no")]
        with self.assertRaises(x.ErrorExtraccion) as c:
            x.extraer({"f.md": ""}, espec)      # una sola línea, vacía
        self.assertIn("vacío", str(c.exception))

    def test_literal_solo_espacios(self):
        espec = [("a.uno", "f.md", r"^(\s+)$", "no")]
        with self.assertRaises(x.ErrorExtraccion) as c:
            x.extraer({"f.md": "   "}, espec)
        self.assertIn("vacío", str(c.exception))

    def test_literal_con_espacios_en_los_extremos(self):
        espec = [("a.uno", "f.md", r"^(\s*Modo:\s*)$", "no")]
        with self.assertRaises(x.ErrorExtraccion):
            x.extraer({"f.md": " Modo: \n"}, espec)

    def test_los_bloques_i18n_no_cuentan_como_original(self):
        # El extractor recibe texto ya sin bloques; esta prueba lo comprueba de
        # extremo a extremo con el helper del validador.
        texto = "- Modo: A\n<!-- i18n:inicio -->\n- Modo: B\n<!-- i18n:fin -->\n"
        fuentes = v.fuentes_desde_textos({"f.md": texto})
        self.assertEqual(x.extraer(fuentes, self.ESPEC)[0]["es"], "Modo:")


class CatalogoGenerado(unittest.TestCase):
    def test_el_fichero_esta_en_sincronia_con_el_original(self):
        self.assertTrue(CATALOGO.is_file(), "falta i18n-es.md: genera con `tools/extraer_es.py escribir`")
        self.assertEqual(CATALOGO.read_text(encoding="utf-8"), x.generar(reales()),
                         "i18n-es.md está desfasado: ejecuta `python3 tools/extraer_es.py escribir`")

    def test_el_catalogo_generado_valida(self):
        self.assertEqual(v.validar_arbol_real(), [])

    def test_declara_el_estado_de_referencia_y_un_glosario(self):
        t = CATALOGO.read_text(encoding="utf-8")
        self.assertIn("- código: es", t)
        self.assertIn("- estado: referencia", t)
        self.assertIn("## Glosario", t)

    def test_incluye_las_entradas_nuevas_si_las_hay(self):
        nuevos = [("aviso.prueba", "nuevo", None, "sí", "Texto nuevo de prueba.")]
        t = x.generar(reales(), nuevos=nuevos)
        self.assertIn("### aviso.prueba", t)
        self.assertIn("origen: nuevo", t)
        self.assertNotIn("fuente: None", t)


class Bloques(unittest.TestCase):
    def test_localiza_los_bloques_de_codigo(self):
        b = x.bloques("a\n```\nuno\n\ndos\n```\nb\n```\ntres\n```\n")
        self.assertEqual([bl["lineas"] for bl in b], [["uno", "", "dos"], ["tres"]])
        self.assertEqual(b[0]["inicio"], 2)

    def test_bloque_sin_cerrar_es_un_error(self):
        with self.assertRaises(x.ErrorExtraccion):
            x.bloques("a\n```\nuno\n")


class Cobertura(unittest.TestCase):
    """Que no quede texto visible fuera del catálogo."""

    def setUp(self):
        self.fuentes = reales()
        self.entradas = x.extraer(self.fuentes)

    def _cobertura(self, fuentes):
        return x.cobertura(fuentes, self.entradas)

    def test_el_arbol_real_esta_cubierto(self):
        self.assertEqual(self._cobertura(self.fuentes), [])

    def test_una_etiqueta_visible_nueva_sin_clave_falla(self):
        f = copia(self.fuentes)
        f["flujo.md"] = f["flujo.md"].replace(
            "- Marcadores usados:", "- Etiqueta nueva: [x]\n- Marcadores usados:", 1)
        r = self._cobertura(f)
        self.assertTrue(any("sin clave" in e and "Etiqueta nueva" in e for e in r), r)

    def test_texto_anadido_a_una_etiqueta_existente_falla(self):
        f = copia(self.fuentes)
        f["flujo.md"] = f["flujo.md"].replace("- Nivel:", "- Nivel final:", 1)
        self.assertTrue(any("sin clave" in e for e in self._cobertura(f)))

    def test_una_lista_de_opciones_nueva_sin_clave_falla(self):
        f = copia(self.fuentes)
        f["flujo.md"] = f["flujo.md"].replace(
            "[sí / no]", "[sí / no / quizá]", 1)
        r = self._cobertura(f)
        self.assertTrue(any("sin clave" in e for e in r), r)

    def test_un_encabezado_nuevo_en_una_plantilla_falla(self):
        f = copia(self.fuentes)
        f["auditoria.md"] = f["auditoria.md"].replace(
            "### Propuestas", "### Observaciones\n### Propuestas", 1)
        r = self._cobertura(f)
        self.assertTrue(any("Observaciones" in e for e in r), r)

    def test_un_bloque_de_codigo_nuevo_sin_clasificar_falla(self):
        f = copia(self.fuentes)
        f["flujo.md"] += "\n```\n## OTRA SALIDA\n```\n"
        r = self._cobertura(f)
        self.assertTrue(any("bloque" in e and "sin clasificar" in e for e in r), r)

    def test_una_instruccion_modificada_se_detecta(self):
        f = copia(self.fuentes)
        f["flujo.md"] = f["flujo.md"].replace("[2-4 líneas]", "[2-5 líneas]", 1)
        r = self._cobertura(f)
        self.assertTrue(any("instrucción declarada" in e and "no figura" in e for e in r), r)
        self.assertTrue(any("sin clave" in e for e in r), r)

    def test_una_clasificacion_de_bloque_obsoleta_se_detecta(self):
        f = copia(self.fuentes)
        f["plantilla-entrada.md"] = f["plantilla-entrada.md"].replace("```", "", 2)
        r = self._cobertura(f)
        self.assertTrue(any("plantilla-entrada.md" in e and "obsolet" in e for e in r), r)

    def test_un_literal_que_ya_no_esta_en_ninguna_plantilla_es_huerfano(self):
        f = copia(self.fuentes)
        f["flujo.md"] = f["flujo.md"].replace("- Marcadores usados:", "- ", 1)
        r = self._cobertura(f)
        self.assertTrue(any("huérfano" in e and "fidelidad.marcadores" in e for e in r), r)

    def test_un_fichero_fuente_ausente_se_informa_sin_romper(self):
        f = copia(self.fuentes)
        del f["plantilla-entrada.md"]
        r = self._cobertura(f)
        self.assertTrue(any("plantilla-entrada.md" in e and "obsolet" in e for e in r), r)

    def test_los_bloques_excluidos_no_exigen_claves(self):
        # El formato de ENTRADA del usuario es documentación: su texto puede
        # cambiar sin que haga falta clave (el bloque sigue clasificado).
        f = copia(self.fuentes)
        f["plantilla-entrada.md"] = f["plantilla-entrada.md"].replace(
            "Identificador interno del caso:", "Cualquier otra etiqueta de entrada:", 1)
        self.assertEqual(self._cobertura(f), [])

def _copia_del_arbol():
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    destino = Path(tmp) / "r"
    shutil.copytree(RAIZ, destino, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
    return tmp, destino


class LineaDeComandos(unittest.TestCase):
    """La CLI es lo que ejecutará el CI."""

    def _arbol(self):
        import shutil
        tmp, destino = _copia_del_arbol()
        self.addCleanup(shutil.rmtree, tmp, True)
        return destino

    def _ejecutar(self, destino, *args):
        import subprocess
        return subprocess.run([sys.executable, str(destino / "tools" / "extraer_es.py"), *args],
                              capture_output=True, text=True)

    def test_comprobar_sale_con_0_si_todo_esta_en_orden(self):
        r = self._ejecutar(self._arbol(), "comprobar")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("OK", r.stdout)

    def test_comprobar_sale_con_1_si_el_catalogo_esta_desfasado(self):
        d = self._arbol()
        f = d / SKILL_DIR / "i18n-es.md"
        f.write_text(f.read_text(encoding="utf-8").replace("es: ## APERTURA", "es: ## OTRA", 1),
                     encoding="utf-8")
        r = self._ejecutar(d, "comprobar")
        self.assertEqual(r.returncode, 1)
        self.assertIn("desfasado", r.stdout)

    def test_comprobar_sale_con_1_si_falta_el_catalogo(self):
        d = self._arbol()
        (d / SKILL_DIR / "i18n-es.md").unlink()
        r = self._ejecutar(d, "comprobar")
        self.assertEqual(r.returncode, 1)
        self.assertIn("falta o está desfasado", r.stdout)

    def test_comprobar_sale_con_1_si_la_extraccion_falla(self):
        d = self._arbol()
        f = d / SKILL_DIR / "flujo.md"
        f.write_text(f.read_text(encoding="utf-8").replace("## APERTURA", "## OTRA COSA", 1),
                     encoding="utf-8")
        r = self._ejecutar(d, "comprobar")
        self.assertEqual(r.returncode, 1)
        self.assertIn("encabezado.apertura", r.stdout)

    def test_comprobar_sale_con_1_si_hay_texto_visible_sin_clave(self):
        d = self._arbol()
        f = d / SKILL_DIR / "flujo.md"
        f.write_text(f.read_text(encoding="utf-8").replace(
            "- Marcadores usados:", "- Etiqueta nueva: [x]\n- Marcadores usados:", 1),
            encoding="utf-8")
        r = self._ejecutar(d, "comprobar")
        self.assertEqual(r.returncode, 1)
        self.assertIn("sin clave", r.stdout)

    def test_escribir_regenera_el_catalogo_identico(self):
        d = self._arbol()
        f = d / SKILL_DIR / "i18n-es.md"
        original = f.read_bytes()
        f.unlink()
        r = self._ejecutar(d, "escribir")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(f.read_bytes(), original)
        self.assertIn("escrito", r.stdout)

    def test_escribir_sale_con_1_si_hay_huecos_de_cobertura(self):
        d = self._arbol()
        f = d / SKILL_DIR / "flujo.md"
        f.write_text(f.read_text(encoding="utf-8").replace(
            "- Marcadores usados:", "- Etiqueta nueva: [x]\n- Marcadores usados:", 1),
            encoding="utf-8")
        r = self._ejecutar(d, "escribir")
        self.assertEqual(r.returncode, 1)
        self.assertIn("sin clave", r.stdout)

    def test_escribir_sale_con_1_si_la_extraccion_falla(self):
        d = self._arbol()
        f = d / SKILL_DIR / "flujo.md"
        f.write_text(f.read_text(encoding="utf-8").replace("## APERTURA", "## OTRA COSA", 1),
                     encoding="utf-8")
        r = self._ejecutar(d, "escribir")
        self.assertEqual(r.returncode, 1)

    def test_sin_argumentos_o_con_argumento_desconocido_sale_con_2(self):
        d = self._arbol()
        for args in ((), ("otra-cosa",), ("escribir", "sobra")):
            with self.subTest(args):
                r = self._ejecutar(d, *args)
                self.assertEqual(r.returncode, 2)
                self.assertIn("escribir", r.stdout)


if __name__ == "__main__":
    unittest.main()
