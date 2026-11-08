$ErrorActionPreference = 'Stop'
$draftPath = 'C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_First_Draft.docx'
$pdfPath = 'C:\Users\lukel\Downloads\GEC1044 Material\_review\draft_render\draft.pdf'
$wordConvert = $null
$draftDoc = $null
try {
    $wordConvert = New-Object -ComObject Word.Application
    $wordConvert.Visible = $false
    $wordConvert.DisplayAlerts = 0
    $draftDoc = $wordConvert.Documents.Open($draftPath, $false, $true)
    $draftDoc.Repaginate()
    $pageCount = $draftDoc.ComputeStatistics(2)
    $draftDoc.ExportAsFixedFormat($pdfPath, 17)
    Write-Output "Exported draft for visual QA; pages=$pageCount"
}
finally {
    if ($null -ne $draftDoc) { $draftDoc.Close(0); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($draftDoc) }
    if ($null -ne $wordConvert) { $wordConvert.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($wordConvert) }
}
