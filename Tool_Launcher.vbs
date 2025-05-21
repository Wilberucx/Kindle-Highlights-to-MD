Dim shell
Set shell = CreateObject("WScript.Shell")
' Ejecuta el script PowerShell en la misma carpeta que este VBS
shell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File """ & Replace(WScript.ScriptFullName, WScript.ScriptName, "") & "InOut_box_windows.ps1""", 0, false
Set shell = Nothing