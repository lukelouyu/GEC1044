$ErrorActionPreference='Stop'
$reportPath='C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Final_Polish.docx'
$qaPath='C:\Users\lukel\Downloads\GEC1044 Material\_review\standard_report_verified_render\report.pdf'
New-Item -ItemType Directory -Force -Path (Split-Path $qaPath) | Out-Null
$reportWord=$null
$reportDoc=$null
try {
    $reportWord=New-Object -ComObject Word.Application
    Write-Output 'Started fresh Word renderer.'
    $reportWord.Visible=$false
    $reportWord.DisplayAlerts=0
    $reportWord.AutomationSecurity=3
    $reportDoc=$reportWord.Documents.Open($reportPath,$false,$true)
    Write-Output 'Opened report for read-only rendering.'
    $reportDoc.ExportAsFixedFormat($qaPath,17)
    Write-Output 'Exported report.'
} finally {
    if($reportDoc){$reportDoc.Close(0);[void][Runtime.InteropServices.Marshal]::ReleaseComObject($reportDoc)}
    if($reportWord){$reportWord.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($reportWord)}
}
