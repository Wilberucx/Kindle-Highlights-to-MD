# InOut_box_windows.ps1 (v2 - con config y mejor manejo de errores)

# --- CARGAR CONFIGURACIÓN ---
$configPath = Join-Path $PSScriptRoot "config.json"
if (-not (Test-Path $configPath)) {
    [System.Windows.Forms.MessageBox]::Show("El archivo 'config.json' no se encuentra. Por favor, asegúrate de que exista.", "Error de Configuración", "OK", "Error")
    exit
}
$config = Get-Content -Path $configPath | ConvertFrom-Json

$pythonScriptPath = Join-Path $PSScriptRoot "kindle_notes_converter.py"
$pythonExecutable = $config.pythonExecutable # Obtiene la ruta de python desde el config

# --- DIÁLOGOS DE ARCHIVO (Sin cambios) ---
Add-Type -AssemblyName System.Windows.Forms

$openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$openFileDialog.Title = "Selecciona tu archivo HTML de anotaciones de Kindle"
$openFileDialog.Filter = "Archivos HTML (*.html)|*.html"
if ($openFileDialog.ShowDialog() -ne 'OK') { exit }
$inputHTMLPath = $openFileDialog.FileName

$saveFileDialog = New-Object System.Windows.Forms.SaveFileDialog
$saveFileDialog.Title = "Guarda tu archivo de notas Markdown"
$saveFileDialog.Filter = "Archivos Markdown (*.md)|*.md"
$saveFileDialog.FileName = [System.IO.Path]::GetFileNameWithoutExtension($inputHTMLPath) + ".md"
if ($saveFileDialog.ShowDialog() -ne 'OK') { exit }
$outputMDPath = $saveFileDialog.FileName

# --- EJECUTAR SCRIPT DE PYTHON CON MEJOR MANEJO DE ERRORES ---
$arguments = @(
    "`"$pythonScriptPath`"",
    "`"$inputHTMLPath`"",
    "`"$outputMDPath`"",
    "`"$configPath`""
)

# Usamos -RedirectStandardError para capturar los errores de Python
$process = Start-Process -FilePath $pythonExecutable -ArgumentList $arguments -Wait -PassThru -NoNewWindow -RedirectStandardError "stderr.log" -RedirectStandardOutput "stdout.log"

$stdErr = Get-Content "stderr.log" -ErrorAction SilentlyContinue
$stdOut = Get-Content "stdout.log" -ErrorAction SilentlyContinue

if ($process.ExitCode -eq 0) {
    $successMessage = "¡Conversión completada exitosamente!`n`nArchivo guardado en: $outputMDPath"
    [System.Windows.Forms.MessageBox]::Show($successMessage, "Éxito", "OK", "Information")
} else {
    $errorMessage = "Hubo un error durante la conversión.`n`nDetalles del error:`n$stdErr"
    [System.Windows.Forms.MessageBox]::Show($errorMessage, "Error en la Conversión", "OK", "Error")
}

# Limpiar archivos de log
Remove-Item "stderr.log", "stdout.log" -ErrorAction SilentlyContinue