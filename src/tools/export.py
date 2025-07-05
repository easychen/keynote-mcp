"""
导出和截图工具
"""

from typing import Any, Dict, List, Optional
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number, validate_file_path, ParameterError


class ExportTools:
    """导出和截图工具类"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
    
    def get_tools(self) -> List[Tool]:
        """获取所有导出和截图工具"""
        return [
            Tool(
                name="screenshot_slide",
                description="截图单个幻灯片",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "output_path": {
                            "type": "string",
                            "description": "输出文件路径"
                        },
                        "format": {
                            "type": "string",
                            "description": "图片格式（png/jpg，默认png）"
                        }
                    },
                    "required": ["slide_number", "output_path"]
                }
            ),
            Tool(
                name="export_pdf",
                description="导出演示文稿为PDF",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "output_path": {
                            "type": "string",
                            "description": "输出文件路径"
                        }
                    },
                    "required": ["output_path"]
                }
            )
        ]
    
    async def screenshot_slide(self, slide_number: int, output_path: str, format: str = "png") -> List[TextContent]:
        """截图单个幻灯片"""
        try:
            validate_slide_number(slide_number)
            validate_file_path(output_path)
            
            # 设置导出格式
            export_format = "JPEG" if format.lower() in ["jpg", "jpeg"] else "PNG"
            
            # 从输出路径获取目录和文件名
            import os
            output_dir = os.path.dirname(output_path)
            output_filename = os.path.basename(output_path)
            
            # 创建临时导出文件夹
            temp_folder = os.path.join(output_dir, "temp_keynote_export")
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    activate
                    set targetDoc to front document
                    set docName to name of targetDoc
                    
                    -- 将所有幻灯片设为跳过，除了目标幻灯片
                    tell targetDoc
                        set skipped of every slide to true
                        set skipped of slide {slide_number} to false
                    end tell
                    
                    -- 创建临时导出文件夹
                    tell application "Finder"
                        if not (exists folder "{temp_folder}") then
                            make new folder at (POSIX file "{output_dir}") with properties {{name:"temp_keynote_export"}}
                        end if
                    end tell
                    
                    -- 导出幻灯片为图片到临时文件夹
                    set outputFolder to POSIX file "{temp_folder}"
                    export targetDoc as slide images to outputFolder with properties {{image format:{export_format}, skipped slides:false}}
                    
                    -- 恢复所有幻灯片
                    tell targetDoc
                        set skipped of every slide to false
                    end tell
                    
                    return "success"
                end tell
            ''')
            
            # 查找生成的文件并重命名为目标文件名
            import glob
            generated_files = glob.glob(os.path.join(temp_folder, f"*.{format.lower()}"))
            if generated_files:
                # 移动第一个文件到目标位置
                import shutil
                shutil.move(generated_files[0], output_path)
                
                # 清理临时文件夹
                shutil.rmtree(temp_folder, ignore_errors=True)
                
                return [TextContent(
                    type="text",
                    text=f"✅ 成功截图幻灯片 {slide_number} 到: {output_path}"
                )]
            else:
                return [TextContent(
                    type="text",
                    text=f"❌ 截图文件未生成"
                )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 截图幻灯片失败: {str(e)}"
            )]
    
    async def export_pdf(self, output_path: str) -> List[TextContent]:
        """导出演示文稿为PDF"""
        try:
            validate_file_path(output_path)
            
            result = self.runner.run_inline_script(f'''
                tell application "Keynote"
                    set targetDoc to front document
                    set outputFile to POSIX file "{output_path}"
                    
                    -- 导出为PDF
                    export targetDoc to outputFile as PDF
                    
                    return "success"
                end tell
            ''')
            
            return [TextContent(
                type="text",
                text=f"✅ 成功导出PDF到: {output_path}"
            )]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 导出PDF失败: {str(e)}"
            )] 