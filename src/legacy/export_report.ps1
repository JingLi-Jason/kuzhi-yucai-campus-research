$ErrorActionPreference='Stop'
$root='${ORIGINAL_WORKSPACE}\研究报告交付'
$inputFile=Join-Path $root '桂阳县苦志育才公益学校调研报告.docx'
$outputFile=Join-Path $root '桂阳县苦志育才公益学校调研报告.pdf'
$word=$null
$doc=$null
try {
    $word=New-Object -ComObject Word.Application
    $word.Visible=$false
    $word.DisplayAlerts=0
    $doc=$word.Documents.Open($inputFile,$false,$false)
    $doc.Fields.Update() | Out-Null
    foreach($toc in $doc.TablesOfContents) {$toc.Update() | Out-Null}
    $doc.Repaginate()
    $pages=$doc.ComputeStatistics(2)
    Write-Output "Pages: $pages"
    $doc.Save()
    $doc.ExportAsFixedFormat($outputFile,17)
    Write-Output "Exported: $outputFile"
} finally {
    if($doc) {try {$doc.Close(0)} catch {}}
    if($word) {try {$word.Quit()} catch {}}
}
