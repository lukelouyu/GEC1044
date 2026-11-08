$ErrorActionPreference = 'Stop'
$reportPath = 'C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Readability_Revision.docx'
$qaPath = 'C:\Users\lukel\Downloads\GEC1044 Material\_review\readability_render\report.pdf'
$reportWord = $null
$reportDoc = $null
try {
    $reportWord = New-Object -ComObject Word.Application
    $reportWord.Visible = $false
    $reportWord.DisplayAlerts = 0
    $reportDoc = $reportWord.Documents.Open($reportPath, $false, $true)
    $reportDoc.Repaginate()
    $reportPages = $reportDoc.ComputeStatistics(2)
    $reportDoc.ExportAsFixedFormat($qaPath, 17)
    Write-Output "Exported readability revision; pages=$reportPages"
}
finally {
    if ($null -ne $reportDoc) { $reportDoc.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($reportDoc) }
    if ($null -ne $reportWord) { $reportWord.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($reportWord) }
}
