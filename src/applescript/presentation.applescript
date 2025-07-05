-- presentation.applescript
-- 演示文稿管理脚本

-- 创建新演示文稿
on createNewPresentation(presentationName, themeName)
    tell application "Keynote"
        activate
        set newDoc to make new document
        
        if themeName is not "" then
            try
                set theme of newDoc to theme themeName
            on error
                -- 如果主题不存在，使用默认主题
                log "Theme " & themeName & " not found, using default theme"
            end try
        end if
        
        -- 将第一页的布局设置为空白
        try
            set layoutType to "Blank"
            set base slide of slide 1 of newDoc to master slide layoutType of theme of newDoc
        on error
            log "Failed to set blank layout for first slide"
        end try
        
        -- 如果指定了名称，则保存到桌面
        if presentationName is not "" then
            set desktopPath to (path to desktop as string) & presentationName & ".key"
            save newDoc in file desktopPath
        end if
        
        return name of newDoc
    end tell
end createNewPresentation

-- 打开演示文稿
on openPresentation(filePath)
    tell application "Keynote"
        set targetFile to POSIX file filePath
        open targetFile
        return name of front document
    end tell
end openPresentation

-- 保存演示文稿
on savePresentation(docName)
    tell application "Keynote"
        if docName is "" then
            save front document
        else
            save document docName
        end if
    end tell
end savePresentation

-- 另存为演示文稿
on saveAsPresentation(docName, filePath)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetFile to POSIX file filePath
        save targetDoc in targetFile
    end tell
end saveAsPresentation

-- 关闭演示文稿
on closePresentation(docName, shouldSave)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        if shouldSave then
            save targetDoc
        end if
        
        close targetDoc
    end tell
end closePresentation

-- 获取演示文稿信息
on getPresentationInfo(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set docInfo to {}
        set end of docInfo to name of targetDoc
        set end of docInfo to count of slides of targetDoc
        
        try
            set end of docInfo to name of theme of targetDoc
        on error
            set end of docInfo to "Unknown Theme"
        end try
        
        return docInfo
    end tell
end getPresentationInfo

-- 设置演示文稿主题
on setPresentationTheme(docName, themeName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        try
            set theme of targetDoc to theme themeName
            return true
        on error
            return false
        end try
    end tell
end setPresentationTheme

-- 获取可用主题列表
on getAvailableThemes()
    tell application "Keynote"
        set themeList to {}
        repeat with t in themes
            set end of themeList to name of t
        end repeat
        return themeList
    end tell
end getAvailableThemes

-- 复制演示文稿
on duplicatePresentation(docName, newName)
    tell application "Keynote"
        if docName is "" then
            set sourceDoc to front document
        else
            set sourceDoc to document docName
        end if
        
        set newDoc to duplicate sourceDoc
        if newName is not "" then
            set name of newDoc to newName
        end if
        
        return name of newDoc
    end tell
end duplicatePresentation

-- 获取演示文稿属性
on getPresentationProperties(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set props to {}
        set end of props to name of targetDoc
        set end of props to count of slides of targetDoc
        
        try
            set end of props to name of theme of targetDoc
        on error
            set end of props to "Unknown"
        end try
        
        try
            set end of props to (height of targetDoc as string)
            set end of props to (width of targetDoc as string)
        on error
            set end of props to "Unknown"
            set end of props to "Unknown"
        end try
        
        return props
    end tell
end getPresentationProperties

-- 获取演示文稿分辨率
on getPresentationResolution(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set resolution to {}
        
        try
            -- 获取文档的宽度和高度
            set docWidth to width of targetDoc
            set docHeight to height of targetDoc
            
            set end of resolution to docWidth
            set end of resolution to docHeight
            
            return resolution
        on error
            -- 如果无法获取分辨率，返回标准16:9分辨率
            set end of resolution to 1920
            set end of resolution to 1080
            return resolution
        end try
    end tell
end getPresentationResolution

-- 获取幻灯片尺寸信息
on getSlideSize(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set sizeInfo to {}
        
        try
            -- 获取幻灯片尺寸
            set slideWidth to width of targetDoc
            set slideHeight to height of targetDoc
            
            -- 计算比例
            set aspectRatio to slideWidth / slideHeight
            
            set end of sizeInfo to slideWidth
            set end of sizeInfo to slideHeight
            set end of sizeInfo to aspectRatio
            
            -- 判断比例类型
            if aspectRatio > 1.7 and aspectRatio < 1.8 then
                set end of sizeInfo to "16:9"
            else if aspectRatio > 1.3 and aspectRatio < 1.4 then
                set end of sizeInfo to "4:3"
            else
                set end of sizeInfo to "Custom"
            end if
            
            return sizeInfo
        on error
            -- 返回默认值
            set end of sizeInfo to 1920
            set end of sizeInfo to 1080
            set end of sizeInfo to 1.777
            set end of sizeInfo to "16:9"
            return sizeInfo
        end try
    end tell
end getSlideSize 