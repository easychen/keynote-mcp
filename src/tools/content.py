"""
内容管理工具
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number, validate_coordinates, validate_file_path, ParameterError


class ContentTools:
    """内容管理工具类"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """获取所有内容管理工具"""
        return [
            Tool(
                name="add_text_box",
                description="在幻灯片中添加文本框",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "text": {
                            "type": "string",
                            "description": "文本内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议范围：50-950像素，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议范围：50-650像素，避免重叠请使用不同坐标"
                        }
                    },
                    "required": ["slide_number", "text"]
                }
            ),
            Tool(
                name="add_title",
                description="在幻灯片中添加标题",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "title": {
                            "type": "string",
                            "description": "标题内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议标题位置：x=100-200，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议标题位置：y=50-100，避免重叠请使用不同坐标"
                        },
                        "font_size": {
                            "type": "number",
                            "description": "字体大小（可选，默认36）"
                        },
                        "font_name": {
                            "type": "string",
                            "description": "字体名称（可选）"
                        }
                    },
                    "required": ["slide_number", "title"]
                }
            ),
            Tool(
                name="add_subtitle",
                description="在幻灯片中添加副标题",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "subtitle": {
                            "type": "string",
                            "description": "副标题内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议副标题位置：x=100-200，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议副标题位置：y=120-180，避免重叠请使用不同坐标"
                        },
                        "font_size": {
                            "type": "number",
                            "description": "字体大小（可选，默认24）"
                        },
                        "font_name": {
                            "type": "string",
                            "description": "字体名称（可选）"
                        }
                    },
                    "required": ["slide_number", "subtitle"]
                }
            ),
            Tool(
                name="add_bullet_list",
                description="在幻灯片中添加项目符号列表",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "列表项内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议列表位置：x=100-150，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议列表位置：y=200-300，避免重叠请使用不同坐标"
                        },
                        "font_size": {
                            "type": "number",
                            "description": "字体大小（可选，默认18）"
                        },
                        "font_name": {
                            "type": "string",
                            "description": "字体名称（可选）"
                        }
                    },
                    "required": ["slide_number", "items"]
                }
            ),
            Tool(
                name="add_numbered_list",
                description="在幻灯片中添加编号列表",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "列表项内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议列表位置：x=100-150，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议列表位置：y=200-300，避免重叠请使用不同坐标"
                        },
                        "font_size": {
                            "type": "number",
                            "description": "字体大小（可选，默认18）"
                        },
                        "font_name": {
                            "type": "string",
                            "description": "字体名称（可选）"
                        }
                    },
                    "required": ["slide_number", "items"]
                }
            ),
            Tool(
                name="add_code_block",
                description="在幻灯片中添加代码块",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "code": {
                            "type": "string",
                            "description": "代码内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议代码块位置：x=100-200，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议代码块位置：y=250-350，避免重叠请使用不同坐标"
                        },
                        "font_size": {
                            "type": "number",
                            "description": "字体大小（可选，默认14）"
                        },
                        "font_name": {
                            "type": "string",
                            "description": "字体名称（可选，默认Monaco）"
                        }
                    },
                    "required": ["slide_number", "code"]
                }
            ),
            Tool(
                name="add_quote",
                description="在幻灯片中添加引用文本",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "quote": {
                            "type": "string",
                            "description": "引用内容"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议引用位置：x=150-250，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议引用位置：y=300-400，避免重叠请使用不同坐标"
                        },
                        "font_size": {
                            "type": "number",
                            "description": "字体大小（可选，默认20）"
                        },
                        "font_name": {
                            "type": "string",
                            "description": "字体名称（可选）"
                        }
                    },
                    "required": ["slide_number", "quote"]
                }
            ),
            Tool(
                name="add_image",
                description="在幻灯片中添加图片",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "image_path": {
                            "type": "string",
                            "description": "图片文件路径"
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（像素，可选）- 左上角为原点(0,0)，向右为正。建议图片位置：x=400-600，避免重叠请使用不同坐标"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（像素，可选）- 左上角为原点(0,0)，向下为正。建议图片位置：y=200-400，避免重叠请使用不同坐标"
                        }
                    },
                    "required": ["slide_number", "image_path"]
                }
            )
        ]
    
    async def add_text_box(self, slide_number: int, text: str, x: Optional[float] = None, y: Optional[float] = None, doc_name: str = "") -> List[TextContent]:
        """添加文本框"""
        try:
            validate_slide_number(slide_number)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 处理文本中的引号
            escaped_text = text.replace('"', '\\"')
            
            # 使用内联脚本，语法正确
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is not "" then
                        set targetDoc to document "{doc_name}"
                    else
                        set targetDoc to front document
                    end if
                    
                    tell targetDoc
                        tell slide {slide_number}
                            -- 创建文本框
                            set newTextBox to make new text item with properties {{object text:"{escaped_text}"}}
                            
                            -- 设置位置（如果指定了x或y坐标）
                            {"" if x is None and y is None else f"set position of newTextBox to {{{x_pos}, {y_pos}}}"}
                        end tell
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加文本框"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加文本框失败: {str(e)}"
            )]
    
    async def add_title(self, slide_number: int, title: str, x: Optional[float] = None, y: Optional[float] = None, 
                       font_size: Optional[int] = None, font_name: str = "", doc_name: str = "") -> List[TextContent]:
        """添加标题"""
        try:
            validate_slide_number(slide_number)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 处理文本中的引号
            escaped_title = title.replace('"', '\\"')
            
            # 构建字体设置命令
            font_command = f'set font of object text to "{font_name}"' if font_name else ""
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is not "" then
                        set targetDoc to document "{doc_name}"
                    else
                        set targetDoc to front document
                    end if
                    
                    tell targetDoc
                        tell slide {slide_number}
                            set newTitle to make new text item with properties {{object text:"{escaped_title}"}}
                            
                            -- 设置位置（如果指定了x或y坐标）
                            {"" if x is None and y is None else f"set position of newTitle to {{{x_pos}, {y_pos}}}"}
                            
                            tell newTitle
                                set size of object text to {font_size if font_size else 36}
                                {font_command if font_command else "-- no font specified"}
                            end tell
                        end tell
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加标题"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加标题失败: {str(e)}"
            )]
    
    async def add_subtitle(self, slide_number: int, subtitle: str, x: Optional[float] = None, y: Optional[float] = None, 
                          font_size: Optional[int] = None, font_name: str = "", doc_name: str = "") -> List[TextContent]:
        """添加副标题"""
        try:
            validate_slide_number(slide_number)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 处理文本中的引号
            escaped_subtitle = subtitle.replace('"', '\\"')
            
            # 构建字体设置命令
            font_command = f'set font of object text to "{font_name}"' if font_name else ""
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is not "" then
                        set targetDoc to document "{doc_name}"
                    else
                        set targetDoc to front document
                    end if
                    
                    tell targetDoc
                        tell slide {slide_number}
                            set newSubtitle to make new text item with properties {{object text:"{escaped_subtitle}"}}
                            
                            -- 设置位置（如果指定了x或y坐标）
                            {"" if x is None and y is None else f"set position of newSubtitle to {{{x_pos}, {y_pos}}}"}
                            
                            tell newSubtitle
                                set size of object text to {font_size if font_size else 24}
                                {font_command if font_command else "-- no font specified"}
                            end tell
                        end tell
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加副标题"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加副标题失败: {str(e)}"
            )]
    
    async def add_bullet_list(self, slide_number: int, items: List[str], x: Optional[float] = None, y: Optional[float] = None, 
                             font_size: Optional[int] = None, font_name: str = "", doc_name: str = "") -> List[TextContent]:
        """添加项目符号列表"""
        try:
            validate_slide_number(slide_number)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 构建列表文本
            list_text = ""
            for i, item in enumerate(items):
                escaped_item = item.replace('"', '\\"')
                list_text += f"• {escaped_item}"
                if i < len(items) - 1:
                    list_text += "\\n"
            
            # 构建字体设置命令
            font_command = f'set font of object text to "{font_name}"' if font_name else ""
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is not "" then
                        set targetDoc to document "{doc_name}"
                    else
                        set targetDoc to front document
                    end if
                    
                    tell targetDoc
                        tell slide {slide_number}
                            set newList to make new text item with properties {{object text:"{list_text}"}}
                            
                            -- 设置位置（如果指定了x或y坐标）
                            {"" if x is None and y is None else f"set position of newList to {{{x_pos}, {y_pos}}}"}
                            
                            tell newList
                                set size of object text to {font_size if font_size else 18}
                                {font_command if font_command else "-- no font specified"}
                            end tell
                        end tell
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加项目符号列表（{len(items)} 项）"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加项目符号列表失败: {str(e)}"
            )]
    
    async def add_numbered_list(self, slide_number: int, items: List[str], x: Optional[float] = None, y: Optional[float] = None, 
                               font_size: Optional[int] = None, font_name: str = "", doc_name: str = "") -> List[TextContent]:
        """添加编号列表"""
        try:
            validate_slide_number(slide_number)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 构建编号列表文本
            list_text = ""
            for i, item in enumerate(items):
                escaped_item = item.replace('"', '\\"')
                list_text += f"{i+1}. {escaped_item}"
                if i < len(items) - 1:
                    list_text += "\\n"
            
            # 构建字体设置命令
            font_command = f'set font of object text to "{font_name}"' if font_name else ""
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is not "" then
                        set targetDoc to document "{doc_name}"
                    else
                        set targetDoc to front document
                    end if
                    
                    tell targetDoc
                        tell slide {slide_number}
                            set newList to make new text item with properties {{object text:"{list_text}"}}
                            
                            -- 设置位置（如果指定了x或y坐标）
                            {"" if x is None and y is None else f"set position of newList to {{{x_pos}, {y_pos}}}"}
                            
                            tell newList
                                set size of object text to {font_size if font_size else 18}
                                {font_command if font_command else "-- no font specified"}
                            end tell
                        end tell
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加编号列表（{len(items)} 项）"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加编号列表失败: {str(e)}"
            )]
    
    async def add_code_block(self, slide_number: int, code: str, x: Optional[float] = None, y: Optional[float] = None, 
                            font_size: Optional[int] = None, font_name: str = "", doc_name: str = "") -> List[TextContent]:
        """添加代码块"""
        try:
            validate_slide_number(slide_number)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 处理代码中的引号和换行
            escaped_code = code.replace('"', '\\"').replace('\n', '\\n')
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is not "" then
                        set targetDoc to document "{doc_name}"
                    else
                        set targetDoc to front document
                    end if
                    
                    tell targetDoc
                        tell slide {slide_number}
                            set newCodeBlock to make new text item with properties {{object text:"{escaped_code}"}}
                            
                            -- 设置位置（如果指定了x或y坐标）
                            {"" if x is None and y is None else f"set position of newCodeBlock to {{{x_pos}, {y_pos}}}"}
                            
                            tell newCodeBlock
                                set size of object text to {font_size if font_size else 14}
                                set font of object text to "{font_name if font_name else 'Monaco'}"
                            end tell
                        end tell
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加代码块"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加代码块失败: {str(e)}"
            )]
    
    async def add_quote(self, slide_number: int, quote: str, x: Optional[float] = None, y: Optional[float] = None, 
                       font_size: Optional[int] = None, font_name: str = "", doc_name: str = "") -> List[TextContent]:
        """添加引用文本"""
        try:
            validate_slide_number(slide_number)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 处理引用文本中的引号
            escaped_quote = quote.replace('"', '\\"')
            # 使用单引号包围，避免嵌套引号问题
            formatted_quote = f"'{escaped_quote}'"
            
            # 构建字体设置命令
            font_command = f'set font of object text to "{font_name}"' if font_name else ""
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    if "{doc_name}" is not "" then
                        set targetDoc to document "{doc_name}"
                    else
                        set targetDoc to front document
                    end if
                    
                    tell targetDoc
                        tell slide {slide_number}
                            set newQuote to make new text item with properties {{object text:"{formatted_quote}"}}
                            
                            -- 设置位置（如果指定了x或y坐标）
                            {"" if x is None and y is None else f"set position of newQuote to {{{x_pos}, {y_pos}}}"}
                            
                            tell newQuote
                                set size of object text to {font_size if font_size else 20}
                                {font_command if font_command else "-- no font specified"}
                            end tell
                        end tell
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加引用文本"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加引用文本失败: {str(e)}"
            )]
    
    async def add_image(self, slide_number: int, image_path: str, x: Optional[float] = None, y: Optional[float] = None) -> List[TextContent]:
        """添加图片"""
        try:
            validate_slide_number(slide_number)
            validate_file_path(image_path)
            x_pos, y_pos = validate_coordinates(x, y)
            
            # 构建位置参数
            position_params = ""
            if x is not None and y is not None:
                position_params = f", position:{{{x_pos}, {y_pos}}}"
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    set targetDoc to front document
                    
                    tell targetDoc
                        tell slide {slide_number}
                            -- 使用正确的alias语法
                            set imageFile to POSIX file "{image_path}" as alias
                            
                            -- 方法1: 尝试标准image对象
                            try
                                set newImage to make new image with properties {{file:imageFile{position_params}}}
                                return "image_success"
                            on error
                                -- 方法2: 尝试movie对象（适用于某些Keynote版本）
                                try
                                    set newMovie to make new movie with properties {{file:imageFile{position_params}}}
                                    return "movie_success"
                                on error
                                    -- 方法3: 使用剪贴板方法
                                    try
                                        tell application "Finder"
                                            select imageFile
                                            copy selection
                                        end tell
                                        
                                        delay 0.5
                                        paste
                                        
                                        return "clipboard_success"
                                    on error
                                        error "所有图片添加方法都失败"
                                    end try
                                end try
                            end try
                        end tell
                    end tell
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功在幻灯片 {slide_number} 添加图片 (方法: {result})"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加图片失败: {str(e)}"
            )] 