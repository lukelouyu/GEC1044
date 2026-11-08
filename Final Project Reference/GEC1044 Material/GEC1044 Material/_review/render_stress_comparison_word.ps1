$ErrorActionPreference='Stop'
$reportPath='C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Stress_Comparison_Revision.docx'
$qaPath='C:\Users\lukel\Downloads\GEC1044 Material\_review\stress_comparison_render\report.pdf'
New-Item -ItemType Directory -Force -Path (Split-Path $qaPath) | Out-Null
$reportWord=$null
$reportDoc=$null
try {
  $reportWord=New-Object -ComObject Word.Application
  $reportWord.Visible=$false
  $reportWord.DisplayAlerts=0
  $reportDoc=$reportWord.Documents.Open($reportPath,$false,$true)
  $reportDoc.Repaginate()
  $reportPages=$reportDoc.ComputeStatistics(2)
  $reportDoc.ExportAsFixedFormat($qaPath,17)
  Write-Output "Exported report; pages=$reportPages"
} finally {
  if($reportDoc){$reportDoc.Close(0);[void][Runtime.InteropServices.Marshal]::ReleaseComObject($reportDoc)}
  if($reportWord){$reportWord.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($reportWord)}
}

