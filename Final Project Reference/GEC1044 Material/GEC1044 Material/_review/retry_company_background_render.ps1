$ErrorActionPreference='Stop'
$stalledHelper=Get-CimInstance Win32_Process -Filter 'ProcessId=38784'
$stalledWord=Get-CimInstance Win32_Process -Filter 'ProcessId=48468'
if($stalledHelper -and $stalledHelper.CommandLine -like '*render_company_background_word.ps1*'){Stop-Process -Id 38784 -Force}
if($stalledWord -and $stalledWord.CommandLine -like '*/Automation*' -and $stalledWord.CreationDate.Date -eq (Get-Date).Date){Stop-Process -Id 48468 -Force}
$taskWord=$null
$taskDoc=$null
try {
 $taskWord=New-Object -ComObject Word.Application
 $taskWord.Visible=$false
 $taskWord.DisplayAlerts=0
 $taskWord.AutomationSecurity=3
 $taskWord.Options.UpdateLinksAtOpen=$false
 $taskWord.Options.UpdateFieldsAtPrint=$false
 $taskWord.Options.UpdateLinksAtPrint=$false
 $taskWord.ScreenUpdating=$false
 $taskDoc=$taskWord.Documents.Open('C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Final_Polish.docx',$false,$true)
 Write-Output 'Opened isolated renderer with automatic link updates disabled.'
 $taskDoc.SaveAs2('C:\Users\lukel\Downloads\GEC1044 Material\_review\company_background_render\report.pdf',17)
 Write-Output 'Exported PDF preview.'
} finally {
 if($taskDoc){$taskDoc.Close(0);[void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskDoc)}
 if($taskWord){$taskWord.Quit();[void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord)}
}
