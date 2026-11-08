$ErrorActionPreference='Stop'
$taskPath='C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Final_Polish.docx'
$qaDir='C:\Users\lukel\Downloads\GEC1044 Material\_review\company_background_render'
New-Item -ItemType Directory -Force -Path $qaDir | Out-Null
$taskWord=$null
$taskDoc=$null
try {
    $taskWord=New-Object -ComObject Word.Application
    $taskWord.Visible=$false
    $taskWord.DisplayAlerts=0
    $taskWord.AutomationSecurity=3
    $taskDoc=$taskWord.Documents.Open($taskPath,$false,$true)
    Write-Output 'Opened report for read-only rendering.'
    $taskDoc.ExportAsFixedFormat((Join-Path $qaDir 'report.pdf'),17)
    Write-Output 'Exported report.'
} finally {
    if($taskDoc){$taskDoc.Close(0);[void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskDoc)}
    if($taskWord){$taskWord.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord)}
}
