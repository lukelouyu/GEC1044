$ErrorActionPreference='Stop'
$taskPath='C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Final_Polish.docx'
$taskWord=[Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
$taskDoc=$null
foreach($candidate in $taskWord.Documents){
    if($candidate.FullName -eq $taskPath){$taskDoc=$candidate;break}
}
if(-not $taskDoc){throw 'The report was not found in the active Word instance.'}
if(-not $taskDoc.Saved){throw 'The report has unsaved changes. Save it before formatting.'}
$wasVisible=$taskWord.Visible
$oldAlerts=$taskWord.DisplayAlerts
$taskWord.DisplayAlerts=0
$taskDoc.Close(0)
$taskDoc=$null
try {
    & 'C:\Users\lukel\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 'C:\Users\lukel\Downloads\GEC1044 Material\_review\format_current_report.py'
    if($LASTEXITCODE -ne 0){throw "Formatting helper failed: $LASTEXITCODE"}
    $taskDoc=$taskWord.Documents.Open($taskPath,$false,$false)
    $taskDoc.Repaginate()
    $qaDir='C:\Users\lukel\Downloads\GEC1044 Material\_review\standard_report_render'
    New-Item -ItemType Directory -Force -Path $qaDir | Out-Null
    $taskDoc.ExportAsFixedFormat((Join-Path $qaDir 'report.pdf'),17)
    Write-Output ('Formatted existing document and exported QA PDF; pages=' + $taskDoc.ComputeStatistics(2))
} finally {
    if(-not $taskDoc){$taskDoc=$taskWord.Documents.Open($taskPath,$false,$false)}
    $taskWord.DisplayAlerts=$oldAlerts
    $taskWord.Visible=$wasVisible
}
