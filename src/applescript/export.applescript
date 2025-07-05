-- export.applescript
-- 导出和截图脚本

-- 截图单个幻灯片
on screenshotSlide(docName, slideNumber, outputPath, imageFormat, quality)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        -- 设置导出格式
        if imageFormat is "jpg" or imageFormat is "jpeg" then
            set exportFormat to JPEG
        else
            set exportFormat to PNG
        end if
        
        -- 导出幻灯片为图片
        set outputFile to POSIX file outputPath
        export targetSlide to outputFile as exportFormat
        
        return true
    end tell
end screenshotSlide

-- 截图所有幻灯片
on screenshotAllSlides(docName, outputDir, imageFormat, quality)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set slideCount to count of slides of targetDoc
        set exportedFiles to {}
        
        -- 设置导出格式
        if imageFormat is "jpg" or imageFormat is "jpeg" then
            set exportFormat to JPEG
            set fileExtension to ".jpg"
        else
            set exportFormat to PNG
            set fileExtension to ".png"
        end if
        
        -- 逐个导出幻灯片
        repeat with i from 1 to slideCount
            set targetSlide to slide i of targetDoc
            set fileName to "slide_" & (i as string) & fileExtension
            set outputPath to outputDir & "/" & fileName
            set outputFile to POSIX file outputPath
            
            export targetSlide to outputFile as exportFormat
            set end of exportedFiles to outputPath
        end repeat
        
        return exportedFiles
    end tell
end screenshotAllSlides

-- 导出演示文稿为 PDF
on exportPDF(docName, outputPath, slideRange)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set outputFile to POSIX file outputPath
        
        if slideRange is "" then
            -- 导出所有幻灯片
            export targetDoc to outputFile as PDF
        else
            -- 导出指定范围的幻灯片
            -- 注意：Keynote 可能不直接支持范围导出，这里提供基本实现
            export targetDoc to outputFile as PDF
        end if
        
        return true
    end tell
end exportPDF

-- 导出演示文稿为图片序列
on exportImages(docName, outputDir, imageFormat, quality)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- 设置导出格式
        if imageFormat is "jpg" or imageFormat is "jpeg" then
            set exportFormat to JPEG
        else
            set exportFormat to PNG
        end if
        
        -- 导出所有幻灯片
        set outputFolder to POSIX file outputDir
        export targetDoc to outputFolder as exportFormat
        
        return true
    end tell
end exportImages

-- 导出演示文稿为 PowerPoint 格式
on exportPowerPoint(docName, outputPath)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set outputFile to POSIX file outputPath
        export targetDoc to outputFile as Microsoft PowerPoint
        
        return true
    end tell
end exportPowerPoint

-- 导出演示文稿为 QuickTime 影片
on exportMovie(docName, outputPath, movieFormat, quality)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set outputFile to POSIX file outputPath
        
        -- 设置影片格式
        if movieFormat is "mov" then
            set exportFormat to QuickTime movie
        else
            set exportFormat to QuickTime movie
        end if
        
        -- 导出为影片
        export targetDoc to outputFile as exportFormat
        
        return true
    end tell
end exportMovie

-- 导出演示文稿为 HTML
on exportHTML(docName, outputPath)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set outputFile to POSIX file outputPath
        export targetDoc to outputFile as HTML
        
        return true
    end tell
end exportHTML

-- 打印演示文稿
on printPresentation(docName, printerName, slideRange)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        -- 基本打印功能
        if printerName is not "" then
            -- 设置打印机（如果指定）
            tell application "System Events"
                tell process "Keynote"
                    keystroke "p" using command down
                    delay 1
                    -- 这里可以添加更多打印设置
                end tell
            end tell
        else
            print targetDoc
        end if
        
        return true
    end tell
end printPresentation

-- 获取导出选项
on getExportOptions()
    set exportOptions to {}
    
    -- 支持的图片格式
    set imageFormats to {"PNG", "JPEG", "TIFF", "GIF"}
    set end of exportOptions to imageFormats
    
    -- 支持的文档格式
    set documentFormats to {"PDF", "PowerPoint", "HTML", "QuickTime"}
    set end of exportOptions to documentFormats
    
    -- 质量选项
    set qualityOptions to {"Low", "Medium", "High", "Maximum"}
    set end of exportOptions to qualityOptions
    
    return exportOptions
end getExportOptions

-- 批量导出多个演示文稿
on batchExport(docNames, outputDir, exportFormat, quality)
    set exportedFiles to {}
    
    repeat with docName in docNames
        try
            tell application "Keynote"
                set targetDoc to document docName
                
                if exportFormat is "PDF" then
                    set fileName to (name of targetDoc) & ".pdf"
                    set outputPath to outputDir & "/" & fileName
                    set outputFile to POSIX file outputPath
                    export targetDoc to outputFile as PDF
                    
                else if exportFormat is "PNG" then
                    set fileName to (name of targetDoc) & ".png"
                    set outputPath to outputDir & "/" & fileName
                    set outputFile to POSIX file outputPath
                    export targetDoc to outputFile as PNG
                    
                else if exportFormat is "JPEG" then
                    set fileName to (name of targetDoc) & ".jpg"
                    set outputPath to outputDir & "/" & fileName
                    set outputFile to POSIX file outputPath
                    export targetDoc to outputFile as JPEG
                    
                end if
                
                set end of exportedFiles to outputPath
            end tell
        on error errorMessage
            log "Error exporting " & docName & ": " & errorMessage
        end try
    end repeat
    
    return exportedFiles
end batchExport

-- 获取幻灯片预览
on getSlidePreview(docName, slideNumber, previewSize)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        -- 创建临时预览文件
        set tempDir to (path to temporary items folder) as string
        set tempFile to tempDir & "slide_preview_" & (slideNumber as string) & ".png"
        set tempPath to POSIX file tempFile
        
        -- 导出预览
        export targetSlide to tempPath as PNG
        
        return tempFile
    end tell
end getSlidePreview 