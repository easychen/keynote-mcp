-- slide.applescript
-- 幻灯片操作脚本

-- 添加新幻灯片
on addSlide(docName, slidePosition, layoutType)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        if slidePosition is 0 then
            set newSlide to make new slide at end of slides of targetDoc
        else
            set newSlide to make new slide at slide slidePosition of targetDoc
        end if
        
        -- 如果没有指定布局，默认使用 Blank 布局来避免默认文本占位符
        if layoutType is "" then
            set layoutType to "Blank"
        end if
        
        if layoutType is not "" then
            try
                set base slide of newSlide to master slide layoutType of targetDoc
            on error
                -- 如果布局不存在，尝试使用 Blank 布局
                try
                    set base slide of newSlide to master slide "Blank" of targetDoc
                    log "Layout " & layoutType & " not found, using Blank layout"
                on error
                    log "Neither " & layoutType & " nor Blank layout found, using default layout"
                end try
            end try
        end if
        
        return slide number of newSlide
    end tell
end addSlide

-- 删除幻灯片
on deleteSlide(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        delete slide slideNumber of targetDoc
    end tell
end deleteSlide

-- 复制幻灯片
on duplicateSlide(docName, slideNumber, newPosition)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set sourceSlide to slide slideNumber of targetDoc
        set newSlide to duplicate sourceSlide
        
        if newPosition is not 0 then
            move newSlide to slide newPosition of targetDoc
        end if
        
        return slide number of newSlide
    end tell
end duplicateSlide

-- 移动幻灯片
on moveSlide(docName, fromPosition, toPosition)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set sourceSlide to slide fromPosition of targetDoc
        move sourceSlide to slide toPosition of targetDoc
    end tell
end moveSlide

-- 获取幻灯片数量
on getSlideCount(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        return count of slides of targetDoc
    end tell
end getSlideCount

-- 选择幻灯片
on selectSlide(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set current slide of targetDoc to slide slideNumber of targetDoc
    end tell
end selectSlide

-- 获取当前幻灯片编号
on getCurrentSlideNumber(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        return slide number of current slide of targetDoc
    end tell
end getCurrentSlideNumber

-- 设置幻灯片布局
on setSlideLayout(docName, slideNumber, layoutType)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        try
            set master slide of slide slideNumber of targetDoc to master slide layoutType of targetDoc
            return true
        on error
            return false
        end try
    end tell
end setSlideLayout

-- 获取可用布局列表
on getAvailableLayouts(docName)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set layoutList to {}
        repeat with masterSlide in master slides of targetDoc
            set end of layoutList to name of masterSlide
        end repeat
        return layoutList
    end tell
end getAvailableLayouts

-- 获取幻灯片信息
on getSlideInfo(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        set slideInfo to {}
        
        set end of slideInfo to slide number of targetSlide
        
        try
            set end of slideInfo to name of master slide of targetSlide
        on error
            set end of slideInfo to "Unknown Layout"
        end try
        
        try
            set end of slideInfo to count of text items of targetSlide
        on error
            set end of slideInfo to 0
        end try
        
        return slideInfo
    end tell
end getSlideInfo

-- 跳转到幻灯片
on goToSlide(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set current slide of targetDoc to slide slideNumber of targetDoc
        show slide slideNumber of targetDoc
    end tell
end goToSlide

-- 获取幻灯片标题
on getSlideTitle(docName, slideNumber)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            -- 尝试获取标题文本框的内容
            repeat with textItem in text items of targetSlide
                if object text of textItem contains "标题" or object text of textItem contains "Title" then
                    return object text of textItem
                end if
            end repeat
            
            -- 如果没有找到标题，返回第一个文本项
            if (count of text items of targetSlide) > 0 then
                return object text of text item 1 of targetSlide
            else
                return ""
            end if
        on error
            return ""
        end try
    end tell
end getSlideTitle

-- 设置幻灯片标题
on setSlideTitle(docName, slideNumber, titleText)
    tell application "Keynote"
        if docName is "" then
            set targetDoc to front document
        else
            set targetDoc to document docName
        end if
        
        set targetSlide to slide slideNumber of targetDoc
        
        try
            -- 尝试找到标题文本框并设置内容
            repeat with textItem in text items of targetSlide
                if object text of textItem contains "标题" or object text of textItem contains "Title" then
                    set object text of textItem to titleText
                    return true
                end if
            end repeat
            
            -- 如果没有找到标题，设置第一个文本项
            if (count of text items of targetSlide) > 0 then
                set object text of text item 1 of targetSlide to titleText
                return true
            else
                return false
            end if
        on error
            return false
        end try
    end tell
end setSlideTitle 