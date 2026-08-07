#!/bin/bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════════
# build-dist.sh — regenera dist/ desde skills/<nombre>/
#
# Hasta la v1.3 el paquete se armaba a mano desde la raíz del repo. Al
# pasar el skill a skills/<nombre>/ (estructura de Agent Plugins 1.0.0)
# la fuente cambia de sitio, así que el empaquetado deja de ser algo que
# recordar y pasa a ser este script.
#
# El paquete NO cambia de forma: sigue siendo un zip con una carpeta
# <nombre>/ en la raíz que contiene el SKILL.md, sus acompañantes y la
# LICENSE. Eso es lo que esperan los cinco destinos del README —
# claude.ai, Perplexity, Mistral, Claude Code y la copia manual—, y el
# estándar Agent Skills pide justamente que la carpeta se llame igual
# que el `name` del frontmatter.
#
# El .skill es una copia byte a byte del .zip: algunos destinos filtran
# por extensión.
#
# Uso:  ./scripts/build-dist.sh
# ═══════════════════════════════════════════════════════════════

NOMBRE="seudonimizador-clinico-juridico"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ORIGEN="skills/$NOMBRE"
[ -f "$ORIGEN/SKILL.md" ] || { echo "❌ no encuentro $ORIGEN/SKILL.md"; exit 1; }

STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$STAGE/$NOMBRE"
cp "$ORIGEN"/*.md "$STAGE/$NOMBRE/"
cp LICENSE "$STAGE/$NOMBRE/"

mkdir -p dist
rm -f dist/"$NOMBRE".zip dist/"$NOMBRE".skill
( cd "$STAGE" && zip -qrX "$ROOT/dist/$NOMBRE.zip" "$NOMBRE" )
cp dist/"$NOMBRE".zip dist/"$NOMBRE".skill

echo "✅ dist/ regenerado:"
unzip -l dist/"$NOMBRE".zip | tail -n +4 | head -n -2 | awk '{print "   " $4}'
