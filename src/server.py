#!/usr/bin/env python3
"""
Keynote-MCP Server
一个专为大模型设计的 MCP 服务器，通过 AppleScript 实现对 Keynote 的全面控制
"""

import asyncio
import json
import sys
from typing import Any, Sequence

from mcp.server import Server
from mcp.types import (
    CallToolRequest,
    ListToolsRequest,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)
from mcp.server.stdio import stdio_server

from .tools import PresentationTools, SlideTools, ContentTools, ExportTools, UnsplashTools
from .utils import KeynoteError, AppleScriptError, FileOperationError, ParameterError


class KeynoteMCPServer:
    """Keynote MCP 服务器"""
    
    def __init__(self):
        self.server = Server("keynote-mcp")
        self.presentation_tools = PresentationTools()
        self.slide_tools = SlideTools()
        self.content_tools = ContentTools()
        self.export_tools = ExportTools()
        try:
            self.unsplash_tools = UnsplashTools()
        except ParameterError as e:
            print(f"⚠️ Unsplash工具初始化失败: {e}")
            self.unsplash_tools = None
        
        # 注册处理器
        self._register_handlers()
    
    def _register_handlers(self):
        """注册 MCP 处理器"""
        
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """列出所有可用工具"""
            tools = []
            tools.extend(self.presentation_tools.get_tools())
            tools.extend(self.slide_tools.get_tools())
            tools.extend(self.content_tools.get_tools())
            tools.extend(self.export_tools.get_tools())
            if self.unsplash_tools:
                tools.extend(self.unsplash_tools.get_tools())
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """调用工具"""
            try:
                # 演示文稿管理工具
                if name == "create_presentation":
                    return await self.presentation_tools.create_presentation(
                        title=arguments["title"],
                        theme=arguments.get("theme", ""),
                        template=arguments.get("template", "")
                    )
                elif name == "open_presentation":
                    return await self.presentation_tools.open_presentation(
                        file_path=arguments["file_path"]
                    )
                elif name == "save_presentation":
                    return await self.presentation_tools.save_presentation(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "close_presentation":
                    return await self.presentation_tools.close_presentation(
                        doc_name=arguments.get("doc_name", ""),
                        should_save=arguments.get("should_save", True)
                    )
                elif name == "list_presentations":
                    return await self.presentation_tools.list_presentations()
                elif name == "set_presentation_theme":
                    return await self.presentation_tools.set_presentation_theme(
                        theme_name=arguments["theme_name"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_presentation_info":
                    return await self.presentation_tools.get_presentation_info(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_available_themes":
                    return await self.presentation_tools.get_available_themes()
                elif name == "get_presentation_resolution":
                    return await self.presentation_tools.get_presentation_resolution(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_slide_size":
                    return await self.presentation_tools.get_slide_size(
                        doc_name=arguments.get("doc_name", "")
                    )
                
                # 幻灯片操作工具
                elif name == "add_slide":
                    return await self.slide_tools.add_slide(
                        doc_name=arguments.get("doc_name", ""),
                        position=arguments.get("position", 0),
                        layout=arguments.get("layout", "")
                    )
                elif name == "delete_slide":
                    return await self.slide_tools.delete_slide(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "duplicate_slide":
                    return await self.slide_tools.duplicate_slide(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", ""),
                        new_position=arguments.get("new_position", 0)
                    )
                elif name == "move_slide":
                    return await self.slide_tools.move_slide(
                        from_position=arguments["from_position"],
                        to_position=arguments["to_position"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_slide_count":
                    return await self.slide_tools.get_slide_count(
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "select_slide":
                    return await self.slide_tools.select_slide(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "set_slide_layout":
                    return await self.slide_tools.set_slide_layout(
                        slide_number=arguments["slide_number"],
                        layout=arguments["layout"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_slide_info":
                    return await self.slide_tools.get_slide_info(
                        slide_number=arguments["slide_number"],
                        doc_name=arguments.get("doc_name", "")
                    )
                elif name == "get_available_layouts":
                    return await self.slide_tools.get_available_layouts(
                        doc_name=arguments.get("doc_name", "")
                    )
                
                # 内容管理工具
                elif name == "add_text_box":
                    return await self.content_tools.add_text_box(
                        slide_number=arguments["slide_number"],
                        text=arguments["text"],
                        x=arguments.get("x"),
                        y=arguments.get("y")
                    )
                elif name == "add_title":
                    return await self.content_tools.add_title(
                        slide_number=arguments["slide_number"],
                        title=arguments["title"],
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        font_size=arguments.get("font_size"),
                        font_name=arguments.get("font_name", "")
                    )
                elif name == "add_subtitle":
                    return await self.content_tools.add_subtitle(
                        slide_number=arguments["slide_number"],
                        subtitle=arguments["subtitle"],
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        font_size=arguments.get("font_size"),
                        font_name=arguments.get("font_name", "")
                    )
                elif name == "add_bullet_list":
                    return await self.content_tools.add_bullet_list(
                        slide_number=arguments["slide_number"],
                        items=arguments["items"],
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        font_size=arguments.get("font_size"),
                        font_name=arguments.get("font_name", "")
                    )
                elif name == "add_numbered_list":
                    return await self.content_tools.add_numbered_list(
                        slide_number=arguments["slide_number"],
                        items=arguments["items"],
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        font_size=arguments.get("font_size"),
                        font_name=arguments.get("font_name", "")
                    )
                elif name == "add_code_block":
                    return await self.content_tools.add_code_block(
                        slide_number=arguments["slide_number"],
                        code=arguments["code"],
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        font_size=arguments.get("font_size"),
                        font_name=arguments.get("font_name", "")
                    )
                elif name == "add_quote":
                    return await self.content_tools.add_quote(
                        slide_number=arguments["slide_number"],
                        quote=arguments["quote"],
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        font_size=arguments.get("font_size"),
                        font_name=arguments.get("font_name", "")
                    )
                elif name == "add_image":
                    return await self.content_tools.add_image(
                        slide_number=arguments["slide_number"],
                        image_path=arguments["image_path"],
                        x=arguments.get("x"),
                        y=arguments.get("y")
                    )
                
                # 导出和截图工具
                elif name == "screenshot_slide":
                    return await self.export_tools.screenshot_slide(
                        slide_number=arguments["slide_number"],
                        output_path=arguments["output_path"],
                        format=arguments.get("format", "png")
                    )
                elif name == "export_pdf":
                    return await self.export_tools.export_pdf(
                        output_path=arguments["output_path"]
                    )
                elif name == "export_images":
                    return await self.export_tools.export_images(
                        output_dir=arguments["output_dir"],
                        format=arguments.get("format", "png")
                    )
                
                # Unsplash配图工具
                elif name == "search_unsplash_images":
                    if not self.unsplash_tools:
                        return [TextContent(
                            type="text",
                            text="❌ Unsplash工具未初始化，请检查环境变量 UNSPLASH_KEY"
                        )]
                    return await self.unsplash_tools.search_unsplash_images(
                        query=arguments["query"],
                        per_page=arguments.get("per_page", 10),
                        orientation=arguments.get("orientation"),
                        order_by=arguments.get("order_by", "relevant")
                    )
                elif name == "add_unsplash_image_to_slide":
                    if not self.unsplash_tools:
                        return [TextContent(
                            type="text",
                            text="❌ Unsplash工具未初始化，请检查环境变量 UNSPLASH_KEY"
                        )]
                    return await self.unsplash_tools.add_unsplash_image_to_slide(
                        slide_number=arguments["slide_number"],
                        query=arguments["query"],
                        image_index=arguments.get("image_index", 0),
                        orientation=arguments.get("orientation"),
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        width=arguments.get("width"),
                        height=arguments.get("height")
                    )
                elif name == "get_random_unsplash_image":
                    if not self.unsplash_tools:
                        return [TextContent(
                            type="text",
                            text="❌ Unsplash工具未初始化，请检查环境变量 UNSPLASH_KEY"
                        )]
                    return await self.unsplash_tools.get_random_unsplash_image(
                        slide_number=arguments["slide_number"],
                        query=arguments.get("query"),
                        orientation=arguments.get("orientation"),
                        x=arguments.get("x"),
                        y=arguments.get("y"),
                        width=arguments.get("width"),
                        height=arguments.get("height")
                    )
                
                else:
                    return [TextContent(
                        type="text",
                        text=f"❌ 未知工具: {name}"
                    )]
                    
            except ParameterError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ 参数错误: {str(e)}"
                )]
            except AppleScriptError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ AppleScript 错误: {str(e)}"
                )]
            except FileOperationError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ 文件操作错误: {str(e)}"
                )]
            except KeynoteError as e:
                return [TextContent(
                    type="text",
                    text=f"❌ Keynote 错误: {str(e)}"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"❌ 未知错误: {str(e)}"
                )]
    
    async def run(self):
        """启动服务器"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """主函数"""
    server = KeynoteMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main()) 