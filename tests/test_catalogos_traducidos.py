"""Pruebas de los catálogos traducidos (i18n-<código>.md distintos de es) y del
registro de estado de traducciones.

Lo que el validador no puede saber (calidad) se acota aquí con tripwires: frases
de seguridad fijadas una a una, restos de español, ortografía coherente y
glosario aplicado. Son heurísticas: NO sustituyen a la revisión humana.

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import validar_i18n as v  # noqa: E402
from linea_base import SKILL_DIR  # noqa: E402

SKILL = RAIZ / SKILL_DIR
ESTADO = RAIZ / "docs" / "estado-traducciones.md"


def catalogos():
    """{código: catálogo parseado} de los i18n-*.md presentes."""
    res = {}
    for f in sorted(SKILL.glob("i18n-*.md")):
        m = v.FICHERO_RE.match(f.name)
        codigo = m.group(1)
        cat, errores = v.parsear(f.read_text(encoding="utf-8"), f.name, codigo)
        assert not errores, errores
        res[codigo] = cat
    return res


def traducciones(codigo):
    cat = catalogos()[codigo]
    return {k: e[codigo] for k, e in cat["entradas"].items()}


def sin_contrato(texto):
    """Quita lo que no es prosa: código entre comillas y tokens entre corchetes."""
    texto = re.sub(r"`[^`]*`", " ", texto)
    return re.sub(r"\[[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9_]+\]", " ", texto)


# ── frases de seguridad fijadas una a una (tripwire: cambiarlas exige tocar esto) ──
SEGURIDAD_EN = {
    "encabezado.mapa": "## MAP — archive or destroy separately from the text",
    "encabezado.riesgo": "## RESIDUAL RISK AUDIT",
    "encabezado.riesgo_estimado": "### Estimated residual risk",
    "lista.nivel": "[low / medium / high]",
    "encabezado.fidelidad": "## FIDELITY CHECK",
    "fidelidad.pregunta":
        "Is any element of the pseudonymised text without a counterpart in the original?",
    "lista.si_no": "[yes / no]",
    "lista.veredicto": "[Pass / Fail / Uncertain]",
    "lista.veredicto_fidelidad": "[Pass / Fail / Uncertain / Not applicable]",
    "lista.recomendacion":
        "[suitable for internal secondary use / requires correction before use / "
        "switch to mode C / split and re-pseudonymise parts / "
        "not suitable without expert human review]",
}


class CatalogoIngles(unittest.TestCase):
    def test_existe_y_valida(self):
        self.assertTrue((SKILL / "i18n-en.md").is_file(), "falta i18n-en.md")
        self.assertEqual(v.validar_arbol_real(), [])

    def test_tiene_todas_las_claves_de_la_referencia(self):
        cats = catalogos()
        self.assertEqual(set(cats["en"]["entradas"]), set(cats["es"]["entradas"]))

    def test_las_frases_de_seguridad_son_las_revisadas(self):
        t = traducciones("en")
        for clave, esperado in SEGURIDAD_EN.items():
            with self.subTest(clave):
                self.assertEqual(t[clave], esperado)

    def test_las_frases_de_seguridad_son_exactamente_las_marcadas(self):
        cats = catalogos()
        marcadas = {k for k, e in cats["es"]["entradas"].items() if e["seguridad"] == "sí"}
        # Las 10 extraídas del original + las 5 nuevas (aviso, encabezado, 3 puertas).
        propias = set(SEGURIDAD_EN)
        nuevas = {k for k, e in cats["es"]["entradas"].items() if e["origen"] == "nuevo"}
        self.assertEqual(marcadas, propias | nuevas)

    def test_el_orden_de_las_listas_de_gravedad_se_conserva(self):
        # Invertir bajo/alto o Pasa/Fallo degradaría una salvaguarda en silencio.
        t = traducciones("en")
        self.assertRegex(t["lista.nivel"], r"^\[low / medium / high\]$")
        self.assertRegex(t["lista.veredicto"], r"^\[Pass / Fail / Uncertain\]$")
        self.assertTrue(t["lista.veredicto_fidelidad"].endswith("Not applicable]"))

    def test_sin_restos_de_espanol(self):
        for clave, texto in traducciones("en").items():
            with self.subTest(clave):
                self.assertNotRegex(sin_contrato(texto), r"[áéíóúñ¿¡]")

    def test_sin_palabras_funcionales_del_espanol(self):
        palabras = re.compile(r"\b(el|la|los|las|del|que|para|por|con|sin|una|uno)\b", re.I)
        # «y» solo en minúscula: «Y» mayúscula es la variable de «Person Y → [TOKEN]».
        conjuncion = re.compile(r"\by\b")
        for clave, texto in traducciones("en").items():
            with self.subTest(clave):
                self.assertIsNone(palabras.search(sin_contrato(texto)), texto)
                self.assertIsNone(conjuncion.search(sin_contrato(texto)), texto)

    # Palabras de ≥ 4 letras que pueden coincidir legítimamente con el español.
    COGNADOS_EN = {"token", "tokens", "audit", "original", "residual", "skill"}

    def test_no_se_deja_sin_traducir_ninguna_palabra_del_literal_espanol(self):
        cats = catalogos()
        for clave, e in cats["en"]["entradas"].items():
            with self.subTest(clave):
                es = set(re.findall(r"[^\W\d_]{4,}", sin_contrato(e["es"]).lower()))
                en = set(re.findall(r"[^\W\d_]{4,}", sin_contrato(e["en"]).lower()))
                self.assertEqual((es & en) - self.COGNADOS_EN, set())

    def test_ortografia_britanica_coherente_con_el_texto_oficial_del_rgpd(self):
        # El inglés oficial de la UE usa «pseudonymisation», «anonymisation».
        for clave, texto in traducciones("en").items():
            with self.subTest(clave):
                self.assertNotRegex(texto.lower(),
                                    r"pseudonymiz|anonymiz|generaliz|organiz")

    def test_las_unidades_y_los_valores_fijos(self):
        t = traducciones("en")
        self.assertEqual(t["unidad.dias"], "+N days")
        self.assertEqual(t["valor.ninguna"], "none")
        self.assertEqual(t["lista.modos"], "[A | B | C]")

    def test_el_aviso_remite_al_espanol_y_dice_que_no_esta_revisado(self):
        t = traducciones("en")["aviso.traduccion"]
        self.assertRegex(t, r"(?i)translated by AI")
        self.assertRegex(t, r"(?i)without human review")
        self.assertRegex(t, r"(?i)Spanish version")


# ── frases de seguridad del francés, fijadas una a una ──
SEGURIDAD_FR = {
    "encabezado.mapa": "## TABLE DE CORRESPONDANCE — à archiver ou détruire séparément du texte",
    "encabezado.riesgo": "## AUDIT DU RISQUE RÉSIDUEL",
    "encabezado.riesgo_estimado": "### Risque résiduel estimé",
    "lista.nivel": "[faible / moyen / élevé]",
    "encabezado.fidelidad": "## CONTRÔLE DE FIDÉLITÉ",
    "fidelidad.pregunta":
        "Un élément du texte pseudonymisé est-il sans correspondance dans l’original\u202f?",
    "lista.si_no": "[oui / non]",
    "lista.veredicto": "[Réussi / Échec / Incertain]",
    "lista.veredicto_fidelidad": "[Réussi / Échec / Incertain / Non applicable]",
    "lista.recomendacion":
        "[apte à un usage secondaire interne / nécessite une correction avant usage / "
        "passer au mode C / fragmenter et pseudonymiser de nouveau certaines parties / "
        "inapte sans révision humaine experte]",
}


class CatalogoFrances(unittest.TestCase):
    NBSP, FINO = "\u00a0", "\u202f"
    # Palabras de ≥ 4 letras que coinciden legítimamente con el español.
    COGNADOS_FR = {"token", "tokens", "audit", "original", "mode", "skill"}

    def test_existe_y_valida(self):
        self.assertTrue((SKILL / "i18n-fr.md").is_file(), "falta i18n-fr.md")
        self.assertEqual(v.validar_arbol_real(), [])

    def test_tiene_todas_las_claves_de_la_referencia(self):
        cats = catalogos()
        self.assertEqual(set(cats["fr"]["entradas"]), set(cats["es"]["entradas"]))

    def test_las_frases_de_seguridad_son_las_revisadas(self):
        t = traducciones("fr")
        for clave, esperado in SEGURIDAD_FR.items():
            with self.subTest(clave):
                self.assertEqual(t[clave], esperado)

    def test_el_orden_de_las_listas_de_gravedad_se_conserva(self):
        t = traducciones("fr")
        self.assertRegex(t["lista.nivel"], r"^\[faible / moyen / élevé\]$")
        self.assertRegex(t["lista.veredicto"], r"^\[Réussi / Échec / Incertain\]$")
        self.assertTrue(t["lista.veredicto_fidelidad"].endswith("Non applicable]"))

    def test_sin_restos_de_espanol(self):
        # En francés valen é è ê à ù ç…; no valen á í ó ú ñ ¿ ¡.
        for clave, texto in traducciones("fr").items():
            with self.subTest(clave):
                self.assertNotRegex(sin_contrato(texto), r"[áíóúñ¿¡]")

    def test_sin_palabras_funcionales_exclusivas_del_espanol(self):
        palabras = re.compile(r"\b(el|los|las|del|para|por|con|sin|una|uno)\b", re.I)
        # «y» conjunción española: en francés solo existe como pronombre tras
        # apóstrofo («il n’y a»), así que se detecta solo si no va precedido de él.
        conjuncion = re.compile(r"(?<!’)\by\b")
        for clave, texto in traducciones("fr").items():
            with self.subTest(clave):
                self.assertIsNone(palabras.search(sin_contrato(texto)), texto)
                self.assertIsNone(conjuncion.search(sin_contrato(texto)), texto)

    def test_sin_restos_de_ingles(self):
        palabras = re.compile(r"\b(the|and|of|for|with|is|if|any)\b", re.I)
        for clave, texto in traducciones("fr").items():
            with self.subTest(clave):
                self.assertIsNone(palabras.search(sin_contrato(texto)), texto)

    def test_no_se_deja_sin_traducir_ninguna_palabra_del_literal_espanol(self):
        for clave, e in catalogos()["fr"]["entradas"].items():
            with self.subTest(clave):
                es = set(re.findall(r"[^\W\d_]{4,}", sin_contrato(e["es"]).lower()))
                fr = set(re.findall(r"[^\W\d_]{4,}", sin_contrato(e["fr"]).lower()))
                self.assertEqual((es & fr) - self.COGNADOS_FR, set())

    # ── tipografía francesa ──
    def test_dos_puntos_con_espacio_insecable_delante(self):
        for clave, texto in traducciones("fr").items():
            with self.subTest(clave):
                self.assertNotRegex(sin_contrato(texto), r"(?<![\u00a0])(?<!\u202f):")

    def test_interrogacion_con_espacio_fino_o_insecable_delante(self):
        for clave, texto in traducciones("fr").items():
            with self.subTest(clave):
                self.assertNotRegex(sin_contrato(texto), r"(?<![\u00a0\u202f])\?")

    def test_sin_apostrofos_ni_comillas_rectas(self):
        for clave, texto in traducciones("fr").items():
            with self.subTest(clave):
                self.assertNotIn("'", texto)
                self.assertNotIn('"', texto)

    def test_las_comillas_francesas_llevan_espacio_insecable_dentro(self):
        for clave, texto in traducciones("fr").items():
            with self.subTest(clave):
                self.assertEqual(texto.count("«"), texto.count("»"))
                self.assertEqual(texto.count("«" + self.NBSP), texto.count("«"))
                self.assertEqual(texto.count(self.NBSP + "»"), texto.count("»"))

    def test_los_valores_fijos_y_la_palabra_de_regenerar(self):
        t = traducciones("fr")
        self.assertEqual(t["unidad.dias"], "+N jours")
        self.assertEqual(t["valor.ninguna"], "aucune")
        self.assertEqual(t["lista.modos"], "[A | B | C]")
        # El modo audit reconoce la palabra entre comillas de esta entrada.
        self.assertIn("«\u00a0régénérer\u00a0»", t["regenerar.texto"])

    def test_el_aviso_remite_al_espanol_y_dice_que_no_esta_revisado(self):
        t = traducciones("fr")["aviso.traduccion"]
        self.assertRegex(t, r"(?i)traduit par une IA")
        self.assertRegex(t, r"(?i)sans révision humaine")
        self.assertRegex(t, r"(?i)version espagnole")

    def test_registro_vous(self):
        # Registro profesional: se trata de «vous», no de «tu».
        for clave in ("puerta.ficticio", "puerta.sin_mediacion", "puerta.modo",
                      "regenerar.texto", "encabezado.regenerar"):
            with self.subTest(clave):
                self.assertNotRegex(traducciones("fr")[clave], r"(?i)\b(tu|ton|ta|tes|toi)\b")


class GlosarioAplicado(unittest.TestCase):
    """Cada término del glosario presente en un literal español aparece traducido
    igual en la traducción. Heurística: pensada para idiomas sin flexión rica."""

    CODIGOS = ("en", "fr")

    def test_los_terminos_se_usan_siempre_igual(self):
        cats = catalogos()
        for codigo in self.CODIGOS:
            glosario = cats[codigo]["glosario"]
            for clave, e in cats[codigo]["entradas"].items():
                es, tr = e["es"].lower(), e[codigo].lower()
                for termino, trad in glosario.items():
                    if termino.lower() in es:
                        with self.subTest(f"{codigo}:{clave}:{termino}"):
                            self.assertIn(trad.lower(), tr)


class RegistroDeEstado(unittest.TestCase):
    """docs/estado-traducciones.md debe decir la verdad sobre cada catálogo."""

    def filas(self):
        self.assertTrue(ESTADO.is_file(), "falta docs/estado-traducciones.md")
        filas = {}
        for linea in ESTADO.read_text(encoding="utf-8").split("\n"):
            if not linea.startswith("|") or set(linea) <= set("|-: "):
                continue
            celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
            if len(celdas) < 6 or celdas[1] in ("Código",):
                continue
            filas[celdas[1]] = {"estado": celdas[2], "redactado": celdas[3],
                                "revisado": celdas[4], "fecha": celdas[5]}
        return filas

    def test_cada_catalogo_tiene_su_fila_y_coincide_con_su_cabecera(self):
        filas = self.filas()
        for codigo, cat in catalogos().items():
            if codigo == "es":
                continue
            with self.subTest(codigo):
                self.assertIn(codigo, filas)
                cab = cat["cabecera"]
                self.assertEqual(filas[codigo]["estado"], cab["estado"])
                self.assertEqual(filas[codigo]["redactado"], cab["redactado-por"])
                self.assertEqual(filas[codigo]["revisado"], cab["revisado-por"])
                self.assertEqual(filas[codigo]["fecha"], cab["fecha-revision"])

    def test_las_filas_pendientes_no_tienen_fichero(self):
        for codigo, f in self.filas().items():
            if f["estado"] == "pendiente":
                with self.subTest(codigo):
                    self.assertFalse((SKILL / f"i18n-{codigo}.md").exists(),
                                     "hay fichero pero la tabla dice «pendiente»")

    def test_las_filas_con_estado_real_tienen_fichero(self):
        for codigo, f in self.filas().items():
            if f["estado"] != "pendiente":
                with self.subTest(codigo):
                    self.assertTrue((SKILL / f"i18n-{codigo}.md").is_file())

    def test_el_registro_declara_lo_que_no_esta_revisado(self):
        t = ESTADO.read_text(encoding="utf-8")
        for fragmento in ("borrador-ia-sin-revision-humana", "línea de respaldo",
                          "puerta.", "aviso.traduccion", "seguridad: sí"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, t)

    AFIRMACION = "**Ninguna traducción está revisada por una persona.**"

    def test_el_registro_afirma_que_nada_esta_revisado_solo_si_es_verdad(self):
        # Honestidad en ambos sentidos: ni se calla un «sin revisar» ni se
        # mantiene tras una revisión.
        hay_revisado = any(f["estado"] == "revisado" for f in self.filas().values())
        t = ESTADO.read_text(encoding="utf-8")
        if hay_revisado:
            self.assertNotIn(self.AFIRMACION, t, "hay catálogos revisados: retira la afirmación")
        else:
            self.assertIn(self.AFIRMACION, t, "ningún catálogo está revisado: el registro debe decirlo")

    def test_los_codigos_de_la_tabla_son_los_acordados(self):
        self.assertEqual(set(self.filas()), {"en", "fr", "ca", "gl", "eu"})


if __name__ == "__main__":
    unittest.main()
