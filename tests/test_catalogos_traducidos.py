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


class PruebasComunes:
    """Comprobaciones compartidas por los catálogos nuevos (ca, gl, eu…).

    Cada clase concreta define sus parámetros; esto evita copiar el bloque por
    idioma. Los idiomas ya cerrados (en, fr) mantienen sus clases propias."""
    CODIGO = None
    SEGURIDAD = {}                    # clave -> traducción fijada (tripwire)
    ORDEN_GRAVEDAD = []               # [(clave, regex exacta)]
    VALORES_FIJOS = {}                # clave -> traducción exacta
    AVISO = []                        # regex que debe cumplir aviso.traduccion
    RE_CARACTERES_ES = r"[áñ¿¡]"      # caracteres que NO existen en el idioma
    RE_PALABRAS_ES = r"\b(los|las|para|por|con|sin|uno)\b"
    # «y» conjunción: solo minúscula («Y» mayúscula es la variable de «Persona Y»).
    RE_CONJUNCION_ES = r"(?<!’)\by\b"
    RE_PALABRAS_EN = r"\b(the|and|of|for|with|is|if|any)\b"
    COGNADOS = {"token", "tokens", "audit", "original", "skill"}

    def trad(self):
        return traducciones(self.CODIGO)

    def test_existe_y_valida(self):
        self.assertTrue((SKILL / f"i18n-{self.CODIGO}.md").is_file(), f"falta i18n-{self.CODIGO}.md")
        self.assertEqual(v.validar_arbol_real(), [])

    def test_tiene_todas_las_claves_de_la_referencia(self):
        cats = catalogos()
        self.assertEqual(set(cats[self.CODIGO]["entradas"]), set(cats["es"]["entradas"]))

    def test_las_frases_de_seguridad_son_las_revisadas(self):
        for clave, esperado in self.SEGURIDAD.items():
            with self.subTest(clave):
                self.assertEqual(self.trad()[clave], esperado)

    def test_se_fijan_exactamente_las_diez_frases_de_seguridad_del_original(self):
        self.assertEqual(set(self.SEGURIDAD), set(SEGURIDAD_EN))

    def test_el_orden_de_las_listas_de_gravedad_se_conserva(self):
        for clave, regex in self.ORDEN_GRAVEDAD:
            with self.subTest(clave):
                self.assertRegex(self.trad()[clave], regex)

    def test_sin_restos_de_espanol(self):
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertNotRegex(sin_contrato(texto), self.RE_CARACTERES_ES)

    def test_sin_palabras_funcionales_exclusivas_del_espanol(self):
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertIsNone(re.search(self.RE_PALABRAS_ES, sin_contrato(texto), re.I), texto)
                self.assertIsNone(re.search(self.RE_CONJUNCION_ES, sin_contrato(texto)), texto)

    def test_sin_restos_de_ingles(self):
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertIsNone(re.search(self.RE_PALABRAS_EN, sin_contrato(texto), re.I), texto)

    # False si el idioma es tan cercano al español que la heurística no discrimina
    # (gallego: ~85 palabras idénticas). Entonces la clase define marcadores propios.
    COMPARA_PALABRAS = True

    def test_no_se_deja_sin_traducir_ninguna_palabra_del_literal_espanol(self):
        if not self.COMPARA_PALABRAS:
            self.skipTest(f"{self.CODIGO}: heurística no informativa; ver marcadores ortográficos propios")
        for clave, e in catalogos()[self.CODIGO]["entradas"].items():
            with self.subTest(clave):
                es = set(re.findall(r"[^\W\d_]{4,}", sin_contrato(e["es"]).lower()))
                tr = set(re.findall(r"[^\W\d_]{4,}", sin_contrato(e[self.CODIGO]).lower()))
                self.assertEqual((es & tr) - self.COGNADOS, set())

    def test_sin_apostrofos_ni_comillas_rectas(self):
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertNotIn("'", texto)
                self.assertNotIn('"', texto)

    def test_las_comillas_angulares_van_balanceadas_y_sin_espacios_dentro(self):
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertEqual(texto.count("«"), texto.count("»"))
                self.assertNotIn("« ", texto)
                self.assertNotIn(" »", texto)

    def test_valores_fijos(self):
        for clave, esperado in self.VALORES_FIJOS.items():
            with self.subTest(clave):
                self.assertEqual(self.trad()[clave], esperado)

    def test_el_aviso_remite_al_espanol_y_dice_que_no_esta_revisado(self):
        t = self.trad()["aviso.traduccion"]
        for regex in self.AVISO:
            with self.subTest(regex):
                self.assertRegex(t, regex)

    def test_la_palabra_de_regenerar_va_entre_comillas_angulares(self):
        self.assertRegex(self.trad()["regenerar.texto"], r"«[^»]+»")


