
# Kindle Notes Converter
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![PowerShell](https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white) ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

Una herramienta elegante para Windows que transforma tus anotaciones de Kindle (exportadas como HTML) en archivos Markdown limpios y personalizables, listos para tu sistema de gestión de conocimiento como Obsidian, Logseq o cualquier otro.

Di adiós al tedioso formateo manual. Define tu estética una vez y convierte tus notas con solo dos clics.

---

## ✨ Características Principales

-   **Formato 100% Personalizable:** Controla el estilo de los títulos, encabezados, citas (highlights) y notas a través de un sencillo archivo de configuración (`config.json`).
-   **Personalización Intuitiva:** Edita las plantillas como si estuvieras escribiendo en un bloc de notas, sin necesidad de entender caracteres especiales como `\n`.
-   **Interfaz Gráfica Nativa:** Utiliza los diálogos de "Abrir" y "Guardar" de Windows para una experiencia de usuario fluida y familiar.
-   **Instalación Simplificada:** Un script se encarga de instalar las dependencias de Python por ti.
-   **Lanzador Rápido:** Incluye un ejecutable para el escritorio que lanza la herramienta sin mostrar ventanas de terminal.
-   **Agrupación Inteligente:** Agrupa automáticamente tus notas y highlights bajo los encabezados de sus respectivos capítulos.
-   **Portátil y Autónomo:** Funciona desde cualquier carpeta de tu ordenador sin necesidad de instalación formal.

---

## 🚀 Instalación (en 3 Sencillos Pasos)

1.  **Descargar la Herramienta**
    -   Ve a la sección [**Releases**](https://github.com/Wilberucx/Kindle-Highlights-to-MD/releases) en la parte derecha de esta página de GitHub.
    -   Descarga el archivo `KindleNotesConverter-v1.0.zip` de la última versión.
    -   Descomprime el archivo `.zip` en una ubicación permanente de tu ordenador (ej. `C:\Herramientas\KindleConverter`).

2.  **Instalar Dependencias**
    -   Dentro de la carpeta descomprimida, haz doble clic en el archivo `Instalar_Dependencias.bat`.
    -   Aparecerá una ventana de terminal que instalará las librerías de Python necesarias (`beautifulsoup4` y `lxml`).
    -   *Requisito: Debes tener Python 3 instalado y añadido al PATH de tu sistema.*

3.  **Crear el Acceso Directo**
    -   Haz clic derecho sobre el archivo `Lanzador.vbs` y selecciona `Crear acceso directo`.
    -   Mueve este acceso directo a tu escritorio, barra de tareas o donde prefieras.
    -   (Opcional) Renómbralo a "Convertir Notas de Kindle" y asígnale un icono personalizado para una mejor identificación.

¡Listo! Tu herramienta está configurada y lista para usarse.

---

## 💡 Uso Diario

1.  **Exporta tus notas de Kindle** a un archivo `.html` desde la web de Amazon o tu dispositivo.
2.  **Haz doble clic** en tu acceso directo "Convertir Notas de Kindle".
3.  Se abrirá una ventana para que **selecciones el archivo `.html`** de entrada.
4.  A continuación, se abrirá otra ventana para que **elijas dónde guardar** el archivo `.md` resultante.
5.  ¡Hecho! El archivo Markdown se generará en la ubicación que seleccionaste, con el formato que definiste.

---

## 🔧 Personalización: Tu Estilo, Tus Reglas (¡Fácil!)

El verdadero poder de esta herramienta está en el archivo `config.json`. Este archivo es tu "panel de control" y te permite dictar, línea por línea, cómo se verá cada parte de tus notas. **Es como escribir en un bloc de notas.**

### ¿Cómo funciona?

El archivo `config.json` contiene plantillas para cada parte de tu nota (título, citas, etc.). Cada plantilla es una **lista de líneas de texto**. El script simplemente tomará estas líneas, rellenará los huecos (placeholders) y las unirá para formar tu archivo final.

### Paso a Paso para Personalizar

1.  **Abre `config.json`:** Búscalo en la carpeta de la herramienta y ábrelo con un editor de texto.
2.  **Elige la plantilla que quieres cambiar,** por ejemplo, `"highlight"`.
3.  **Edita las líneas** directamente, tal como lo harías en Obsidian o cualquier editor de Markdown.

   - **¿Quieres una línea en blanco?** Escribe `""`.
   - **¿Quieres una cita?** Empieza la línea con `> `.
   - **¿Quieres una lista?** Empieza la línea con `- `.

### Ejemplos Prácticos para Inspirarte

#### 1. Estilo de Cita Minimalista

**Objetivo:** No te gustan los callouts de Obsidian, quieres una cita simple con la página debajo.

**Busca la plantilla `"highlight"` en `config.json`:**
```json
"highlight": [
  ">[!quote] {page_info}",
  ">",
  "> {content}"
],
```

Reemplázala por tu nuevo estilo:
```json
"highlight": [
  "> {content}",
  ">",
  "> — *Página {page_info}*"
],
```
2. Formato de Notas más Visual

Objetivo: Quieres que tus notas personales resalten con un emoji y un separador.

Busca la plantilla "note":
```json
"note": [
  "**Note** - {page_info}",
  "- {content}"
],
```
Reemplázala por tu nuevo estilo:
```json
"note": [
  "",
  "---",
  "✍️ **Mi Nota Personal** ({page_info})",
  "{content}",
  "---"
],
```

Como puedes ver, lo que escribes en el JSON es casi exactamente lo que obtienes en el resultado final. ¡Es así de simple!

Placeholders Disponibles

Recuerda que puedes usar estos "huecos" en cualquiera de tus líneas:

{book_title}: El título del libro.

{section_title}: El título del capítulo.

{content}: El texto del highlight o tu nota.

{page_info}: La ubicación de la nota.

