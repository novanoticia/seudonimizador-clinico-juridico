"""Pruebas del workflow de CI y de la guía web de GitHub.

No se puede ejecutar GitHub Actions aquí, así que se vigilan las propiedades que
importan: permisos de solo lectura, historial completo (las pruebas comparan con
`git show`), los cuatro comandos de verificación, sin patrones de inyección, y
que la guía cite el MISMO nombre de check que define el workflow (si difieren,
la protección de rama exigiría un check que nunca llega y bloquearía todo).

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import re
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
WORKFLOW = RAIZ / ".github" / "workflows" / "verificar.yml"
GUIA = RAIZ / "docs" / "guia-web-github.md"

COMANDOS_ESPERADOS = [
    "python3 -m unittest discover -s tests -v",
    "python3 tools/validar_i18n.py",
    "python3 tools/extraer_es.py comprobar",
    "python3 tools/linea_base.py comparar",
]


def workflow():
    assert WORKFLOW.is_file(), "falta .github/workflows/verificar.yml"
    return WORKFLOW.read_text(encoding="utf-8")


def guia():
    assert GUIA.is_file(), "falta docs/guia-web-github.md"
    return GUIA.read_text(encoding="utf-8")


def nombre_del_check():
    m = re.search(r"^\s{4}name:\s*(\S+)\s*$", workflow(), re.M)
    assert m, "el job no tiene `name:` explícito"
    return m.group(1)


class Workflow(unittest.TestCase):
    def test_es_yaml_valido_con_la_estructura_esperada(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML no está instalado")
        datos = yaml.safe_load(workflow())
        eventos = datos.get("on", datos.get(True))        # YAML 1.1 lee `on` como True
        self.assertEqual(set(eventos), {"pull_request", "push", "workflow_dispatch"})
        job = datos["jobs"]["verificar"]
        self.assertEqual(job["name"], "verificar")
        self.assertEqual(job["runs-on"], "ubuntu-latest")
        self.assertEqual(datos["permissions"], {"contents": "read"})
        pasos = job["steps"]
        self.assertEqual(pasos[0]["uses"], "actions/checkout@v4")
        self.assertEqual(pasos[0]["with"]["fetch-depth"], 0)
        self.assertEqual([p["run"] for p in pasos if "run" in p], COMANDOS_ESPERADOS)

    def test_existe_y_tiene_nombre(self):
        self.assertRegex(workflow(), r"(?m)^name:\s*\S+")

    def test_se_dispara_en_pull_request_push_y_a_mano(self):
        t = workflow()
        for evento in ("pull_request", "push", "workflow_dispatch"):
            with self.subTest(evento):
                self.assertRegex(t, rf"(?m)^  {evento}:")

    def test_no_usa_pull_request_target(self):
        # Ese evento corre con permisos de escritura sobre código de terceros.
        self.assertNotIn("pull_request_target", workflow())

    def test_permisos_de_solo_lectura(self):
        t = workflow()
        self.assertRegex(t, r"(?m)^permissions:\s*\n  contents: read\s*$")
        self.assertNotRegex(t, r"(?m):\s*write\b")

    def test_no_usa_secretos(self):
        self.assertNotIn("secrets.", workflow())

    def test_los_pasos_run_no_interpolan_expresiones(self):
        # `${{ … }}` dentro de `run:` es la vía clásica de inyección de comandos.
        lineas_run = [l for l in workflow().split("\n") if re.match(r"\s*(-\s+)?run:", l)]
        self.assertEqual(len(lineas_run), 4)       # que la prueba no sea vacía
        for linea in lineas_run:
            self.assertNotIn("${{", linea, linea)

    def test_la_comprobacion_de_inyeccion_detecta_una_expresion(self):
        # Prueba sintética: la misma expresión aplicada a un workflow malo debe fallar.
        malo = "      - run: echo ${{ github.event.pull_request.title }}"
        lineas_run = [l for l in malo.split("\n") if re.match(r"\s*(-\s+)?run:", l)]
        self.assertTrue(any("${{" in l for l in lineas_run))

    def test_historial_completo_para_la_comparacion_con_git(self):
        self.assertRegex(workflow(), r"fetch-depth:\s*0")

    def test_las_acciones_van_fijadas_a_una_version(self):
        usos = re.findall(r"uses:\s*(\S+)", workflow())
        self.assertTrue(usos)
        for uso in usos:
            with self.subTest(uso):
                self.assertRegex(uso, r"@(v\d+(\.\d+)*|[0-9a-f]{40})$")
                self.assertNotRegex(uso, r"@(main|master|latest)$")

    def test_python_3_12_y_tiempo_limite(self):
        t = workflow()
        self.assertRegex(t, r'python-version:\s*"3\.12"')
        self.assertRegex(t, r"timeout-minutes:\s*\d+")

    def test_corre_los_cuatro_comandos_en_este_orden(self):
        comandos = re.findall(r"(?m)^\s+(?:-\s+)?run:\s*(.+?)\s*$", workflow())
        self.assertEqual(comandos, COMANDOS_ESPERADOS)

    def test_el_job_tiene_nombre_ascii_sin_espacios(self):
        # Es el nombre que se escribe en la protección de rama: sin tildes ni
        # espacios para que no haya que adivinar cómo teclearlo.
        self.assertRegex(nombre_del_check(), r"^[a-z][a-z0-9_-]*$")

    def test_no_filtra_por_rutas(self):
        # Un filtro `paths:` haría que el check no llegara a veces y la protección
        # dejaría el PR esperando para siempre.
        self.assertNotRegex(workflow(), r"(?m)^\s+paths(-ignore)?:")

    def test_cancela_ejecuciones_obsoletas_de_la_misma_rama(self):
        self.assertRegex(workflow(), r"cancel-in-progress:\s*true")

    def test_los_comandos_no_destructivos_pasan_en_local(self):
        # unittest se omite a propósito (sería recursivo): lo ejecuta la suite.
        for cmd in COMANDOS_ESPERADOS[1:]:
            with self.subTest(cmd):
                r = subprocess.run(cmd.split(), cwd=RAIZ, capture_output=True, text=True)
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class GuiaWeb(unittest.TestCase):
    def test_cita_el_mismo_nombre_de_check_que_el_workflow(self):
        nombre = nombre_del_check()
        self.assertIn(f"`{nombre}`", guia())

    def test_todas_las_menciones_al_check_usan_el_mismo_nombre(self):
        # Un solo nombre equivocado en la guía haría que la protección exigiera un
        # check que nunca llega y bloquearía todos los PR.
        nombre = nombre_del_check()
        menciones = re.findall(r"checks?[^.\n`]{0,40}`([a-z_-]+)`", guia(), re.I)
        menciones += re.findall(r"Add checks\*\*[^`\n]{0,30}\*\*`([a-z_-]+)`\*\*", guia())
        self.assertGreaterEqual(len(menciones), 4)
        self.assertEqual(set(menciones), {nombre}, menciones)

    def test_explica_la_diferencia_entre_avisar_y_bloquear(self):
        t = guia()
        for fragmento in ("check que avisa", "protección de rama", "bloquea"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, t)

    def test_incluye_los_pasos_basicos_de_la_web(self):
        t = guia()
        for fragmento in ("Pull requests", "New pull request", "Merge pull request",
                          "Settings", "Rules", "Actions"):
            with self.subTest(fragmento):
                self.assertIn(fragmento, t)

    def test_distingue_lo_comprobado_de_lo_que_no(self):
        t = guia()
        self.assertIn("Comprobado en este repositorio", t)
        self.assertIn("No comprobado", t)

    def test_declara_los_hechos_comprobados_del_repositorio(self):
        t = guia()
        self.assertIn("público", t)
        self.assertIn("protected: false", t)

    def test_no_promete_que_el_ci_bloquee_por_si_solo(self):
        t = guia()
        self.assertRegex(t, r"(?i)por sí solo no bloquea|solo avisa|no bloquea nada")

    def test_cierra_con_la_nota_etica(self):
        self.assertIn("asistencia de IA", guia().strip().split("\n")[-1])

    def test_no_se_cita_la_ruta_del_icono_como_texto(self):
        # El validador del directorio de plugins marca esa referencia (CHANGELOG, PR 5).
        self.assertNotIn("icon.png", guia())


if __name__ == "__main__":
    unittest.main()
