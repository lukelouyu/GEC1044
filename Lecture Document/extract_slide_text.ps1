$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null = [Windows.Graphics.Imaging.SoftwareBitmap,Windows.Graphics.Imaging,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrResult,Windows.Foundation,ContentType=WindowsRuntime]
$null = [Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime]
$asTaskMethod = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
function Await-Result($Operation, [Type]$ResultType) {
    $task = $asTaskMethod.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.GetAwaiter().GetResult()
}
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$outDir = Join-Path $root 'ocr-en'
New-Item -ItemType Directory -Path $outDir -Force | Out-Null
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage([Windows.Globalization.Language]::new('en-US'))
$results = @()
foreach ($inputFile in (Get-ChildItem -LiteralPath (Join-Path $root 'ocr-input') -Filter '*.png' | Sort-Object Name)) {
    $storageFile = Await-Result ([Windows.Storage.StorageFile]::GetFileFromPathAsync($inputFile.FullName)) ([Windows.Storage.StorageFile])
    $stream = Await-Result ($storageFile.OpenAsync([Windows.Storage.FileAccessMode]::Read)) ([Windows.Storage.Streams.IRandomAccessStream])
    $decoder = Await-Result ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)) ([Windows.Graphics.Imaging.BitmapDecoder])
    $bitmap = Await-Result ($decoder.GetSoftwareBitmapAsync()) ([Windows.Graphics.Imaging.SoftwareBitmap])
    $ocrResult = Await-Result ($engine.RecognizeAsync($bitmap)) ([Windows.Media.Ocr.OcrResult])
    $lines = @($ocrResult.Lines | ForEach-Object { $_.Text })
    $lines | Set-Content -LiteralPath (Join-Path $outDir ($inputFile.BaseName + '.txt')) -Encoding UTF8
    $results += [pscustomobject]@{image=$inputFile.BaseName;lines=$lines}
    $bitmap.Dispose()
    $stream.Dispose()
}
$results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $outDir 'all-slides.json') -Encoding UTF8
Write-Output ('OCR completed: ' + $results.Count + ' screenshots')
