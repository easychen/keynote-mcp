"""
演示文稿管理工具
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_file_path, KeynoteError


class PresentationTools:
    """演示文稿管理工具类"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """获取所有演示文稿管理工具"""
        return [
            Tool(
                name="create_presentation",
                description="创建新的 Keynote 演示文稿",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "演示文稿标题"
                        },
                        "theme": {
                            "type": "string",
                            "description": "主题名称（可选）"
                        },
                        "template": {
                            "type": "string",
                            "description": "模板路径（可选）"
                        }
                    },
                    "required": ["title"]
                }
            ),
            Tool(
                name="open_presentation",
                description="打开现有的 Keynote 演示文稿",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "演示文稿文件路径"
                        }
                    },
                    "required": ["file_path"]
                }
            ),
            Tool(
                name="save_presentation",
                description="保存演示文稿",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "文档名称（可选，默认为当前文档）"
                        }
                    }
                }
            ),
            Tool(
                name="close_presentation",
                description="关闭演示文稿",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "文档名称（可选，默认为当前文档）"
                        },
                        "should_save": {
                            "type": "boolean",
                            "description": "是否保存（默认为 true）"
                        }
                    }
                }
            ),
            Tool(
                name="list_presentations",
                description="列出所有打开的演示文稿",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="set_presentation_theme",
                description="设置演示文稿主题",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "文档名称（可选，默认为当前文档）"
                        },
                        "theme_name": {
                            "type": "string",
                            "description": "主题名称"
                        }
                    },
                    "required": ["theme_name"]
                }
            ),
            Tool(
                name="get_presentation_info",
                description="获取演示文稿信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "文档名称（可选，默认为当前文档）"
                        }
                    }
                }
            ),
            Tool(
                name="get_available_themes",
                description="获取可用主题列表",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="get_presentation_resolution",
                description="获取演示文稿分辨率信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "文档名称（可选，默认为当前文档）"
                        }
                    }
                }
            ),
            Tool(
                name="get_slide_size",
                description="获取幻灯片尺寸和比例信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "doc_name": {
                            "type": "string",
                            "description": "文档名称（可选，默认为当前文档）"
                        }
                    }
                }
            )
        ]
    
    async def create_presentation(self, title: str, theme: str = "", template: str = "") -> List[TextContent]:
        """创建新演示文稿"""
        try:
            # 确保 Keynote 运行
            if not self.runner.check_keynote_running():
                self.runner.launch_keynote()
            
            # 创建演示文稿
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    set newDoc to make new document
                    
                    if "{theme}" is not "" then
                        try
                            set theme of newDoc to theme "{theme}"
                        on error
                            log "Theme {theme} not found, using default theme"
                        end try
                    end if

                    set layout to "Blank"
                    
                    -- 如果指定了标题，保存到桌面
                    if "{title}" is not "" then
                        set desktopPath to (path to desktop as string) & "{title}.key"
                        save newDoc in file desktopPath
                    end if
                    
                    return name of newDoc
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功创建演示文稿: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 创建演示文稿失败: {str(e)}"
            )]
    
    async def open_presentation(self, file_path: str) -> List[TextContent]:
        """打开演示文稿"""
        try:
            validate_file_path(file_path)
            
            # 确保 Keynote 运行
            if not self.runner.check_keynote_running():
                self.runner.launch_keynote()
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    set targetFile to POSIX file "{file_path}"
                    open targetFile
                    return name of front document
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功打开演示文稿: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 打开演示文稿失败: {str(e)}"
            )]
    
    async def save_presentation(self, doc_name: str = "") -> List[TextContent]:
        """保存演示文稿"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        save front document
                        return name of front document
                    else
                        save document "{doc_name}"
                        return "{doc_name}"
                    end if
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功保存演示文稿: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 保存演示文稿失败: {str(e)}"
            )]
    
    async def close_presentation(self, doc_name: str = "", should_save: bool = True) -> List[TextContent]:
        """关闭演示文稿"""
        try:
            save_flag = "true" if should_save else "false"
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set docName to name of targetDoc
                    
                    if {save_flag} then
                        save targetDoc
                    end if
                    
                    close targetDoc
                    return docName
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功关闭演示文稿: {result}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 关闭演示文稿失败: {str(e)}"
            )]
    
    async def list_presentations(self) -> List[TextContent]:
        """列出所有打开的演示文稿"""
        try:
            result = self.runner.run_inline_script('''
                tell application "Keynote"
                    set docList to {}
                    repeat with doc in documents
                        set end of docList to name of doc
                    end repeat
                    return docList as string
                end tell
            ''')
            
            if result:
                presentations = result.replace("{", "").replace("}", "").split(", ")
                presentation_list = "\n".join([f"• {name}" for name in presentations])
                return [TextContent(
                    type="text",
                    text=f"📋 打开的演示文稿:\n{presentation_list}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="📋 当前没有打开的演示文稿"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取演示文稿列表失败: {str(e)}"
            )]
    
    async def set_presentation_theme(self, theme_name: str, doc_name: str = "") -> List[TextContent]:
        """设置演示文稿主题"""
        try:
            # 使用 Keynote 14 兼容的主题设置方法
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    -- 首先检查主题是否存在
                    set themeExists to false
                    repeat with t in themes
                        if name of t is "{theme_name}" then
                            set themeExists to true
                            exit repeat
                        end if
                    end repeat
                    
                    if not themeExists then
                        return "theme_not_found"
                    end if
                    
                    -- 使用 document theme 属性设置主题
                    try
                        set document theme of targetDoc to theme "{theme_name}"
                        return "success"
                    on error errMsg
                        return "error: " & errMsg
                    end try
                end tell
            ''')
            
            if result == "success":
                return [TextContent(
                    type="text",
                    text=f"✅ 成功设置主题: {theme_name}"
                )]
            elif result == "theme_not_found":
                return [TextContent(
                    type="text",
                    text=f"❌ 主题不存在: {theme_name}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ 设置主题失败: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 设置主题失败: {str(e)}"
            )]
    
    async def get_presentation_info(self, doc_name: str = "") -> List[TextContent]:
        """获取演示文稿信息"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    set docInfo to {{}}
                    set end of docInfo to name of targetDoc
                    set end of docInfo to count of slides of targetDoc
                    
                    try
                        set end of docInfo to name of theme of targetDoc
                    on error
                        set end of docInfo to "Unknown Theme"
                    end try
                    
                    return docInfo as string
                end tell
            ''')
            
            info_parts = result.replace("{", "").replace("}", "").split(", ")
            if len(info_parts) >= 3:
                name, slide_count, theme = info_parts[0], info_parts[1], info_parts[2]
                return [TextContent(
                    type="text",
                    text=f"📊 演示文稿信息:\n• 名称: {name}\n• 幻灯片数量: {slide_count}\n• 主题: {theme}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"📊 演示文稿信息: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取演示文稿信息失败: {str(e)}"
            )]
    
    async def get_available_themes(self) -> List[TextContent]:
        """获取可用主题列表"""
        try:
            # 使用更好的分隔符来获取主题列表
            result = self.runner.run_inline_script('''
                tell application "Keynote"
                    set themeList to {}
                    repeat with t in themes
                        set end of themeList to name of t
                    end repeat
                    
                    set AppleScript's text item delimiters to "|||"
                    set themeString to themeList as string
                    set AppleScript's text item delimiters to ""
                    
                    return themeString
                end tell
            ''')
            
            if result:
                themes = result.split("|||")
                theme_list = "\n".join([f"• {theme}" for theme in themes if theme.strip()])
                return [TextContent(
                    type="text",
                    text=f"🎨 可用主题 ({len(themes)} 个):\n{theme_list}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text="🎨 没有找到可用主题"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取主题列表失败: {str(e)}"
            )]
    
    async def get_presentation_resolution(self, doc_name: str = "") -> List[TextContent]:
        """获取演示文稿分辨率"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    try
                        set docWidth to width of targetDoc
                        set docHeight to height of targetDoc
                        
                        set AppleScript's text item delimiters to ","
                        set resolution to {{docWidth, docHeight}} as string
                        set AppleScript's text item delimiters to ""
                        
                        return resolution
                    on error
                        -- 返回标准16:9分辨率
                        return "1920,1080"
                    end try
                end tell
            ''')
            
            # 解析结果
            resolution_parts = result.split(",")
            if len(resolution_parts) >= 2:
                width, height = resolution_parts[0], resolution_parts[1]
                aspect_ratio = round(float(width) / float(height), 3)
                
                # 判断比例类型
                if 1.7 < aspect_ratio < 1.8:
                    ratio_type = "16:9"
                elif 1.3 < aspect_ratio < 1.4:
                    ratio_type = "4:3"
                else:
                    ratio_type = "自定义"
                
                return [TextContent(
                    type="text",
                    text=f"📐 演示文稿分辨率:\n• 宽度: {width} 像素\n• 高度: {height} 像素\n• 比例: {aspect_ratio} ({ratio_type})"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"📐 分辨率信息: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取分辨率失败: {str(e)}"
            )]
    
    async def get_slide_size(self, doc_name: str = "") -> List[TextContent]:
        """获取幻灯片尺寸和比例信息"""
        try:
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    if "{doc_name}" is "" then
                        set targetDoc to front document
                    else
                        set targetDoc to document "{doc_name}"
                    end if
                    
                    try
                        set slideWidth to width of targetDoc
                        set slideHeight to height of targetDoc
                        set aspectRatio to slideWidth / slideHeight
                        
                        -- 判断比例类型
                        set ratioType to ""
                        if aspectRatio > 1.7 and aspectRatio < 1.8 then
                            set ratioType to "16:9"
                        else if aspectRatio > 1.3 and aspectRatio < 1.4 then
                            set ratioType to "4:3"
                        else
                            set ratioType to "Custom"
                        end if
                        
                        set AppleScript's text item delimiters to ","
                        set sizeInfo to {{slideWidth, slideHeight, aspectRatio, ratioType}} as string
                        set AppleScript's text item delimiters to ""
                        
                        return sizeInfo
                    on error
                        -- 返回默认值
                        return "1920,1080,1.777,16:9"
                    end try
                end tell
            ''')
            
            # 解析结果
            size_parts = result.split(",")
            if len(size_parts) >= 4:
                width, height, ratio, ratio_type = size_parts[0], size_parts[1], size_parts[2], size_parts[3]
                
                # 计算一些有用的布局信息
                width_num = float(width)
                height_num = float(height)
                
                # 计算安全区域（留出边距）
                safe_width = int(width_num * 0.9)
                safe_height = int(height_num * 0.9)
                margin_x = int((width_num - safe_width) / 2)
                margin_y = int((height_num - safe_height) / 2)
                
                # 计算常用位置
                center_x = int(width_num / 2)
                center_y = int(height_num / 2)
                
                layout_info = f"""📏 幻灯片尺寸信息:
• 尺寸: {width} × {height} 像素
• 比例: {float(ratio):.3f} ({ratio_type})
• 中心点: ({center_x}, {center_y})

📐 布局参考:
• 安全区域: {safe_width} × {safe_height} 像素
• 边距: {margin_x} × {margin_y} 像素
• 标题区域建议: y = {margin_y} - {margin_y + 100}
• 内容区域建议: y = {margin_y + 120} - {safe_height + margin_y}"""
                
                return [TextContent(
                    type="text",
                    text=layout_info
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"📏 尺寸信息: {result}"
                )]
                
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取幻灯片尺寸失败: {str(e)}"
            )] 