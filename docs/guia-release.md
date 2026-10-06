# Guía web para publicar la Release v1.5.0

Para alguien con poco manejo de GitHub. Todo desde el navegador. **Claude no publica nada**: la
Release la creas tú, cuando decidas. Esta guía es el mapa, y el texto ya redactado de la Release está
en [`docs/release-v1.5.0.md`](release-v1.5.0.md).

Cada afirmación sobre GitHub va marcada: **Comprobado en este repositorio** (lo he leído yo con la API)
o **No comprobado** (lo recuerdo de la documentación; la interfaz cambia, busca el parecido).

## 0. Qué es una Release, en cristiano

- Una **etiqueta** (*tag*) es un marcador fijo sobre un commit concreto: `v1.5.0` significa «la foto
  de `main` en este momento».
- Una **Release** es una página pública que cuelga de una etiqueta y lleva un texto y **archivos
  adjuntos** (aquí: el `.zip` y el `.skill`).
- La Release marcada como **Latest** (la última) es la que sirven los enlaces
  `…/releases/latest/download/…` del README. Por eso importa mucho cuál es la «Latest».

## 1. Lo que ya existe (hechos)

### Comprobado en este repositorio

- La Release **Latest** es hoy **`v1.4.0`**: no es borrador ni pre-release.
- Lleva **dos archivos**: `seudonimizador-clinico-juridico.zip` y `seudonimizador-clinico-juridico.skill`,
  del mismo tamaño y con el mismo `sha256` (son idénticos).
- Esos archivos ya acumulan **5 descargas** (3 del `.zip` y 2 del `.skill`): hay gente con el
  **paquete antiguo, sin idiomas**. El texto de la Release les avisa de que deben **reinstalar** el paquete completo.
- Las etiquetas existentes son `v1.1`, `v1.3` y `v1.4.0`. Los manifiestos dicen `1.5.0`, así que la nueva es **`v1.5.0`**.
- El README enlaza los paquetes con `releases/latest/download/…`: si `v1.5.0` no fuera la «Latest», esos
  enlaces seguirían entregando el paquete antiguo.
- `dist/` está en `.gitignore`: los paquetes **no** se suben al repositorio, solo a la Release.

### No comprobado

- Que una Release marcada como **pre-release** quede **excluida** de «Latest» (lo recuerdo de la
  documentación de GitHub; no he creado ninguna para probarlo).
- Los nombres exactos de botones y casillas de abajo.
- Que Codespaces tenga cuota gratuita suficiente en tu cuenta, y que traiga `zip` instalado.

## 2. Antes de empezar (lista de control)

1. **Primero fusiona el Pull Request** en `main` (ver [guia-web-github.md](guia-web-github.md)). Una Release
   se hace sobre `main`: si la creas antes de fusionar, la etiqueta apuntaría a un `main` sin los idiomas
   y el paquete saldría viejo.
2. Comprueba que el check `verificar` de `main` está en **verde**.
3. **Antes de publicar, actualiza el «estado real»** de [`docs/release-v1.5.0.md`](release-v1.5.0.md): la
   sección «Estado real de las traducciones» debe decir lo que se haya probado de verdad (por ejemplo, si
   alguien ha revisado un idioma, o si se ha ejecutado en una plataforma real). No publiques una frase que
   ya no sea cierta.

## 3. Generar el paquete

El paquete lo genera `scripts/build-dist.sh` y deja dos ficheros en `dist/`.

### Opción A — sin instalar nada, con Codespaces (en el navegador)

1. En la página del repositorio, pulsa **Code** → pestaña **Codespaces** → **Create codespace on main**.
2. Espera a que se abra un editor en el navegador. Abre la terminal (menú ☰ → **Terminal** → **New Terminal**).
3. Escribe: `./scripts/build-dist.sh` y pulsa Intro.
4. Si dice `zip: command not found` (No comprobado), escribe `sudo apt-get install -y zip` y repite el paso 3.
5. En el panel izquierdo aparece la carpeta `dist/`. Pulsa con el botón derecho sobre cada fichero →
   **Download** y guárdalos en tu ordenador.

### Opción B — en local (en tu ordenador)

Necesitas Git y el programa `zip`. En una terminal:

```bash
git clone https://github.com/novanoticia/seudonimizador-clinico-juridico
cd seudonimizador-clinico-juridico
./scripts/build-dist.sh
```

Los ficheros quedan en la carpeta `dist/`.

