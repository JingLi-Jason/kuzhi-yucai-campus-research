$ErrorActionPreference='Stop'
$taskRoot='${ORIGINAL_WORKSPACE}\论文与作品集'
$wordApp=$null
try {
    foreach($language in @('EN','ZH')) {
        $paperCheck=Join-Path $taskRoot "工作文件\Paper_${language}_Word_check.pdf"
        if(Test-Path -LiteralPath $paperCheck) {continue}
        $wordApp=New-Object -ComObject Word.Application
        $wordApp.Visible=$false
        $wordApp.DisplayAlerts=0
        $paperDoc=$null
        try {
            $paperInput=Join-Path $taskRoot "Paper_${language}_Editable.docx"
            $paperCheck=Join-Path $taskRoot "工作文件\Paper_${language}_Word_check.pdf"
            $paperDoc=$wordApp.Documents.Open($paperInput,$false,$false)
            $paperDoc.Fields.Update() | Out-Null
            $paperDoc.Repaginate()
            Write-Output "$language Word pages: $($paperDoc.ComputeStatistics(2))"
            $paperDoc.Save()
            $paperDoc.ExportAsFixedFormat($paperCheck,17)
        } finally {
            if($paperDoc) {try {$paperDoc.Close(0)} catch {}}
            if($wordApp) {try {$wordApp.Quit()} catch {}}
        }
    }
} finally {
    if($wordApp) {try {$wordApp.Quit()} catch {}}
}
