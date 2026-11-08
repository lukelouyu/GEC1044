$ErrorActionPreference='Stop'
$taskPath='C:\Users\lukel\Downloads\GEC1044 Material\GEC1044_Tong_Keow_Final_Polish.docx'
$taskWord=$null
$taskDoc=$null
try {$taskWord=[Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')} catch {}
if($taskWord){foreach($candidate in $taskWord.Documents){if($candidate.FullName -eq $taskPath){$taskDoc=$candidate;break}}}
$closedForEdit=$false
if($taskDoc){
    if(-not $taskDoc.Saved){throw 'The report has unsaved edits. Save it before applying the addition.'}
    $taskDoc.Close(0)
    $taskDoc=$null
    $closedForEdit=$true
}
try {
    & 'C:\Users\lukel\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' -X utf8 'C:\Users\lukel\Downloads\GEC1044 Material\_review\insert_company_background.py'
    if($LASTEXITCODE -ne 0){throw "Insertion failed: $LASTEXITCODE"}
} finally {
    if($closedForEdit){$taskDoc=$taskWord.Documents.Open($taskPath,$false,$false)}
}
Write-Output 'Updated the original report in place.'
