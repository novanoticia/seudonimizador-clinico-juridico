# Guía web de GitHub (sin instalar nada)

Para alguien con poco manejo de GitHub. Todo se hace desde el navegador, en
<https://github.com/novanoticia/seudonimizador-clinico-juridico>. No hace falta terminal.

Cada afirmación sobre cómo funciona GitHub va marcada:

- **Comprobado en este repositorio**: lo he mirado yo, con la API de GitHub, en este repositorio.
- **No comprobado**: lo dice la documentación o mi conocimiento general de GitHub, pero no he podido
  abrirlo ni probarlo desde aquí. La interfaz de GitHub cambia de vez en cuando: si un nombre de
  botón no coincide, busca el parecido.

## 0. Dónde estamos

- Todo el trabajo está en una **rama** llamada `claude/inspiring-archimedes-0onxom`, ya subida a GitHub.
- La rama principal, `main`, **no se ha tocado**.
- **No hay ningún Pull Request abierto.** Claude solo lo crea si se lo pides.

## 1. Cinco palabras que vas a ver

| Palabra | Qué es, en cristiano |
|---|---|
| **Rama** (*branch*) | Una copia de trabajo paralela. `main` es la «oficial»; la rama de Claude es el borrador. |
| **Commit** | Un paso guardado dentro de una rama, con un mensaje que lo explica. |
| **Pull Request** (PR) | Una petición para pasar los cambios de una rama a `main`. Es el sitio donde se revisa. |
| **Check** | Una comprobación automática que GitHub ejecuta sobre un PR o una rama. Sale verde (✓) o roja (✗). |
| **Merge** (fusionar) | Pasar los cambios del PR a `main`. Es lo que hace el botón «Merge pull request». |

## 2. Mirar el trabajo antes de decidir

1. Abre <https://github.com/novanoticia/seudonimizador-clinico-juridico/compare/main...claude/inspiring-archimedes-0onxom>.
2. Verás la lista de commits y, en **Files changed**, qué ficheros cambian. El español debe aparecer
   solo con **líneas añadidas** en `SKILL.md`, `flujo.md` y `auditoria.md` (en verde, ninguna en rojo).

## 3. Ver el CI (la comprobación automática)

El **CI** es el robot que ejecuta las pruebas por ti. Está en `.github/workflows/verificar.yml` y
produce **un único check llamado `verificar`**.

1. Entra en la pestaña **Actions** del repositorio.
2. Cada fila es una ejecución. El icono indica el resultado:
   ✓ verde = todo bien; ✗ rojo = algo falla; ● amarillo = en curso.
3. Pulsa una fila, luego el job `verificar`: verás cuatro pasos, uno por comprobación (pruebas,
   validador de catálogos, referencia en español, línea base del español). Si uno falla, ábrelo y
   lee el final del texto: dice qué prueba y por qué.

Se ejecuta en cada subida de una rama y en cada Pull Request. Tarda en torno a un minuto
(la suite de pruebas local tarda unos 3 segundos).

## 4. Un check que avisa NO es una protección de rama que bloquea

Esta es la confusión más habitual, así que va despacio.

- **Check que avisa.** El CI marca el PR en verde o en rojo. Pero **por sí solo no bloquea nada**:
  aunque esté rojo, el botón «Merge pull request» **sigue activo** y puedes fusionar.
- **Protección de rama que bloquea.** Una regla que le dices a GitHub: «en `main` no se fusiona nada
  sin pasar por un PR y sin que el check `verificar` esté verde». Con ella, el botón se desactiva
  mientras el check esté rojo o pendiente.

| Situación | ¿Se puede fusionar con el CI en rojo? |
|---|---|
| Solo el check (como hoy) | **Sí.** El rojo es un aviso. |
| Check + protección de rama que exige `verificar` | **No**, hasta que esté verde. |

### Comprobado en este repositorio

- El repositorio es **público**.
- Las tres ramas tienen **`protected: false`**: hoy **nada impide fusionar nada**, y nada obliga a
  pasar por un PR.