# ── catalán ──
SEGURIDAD_CA = {
    "encabezado.mapa": "## MAPA — arxivar o destruir per separat del text",
    "encabezado.riesgo": "## AUDITORIA DEL RISC RESIDUAL",
    "encabezado.riesgo_estimado": "### Risc residual estimat",
    "lista.nivel": "[baix / mitjà / alt]",
    "encabezado.fidelidad": "## CONTROL DE FIDELITAT",
    "fidelidad.pregunta": "Hi ha algun element del text pseudonimitzat sense correspondència a l’original?",
    "lista.si_no": "[sí / no]",
    "lista.veredicto": "[Passa / Falla / Dubte]",
    "lista.veredicto_fidelidad": "[Passa / Falla / Dubte / No aplicable]",
    "lista.recomendacion":
        "[apte per a ús secundari intern / requereix correcció abans de l’ús / "
        "passar al mode C / fragmentar i tornar a pseudonimitzar parts / "
        "no apte sense revisió humana experta]",
}


class CatalogoCatala(PruebasComunes, unittest.TestCase):
    CODIGO = "ca"
    SEGURIDAD = SEGURIDAD_CA
    ORDEN_GRAVEDAD = [
        ("lista.nivel", r"^\[baix / mitjà / alt\]$"),
        ("lista.veredicto", r"^\[Passa / Falla / Dubte\]$"),
        ("lista.veredicto_fidelidad", r"^\[Passa / Falla / Dubte / No aplicable\]$"),
    ]
    VALORES_FIJOS = {"unidad.dias": "+N dies", "valor.ninguna": "cap",
                     "lista.modos": "[A | B | C]"}
    AVISO = [r"(?i)traduït per una IA", r"(?i)sense revisió humana", r"(?i)versió en castellà"]
    # En catalán son válidos à è é í ò ó ú ï ü ç y l·l; no existen á ñ ¿ ¡.
    RE_CARACTERES_ES = r"[áñ¿¡]"
    # Palabras idénticas en catalán y español, juzgadas una a una (tarea 7). Es una lista
    # larga porque las lenguas son hermanas; su coste: una palabra española que coincida
    # con ellas no se detecta por esta vía (solo la revisión humana lo haría).
    COGNADOS = PruebasComunes.COGNADOS | {
        "regenerar", "global", "control", "residual", "mode",
        "aplicable", "casos", "clínica", "combinada", "consulta", "destruir", "experta",
        "extrema", "fragmentar", "funcional", "humana", "identificadores", "indica",
        "interna", "jurídica", "mapa", "persona", "recuperables", "sobre", "temporal",
    }

    def test_punt_volat_correcto(self):
        # «l·l» con punto medio (U+00B7), no «l.l» ni «l-l».
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertNotRegex(texto, r"l[.\-]l")

    def test_preguntas_sin_signo_de_apertura(self):
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertNotIn("¿", texto)


