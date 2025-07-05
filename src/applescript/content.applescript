-- content.applescript
-- 内容管理脚本

-- 添加文本框
on addTextBox(docName, slideNumber, textContent, xPos, yPos, textWidth, textHeight)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 创建文本框
                set newTextBox to make new text item with properties {object text:textContent}
                
                -- 设置位置和大小
                if xPos is not 0 or yPos is not 0 then
                    set position of newTextBox to {xPos, yPos}
                end if
                
                if textWidth is not 0 or textHeight is not 0 then
                    set size of newTextBox to {textWidth, textHeight}
                end if
            end tell
        end tell
        
        return true
    end tell
end addTextBox

-- 添加标题
on addTitle(docName, slideNumber, titleText, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 创建标题文本框
                set newTitle to make new text item with properties {object text:titleText}
                
                -- 设置位置
                if xPos is not 0 or yPos is not 0 then
                    set position of newTitle to {xPos, yPos}
                end if
                
                -- 设置字体样式
                tell newTitle
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 36  -- 默认标题大小
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    end if
                    
                    -- 设置为粗体
                    set font style of object text to bold
                end tell
            end tell
        end tell
        
        return true
    end tell
end addTitle

-- 添加副标题
on addSubtitle(docName, slideNumber, subtitleText, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 创建副标题文本框
                set newSubtitle to make new text item with properties {object text:subtitleText}
                
                -- 设置位置
                if xPos is not 0 or yPos is not 0 then
                    set position of newSubtitle to {xPos, yPos}
                end if
                
                -- 设置字体样式
                tell newSubtitle
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 24  -- 默认副标题大小
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    end if
                end tell
            end tell
        end tell
        
        return true
    end tell
end addSubtitle

-- 添加项目符号列表
on addBulletList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 构建列表文本
                set listText to ""
                repeat with i from 1 to count of listItems
                    set listText to listText & "• " & (item i of listItems)
                    if i < count of listItems then
                        set listText to listText & return
                    end if
                end repeat
                
                -- 创建列表文本框
                set newList to make new text item with properties {object text:listText}
                
                -- 设置位置
                if xPos is not 0 or yPos is not 0 then
                    set position of newList to {xPos, yPos}
                end if
                
                -- 设置字体样式
                tell newList
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 18  -- 默认列表大小
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    end if
                end tell
            end tell
        end tell
        
        return true
    end tell
end addBulletList

-- 添加编号列表
on addNumberedList(docName, slideNumber, listItems, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 构建编号列表文本
                set listText to ""
                repeat with i from 1 to count of listItems
                    set listText to listText & (i as string) & ". " & (item i of listItems)
                    if i < count of listItems then
                        set listText to listText & return
                    end if
                end repeat
                
                -- 创建编号列表文本框
                set newList to make new text item with properties {object text:listText}
                
                -- 设置位置
                if xPos is not 0 or yPos is not 0 then
                    set position of newList to {xPos, yPos}
                end if
                
                -- 设置字体样式
                tell newList
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 18  -- 默认列表大小
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    end if
                end tell
            end tell
        end tell
        
        return true
    end tell
end addNumberedList

-- 添加代码块
on addCodeBlock(docName, slideNumber, codeText, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 创建代码块文本框
                set newCodeBlock to make new text item with properties {object text:codeText}
                
                -- 设置位置
                if xPos is not 0 or yPos is not 0 then
                    set position of newCodeBlock to {xPos, yPos}
                end if
                
                -- 设置字体样式（等宽字体）
                tell newCodeBlock
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 14  -- 默认代码字体大小
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    else
                        set font of object text to "Monaco"  -- 默认等宽字体
                    end if
                end tell
            end tell
        end tell
        
        return true
    end tell
end addCodeBlock

-- 添加引用文本
on addQuote(docName, slideNumber, quoteText, xPos, yPos, fontSize, fontName)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 为引用文本添加引号
                set formattedQuote to """ & quoteText & """
                
                -- 创建引用文本框
                set newQuote to make new text item with properties {object text:formattedQuote}
                
                -- 设置位置
                if xPos is not 0 or yPos is not 0 then
                    set position of newQuote to {xPos, yPos}
                end if
                
                -- 设置字体样式（斜体）
                tell newQuote
                    if fontSize is not 0 then
                        set size of object text to fontSize
                    else
                        set size of object text to 20  -- 默认引用字体大小
                    end if
                    
                    if fontName is not "" then
                        set font of object text to fontName
                    end if
                    
                    -- 设置为斜体
                    set font style of object text to italic
                end tell
            end tell
        end tell
        
        return true
    end tell
end addQuote

-- 编辑文本框内容
on editTextBox(docName, slideNumber, textIndex, newContent)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            set object text of text item textIndex of targetSlide to newContent
            return true
        on error
            return false
        end try
    end tell
end editTextBox

-- 添加图片
on addImage(docName, slideNumber, imagePath, xPos, yPos, imageWidth, imageHeight)
    tell application "Keynote"
        activate
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        tell targetDoc
            tell slide slideNumber
                -- 添加图片
                set imageFile to POSIX file imagePath
                set newImage to make new image with properties {file:imageFile}
                
                -- 设置位置和大小
                if xPos is not 0 or yPos is not 0 then
                    set position of newImage to {xPos, yPos}
                end if
                
                if imageWidth is not 0 or imageHeight is not 0 then
                    set size of newImage to {imageWidth, imageHeight}
                end if
            end tell
        end tell
        
        return true
    end tell
end addImage

-- 添加形状
on addShape(docName, slideNumber, shapeType, xPos, yPos, shapeWidth, shapeHeight)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        -- 创建形状
        set newShape to make new shape at end of shapes of targetSlide
        
        -- 设置形状类型（简化版本）
        -- 注意：实际的形状类型设置可能需要根据具体的 Keynote 版本调整
        
        -- 设置位置和大小
        if xPos is not 0 or yPos is not 0 then
            set position of newShape to {xPos, yPos}
        end if
        
        if shapeWidth is not 0 or shapeHeight is not 0 then
            set size of newShape to {shapeWidth, shapeHeight}
        end if
        
        return true
    end tell
end addShape

-- 添加表格
on addTable(docName, slideNumber, rowCount, columnCount, xPos, yPos)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        -- 创建表格
        set newTable to make new table at end of tables of targetSlide
        set row count of newTable to rowCount
        set column count of newTable to columnCount
        
        -- 设置位置
        if xPos is not 0 or yPos is not 0 then
            set position of newTable to {xPos, yPos}
        end if
        
        return true
    end tell
end addTable

-- 设置表格单元格内容
on setTableCell(docName, slideNumber, tableIndex, rowIndex, columnIndex, cellContent)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            set targetTable to table tableIndex of targetSlide
            set value of cell columnIndex of row rowIndex of targetTable to cellContent
            return true
        on error
            return false
        end try
    end tell
end setTableCell

-- 设置文本样式
on setTextStyle(docName, slideNumber, textIndex, fontSize, fontColor, fontName, isBold, isItalic)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            set targetText to text item textIndex of targetSlide
            
            -- 设置字体大小
            if fontSize is not 0 then
                set size of targetText to fontSize
            end if
            
            -- 设置字体名称
            if fontName is not "" then
                set font of targetText to fontName
            end if
            
            -- 设置粗体和斜体（简化版本）
            -- 注意：字体样式设置可能需要根据具体的 Keynote 版本调整
            
            return true
        on error
            return false
        end try
    end tell
end setTextStyle

-- 设置对象位置
on positionObject(docName, slideNumber, objectType, objectIndex, xPos, yPos)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            if objectType is "text" then
                set position of text item objectIndex of targetSlide to {xPos, yPos}
            else if objectType is "image" then
                set position of image objectIndex of targetSlide to {xPos, yPos}
            else if objectType is "shape" then
                set position of shape objectIndex of targetSlide to {xPos, yPos}
            else if objectType is "table" then
                set position of table objectIndex of targetSlide to {xPos, yPos}
            end if
            
            return true
        on error
            return false
        end try
    end tell
end positionObject

-- 调整对象大小
on resizeObject(docName, slideNumber, objectType, objectIndex, newWidth, newHeight)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            if objectType is "text" then
                set size of text item objectIndex of targetSlide to {newWidth, newHeight}
            else if objectType is "image" then
                set size of image objectIndex of targetSlide to {newWidth, newHeight}
            else if objectType is "shape" then
                set size of shape objectIndex of targetSlide to {newWidth, newHeight}
            else if objectType is "table" then
                set size of table objectIndex of targetSlide to {newWidth, newHeight}
            end if
            
            return true
        on error
            return false
        end try
    end tell
end resizeObject

-- 删除对象
on deleteObject(docName, slideNumber, objectType, objectIndex)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            if objectType is "text" then
                delete text item objectIndex of targetSlide
            else if objectType is "image" then
                delete image objectIndex of targetSlide
            else if objectType is "shape" then
                delete shape objectIndex of targetSlide
            else if objectType is "table" then
                delete table objectIndex of targetSlide
            end if
            
            return true
        on error
            return false
        end try
    end tell
end deleteObject

-- 获取幻灯片内容统计
on getSlideContentStats(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        set stats to {}
        
        try
            set end of stats to count of text items of targetSlide
        on error
            set end of stats to 0
        end try
        
        try
            set end of stats to count of images of targetSlide
        on error
            set end of stats to 0
        end try
        
        try
            set end of stats to count of shapes of targetSlide
        on error
            set end of stats to 0
        end try
        
        try
            set end of stats to count of tables of targetSlide
        on error
            set end of stats to 0
        end try
        
        return stats
    end tell
end getSlideContentStats 