- Antes de este cambio **no había ningún workflow** (`total_count: 0`).
- Tu cuenta tiene permiso de **administrador** sobre el repositorio, así que puedes activar la protección.
- El historial usa **commits de fusión** («Merge pull request #N…»): esa es la opción que ya has
  usado al fusionar PR anteriores.
- El nombre exacto del check es el del job en el workflow: `verificar`. Una prueba automática vigila
  que esta guía y el workflow digan lo mismo.

### No comprobado

- Que en un repositorio **público** las protecciones de rama estén disponibles sin plan de pago
  (lo recuerdo de la documentación; el repositorio es público, pero no lo he probado).
- Que un check **solo aparezca en el buscador de checks requeridos si se ha ejecutado alguna vez
  recientemente** (recuerdo «en los últimos 7 días»). Por eso conviene que `verificar` ya haya corrido
  antes de configurar la regla.
- Cómo se comportan los **administradores** frente a la regla: en las reglas modernas (*rulesets*) la
  lista de excepciones empieza vacía, y en las reglas clásicas existe una casilla para «no permitir
  saltarse la regla». Revisa ese punto al configurarla.

## 5. Crear el Pull Request (cuando quieras)

1. Abre el enlace de comparación de la sección 2.
2. Pulsa **Create pull request** (en algunas pantallas aparece como **New pull request** y luego
   **Create pull request**).
3. Comprueba que arriba pone **base: `main`** y **compare: `claude/inspiring-archimedes-0onxom`**.
4. Escribe un título y una descripción cortos (o pídele a Claude que los redacte).
5. Pulsa **Create pull request**.
6. En la pestaña **Pull requests** verás el PR. Abajo aparece el check `verificar`: primero amarillo,
   luego verde o rojo.

## 6. Fusionar

1. Abre el PR desde la pestaña **Pull requests**.
2. Si `verificar` está en **verde**, pulsa **Merge pull request** y después **Confirm merge**.
3. Si está en **rojo**, no fusiones: ve a la sección 8.
4. Tras fusionar, pulsa **Delete branch** (borra la rama de trabajo; el contenido ya está en `main`).

## 7. Activar la protección de rama (una sola vez)

Hazlo cuando el check `verificar` ya haya salido en verde al menos una vez.

1. Ve a **Settings** (pestaña del repositorio, arriba a la derecha).
2. En el menú de la izquierda: **Rules** → **Rulesets**.
3. Pulsa **New ruleset** → **New branch ruleset**.
4. **Ruleset name**: por ejemplo `proteger-main`.
5. **Enforcement status**: **Active**.
6. **Target branches** → **Add target** → **Include default branch** (la rama por defecto es `main`).
7. En **Branch rules**, marca:
   - **Require a pull request before merging** (obliga a pasar por un PR).
   - **Require status checks to pass** → **Add checks** → busca y elige **`verificar`**.
   - **Block force pushes** (impide reescribir la historia de `main`).
8. Deja vacía la lista de excepciones (**Bypass list**) si quieres que la regla valga también para ti.
9. Pulsa **Create**.

Alternativa «clásica» (más antigua): **Settings → Branches → Add branch protection rule**, con el
nombre de rama `main`, y marcando **Require status checks to pass before merging** y el check `verificar`.

**Comprueba que funciona** (la regla solo sirve si la has probado): abre un PR de prueba con un cambio
trivial; el botón de fusionar debe estar desactivado mientras `verificar` esté en amarillo o rojo.

## 8. Si el CI sale rojo

1. Abre la pestaña **Actions** → la ejecución roja → el job `verificar` → el paso que falla.
2. Copia las últimas líneas del error y pégaselas a Claude: dirá qué falla y por qué.
3. No fusiones hasta que esté verde. Un rojo casi siempre significa que alguien cambió el español
   original, que un catálogo de idioma está incompleto, o que una prueba detecta un problema real.

## 9. Sobre el «.patch»

No necesitas ningún fichero `.patch`: los cambios ya están en la rama. Si alguna vez quieres uno, en
cualquier PR basta con **añadir `.patch` al final de su dirección web** (por ejemplo
`…/pull/7.patch`) y GitHub te lo muestra. Aplicarlo en tu ordenador sí requiere terminal y Git, y
para este flujo no hace falta.

## 10. Resumen de lo que está y no está comprobado

| Tema | Estado |
|---|---|
| Repositorio público, `main` sin protección, sin workflows previos, tu cuenta es administradora | Comprobado en este repositorio |
| Nombre del check: `verificar` | Comprobado: coincide con el job del workflow (prueba automática) |
| Que el workflow se ejecuta en GitHub y sale verde | Ver el estado de la ejecución en la pestaña **Actions** (lo anota el informe de la tarea 8) |
| Pasos de la interfaz para crear la regla | No comprobado: de memoria; la interfaz cambia |
| Plan gratuito, regla de los 7 días, comportamiento de administradores | No comprobado |

---
*Elaborado con asistencia de IA; requiere revisión humana.*
