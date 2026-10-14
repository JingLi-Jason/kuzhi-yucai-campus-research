$ErrorActionPreference='Stop'
$taskPptRoot='${ORIGINAL_WORKSPACE}\论文与作品集'
$taskPptBuild=Join-Path $taskPptRoot '工作文件\ppt_build'
$taskPowerPoint=$null
try {
    foreach($language in @('EN')) {
        $taskPowerPoint=New-Object -ComObject PowerPoint.Application
        $taskDeck=$null
        try {
            $taskPptInput=Join-Path $taskPptRoot "英文15页紧凑版\Campus_Research_Portfolio_${language}_15pages_Final.pptx"
            $taskDeck=$taskPowerPoint.Presentations.Open($taskPptInput,-1,0,0)
            $taskMetrics=@()
            foreach($slide in $taskDeck.Slides) {
                foreach($shape in $slide.Shapes) {
                    if($shape.HasTextFrame -eq -1 -and $shape.TextFrame2.HasText -eq -1) {
                        $taskMetrics+=@{
                            slide=$slide.SlideIndex;id=$shape.Id;name=$shape.Name
                            text=$shape.TextFrame2.TextRange.Text
                            x=$shape.Left;y=$shape.Top;width=$shape.Width;height=$shape.Height
                            boundHeight=$shape.TextFrame2.TextRange.BoundHeight
                            boundWidth=$shape.TextFrame2.TextRange.BoundWidth
                        }
                    }
                }
            }
            $taskMetrics | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskPptBuild "Tight15_metrics_${language}.json") -Encoding utf8
            Write-Output "$language opened and rendered: $($taskDeck.Slides.Count) slides"
            $taskDeck.SaveAs((Join-Path $taskPptBuild "Tight15_${language}.pdf"),32)
        } finally {
            if($taskDeck) {try {$taskDeck.Close()} catch {}}
            if($taskPowerPoint) {try {$taskPowerPoint.Quit()} catch {}}
        }
    }
} finally {
    if($taskPowerPoint) {try {$taskPowerPoint.Quit()} catch {}}
}




