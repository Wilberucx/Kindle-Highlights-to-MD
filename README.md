# Procesador de Anotaciones de Kindle a Markdown Personalizado


## Descripción del Proyecto

Este proyecto es una herramienta diseñada para **procesar y transformar las anotaciones exportadas de Kindle (en formato HTML) a un formato Markdown (`.md`) altamente personalizado**, adaptado a las preferencias estéticas y de procesamiento utilizadas en mi sistema de gestión de notas, como Obsidian.

Aunque existen plugins dentro de Obsidian para procesar estos archivos, su estética por defecto no se alinea con mis requisitos visuales y de formato, haciendo el proceso manual muy tedioso y repetitivo. Por ello, opté por desarrollar esta solución alternativa que garantiza una estética consistente con mis preferencias.

---

## Características Principales

* **Conversión Personalizada:** Transforma archivos HTML de anotaciones de Kindle a Markdown siguiendo una estética y estructura definidas.
* **Automatización del Flujo de Trabajo:** Minimiza la necesidad de procesamiento manual y repetitivo de las notas de lectura.
* **Interfaz Gráfica Sencilla (Ventanas de Selección):** Utiliza diálogos gráficos de Windows para seleccionar los archivos de entrada y salida, facilitando el uso para cualquier usuario.
* **Lanzador Rápido:** Incluye un script `tool_launcher.vbs` para un acceso rápido y directo desde el escritorio, evitando la necesidad de ejecutar comandos manualmente en PowerShell.
* **Integración con Obsidian (y otros sistemas de notas):** Diseñado pensando en la compatibilidad con estéticas de notas personales.
* **Personalización del Estilo:** El script principal (`kindle_notes_converter.py`) es adaptable, permitiendo modificar fácilmente la estética de salida en Markdown (ej. formato de bloques de cita, notas) según las preferencias del usuario.

---

##  Requisitos del Sistema y Dependencias

Para utilizar este proyecto, tu sistema debe cumplir con los siguientes requisitos:

* **Sistema Operativo:** Windows (probado en Windows 10/11)
* **Python 3:** El script principal está escrito en Python.
    * Puedes instalarlo fácilmente usando Chocolatey: `choco install python3`
* **Windows PowerShell:** Viene preinstalado en Windows y es necesario para ejecutar el script coordinador.
* **VBScript:** Viene preinstalado en Windows y es necesario para el lanzador de escritorio.

### Dependencias de Python (Librerías)

El script de Python requiere las siguientes librerías, que puedes instalar usando `pip`:

* `beautifulsoup4`: Para el análisis (parsing) del contenido HTML de Kindle.
* `lxml`: Un parser de HTML/XML rápido, utilizado por `beautifulsoup4`.

Puedes instalar ambas librerías ejecutando el siguiente comando en tu terminal:

```bash
pip install beautifulsoup4 lxml
```
##  Instalación y Configuración

Sigue estos pasos para poner en marcha el conversor de notas de Kindle:

1. **Clonar el Repositorio:** Abre una terminal (PowerShell) y clona este repositorio en la ubicación deseada de tu máquina local (ej. `C:\MyKindleNotesProcessor`)
```bash
git clone [https://github.com/tu_usuario/nombre_del_repositorio.git](https://github.com/tu_usuario/nombre_del_repositorio.git)
cd nombre_del_repositorio
```

2. **Instalar Dependencias de Python:** Asegúrate de tener Python instalado. Luego, desde la raíz del repositorio clonado, ejecuta:
  
Bash
```bash
pip install beautifulsoup4 lxml
```

(**Consejo:** Considera crear un entorno virtual para tus proyectos Python para gestionar mejor las dependencias, aunque para este script simple no es estrictamente necesario para empezar.)_

3. **Crear el Lanzador en el Escritorio:**

- Crea un atajo de `tool_launcher.vbs` y pégalo en tu escritorio (o donde prefieras).
- (Opcional) Puedes cambiarle el nombre a algo más descriptivo, como "Procesar Notas Kindle" y asignarle un ícono personalizado para una mejor identificación visual esto se logra con las propiedades del atajo con `alt + Enter` o click derecho y luego propiedades.

---

##  Uso

1. **Prepara tus Anotaciones HTML:** Exporta tus anotaciones de Kindle (generalmente un archivo `.html`) desde el sitio web de Amazon o desde tu Kindle.
2. **Ejecuta el Lanzador:** Haz doble clic en el archivo `tool_launcher.vbs` que colocaste en tu escritorio.
3. **Selecciona el Archivo de Entrada:** Se abrirá una ventana de selección de archivo. Navega hasta tu archivo HTML de anotaciones de Kindle y selecciónalo.
4. **Selecciona la Ubicación de Salida:** A continuación, se abrirá otra ventana. Elige dónde quieres guardar el archivo Markdown resultante y el nombre que deseas darle (se sugerirá un nombre basado en el HTML de entrada).
5. **Procesamiento y Confirmación:** El script de PowerShell se ejecutará y llamará a tu script de Python para procesar el archivo. Una vez completado, verás un mensaje de éxito o un error si algo salió mal (los detalles del error aparecerán en la consola de PowerShell si lo ejecutas directamente, o se te indicará dónde buscar).
6. **Accede a tus Notas Markdown:** El archivo Markdown personalizado se generará en la ubicación que seleccionaste.

---

##  Personalización de la Estética

El estilo de las notas Markdown se define directamente en el script `kindle_notes_converter.py`. Las secciones clave para modificar son:

- **Título del Libro:** Definido por `# {book_title}`.
- **Separadores:** Líneas `---`.
- **Resaltados (Highlights):** Utilizan el formato de Obsidian `>[!quote] {page_info}\n>\n> {note_content}\n\n`. Puedes cambiar `[!quote]` por otro tipo de callout de Obsidian, o por un formato de cita estándar de Markdown (ej. `> {note_content}`).
- **Notas:** Utilizan el formato `**Note**\n- {note_content}\n\n`. Puedes ajustar si quieres negritas, si es una lista (`-`), etc.
- **Encabezados de Sección:** Las secciones se agrupan con `## {section_in_highlight_heading}`.

Siéntete libre de modificar estas líneas para que la salida se adapte perfectamente a tu sistema de notas y preferencias visuales.

---

## 📂 Estructura del Proyecto Sugerida

```
MyKindleNotesProcessor/
├── in/                                # (Opcional) Puedes usar esta carpeta para colocar tus archivos HTML de entrada temporalmente.
├── out/                               # (Opcional) Puedes usar esta carpeta para guardar los archivos Markdown de salida.
├── kindle_notes_converter.py          # El script principal de Python para la conversión.
├── InOut_box_windows.ps1              # Script PowerShell que coordina la entrada/salida y ejecuta Python.
├── tool_launcher.vbs                  # El lanzador VBS para ejecutar el script PowerShell sin complicaciones.
├── README.md                          # Este documento.
└── requirements.txt                   # Archivo que lista las dependencias de Python (beautifulsoup4, lxml).
```

---

