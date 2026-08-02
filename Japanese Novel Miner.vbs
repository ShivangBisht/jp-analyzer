Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
repo = fso.GetParentFolderName(WScript.ScriptFullName)
pythonw = repo & "\.venv\Scripts\pythonw.exe"
launcher = repo & "\launch_japanese_novel_miner.pyw"
If Not fso.FileExists(pythonw) Then
  MsgBox "JP Analyzer Python was not found:" & vbCrLf & pythonw, 16, "Japanese Novel Miner"
  WScript.Quit 1
End If
shell.Run Chr(34) & pythonw & Chr(34) & " " & Chr(34) & launcher & Chr(34), 0, False
