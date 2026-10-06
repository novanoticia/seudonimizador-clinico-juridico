"""Pruebas del paquete que se distribuye y de la documentación de la Release (tarea 10).

El paquete es lo que descarga la gente (claude.ai, Perplexity, Mistral, Claude Code):
si le falta un catálogo, el idioma «no funciona» y no hay ningún error visible. Estas
pruebas comprueban, en una copia temporal, que el script de empaquetado lo incluye TODO,
que es idéntico al árbol y que no cuela nada más.

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import linea_base as lb  # noqa: E402

SKILL = RAIZ / lb.SKILL_DIR
NOMBRE = lb.NOMBRE
GUIA = RAIZ / "docs" / "guia-release.md"
TEXTO = RAIZ / "docs" / "release-v1.5.0.md"
README = RAIZ / "README.md"
LIMITE_BYTES_SIN_COMPRIMIR = 250_000


def sha(b):
    return hashlib.sha256(b).hexdigest()


def esperado():
    """Nombres que debe contener el paquete, calculados del árbol."""
    md = {f"{NOMBRE}/{f}" for f in lb.FICHEROS_MD}
    catalogos = {f"{NOMBRE}/{p.name}" for p in SKILL.glob("i18n-*.md")}
    return md | catalogos | {f"{NOMBRE}/LICENSE"}


def version():
    return json.loads((RAIZ / "plugin.json").read_text(encoding="utf-8"))["version"]


def leer(p):
    assert p.is_file(), f"falta {p.relative_to(RAIZ)}"
    return p.read_text(encoding="utf-8")


def hay_catalogo_revisado():
    return any("estado: revisado" in f.read_text(encoding="utf-8")
               for f in SKILL.glob("i18n-*.md") if f.name != "i18n-es.md")


class ContenidoDelPaquete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.paquete = lb.construir_paquete(RAIZ)
        cls.miembros = cls.paquete["miembros"]

    def test_contiene_exactamente_los_ficheros_esperados(self):
        self.assertEqual(set(self.miembros), esperado())

    def test_cada_catalogo_del_arbol_viaja_en_el_paquete(self):
        for p in SKILL.glob("i18n-*.md"):
            with self.subTest(p.name):
                self.assertIn(f"{NOMBRE}/{p.name}", self.miembros)

    def test_los_seis_catalogos_acordados_estan(self):
        for c in ("es", "en", "fr", "ca", "gl", "eu"):
            with self.subTest(c):
                self.assertIn(f"{NOMBRE}/i18n-{c}.md", self.miembros)

    def test_los_ficheros_son_identicos_a_los_del_arbol(self):
        for nombre, m in self.miembros.items():
            origen = RAIZ / "LICENSE" if nombre.endswith("/LICENSE") else SKILL / nombre.split("/", 1)[1]
            with self.subTest(nombre):
                self.assertEqual(m["sha256"], sha(origen.read_bytes()))

    def test_una_sola_carpeta_raiz_con_el_nombre_del_skill(self):
        raices = {n.split("/", 1)[0] for n in self.miembros}
        self.assertEqual(raices, {NOMBRE})

    def test_un_solo_skill_md(self):
        self.assertEqual([n for n in self.miembros if n.endswith("/SKILL.md")],
                         [f"{NOMBRE}/SKILL.md"])

    def test_sin_basura(self):
        for n in self.miembros:
            with self.subTest(n):
                self.assertNotRegex(n, r"__pycache__|\.DS_Store|\.git|\.pyc$|~$")

    def test_el_skill_es_copia_exacta_del_zip(self):
        self.assertTrue(self.paquete["skill_igual_zip"])

    def test_tamano_razonable(self):
        total = sum(len(m["texto"].encode("utf-8")) for m in self.miembros.values()
                    if m["texto"] is not None)
        self.assertLess(total, LIMITE_BYTES_SIN_COMPRIMIR)

    def test_el_frontmatter_del_skill_empaquetado_es_el_del_arbol(self):
        texto = self.miembros[f"{NOMBRE}/SKILL.md"]["texto"]
        self.assertEqual(lb.comparar_frontmatter(texto), [])

    def test_el_skill_empaquetado_contiene_los_bloques_i18n(self):
        texto = self.miembros[f"{NOMBRE}/SKILL.md"]["texto"]
        self.assertEqual(texto.count(lb.INICIO), 2)


class SalidaDelScript(unittest.TestCase):
    """Lo que el script imprime (su `unzip -l`) es lo que verá la persona que lo ejecute."""

    def _ejecutar(self, extra=None):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        copia = Path(tmp) / "r"
        shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
        for nombre, contenido in (extra or {}).items():
            (copia / lb.SKILL_DIR / nombre).write_text(contenido, encoding="utf-8")
        r = subprocess.run(["bash", "scripts/build-dist.sh"], cwd=copia,
                           capture_output=True, text=True)
        return r, copia

    def test_el_listado_muestra_todos_los_catalogos(self):
        r, _ = self._ejecutar()
        self.assertEqual(r.returncode, 0, r.stderr)
        for p in SKILL.glob("i18n-*.md"):
            with self.subTest(p.name):
                self.assertIn(p.name, r.stdout)

    def test_genera_el_zip_y_el_skill(self):
        r, copia = self._ejecutar()
        self.assertTrue((copia / "dist" / f"{NOMBRE}.zip").is_file())
        self.assertTrue((copia / "dist" / f"{NOMBRE}.skill").is_file())

    def test_un_catalogo_nuevo_se_empaqueta_sin_tocar_el_script(self):
        r, copia = self._ejecutar({"i18n-pt.md": "# i18n-pt\n"})
        self.assertIn("i18n-pt.md", r.stdout)

    def test_los_paquetes_se_regeneran_limpios(self):
        # Un zip antiguo en dist/ no debe sobrevivir ni mezclarse con el nuevo.
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        copia = Path(tmp) / "r"
        shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
        (copia / "dist").mkdir()
        (copia / "dist" / f"{NOMBRE}.zip").write_bytes(b"paquete antiguo corrupto")
        subprocess.run(["bash", "scripts/build-dist.sh"], cwd=copia, capture_output=True, check=True)
        import zipfile
        with zipfile.ZipFile(copia / "dist" / f"{NOMBRE}.zip") as z:
            self.assertIn(f"{NOMBRE}/i18n-en.md", z.namelist())


class PaquetesAntiguos(unittest.TestCase):
    """Quien descargó la v1.4.0 tiene un paquete SIN idiomas. La documentación debe avisarlo."""

    def test_la_linea_base_confirma_que_el_paquete_antiguo_no_tenia_catalogos(self):
        base = json.loads((RAIZ / "tests" / "baseline" / "paquete.json").read_text())
        self.assertFalse([n for n in base["miembros"] if "i18n-" in n])

    def test_la_guia_avisa_de_que_hay_que_reinstalar_el_paquete_antiguo(self):
        self.assertRegex(leer(GUIA), r"(?is)paquete antiguo.{0,200}reinstal")

    def test_el_texto_de_la_release_tiene_una_seccion_para_el_paquete_antiguo(self):
        t = leer(TEXTO)
        self.assertRegex(t, r"(?m)^## .*paquete antiguo")
        self.assertRegex(t, r"(?ims)^## .*paquete antiguo.*?\*\*Reinstala\*\*")
        self.assertRegex(t, r"(?i)no contiene los catálogos")


class GuiaDeLaRelease(unittest.TestCase):
    def setUp(self):
        self.t = leer(GUIA)

    def test_nombra_la_etiqueta_de_esta_version(self):
        self.assertIn(f"v{version()}", self.t)

    def test_pasos_de_la_pagina_de_releases(self):
        for fragmento in ("Releases", "Draft a new release", "Choose a tag",
                          "Save draft", "Publish release"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.t)

    def test_dice_que_no_se_marque_como_pre_release_y_por_que(self):
        self.assertRegex(self.t, r"(?i)no marques.{0,60}pre-release|pre-release.{0,80}no (la )?marques")
        self.assertIn("releases/latest/download", self.t)
        self.assertRegex(self.t, r"(?i)Latest")

    def test_marca_como_ultima_version(self):
        self.assertIn("Set as the latest release", self.t)

    def test_el_orden_primero_fusionar_y_despues_publicar(self):
        self.assertRegex(self.t, r"(?m)^1\. \*\*Primero fusiona el Pull Request\*\*")

    def test_explica_como_generar_el_paquete_sin_instalar_nada_y_en_local(self):
        for fragmento in ("Codespaces", "scripts/build-dist.sh", "dist/", "unzip -l"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.t)
        self.assertRegex(self.t, r"(?i)en local|en tu ordenador")

    def test_explica_como_borrar_el_entorno_despues(self):
        self.assertRegex(self.t, r"(?i)borra(r)? (el|tu) codespace|Delete")
        self.assertIn("github.com/codespaces", self.t)

    def test_cita_los_dos_archivos_con_el_nombre_real(self):
        self.assertIn(f"`{NOMBRE}.zip`", self.t)
        self.assertIn(f"`{NOMBRE}.skill`", self.t)

    def test_remite_al_texto_de_la_release_que_existe(self):
        self.assertIn("docs/release-v1.5.0.md", self.t)
        self.assertTrue(TEXTO.is_file())

    def test_explica_como_comprobar_despues_de_publicar(self):
        for fragmento in ("releases/latest", "unzip -l"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.t)

    def test_dice_que_hacer_si_te_equivocas(self):
        self.assertRegex(self.t, r"(?i)si te equivocas|si algo sale mal|editar la release")

    def test_distingue_lo_comprobado_de_lo_que_no(self):
        self.assertIn("Comprobado en este repositorio", self.t)
        self.assertIn("No comprobado", self.t)

    def test_declara_los_hechos_comprobados_de_la_release_actual(self):
        for fragmento in ("v1.4.0", "Latest"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.t)
        # Dato leído en la API: 5 descargas del paquete antiguo (3 del zip y 2 del .skill).
        self.assertRegex(self.t, r"(?i)\b5\b.{0,60}descarga|descarga.{0,60}\b5\b")

    def test_pide_actualizar_el_estado_real_antes_de_publicar(self):
        # La instrucción concreta de la lista de control, en una sola frase.
        self.assertRegex(self.t, r"(?is)\*\*antes de publicar,? actualiza el «estado real»\*\*")

    def test_no_se_publica_nada_sin_que_lo_decida_la_persona(self):
        self.assertIn("**Claude no publica nada**", self.t)
        self.assertRegex(self.t, r"(?m)^Claude \*\*no publica\*\* Releases")

    def test_cierra_con_la_nota_etica_y_no_cita_el_icono(self):
        self.assertIn("asistencia de IA", self.t.strip().split("\n")[-1])
        self.assertNotIn("icon.png", self.t)


class TextoDeLaRelease(unittest.TestCase):
    def setUp(self):
        self.t = leer(TEXTO)

    def test_titulo_con_la_version(self):
        self.assertRegex(self.t.split("\n")[0], rf"v{re.escape(version())}")

    def test_declara_el_estado_real(self):
        for fragmento in ("experimental", "plataforma real", "EUR-Lex", "sin revisión humana"):
            with self.subTest(fragmento):
                self.assertRegex(self.t, rf"(?i){re.escape(fragmento)}")

    def test_la_afirmacion_de_nada_revisado_solo_si_es_verdad(self):
        afirmacion = "**Ninguna de las traducciones ha sido revisada por una persona.**"
        if hay_catalogo_revisado():
            self.assertNotIn(afirmacion, self.t)
        else:
            self.assertIn(afirmacion, self.t)

    def test_no_presenta_las_traducciones_como_estables_ni_revisadas(self):
        self.assertNotRegex(self.t, r"(?i)traducciones? (estables?|revisadas?|verificadas?)")

    def test_cita_los_cinco_idiomas(self):
        for c in ("en", "fr", "ca", "gl", "eu"):
            with self.subTest(c):
                self.assertIn(f"`{c}`", self.t)

    def test_tabla_de_archivos_con_los_nombres_reales(self):
        self.assertIn(f"`{NOMBRE}.zip`", self.t)
        self.assertIn(f"`{NOMBRE}.skill`", self.t)

    def test_avisa_a_quien_tiene_el_paquete_antiguo(self):
        self.assertRegex(self.t, r"(?m)^## .*paquete antiguo \(v1\.4\.0 o anterior\)")

    def test_avisa_de_que_no_sustituye_la_anonimizacion_formal(self):
        self.assertRegex(self.t, r"(?i)no sustituye la anonimización formal")

    def test_enlaza_changelog_y_registro_de_estado(self):
        self.assertIn("CHANGELOG.md", self.t)
        self.assertIn("estado-traducciones.md", self.t)

    def test_no_dice_que_el_skill_este_probado_con_idiomas_en_una_plataforma_real(self):
        self.assertRegex(self.t, r"(?i)no se ha (probado|ejecutado).{0,80}plataforma real")

    def test_cierra_con_la_nota_etica(self):
        self.assertIn("asistencia de IA", self.t.strip().split("\n")[-1])

    def test_tiene_un_tamano_razonable_para_el_cuerpo_de_una_release(self):
        self.assertLess(len(self.t), 20_000)


class EnlacesDelReadmeALosDescargables(unittest.TestCase):
    def test_los_enlaces_de_descarga_apuntan_a_los_dos_archivos_reales(self):
        enlaces = re.findall(r"releases/latest/download/([^)\s]+)", leer(README))
        self.assertTrue(enlaces)
        self.assertLessEqual(set(enlaces), {f"{NOMBRE}.zip", f"{NOMBRE}.skill"})


if __name__ == "__main__":
    unittest.main()
