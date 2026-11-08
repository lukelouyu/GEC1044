$ErrorActionPreference='Stop'
$taskWord=[Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
$taskDoc=$null
foreach($candidate in $taskWord.Documents){
    if($candidate.FullName -eq 'C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Final_Polish.docx'){$taskDoc=$candidate;break}
}
if(-not $taskDoc){throw 'Report not open.'}
Write-Output ('Current report paragraphs=' + $taskDoc.Paragraphs.Count)
$qaDir='C:\Users\lukel\Downloads\GEC1044 Material\_review\standard_report_render'
New-Item -ItemType Directory -Force -Path $qaDir | Out-Null
$taskDoc.ExportAsFixedFormat((Join-Path $qaDir 'report.pdf'),17)
Write-Output 'QA PDF exported.'
