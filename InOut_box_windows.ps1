# --- CONFIGURACIÓN ---
# RUTA AL SCRIPT DE PYTHON: Asegúrate de que esta ruta sea la correcta para tu archivo .py
$pythonScriptPath = Join-Path $PSScriptRoot "kindle_notes_converter.py" # <--- ¡AJUSTADO PARA PORTABILIDAD!

# RUTA AL EJECUTABLE DE PYTHON: Esto es usualmente 'python' si está en tu PATH
$pythonExecutable = "python" 
# -------------------

# Ruta para el archivo de log temporal donde se guardará la salida del script de Python
$tempLogFile = Join-Path $env:TEMP "kindle_converter_log.txt"

# Añadir tipos de .NET para diálogos de archivo
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ================================
# 1. Ventana de Selección de Archivo HTML de Entrada (OpenFileDialog)
# ================================
$openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$openFileDialog.Title = "Selecciona tu archivo HTML de anotaciones de Kindle"
$openFileDialog.Filter = "Archivos HTML (*.html)|*.html|Todos los archivos (*.*)|*.*"
$openFileDialog.FilterIndex = 1
$openFileDialog.RestoreDirectory = $true # Recordar la última carpeta

if ($openFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $inputHTMLPath = $openFileDialog.FileName
} else {
    [System.Windows.Forms.MessageBox]::Show("Operación cancelada. No se seleccionó ningún archivo HTML.", "Conversión Cancelada", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
    exit
}

# ================================
# 2. Ventana de Guardado de Archivo Markdown de Salida (SaveFileDialog)
# ================================
$saveFileDialog = New-Object System.Windows.Forms.SaveFileDialog
$saveFileDialog.Title = "Guarda tu archivo de notas Markdown"
$saveFileDialog.Filter = "Archivos Markdown (*.md)|*.md|Todos los archivos (*.*)|*.*"
$saveFileDialog.FilterIndex = 1
$saveFileDialog.RestoreDirectory = $true # Recordar la última carpeta

# Sugerir un nombre de archivo basado en el HTML de entrada
$suggestedFileName = [System.IO.Path]::GetFileNameWithoutExtension($inputHTMLPath) + ".md"
$saveFileDialog.FileName = $suggestedFileName

if ($saveFileDialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
    $outputMDPath = $saveFileDialog.FileName
} else {
    [System.Windows.Forms.MessageBox]::Show("Operación cancelada. No se seleccionó la ubicación de guardado.", "Conversión Cancelada", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
    exit
}

# ================================
# 3. Ejecutar el Script de Python y Redirigir Salida a Log
# ================================
# Construir la lista de argumentos para el script de Python
$arguments = @("`"$pythonScriptPath`"", "`"$inputHTMLPath`"", "`"$outputMDPath`"")

Write-Host "Ejecutando script Python..." # Mensaje más directo

# Ejecutar el proceso de Python.
# Para depuración, QUITAR -NoNewWindow y las redirecciones a archivo.
# Esto hará que cualquier 'print' o error del script Python aparezca directamente en esta consola de PowerShell.
# QUITAR O COMENTAR: -NoNewWindow -RedirectStandardOutput $tempLogFile -RedirectStandardError $tempLogFile
$process = Start-Process -FilePath $pythonExecutable -ArgumentList $arguments -Wait -PassThru

# *** IMPORTANTE: Para depuración, el contenido del log temporal YA NO SE LEERÁ/MOSTRARÁ así,
#     porque la salida de Python irá directamente a la consola.
#     Por lo tanto, comentamos/eliminamos las siguientes líneas relacionadas con el log. ***

# Comprobar el código de salida del proceso de Python
if ($process.ExitCode -eq 0) {
    [System.Windows.Forms.MessageBox]::Show("¡Conversión completada exitosamente!" + "`n" + "Archivo guardado en: " + $outputMDPath, "Éxito", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
} else {
    # Si hubo un error, ahora el traceback debería haber aparecido directamente en la consola.
    [System.Windows.Forms.MessageBox]::Show(
        "Hubo un error durante la conversión (Código de salida Python: $($process.ExitCode))." + "`n`n" +
        "Por favor, revisa la CONSOLA DE POWERSHELL para ver los detalles completos del error." + "`n" +
        "Si la ventana se cierra rápidamente, considera ejecutar el script desde una consola de PowerShell abierta." ,
        "Error en la Conversión",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Error
    )
}

# Limpiar objetos
# Comentar o eliminar esta línea también, para que el log (si lo hubiera, aunque ya no lo usaremos activamente) no se borre.
# Remove-Item $tempLogFile -ErrorAction SilentlyContinue
Remove-Variable openFileDialog, saveFileDialog, process -ErrorAction SilentlyContinue # Opcional: limpiar variables