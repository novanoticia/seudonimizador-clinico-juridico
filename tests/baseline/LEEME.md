# Línea base del idioma por defecto (español)

Captura del original en el commit indicado en `commit_base.txt`. Criterio de éxito
principal del proyecto multiidioma: **el español no cambia**.

| Fichero | Qué guarda |
|---|---|
| `commit_base.txt` | Commit del que se capturó todo (no del árbol de trabajo, para que sea determinista). |
| `lineas.json` | Para cada `.md` del skill: nº de líneas, SHA-256 del fichero y de cada línea. |
| `frontmatter.json` | Claves, `name`, hash/longitud de `description` de `SKILL.md`. |
| `manifiestos.json` | Los tres manifiestos sin el campo `version` (lo único que puede cambiar). |
| `paquete.json` | SHA-256 de cada miembro del `.zip` generado por `scripts/build-dist.sh`. |
| `reemplazos.txt` | Lista **cerrada** de líneas del original que pueden cambiar. Vacía: solo se aprobaron adiciones. |

## Qué se permite distinto de la línea base
1. **Adiciones** entre `<!-- i18n:inicio -->` y `<!-- i18n:fin -->`, más una línea en
   blanco inmediatamente posterior (si la hay y no es el salto final del fichero).
2. Las líneas de `reemplazos.txt`, una a una.
3. El campo `version` de los manifiestos.
4. Ficheros nuevos `i18n-<código>.md` en el paquete.

Cualquier otra diferencia es un fallo.

## Comandos
```bash
python3 tools/linea_base.py comparar        # compara el árbol con la línea base
python3 -m unittest discover -s tests -v    # pruebas (incluye pruebas que deben fallar)
python3 tools/linea_base.py capturar <commit>   # SOLO para rehacer la base: requiere aprobación
```
La comparación con `git show` necesita el historial completo (`fetch-depth: 0` en CI).
