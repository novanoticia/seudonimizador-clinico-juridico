"""Pruebas de la documentación del ciclo multiidioma (tarea 9).

Vigilan coherencias que se desfasan en silencio: versión en los tres manifiestos y
en el README, enlaces relativos, que la documentación no afirme más de lo cierto
sobre el estado de las traducciones y que AGENTS.md cite comandos que existen.

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import json
import re
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import linea_base as lb  # noqa: E402

README = RAIZ / "README.md"
CHANGELOG = RAIZ / "CHANGELOG.md"
AGENTS = RAIZ / "AGENTS.md"
CLAUDE = RAIZ / "CLAUDE.md"
ESTADO = RAIZ / "docs" / "estado-traducciones.md"
SKILL = RAIZ / lb.SKILL_DIR
VERSION = "1.5.0"
CODIGOS = ["en", "fr", "ca", "gl", "eu"]


def leer(p):
    assert p.is_file(), f"falta {p.relative_to(RAIZ)}"
    return p.read_text(encoding="utf-8")


def seccion(texto, titulo):
    """Cuerpo de una sección `## titulo` hasta la siguiente `## `."""
    m = re.search(rf"(?ms)^## {re.escape(titulo)}\s*\n(.*?)(?=^## |\Z)", texto)
    assert m, f"no hay sección «{titulo}»"
    return m.group(1)


def hay_catalogo_revisado():
    return any("estado: revisado" in f.read_text(encoding="utf-8")
               for f in SKILL.glob("i18n-*.md") if f.name != "i18n-es.md")


class Versiones(unittest.TestCase):
    def test_los_tres_manifiestos_tienen_la_misma_version(self):
        versiones = {
            "plugin.json": json.loads(leer(RAIZ / "plugin.json"))["version"],
            ".claude-plugin/plugin.json":
                json.loads(leer(RAIZ / ".claude-plugin" / "plugin.json"))["version"],
            ".claude-plugin/marketplace.json":
                json.loads(leer(RAIZ / ".claude-plugin" / "marketplace.json"))["plugins"][0]["version"],
        }
        self.assertEqual(set(versiones.values()), {VERSION}, versiones)

    def test_el_readme_dice_la_misma_version_mayor_menor(self):
        m = re.search(r"\*\*Versión actual: v(\d+\.\d+)\*\*", leer(README))
        self.assertIsNotNone(m)
        self.assertEqual(m.group(1), ".".join(VERSION.split(".")[:2]))

    def test_el_changelog_tiene_la_entrada_de_esta_version(self):
        self.assertRegex(leer(CHANGELOG), r"(?m)^## \[1\.5\]")

    def test_la_descripcion_de_los_manifiestos_no_ha_cambiado(self):
        self.assertEqual(lb.comparar_manifiestos(RAIZ), [])


class Readme(unittest.TestCase):
    def setUp(self):
        self.t = leer(README)
        self.s = seccion(self.t, "Idioma de la respuesta")

    def test_explica_como_pedir_idioma(self):
        self.assertIn("/seudonimizar A en", self.s)
        self.assertRegex(self.s, r"(?i)primera línea")
        self.assertRegex(self.s, r"(?i)línea siguiente")

    def test_lista_los_cinco_idiomas_mas_el_espanol_con_su_estado(self):
        for c in ["es"] + CODIGOS:
            with self.subTest(c):
                self.assertRegex(self.s, rf"(?m)^\| `{c}` \|")
        self.assertRegex(self.s, r"(?is)`eu`.*experimental")

    def test_dice_que_se_traduce_y_que_no(self):
        for fragmento in ("texto del caso", "[DATO_ELIMINADO]", "[NO_CONSTA]", "tokens",
                          "modos", "nombres de fichero"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.s)

    def test_explica_los_casos_limite(self):
        for fragmento in ("código desconocido", "solo `SKILL.md`", "responde en español"):
            with self.subTest(fragmento):
                self.assertRegex(self.s, rf"(?i){re.escape(fragmento)}")

    def test_explica_como_anadir_un_idioma_con_los_comandos_reales(self):
        for fragmento in ("i18n-<código>.md", "python3 tools/validar_i18n.py",
                          "python3 tools/extraer_es.py escribir",
                          "python3 -m unittest discover -s tests",
                          "docs/estado-traducciones.md"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.s)
        self.assertRegex(self.s, r"(?i)no hay que (editar|tocar) `SKILL.md`")

    def test_declara_que_las_traducciones_son_de_ia_sin_revision(self):
        self.assertRegex(self.s, r"(?i)las ha (escrito|redactado) una IA")
        self.assertRegex(self.s, r"(?i)revisión humana")

    def test_la_afirmacion_de_nada_revisado_solo_si_es_verdad(self):
        afirmacion = "**Ninguna de las traducciones ha sido revisada por una persona.**"
        if hay_catalogo_revisado():
            self.assertNotIn(afirmacion, self.s)
        else:
            self.assertIn(afirmacion, self.s)

    def test_la_opcion_7_incluye_el_catalogo_del_idioma(self):
        opcion = re.search(r"(?ms)^### Opción 7.*?(?=^## )", self.t).group(0)
        self.assertIn("i18n-<código>.md", opcion)

    def test_la_documentacion_enlaza_catalogos_registro_guia_y_agentes(self):
        doc = seccion(self.t, "Documentación")
        for fragmento in ("docs/estado-traducciones.md", "docs/guia-web-github.md",
                          "AGENTS.md", "i18n-"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, doc)

    def test_las_limitaciones_incluyen_las_de_idioma(self):
        lim = seccion(self.t, "Limitaciones conocidas")
        for fragmento in ("traducciones", "tokens", "experimental"):
            with self.subTest(fragmento):
                self.assertRegex(lim, rf"(?i){fragmento}")

    def test_los_enlaces_relativos_resuelven(self):
        for destino in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", self.t):
            if re.match(r"[a-z]+:", destino):
                continue
            with self.subTest(destino):
                self.assertTrue((RAIZ / destino).exists(), destino)

    def test_sigue_terminando_con_la_nota_etica(self):
        self.assertIn("asistencia de IA", self.t.strip().split("\n")[-1])


class Changelog(unittest.TestCase):
    def setUp(self):
        t = leer(CHANGELOG)
        m = re.search(r"(?ms)^## \[1\.5\].*?(?=^## \[)", t)
        self.assertIsNotNone(m, "no hay entrada [1.5]")
        self.e = m.group(0)

    def test_tiene_las_cuatro_secciones(self):
        for s in ("Añadido", "Cambiado", "Corregido", "Limitaciones"):
            with self.subTest(s):
                self.assertRegex(self.e, rf"(?m)^### {s}\s*$")

    def test_lista_los_cuatro_cambios_aprobados_al_original(self):
        for fragmento in ("`SKILL.md`", "`flujo.md`", "`auditoria.md`", "adicion"):
            with self.subTest(fragmento):
                self.assertRegex(self.e, rf"(?i){re.escape(fragmento)}")
        self.assertRegex(self.e, r"(?i)ninguna línea (eliminada|reescrita)|0 eliminadas")

    def test_declara_el_estado_real_de_las_traducciones_y_lo_no_verificado(self):
        for fragmento in ("sin revisión humana", "experimental", "EUR-Lex",
                          "plataforma real"):
            with self.subTest(fragmento):
                self.assertRegex(self.e, rf"(?i){re.escape(fragmento)}")

    def test_cita_todos_los_idiomas(self):
        for c in CODIGOS:
            with self.subTest(c):
                self.assertIn(f"`{c}`", self.e)


class Agents(unittest.TestCase):
    def setUp(self):
        self.t = leer(AGENTS)

    def test_cita_los_comandos_de_verificacion_del_ci(self):
        wf = leer(RAIZ / ".github" / "workflows" / "verificar.yml")
        for cmd in re.findall(r"(?m)^\s+- run:\s*(.+?)\s*$", wf):
            with self.subTest(cmd):
                self.assertIn(cmd.replace(" -v", ""), self.t.replace(" -v", ""))

    def test_los_comandos_citados_existen(self):
        for ruta in re.findall(r"python3 (tools/\w+\.py)", self.t):
            with self.subTest(ruta):
                self.assertTrue((RAIZ / ruta).is_file(), ruta)

    def test_recoge_las_reglas_del_multiidioma(self):
        for fragmento in (
            "<!-- i18n:inicio -->", "<!-- i18n:fin -->",       # bloques delimitados
            "frontmatter", "`description`",                    # frontmatter intacto
            "i18n-es.md", "no se edita a mano",                # referencia generada
            "seguridad: sí", "revisión humana",                # diffs de seguridad
            "`revisado`", "experimental",                      # honestidad de estado
            "CI en rojo", "main",                              # el rojo no se fusiona
            "línea base", "reemplazos.txt",                    # el español no cambia
            "[DATO_ELIMINADO]", "[NO_CONSTA]",                 # contratos de máquina
        ):
            with self.subTest(fragmento):
                self.assertIn(fragmento, self.t)

    def test_prohibe_ampliar_exenciones_y_saltarse_pruebas(self):
        self.assertRegex(self.t, r"(?i)no (amplíes|ampliar).{0,40}exenci")
        self.assertRegex(self.t, r"(?i)no (saltes|desactives|omitas).{0,60}prueba")

    def test_distingue_automatico_simulado_y_real(self):
        for fragmento in ("automático", "simulado", "plataforma real"):
            with self.subTest(fragmento):
                self.assertRegex(self.t, rf"(?i){fragmento}")

    def test_declara_los_pendientes_ajenos_conocidos(self):
        self.assertRegex(self.t, r"(?i)derecho foral")
        self.assertRegex(self.t, r"v1\.1")


class Claude(unittest.TestCase):
    def test_remite_a_agents(self):
        t = leer(CLAUDE)
        self.assertIn("AGENTS.md", t)
        self.assertLessEqual(len([l for l in t.split("\n") if l.strip()]), 4)

    def test_el_enlace_a_agents_resuelve(self):
        self.assertTrue(AGENTS.is_file())


if __name__ == "__main__":
    unittest.main()