### Comprobar el paquete antes de subirlo

El propio script imprime la lista. Debe contener estos 12 ficheros (los cinco `.md` del skill, los
**seis catálogos** y la licencia), más la línea de la carpeta:

```text
seudonimizador-clinico-juridico/
seudonimizador-clinico-juridico/SKILL.md
seudonimizador-clinico-juridico/flujo.md
seudonimizador-clinico-juridico/auditoria.md
seudonimizador-clinico-juridico/plantilla-entrada.md
seudonimizador-clinico-juridico/plantilla-tokens.md
seudonimizador-clinico-juridico/i18n-es.md
seudonimizador-clinico-juridico/i18n-en.md
seudonimizador-clinico-juridico/i18n-fr.md
seudonimizador-clinico-juridico/i18n-ca.md
seudonimizador-clinico-juridico/i18n-gl.md
seudonimizador-clinico-juridico/i18n-eu.md
seudonimizador-clinico-juridico/LICENSE
```

(El orden da igual.) Para volver a ver la lista: `unzip -l dist/seudonimizador-clinico-juridico.zip`.
Y para comprobar que el `.skill` es copia del `.zip`: `cmp dist/seudonimizador-clinico-juridico.zip dist/seudonimizador-clinico-juridico.skill`
(sin salida = idénticos). **Si falta algún `i18n-*.md`, no publiques.**

## 4. Borrar el entorno después (Codespaces)

Un Codespace sigue existiendo y puede consumir tu cuota hasta que lo borras.

1. Abre <https://github.com/codespaces>.
2. A la derecha de tu Codespace, pulsa **⋯** → **Delete**.
3. Confirma. (No comprobado: los nombres de los botones.) Los ficheros ya los tienes descargados.

## 5. Crear la Release como borrador

1. En el repositorio, pestaña **Releases** (columna derecha) → **Draft a new release**.
2. **Choose a tag** → escribe `v1.5.0` → elige **Create new tag: v1.5.0 on publish**.
3. **Target**: `main`.
4. **Release title**: copia la primera línea de [`docs/release-v1.5.0.md`](release-v1.5.0.md) (sin la `#`).
5. **Describe this release**: pega el resto del fichero.
6. Arrastra a la zona de adjuntos los **dos archivos** de `dist/`: `seudonimizador-clinico-juridico.zip` y
   `seudonimizador-clinico-juridico.skill`. Espera a que terminen de subirse.
7. **No marques** la casilla **Set as a pre-release**. Un pre-release se sirve como «versión no
   definitiva» y, según la documentación (No comprobado aquí), **no cuenta como «Latest»**: los enlaces del
   README seguirían entregando el paquete antiguo, y además sugeriría menos madurez de la real. El
   estado real (traducciones sin revisar, sin prueba en plataforma real) ya se declara en el texto.
8. Deja marcada **Set as the latest release**.
9. Pulsa **Save draft** (no **Publish release** todavía).

## 6. Revisar el borrador y publicar

1. Abre el borrador desde **Releases**. Léelo entero, como lo vería un lector.
2. Comprueba que están los dos archivos y que **no** pone «pre-release».
3. Pulsa **Publish release**.

## 7. Comprobar después de publicar

1. Abre <https://github.com/novanoticia/seudonimizador-clinico-juridico/releases/latest>: debe mostrar **v1.5.0**.
2. Descarga el `.zip` desde esa página y ejecuta `unzip -l` sobre él: deben salir los seis `i18n-*.md`.
3. Abre la etiqueta `v1.5.0`: el commit al que apunta debe contener `skills/…/i18n-en.md`.
4. Prueba los enlaces de descarga del README.

## 8. Si te equivocas

- **Texto o adjuntos:** abre la Release → icono del lápiz (**Edit**) → corrige o borra y vuelve a subir un
  adjunto → **Update release**. Funciona también con una Release ya publicada.
- **Paquete con contenido equivocado:** no borres la etiqueta (los enlaces y las descargas ya hechas
  la citan). Corrige en `main` y publica **`v1.5.1`**.
- **Publicaste con una frase que ya no es cierta** (por ejemplo, el «estado real»): edítala cuanto antes.

## 9. Qué no hace Claude

Claude **no publica** Releases, no crea etiquetas y no sube adjuntos: lo haces tú. Si quieres, Claude
puede repasar contigo el borrador antes de publicar.

---
*Elaborado con asistencia de IA; requiere revisión humana.*
