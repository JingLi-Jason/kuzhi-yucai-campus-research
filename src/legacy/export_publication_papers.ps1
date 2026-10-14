$ErrorActionPreference='Stop'
$taskRoot='${ORIGINAL_WORKSPACE}\论文与作品集'
$wordApp=$null
try {
    foreach($language in @('EN','ZH')) {
        $paperCheck=Join-Path $taskRoot "工作文件\Publication_Paper_${language}.pdf"
        if(Test-Path -LiteralPath $paperCheck) {continue}
        $wordApp=New-Object -ComObject Word.Application
        $wordApp.Visible=$false
        $wordApp.DisplayAlerts=0
        $paperDoc=$null
        try {
            $paperInput=Join-Path $taskRoot "对外展示修订版\Paper_${language}.docx"
            $paperCheck=Join-Path $taskRoot "工作文件\Publication_Paper_${language}.pdf"
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

