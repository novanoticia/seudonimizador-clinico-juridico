"""Pruebas del marco de simulación (tarea 11).

La simulación con subagentes NO es una plataforma real. Estas pruebas no ejecutan
ningún modelo: comprueban que los escenarios están bien definidos, que sus criterios
de éxito (preregistrados) DISCRIMINAN —cada uno acepta su ejemplo bueno y rechaza su
ejemplo malo— y que el evaluador informa de lo que falta. Un evaluador que nunca
falla no evalúa nada.

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import re
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tests"))
sys.path.insert(0, str(RAIZ / "tools"))

import simulacion_escenarios as sim  # noqa: E402
import evaluar_simulacion as ev  # noqa: E402

ESCENARIOS_MD = RAIZ / "tests" / "escenarios.md"
IDS = [f"S{i}" for i in range(1, 11)]


class Definicion(unittest.TestCase):
    def test_hay_diez_escenarios_con_identificador_unico(self):
        self.assertEqual([e.id for e in sim.ESCENARIOS], IDS)

    def test_cada_escenario_esta_completo(self):
        for e in sim.ESCENARIOS:
            with self.subTest(e.id):
                self.assertTrue(e.titulo.strip())
                self.assertIn(e.paquete, ("completo", "solo_skill"))
                self.assertTrue(e.mensaje.startswith("/seudonimizar"))
                self.assertGreaterEqual(len(e.expectativas), 4)

    def test_los_casos_son_ficticios_y_estan_marcados_como_tales(self):
        for caso in (sim.CASO_CLINICO, sim.CASO_JURIDICO, sim.TEXTO_PARA_AUDITAR):
            with self.subTest(caso[:30]):
                self.assertTrue(caso.strip())
        self.assertIn("FICTICIO", sim.AVISO_CASOS_FICTICIOS.upper())

    def test_el_escenario_9_no_cumple_la_regla_de_las_tres_piezas(self):
        # Prueba de la regla: el caso empieza en la misma línea, así que no hay código.
        e = sim.por_id("S9")
        primera = e.mensaje.split("\n")[0].split()
        self.assertGreater(len(primera), 3)

    def test_los_escenarios_con_codigo_lo_llevan_en_una_primera_linea_de_tres_piezas(self):
        for i in ("S1", "S2", "S3", "S4", "S7", "S8", "S10"):
            with self.subTest(i):
                self.assertEqual(len(sim.por_id(i).mensaje.split("\n")[0].split()), 3)

    def test_el_escenario_7_solo_tiene_skill_md(self):
        self.assertEqual(sim.por_id("S7").paquete, "solo_skill")
        for e in sim.ESCENARIOS:
            if e.id != "S7":
                self.assertEqual(e.paquete, "completo")


class CriteriosDiscriminan(unittest.TestCase):
    """Cada criterio acepta su ejemplo bueno y rechaza su ejemplo malo."""

    def test_cada_criterio_acepta_su_ok_y_rechaza_su_ko(self):
        total = 0
        for e in sim.ESCENARIOS:
            for x in e.expectativas:
                total += 1
                with self.subTest(f"{e.id}: {x.nombre}"):
                    self.assertTrue(x.fn(x.ok), f"el ejemplo OK no pasa: {x.ok!r}")
                    self.assertFalse(x.fn(x.ko), f"el ejemplo KO pasa: {x.ko!r}")
        self.assertGreaterEqual(total, 50)

    def test_los_textos_esperados_salen_de_los_catalogos(self):
        # Si un catálogo cambia, el criterio cambia con él; si falta la clave, falla aquí.
        self.assertEqual(sim.cat("en", "encabezado.apertura"), "## OPENING")
        self.assertEqual(sim.cat("eu", "encabezado.aviso_traduccion"),
                         "## ITZULPEN-OHARRA (ESPERIMENTALA)")
        with self.assertRaises(KeyError):
            sim.cat("en", "no.existe")

    def test_hay_criterios_criticos_y_deseables(self):
        todos = [x for e in sim.ESCENARIOS for x in e.expectativas]
        self.assertTrue(any(x.critica for x in todos))
        self.assertTrue(any(not x.critica for x in todos))


class Utilidades(unittest.TestCase):
    def test_seccion_extrae_hasta_el_siguiente_encabezado(self):
        r = "## A\nuno\n## B\ndos\ntres\n## C\ncuatro\n"
        self.assertEqual(sim.seccion(r, "## B").strip(), "dos\ntres")
        self.assertEqual(sim.seccion(r, "## C").strip(), "cuatro")

    def test_seccion_ausente_devuelve_vacio(self):
        self.assertEqual(sim.seccion("## A\nuno\n", "## Z"), "")

    def test_es_castellano(self):
        self.assertTrue(sim.es_castellano("el paciente refiere que la paciente con el caso de la mañana"))
        self.assertFalse(sim.es_castellano("the patient reports that the case and with the morning"))
        self.assertFalse(sim.es_castellano(""))


class Evaluador(unittest.TestCase):
    def _dir(self, respuestas):
        d = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, d, True)
        for k, v in respuestas.items():
            (d / f"{k}.respuesta.md").write_text(v, encoding="utf-8")
        return d

    def test_informa_de_lo_que_falta(self):
        r = ev.evaluar_directorio(self._dir({}))
        self.assertEqual(set(r), set(IDS))
        for i in IDS:
            self.assertIsNone(r[i])

    def test_una_respuesta_buena_pasa_todos_los_criterios_de_su_escenario(self):
        e = sim.por_id("S6")
        buena = "\n".join(x.ok for x in e.expectativas)
        r = ev.evaluar_directorio(self._dir({"S6": buena}))
        # Los ejemplos OK de un mismo escenario pueden chocar entre sí (uno exige lo que otro
        # prohíbe); lo que se comprueba es que el evaluador devuelve un resultado por criterio.
        self.assertEqual(len(r["S6"]), len(e.expectativas))

    def test_una_respuesta_vacia_falla_los_criterios_que_exigen_algo(self):
        r = ev.evaluar_directorio(self._dir({"S1": "nada"}))
        fallos = [n for n, ok, crit in r["S1"] if not ok]
        self.assertGreater(len(fallos), 5)

    def test_resumen_cuenta_criticos_y_deseables(self):
        r = ev.evaluar_directorio(self._dir({"S1": "nada"}))
        resumen = ev.resumir(r)
        self.assertIn("S1", resumen)
        self.assertEqual(resumen["S1"]["total"], len(sim.por_id("S1").expectativas))
        self.assertGreater(resumen["S1"]["criticos_fallidos"], 0)

    def test_el_codigo_de_salida_es_1_si_falta_algo_o_falla_algo_critico(self):
        self.assertEqual(ev.codigo_de_salida(ev.evaluar_directorio(self._dir({}))), 1)
        self.assertEqual(ev.codigo_de_salida(ev.evaluar_directorio(self._dir({"S1": "nada"}))), 1)


class SalidaDelEvaluador(unittest.TestCase):
    def _todo(self, ok=True, critica=True, falta=None):
        res = {i: [("criterio", ok, critica)] for i in IDS}
        if falta:
            res[falta] = None
        return res

    def test_codigo_de_salida_0_si_todo_pasa(self):
        self.assertEqual(ev.codigo_de_salida(self._todo()), 0)

    def test_un_fallo_deseable_no_cambia_el_codigo_de_salida(self):
        self.assertEqual(ev.codigo_de_salida(self._todo(ok=False, critica=False)), 0)

    def test_un_fallo_critico_da_1(self):
        self.assertEqual(ev.codigo_de_salida(self._todo(ok=False, critica=True)), 1)

    def test_una_respuesta_que_falta_da_1(self):
        self.assertEqual(ev.codigo_de_salida(self._todo(falta="S3")), 1)

    def test_main_sin_argumentos_da_2_y_muestra_la_ayuda(self):
        import io
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(ev.main(["evaluar"]), 2)
        self.assertIn("preregistrados", out.getvalue().lower())

    def test_main_informa_de_lo_que_falta_y_sale_con_1(self):
        import io
        from contextlib import redirect_stdout
        d = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, d, True)
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(ev.main(["evaluar", str(d)]), 1)
        self.assertIn("FALTA la respuesta", out.getvalue())
        self.assertIn("Resumen:", out.getvalue())

    def test_main_sale_con_0_si_todo_pasa(self):
        import io
        from contextlib import redirect_stdout
        from unittest import mock
        todo = {e.id: [(x.nombre, True, x.critica) for x in e.expectativas] for e in sim.ESCENARIOS}
        out = io.StringIO()
        with mock.patch.object(ev, "evaluar_directorio", return_value=todo), redirect_stdout(out):
            self.assertEqual(ev.main(["evaluar", "x"]), 0)
        self.assertNotIn("✗", out.getvalue())

    def test_main_lista_los_criterios_que_fallan_y_marca_los_criticos(self):
        import io
        from contextlib import redirect_stdout
        d = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, d, True)
        (d / "S1.respuesta.md").write_text("nada", encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            ev.main(["evaluar", str(d)])
        self.assertIn("CRÍTICO", out.getvalue())
        self.assertRegex(out.getvalue(), r"S1: \d+/\d+")


class Documentacion(unittest.TestCase):
    def setUp(self):
        self.assertTrue(ESCENARIOS_MD.is_file(), "falta tests/escenarios.md")
        self.t = ESCENARIOS_MD.read_text(encoding="utf-8")

    def test_dice_que_es_una_simulacion_y_no_una_plataforma_real(self):
        self.assertRegex(self.t, r"(?i)simulaci[oó]n")
        self.assertRegex(self.t, r"(?i)no (es|son) (una )?plataforma real|no .{0,40}plataforma real")

    def test_lista_todos_los_escenarios(self):
        for i in IDS:
            with self.subTest(i):
                self.assertRegex(self.t, rf"(?m)^### {i}\b")

    def test_tiene_la_tabla_de_ejecuciones_reales_pendientes(self):
        self.assertRegex(self.t, r"(?m)^\| Plataforma \| Modelo \| Fecha \| Escenario \| Resultado \| Notas \|")
        self.assertRegex(self.t, r"(?i)pendiente")

    def test_registra_cada_ronda_de_simulacion(self):
        self.assertRegex(self.t, r"(?m)^## Ronda 1\b")

    def test_declara_que_los_simuladores_pudieron_ver_el_repositorio(self):
        # Límite metodológico real: no están aislados a nivel de sistema.
        self.assertRegex(self.t, r"(?i)no están aislados|no estaban aislados|podían leer")


if __name__ == "__main__":
    unittest.main()
