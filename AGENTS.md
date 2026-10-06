# AGENTS.md — reglas para quien modifique este repositorio

Para personas y agentes. Si algo de aquí choca con una instrucción puntual de la persona
responsable del repositorio, manda ella, pero **dilo** en vez de resolverlo en silencio.

## Qué es esto

Un **skill de instrucciones** (Markdown) para un modelo: no tiene código ejecutable. El skill vive en
`skills/seudonimizador-clinico-juridico/`. Lo que hay en `tools/` y `tests/` solo **verifica** el
skill y no forma parte del paquete que se distribuye. Solo biblioteca estándar de Python: no añadas
dependencias.

## Comandos de verificación

Ejecútalos antes de dar nada por hecho. Son los mismos que corre el CI (check `verificar`).

```bash
python3 -m unittest discover -s tests -v
python3 tools/validar_i18n.py
python3 tools/extraer_es.py comprobar
python3 tools/linea_base.py comparar
```

Para regenerar la referencia en español tras tocar el original: `python3 tools/extraer_es.py escribir`.

## Reglas del multiidioma

1. **El español no cambia.** Es el criterio de éxito principal. `python3 tools/linea_base.py comparar`
   debe pasar: solo se permiten **adiciones** entre `<!-- i18n:inicio -->` y `<!-- i18n:fin -->` (con una
   línea en blanco antes y otra después). No reescribas ni borres líneas del original. Si de verdad hiciera
   falta, la única vía es la lista cerrada `tests/baseline/reemplazos.txt`, con aprobación expresa y una
   justificación en el CHANGELOG. Rehacer la línea base (`linea_base.py capturar`) también exige aprobación.
2. **Ningún texto visible fuera del catálogo.** Todo encabezado o etiqueta de una plantilla de salida es un
   literal con clave (lo comprueba `tools/extraer_es.py`) o una instrucción declarada. No escribas literales
   nuevos fuera del catálogo. **`i18n-es.md` se genera y no se edita a mano.**
3. **Frontmatter intacto.** El `frontmatter` de `SKILL.md` solo tiene `name` y `description`: una clave de
   más falla con error duro en varias plataformas. No toques la `description`: debe medir menos de 500
   caracteres (Mistral cuenta caracteres) y menos de 1024 bytes (Perplexity cuenta bytes).
4. **No se traducen** los contratos de máquina: tokens (`[PACIENTE_A]`…), `[DATO_ELIMINADO]`,
   `[NO_CONSTA]`, modos (`A`, `B`, `C`, `audit`), el comando y los nombres de fichero.
5. **Un idioma nuevo es un fichero** `i18n-<código>.md` más una fila en `docs/estado-traducciones.md`.
   `SKILL.md` no lleva lista de idiomas. El validador dice qué falta.
6. **Frases de seguridad.** Las entradas con `seguridad: sí` son las que, mal traducidas, degradan una
   salvaguarda (invertir un nivel de riesgo o un veredicto, aflojar la separación del mapa, el control de
   fidelidad). **Cualquier diff que las toque requiere revisión humana**, a ser posible de una persona nativa
   y con formación jurídica o sanitaria. Están fijadas en las pruebas para que el cambio sea visible.
7. **Honestidad de estado.** Nunca marques un catálogo como `revisado` ni quites la advertencia de
   `experimental` sin un revisor real, con nombre y fecha, en la cabecera y en el registro. Distingue siempre
   lo **automático** (pruebas, validadores) de lo **simulado** (subagentes) y de lo ejecutado en
   **plataforma real**: no digas «verificado» de lo que solo has simulado. Los nombres oficiales (RGPD…) se
   comprueban en la fuente oficial; una búsqueda web no es el texto literal.
8. **No amplíes exenciones de seguridad.** La excepción de los tokens fijos en la comprobación 6 del modo
   `audit` es la única; cualquier otro resto en otro idioma sigue contando.

## Flujo de trabajo

- **Pruebas primero y viéndolas fallar.** Después, sabotea tu propio trabajo: estropea la implementación
  o los datos de varias formas y exige que alguna prueba falle. Un validador que nunca falla no valida nada.
- Una tarea cada vez; enseña lo hecho antes de seguir.
- **No hagas push a `main`.** Trabaja en una rama. Un **CI en rojo no se fusiona**. El check solo avisa;
  que bloquee depende de la protección de rama (ver `docs/guia-web-github.md`).
- No abras un Pull Request, no publiques una Release ni fusiones sin que te lo pidan.
- No saltes, desactives ni omitas una prueba para llegar a verde.
- Commits en español, con atribución, y cada texto público (README, Release) termina con la nota de
  asistencia de IA y revisión humana.
- Lo que no sea del objetivo (refactors, estilo, bugs ajenos) se **anota**, no se hace.

## Pendientes ajenos, ya conocidos (no los arregles de pasada)

- `SKILL.md` dice «v1.1» como versión interna, desfasada respecto a los manifiestos.
- La sección `[Sin publicar]` del CHANGELOG recoge cosas ya publicadas en la Release v1.4.0.
- El **derecho foral** es contenido jurídico sustantivo y va al repositorio de derecho civil español.