# ── gallego ──
SEGURIDAD_GL = {
    "encabezado.mapa": "## MAPA — arquivar ou destruír por separado do texto",
    "encabezado.riesgo": "## AUDITORÍA DO RISCO RESIDUAL",
    "encabezado.riesgo_estimado": "### Risco residual estimado",
    "lista.nivel": "[baixo / medio / alto]",
    "encabezado.fidelidad": "## CONTROL DE FIDELIDADE",
    "fidelidad.pregunta":
        "Hai algún elemento do texto pseudonimizado sen correspondencia no orixinal?",
    "lista.si_no": "[si / non]",
    "lista.veredicto": "[Pasa / Fallo / Dúbida]",
    "lista.veredicto_fidelidad": "[Pasa / Fallo / Dúbida / Non aplicable]",
    "lista.recomendacion":
        "[apto para uso secundario interno / require corrección antes do uso / "
        "pasar ao modo C / fragmentar e pseudonimizar de novo partes / "
        "non apto sen revisión humana experta]",
}


class CatalogoGalego(PruebasComunes, unittest.TestCase):
    CODIGO = "gl"
    SEGURIDAD = SEGURIDAD_GL
    ORDEN_GRAVEDAD = [
        ("lista.nivel", r"^\[baixo / medio / alto\]$"),
        ("lista.veredicto", r"^\[Pasa / Fallo / Dúbida\]$"),
        ("lista.veredicto_fidelidad", r"^\[Pasa / Fallo / Dúbida / Non aplicable\]$"),
    ]
    VALORES_FIJOS = {"unidad.dias": "+N días", "valor.ninguna": "ningunha",
                     "lista.modos": "[A | B | C]"}
    AVISO = [r"(?i)traducido por unha IA", r"(?i)sen revisión humana",
             r"(?i)versión en castelán"]
    # En gallego valen á é í ó ú y ñ; no existen ¿ ¡.
    RE_CARACTERES_ES = r"[¿¡]"
    # En gallego «para», «por», «con», «que» y «el» (pronombre) existen: no se vigilan.
    RE_PALABRAS_ES = r"\b(los|las|sin|uno|una|del)\b"
    COMPARA_PALABRAS = False     # ~85 palabras idénticas con el español: no discrimina
    MAX_INVARIABLES = 12         # hoy 10; más indicaría un catálogo mayormente copiado

    def test_el_numero_de_entradas_invariables_esta_acotado(self):
        invariables = [k for k, e in catalogos()["gl"]["entradas"].items()
                       if e["gl"] == e["es"]]
        self.assertLessEqual(len(invariables), self.MAX_INVARIABLES, invariables)

    def test_sin_marcadores_ortograficos_del_espanol(self):
        # -dad (gl: -dade), -miento (gl: -mento) y palabras sin equivalente idéntico.
        # No se vigila «ll»: existe en palabras gallegas (detalles, fallo) y en «skill».
        patrones = [r"\b\w+dad\b", r"\b\w+miento\b",
                    r"\b(hay|también|muy|mucho|cuando|donde|puede|tiene)\b"]
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                for p in patrones:
                    self.assertNotRegex(sin_contrato(texto).lower(), p)

    def test_sin_la_letra_j(self):
        # En gallego la «j» solo aparece en préstamos: delata «jurídico», «justificación»…
        for clave, texto in self.trad().items():
            with self.subTest(clave):
                self.assertNotRegex(sin_contrato(texto).lower(), r"j")

    def test_formas_gallegas_de_los_terminos_clave(self):
        t = self.trad()
        self.assertIn("xustificación", t["riesgo.justificacion"].lower())
        self.assertIn("xeneralización", t["riesgo.propuesta"].lower())
        self.assertIn("desprazamento", t["mapa.desplazamiento"].lower())
        self.assertIn("rexenerar", t["encabezado.regenerar"].lower())


class GlosarioAplicado(unittest.TestCase):
    """Cada término del glosario presente en un literal español aparece traducido
    igual en la traducción. Heurística: pensada para idiomas sin flexión rica."""

    CODIGOS = ("en", "fr", "ca", "gl")

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
