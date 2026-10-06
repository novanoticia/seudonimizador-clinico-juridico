#!/usr/bin/env python3
"""Evalúa las respuestas de una ronda de simulación contra los criterios PREREGISTRADOS
de tests/simulacion_escenarios.py.

La simulación NO es una plataforma real. Este evaluador solo comprueba lo que se pudo
preregistrar de forma mecánica; la lectura de las respuestas y de las notas de los
simuladores sigue siendo necesaria.

Uso:  python3 tools/evaluar_simulacion.py <directorio con S1.respuesta.md … S10.respuesta.md>
Sale con 1 si falta alguna respuesta o falla algún criterio crítico.
"""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tests"))

import simulacion_escenarios as sim  # noqa: E402


def evaluar_directorio(directorio):
    """{id: None si falta la respuesta | [(criterio, pasa, crítico)]}."""
    directorio = Path(directorio)
    res = {}
    for e in sim.ESCENARIOS:
        f = directorio / f"{e.id}.respuesta.md"
        if not f.is_file():
            res[e.id] = None
            continue
        r = f.read_text(encoding="utf-8")
        res[e.id] = [(x.nombre, bool(x.fn(r)), x.critica) for x in e.expectativas]
    return res


def resumir(resultados):
    out = {}
    for i, lista in resultados.items():
        if lista is None:
            out[i] = {"falta": True, "total": len(sim.por_id(i).expectativas),
                      "fallidos": None, "criticos_fallidos": None}
            continue
        out[i] = {"falta": False, "total": len(lista),
                  "fallidos": sum(1 for _, ok, _ in lista if not ok),
                  "criticos_fallidos": sum(1 for _, ok, crit in lista if not ok and crit)}
    return out


def codigo_de_salida(resultados):
    for i, r in resumir(resultados).items():
        if r["falta"] or r["criticos_fallidos"]:
            return 1
    return 0


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    resultados = evaluar_directorio(argv[1])
    for e in sim.ESCENARIOS:
        lista = resultados[e.id]
        if lista is None:
            print(f"\n{e.id} — {e.titulo}\n  ✗ FALTA la respuesta")
            continue
        fallos = [(n, c) for n, ok, c in lista if not ok]
        print(f"\n{e.id} — {e.titulo}\n  {len(lista) - len(fallos)}/{len(lista)} criterios")
        for n, c in fallos:
            print(f"  ✗ {'CRÍTICO ' if c else 'deseable'} {n}")
    r = resumir(resultados)
    print("\nResumen:",
          ", ".join(f"{i}: " + ("falta" if v["falta"] else f"{v['total'] - v['fallidos']}/{v['total']}"
                                 + (f" ({v['criticos_fallidos']} críticos)" if v["criticos_fallidos"] else ""))
                    for i, v in r.items()))
    return codigo_de_salida(resultados)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
