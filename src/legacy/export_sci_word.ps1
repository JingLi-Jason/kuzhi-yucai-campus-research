$ErrorActionPreference='Stop'
$taskWordApp=$null
$taskWordDocument=$null
try {
    $taskWordApp=New-Object -ComObject Word.Application
    $taskWordApp.Visible=$false
    $taskWordApp.DisplayAlerts=0
    $taskDocxPath='${ORIGINAL_WORKSPACE}\论文与作品集\英文Word论文\Kuzhi_Yucai_Campus_Research_EN.docx'
    $taskPdfPath='${ORIGINAL_WORKSPACE}\论文与作品集\工作文件\SCI_Word\Word_Render.pdf'
    $taskWordDocument=$taskWordApp.Documents.Open($taskDocxPath,$false,$false)
    $taskWordDocument.Fields.Update() | Out-Null
    $taskWordDocument.Repaginate()
    Write-Output "Rendered pages: $($taskWordDocument.ComputeStatistics(2))"
    $taskWordDocument.Save()
    $taskWordDocument.ExportAsFixedFormat($taskPdfPath,17)
} finally {
    if($taskWordDocument) {try {$taskWordDocument.Close(0)} catch {}}
    if($taskWordApp) {try {$taskWordApp.Quit()} catch {}}
}
