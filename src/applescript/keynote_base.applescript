-- keynote_base.applescript
-- 基础 Keynote 操作脚本

-- 检查 Keynote 是否运行
on checkKeynoteRunning()
    tell application "System Events"
        return (name of processes) contains "Keynote"
    end tell
end checkKeynoteRunning

-- 启动 Keynote
on launchKeynote()
    tell application "Keynote"
        activate
    end tell
end launchKeynote

-- 退出 Keynote
on quitKeynote()
    tell application "Keynote"
        quit
    end tell
end quitKeynote

-- 获取 Keynote 版本
on getKeynoteVersion()
    tell application "Keynote"
        return version
    end tell
end getKeynoteVersion

-- 获取当前活动文档
on getCurrentDocument()
    tell application "Keynote"
        if (count of documents) > 0 then
            return front document
        else
            return missing value
        end if
    end tell
end getCurrentDocument

-- 检查文档是否存在
on documentExists(docName)
    tell application "Keynote"
        try
            set targetDoc to document docName
            return true
        on error
            return false
        end try
    end tell
end documentExists

-- 获取所有打开的文档列表
on getOpenDocuments()
    tell application "Keynote"
        set docList to {}
        repeat with doc in documents
            set end of docList to name of doc
        end repeat
        return docList
    end tell
end getOpenDocuments

-- 激活指定文档
on activateDocument(docName)
    tell application "Keynote"
        set front document to document docName
    end tell
end activateDocument 