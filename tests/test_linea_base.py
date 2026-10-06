"""Pruebas de la línea base del idioma por defecto (español).

Criterio de éxito principal del proyecto: el español no cambia. Estas pruebas
comprueban que (a) la comparación contra la línea base pasa en el árbol real y
(b) FALLA cuando debe: una línea base que no puede fallar no vale nada.

Ejecutar:  python3 -m unittest discover -s tests -v
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))

import linea_base as lb  # noqa: E402

SKILL = RAIZ / lb.SKILL_DIR
INICIO, FIN = lb.INICIO, lb.FIN


def leer(nombre):
    return (SKILL / nombre).read_text(encoding="utf-8")


def con_bloque(texto, despues_de_linea, cuerpo="Texto añadido de prueba."):
    """Inserta un bloque delimitado (más su línea en blanco final) tras una línea."""
    ls = texto.split("\n")
    bloque = [INICIO, cuerpo, FIN, ""]
    return "\n".join(ls[:despues_de_linea] + bloque + ls[despues_de_linea:])


class LineaBaseExiste(unittest.TestCase):
    def test_ficheros_de_la_linea_base(self):
        for f in ("commit_base.txt", "lineas.json", "frontmatter.json",
                  "manifiestos.json", "paquete.json", "reemplazos.txt"):
            self.assertTrue((RAIZ / "tests" / "baseline" / f).is_file(), f)

    def test_commit_base_existe_en_git(self):
        commit = lb.commit_base()
        r = subprocess.run(["git", "cat-file", "-e", commit + "^{commit}"],
                           cwd=RAIZ, capture_output=True)
        self.assertEqual(r.returncode, 0, "el commit base no está en el historial")

    def test_cubre_los_cinco_md(self):
        datos = json.loads((RAIZ / "tests/baseline/lineas.json").read_text())
        self.assertEqual(sorted(datos), sorted(lb.FICHEROS_MD))

    def test_reemplazos_vacio_hasta_que_se_apruebe_otra_cosa(self):
        # Lista cerrada: la Fase 1.4 aprobó solo ADICIONES, ninguna reescritura.
        self.assertEqual(lb.leer_reemplazos(), {})


class ArbolReal(unittest.TestCase):
    def test_arbol_coincide_con_la_linea_base(self):
        self.assertEqual(lb.comparar_todo(RAIZ), [])

    def test_comparacion_con_git_show(self):
        # Segunda vía, independiente de los hashes: texto íntegro del commit base.
        for f in lb.FICHEROS_MD:
            with self.subTest(f):
                self.assertEqual(lb.comparar_con_git(f, leer(f)), [])

    def test_description_bajo_el_limite_de_mistral(self):
        fm = lb.frontmatter(leer("SKILL.md"))
        self.assertLess(len(fm["description"]), 500)
        self.assertLess(len(fm["description"].encode()), 1024)

    def test_frontmatter_conjunto_cerrado(self):
        self.assertEqual(lb.frontmatter(leer("SKILL.md"))["claves"],
                         ["name", "description"])


class SinteticasDebenFallar(unittest.TestCase):
    """Cada prueba rompe a propósito una copia en memoria y exige que falle."""

    def test_cambiar_una_linea_fuera_de_marcadores_falla_y_la_localiza(self):
        ls = leer("flujo.md").split("\n")
        ls[5] = ls[5] + " (alterada)"
        errores = lb.comparar_md("flujo.md", "\n".join(ls))
        self.assertTrue(errores)
        self.assertIn("flujo.md", errores[0])
        self.assertIn("6", errores[0])  # línea 6 del original

    def test_borrar_una_linea_falla(self):
        ls = leer("SKILL.md").split("\n")
        del ls[20]
        self.assertTrue(lb.comparar_md("SKILL.md", "\n".join(ls)))

    def test_anadir_una_linea_fuera_de_marcadores_falla(self):
        ls = leer("auditoria.md").split("\n")
        ls.insert(30, "línea intrusa")
        self.assertTrue(lb.comparar_md("auditoria.md", "\n".join(ls)))

    def test_anadir_un_bloque_delimitado_pasa(self):
        for f in ("SKILL.md", "flujo.md", "auditoria.md"):
            with self.subTest(f):
                self.assertEqual(
                    lb.comparar_md(f, con_bloque(leer(f), 25)), [])

    def test_bloque_al_final_del_fichero_pasa(self):
        texto = leer("flujo.md")
        ls = texto.split("\n")
        # ls termina en '' (salto final); insertamos antes de ese ''.
        nuevo = "\n".join(ls[:-1] + [INICIO, "x", FIN] + [ls[-1]])
        self.assertEqual(lb.comparar_md("flujo.md", nuevo), [])

    def test_marcador_sin_cerrar_falla(self):
        ls = leer("SKILL.md").split("\n")
        ls[30:30] = [INICIO, "texto"]
        self.assertTrue(lb.comparar_md("SKILL.md", "\n".join(ls)))

    def test_marcador_fin_sin_inicio_falla(self):
        ls = leer("SKILL.md").split("\n")
        ls[30:30] = [FIN]
        self.assertTrue(lb.comparar_md("SKILL.md", "\n".join(ls)))

    def test_marcadores_anidados_fallan(self):
        ls = leer("SKILL.md").split("\n")
        ls[30:30] = [INICIO, INICIO, "x", FIN, FIN]
        self.assertTrue(lb.comparar_md("SKILL.md", "\n".join(ls)))

    def test_reemplazos_permiten_solo_la_linea_listada(self):
        ls = leer("flujo.md").split("\n")
        ls[5] = "reescrita con permiso"
        self.assertEqual(lb.comparar_md("flujo.md", "\n".join(ls), {6}), [])
        ls[7] = "reescrita SIN permiso"
        self.assertTrue(lb.comparar_md("flujo.md", "\n".join(ls), {6}))

    def test_tocar_el_frontmatter_falla(self):
        t = leer("SKILL.md").replace("name: seudonimizador-clinico-juridico",
                                     "name: otro-nombre", 1)
        self.assertTrue(lb.comparar_frontmatter(t))

    def test_anadir_clave_al_frontmatter_falla(self):
        t = leer("SKILL.md").replace("description: >-", "version: 9\ndescription: >-", 1)
        self.assertTrue(lb.comparar_frontmatter(t))

    def test_description_mas_larga_de_500_caracteres_falla(self):
        t = leer("SKILL.md").replace("RGPD/LOPDGDD para publicación",
                                     "RGPD/LOPDGDD " + "x" * 600 + " para publicación", 1)
        self.assertTrue(lb.comparar_frontmatter(t))


class ReglasAisladas(unittest.TestCase):
    """Cada regla se ejercita sola, sin que otra la tape."""

    def test_limite_de_caracteres_de_mistral(self):
        self.assertEqual(lb.limites_description("x" * 499), [])
        self.assertTrue(lb.limites_description("x" * 500))

    def test_limite_de_bytes_de_perplexity(self):
        self.assertEqual(lb.limites_description("é" * 450), [])      # 900 B, 450 car.
        # 400 caracteres (< 500) pero 1200 bytes (>= 1024): solo salta el de bytes.
        r = lb.limites_description("€" * 400)
        self.assertEqual(len(r), 1)
        self.assertIn("bytes", r[0])

    def test_los_errores_de_marcadores_se_informan_por_si_solos(self):
        _, errores = lb.quitar_bloques(["a", INICIO, "b"])
        self.assertTrue(any("sin cerrar" in e for e in errores))
        _, errores = lb.quitar_bloques(["a", FIN, "b"])
        self.assertTrue(any("sin inicio" in e for e in errores))
        _, errores = lb.quitar_bloques([INICIO, INICIO, FIN, FIN])
        self.assertTrue(any("anidado" in e for e in errores))
        _, errores = lb.quitar_bloques(["a", INICIO, "b", FIN, "c"])
        self.assertEqual(errores, [])


class Manifiestos(unittest.TestCase):
    def test_arbol_real(self):
        self.assertEqual(lb.comparar_manifiestos(RAIZ), [])

    def test_la_version_puede_cambiar_la_descripcion_no(self):
        base = json.loads((RAIZ / "plugin.json").read_text())
        ok = dict(base, version="9.9.9")
        self.assertEqual(lb.comparar_manifiesto_dato("plugin.json", ok), [])
        mal = dict(base, description=base["description"] + " x")
        self.assertTrue(lb.comparar_manifiesto_dato("plugin.json", mal))


def arbol_con(extra):
    """Copia temporal del árbol con ficheros añadidos a la carpeta del skill."""
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    copia = Path(tmp) / "r"
    shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
    for nombre, contenido in extra.items():
        (copia / lb.SKILL_DIR / nombre).write_text(contenido, encoding="utf-8")
    return tmp, copia


class Paquete(unittest.TestCase):
    def test_un_catalogo_i18n_entra_solo_en_el_paquete(self):
        tmp, copia = arbol_con({"i18n-xx.md": "# prueba\n"})
        try:
            r = lb.comparar_paquete(copia)
            miembros = lb.construir_paquete(copia)["miembros"]
        finally:
            import shutil
            shutil.rmtree(tmp)
        self.assertEqual(r, [])
        self.assertIn(f"{lb.NOMBRE}/i18n-xx.md", miembros)

    def test_un_fichero_md_inesperado_en_el_paquete_falla(self):
        tmp, copia = arbol_con({"notas-privadas.md": "# no debería viajar\n"})
        try:
            r = lb.comparar_paquete(copia)
        finally:
            import shutil
            shutil.rmtree(tmp)
        self.assertTrue(any("inesperado" in e for e in r), r)

    def test_un_catalogo_con_nombre_mal_formado_falla(self):
        tmp, copia = arbol_con({"i18n-ES.md": "x", "i18n-.md": "x"})
        try:
            r = lb.comparar_paquete(copia)
        finally:
            import shutil
            shutil.rmtree(tmp)
        self.assertEqual(len([e for e in r if "inesperado" in e]), 2, r)


    def test_contenido_del_paquete_igual_a_la_linea_base(self):
        self.assertEqual(lb.comparar_paquete(RAIZ), [])

    def test_si_el_skill_deja_de_ser_copia_del_zip_se_informa(self):
        from unittest import mock
        real = lb.construir_paquete(RAIZ)
        roto = dict(real, skill_igual_zip=False)
        with mock.patch.object(lb, "construir_paquete", return_value=roto):
            r = lb.comparar_paquete(RAIZ)
        self.assertTrue(any(".skill" in e for e in r), r)

    def test_el_skill_es_copia_exacta_del_zip(self):
        self.assertTrue(lb.construir_paquete(RAIZ)["skill_igual_zip"])


# ── pruebas añadidas tras el sabotaje sistemático ────────────────────────────

def copiar_arbol(con_git=False):
    """Copia temporal del árbol (opcionalmente con .git). Devuelve (tmp, copia)."""
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp()
    copia = Path(tmp) / "r"
    ignorar = ["dist", "__pycache__"] + ([] if con_git else [".git"])
    shutil.copytree(RAIZ, copia, ignore=shutil.ignore_patterns(*ignorar))
    return tmp, copia


class FinalDeFichero(unittest.TestCase):
    """Lo que se pierde o se añade AL FINAL no puede pasar inadvertido."""

    def test_borrar_la_ultima_linea_falla(self):
        ls = leer("plantilla-tokens.md").split("\n")
        self.assertTrue(lb.comparar_md("plantilla-tokens.md", "\n".join(ls[:-2] + [ls[-1]])))

    def test_quitar_el_salto_de_linea_final_falla(self):
        self.assertTrue(lb.comparar_md("flujo.md", leer("flujo.md").rstrip("\n")))

    def test_anadir_lineas_al_final_falla(self):
        errores = lb.comparar_md("flujo.md", leer("flujo.md") + "extra\n")
        self.assertTrue(any("líneas" in e for e in errores), errores)

    def test_el_informe_localiza_la_primera_divergencia(self):
        ls = leer("flujo.md").split("\n")
        ls.insert(10, "intrusa")
        errores = lb.comparar_md("flujo.md", "\n".join(ls))
        self.assertTrue(any("primera divergencia en la línea 11" in e for e in errores), errores)


class ComparacionConGitEnNegativo(unittest.TestCase):
    def test_cambiar_una_linea_falla(self):
        ls = leer("auditoria.md").split("\n")
        ls[3] = "alterada"
        self.assertTrue(lb.comparar_con_git("auditoria.md", "\n".join(ls)))

    def test_cambiar_el_numero_de_lineas_falla(self):
        self.assertTrue(lb.comparar_con_git("auditoria.md", leer("auditoria.md") + "x\n"))

    def test_una_linea_de_mas_tras_el_salto_final_se_detecta_por_longitud(self):
        # Las líneas anteriores coinciden una a una: solo la longitud lo delata.
        errores = lb.comparar_con_git("auditoria.md", leer("auditoria.md") + "\nextra")
        self.assertTrue(any("nº de líneas" in e for e in errores), errores)

    def test_bloques_mal_formados_fallan(self):
        ls = leer("auditoria.md").split("\n")
        ls[3:3] = [INICIO]
        self.assertTrue(lb.comparar_con_git("auditoria.md", "\n".join(ls)))

    def test_un_bloque_delimitado_pasa(self):
        self.assertEqual(
            lb.comparar_con_git("auditoria.md", con_bloque(leer("auditoria.md"), 12)), [])


class FrontmatterFormas(unittest.TestCase):
    def test_sin_frontmatter_lanza_error(self):
        with self.assertRaises(ValueError):
            lb.frontmatter("# solo un titulo\n")

    def test_description_en_la_misma_linea(self):
        fm = lb.frontmatter("---\nname: x\ndescription: texto simple\n---\ncuerpo\n")
        self.assertEqual(fm["description"], "texto simple")
        self.assertEqual(fm["claves"], ["name", "description"])

    def test_la_description_no_absorbe_la_clave_siguiente(self):
        fm = lb.frontmatter("---\ndescription: >-\n  uno\n  dos\nname: x\n---\n")
        self.assertEqual(fm["description"], "uno dos")
        self.assertEqual(fm["name"], "x")
        self.assertEqual(fm["claves"], ["description", "name"])

    def test_una_linea_suelta_antes_de_description_no_cuenta(self):
        fm = lb.frontmatter("---\nname: x\n  linea suelta\ndescription: >-\n  a\n---\n")
        self.assertEqual(fm["description"], "a")

    def test_los_marcadores_de_bloque_no_son_descripcion(self):
        fm = lb.frontmatter("---\nname: x\ndescription: >-\n  a\n---\n")
        self.assertEqual(fm["description"], "a")

    def test_cambio_pequeno_de_description_falla(self):
        t = leer("SKILL.md").replace("Seudonimiza casos clínicos", "Seudonimiza casos jurídicos", 1)
        errores = lb.comparar_frontmatter(t)
        self.assertTrue(any("`description` ha cambiado" in e for e in errores), errores)


class PaqueteEnNegativo(unittest.TestCase):
    def _comparar(self, modificar):
        import shutil
        tmp, copia = copiar_arbol()
        try:
            modificar(copia)
            return lb.comparar_paquete(copia)
        finally:
            shutil.rmtree(tmp)

    def test_falta_un_fichero_del_paquete(self):
        r = self._comparar(lambda c: (c / lb.SKILL_DIR / "plantilla-tokens.md").unlink())
        self.assertTrue(any("falta" in e and "plantilla-tokens.md" in e for e in r), r)

    def test_cambia_un_fichero_que_no_es_md(self):
        r = self._comparar(lambda c: (c / "LICENSE").write_text("otra licencia\n"))
        self.assertTrue(any("LICENSE" in e and "ha cambiado" in e for e in r), r)

    def test_cambia_un_md_dentro_del_paquete(self):
        def mod(c):
            f = c / lb.SKILL_DIR / "flujo.md"
            f.write_text(f.read_text(encoding="utf-8").replace("No inventar", "Inventar", 1),
                         encoding="utf-8")
        r = self._comparar(mod)
        self.assertTrue(any(e.startswith("paquete/flujo.md") for e in r), r)


class LeerReemplazos(unittest.TestCase):
    def _con(self, contenido):
        import shutil
        import tempfile
        from unittest import mock
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, True)
        if contenido is not None:
            (tmp / "reemplazos.txt").write_text(contenido, encoding="utf-8")
        # commit_base() lee de DIR_BASE: la copia mantiene el mismo commit.
        (tmp / "commit_base.txt").write_text(lb.commit_base() + "\n")
        return mock.patch.object(lb, "DIR_BASE", tmp)

    def test_fichero_ausente(self):
        with self._con(None):
            self.assertEqual(lb.leer_reemplazos(), {})

    def test_parsea_comentarios_vacias_y_varias_lineas(self):
        contenido = ("# comentario\n\nflujo.md:12   # regla 6\n"
                     "flujo.md:13\nSKILL.md:7\n   \n")
        with self._con(contenido):
            self.assertEqual(lb.leer_reemplazos(),
                             {"flujo.md": {12, 13}, "SKILL.md": {7}})

    def test_una_linea_listada_permite_el_cambio_en_todo_el_flujo(self):
        ls = leer("flujo.md").split("\n")
        ls[5] = "reescrita con permiso"
        with self._con("flujo.md:6\n"):
            self.assertEqual(lb.comparar_con_git("flujo.md", "\n".join(ls)), [])


class CapturaYLineaDeComandos(unittest.TestCase):
    def test_la_captura_es_reproducible(self):
        """Recapturar desde el mismo commit da exactamente la línea base guardada."""
        import shutil
        tmp, copia = copiar_arbol(con_git=True)
        try:
            base = copia / "tests" / "baseline"
            for f in base.iterdir():
                if f.name not in ("LEEME.md", "reemplazos.txt"):
                    f.unlink()
            r = subprocess.run([sys.executable, str(copia / "tools" / "linea_base.py"),
                                "capturar", lb.commit_base()],
                               cwd=copia, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            for f in ("commit_base.txt", "lineas.json", "frontmatter.json",
                      "manifiestos.json", "paquete.json"):
                self.assertEqual((base / f).read_bytes(),
                                 (RAIZ / "tests" / "baseline" / f).read_bytes(), f)
        finally:
            shutil.rmtree(tmp)

    def test_la_captura_crea_reemplazos_si_no_existe_y_no_lo_pisa(self):
        import shutil
        tmp, copia = copiar_arbol(con_git=True)
        try:
            ruta = copia / "tests" / "baseline" / "reemplazos.txt"
            ruta.unlink()
            cmd = [sys.executable, str(copia / "tools" / "linea_base.py"),
                   "capturar", lb.commit_base()]
            subprocess.run(cmd, cwd=copia, capture_output=True, check=True)
            self.assertIn("ADICIONES", ruta.read_text(encoding="utf-8"))
            ruta.write_text("flujo.md:6\n", encoding="utf-8")
            subprocess.run(cmd, cwd=copia, capture_output=True, check=True)
            self.assertEqual(ruta.read_text(encoding="utf-8"), "flujo.md:6\n")
        finally:
            shutil.rmtree(tmp)

    def _cli(self, *args, cwd=RAIZ):
        return subprocess.run([sys.executable, str(RAIZ / "tools" / "linea_base.py"), *args],
                              cwd=cwd, capture_output=True, text=True)

    def test_comparar_sale_con_0_en_el_arbol_real(self):
        r = self._cli("comparar")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("OK", r.stdout)

    def test_comparar_sale_con_1_si_algo_cambia(self):
        import shutil
        tmp, copia = copiar_arbol()
        try:
            f = copia / lb.SKILL_DIR / "flujo.md"
            f.write_text(f.read_text(encoding="utf-8").replace("No inventar", "Inventar", 1),
                         encoding="utf-8")
            r = subprocess.run([sys.executable, str(copia / "tools" / "linea_base.py"), "comparar"],
                               cwd=copia, capture_output=True, text=True)
        finally:
            shutil.rmtree(tmp)
        self.assertEqual(r.returncode, 1)
        self.assertIn("✗", r.stdout)

    def test_sin_argumentos_sale_con_2_y_muestra_la_ayuda(self):
        r = self._cli()
        self.assertEqual(r.returncode, 2)
        self.assertIn("capturar", r.stdout)


if __name__ == "__main__":
    unittest.main()
