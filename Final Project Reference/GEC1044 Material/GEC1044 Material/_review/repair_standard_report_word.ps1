$ErrorActionPreference='Stop'
$taskPath='C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Final_Polish.docx'
$taskWord=[Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
$taskDoc=$null
foreach($candidate in $taskWord.Documents){if($candidate.FullName -eq $taskPath){$taskDoc=$candidate;break}}
if(-not $taskDoc){throw 'Report not found in Word.'}
if(-not $taskDoc.Saved){throw 'Report has unsaved user changes.'}
$taskDoc.Close(0)
$taskDoc=$null
try {
    & 'C:\Users\lukel\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 'C:\Users\lukel\Downloads\GEC1044 Material\_review\repair_standard_report.py'
    if($LASTEXITCODE -ne 0){throw "Repair helper failed: $LASTEXITCODE"}
} finally {
    $taskDoc=$taskWord.Documents.Open($taskPath,$false,$false)
}
Write-Output 'Reopened the updated original report.'
