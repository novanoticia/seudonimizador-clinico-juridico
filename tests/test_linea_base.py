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


if __name__ == "__main__":
    unittest.main()
