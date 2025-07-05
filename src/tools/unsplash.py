"""
Unsplash配图工具
"""

import os
import tempfile
from typing import Any, Dict, List, Optional
import aiohttp
import aiofiles
from pathlib import Path
from mcp.types import Tool, TextContent
from ..utils import AppleScriptRunner, validate_slide_number, ParameterError


class UnsplashTools:
    """Unsplash配图工具类"""
    
    def __init__(self):
        self.runner = AppleScriptRunner()
        
        # 尝试加载 .env 文件
        self._load_env_if_needed()
        
        self.api_key = os.getenv('UNSPLASH_KEY')
        if not self.api_key:
            raise ParameterError("环境变量 UNSPLASH_KEY 未设置，请检查 .env 文件或系统环境变量")
        
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            "Authorization": f"Client-ID {self.api_key}",
            "Accept-Version": "v1"
        }
    
    def _load_env_if_needed(self):
        """如果需要，加载 .env 文件"""
        try:
            from dotenv import load_dotenv
            
            # 查找项目根目录的 .env 文件
            current_dir = Path(__file__).parent
            while current_dir != current_dir.parent:
                env_path = current_dir / '.env'
                if env_path.exists():
                    load_dotenv(env_path)
                    break
                current_dir = current_dir.parent
        except ImportError:
            # python-dotenv 未安装，忽略
            pass
    
    def get_tools(self) -> List[Tool]:
        """获取所有Unsplash配图工具"""
        return [
            Tool(
                name="search_unsplash_images",
                description="搜索Unsplash图片",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "per_page": {
                            "type": "integer",
                            "description": "每页图片数量（1-30，默认10）",
                            "minimum": 1,
                            "maximum": 30
                        },
                        "orientation": {
                            "type": "string",
                            "description": "图片方向（landscape/portrait/squarish）",
                            "enum": ["landscape", "portrait", "squarish"]
                        },
                        "order_by": {
                            "type": "string",
                            "description": "排序方式（relevant/latest/popular）",
                            "enum": ["relevant", "latest", "popular"]
                        }
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="add_unsplash_image_to_slide",
                description="搜索Unsplash图片并添加到幻灯片",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "query": {
                            "type": "string",
                            "description": "搜索关键词"
                        },
                        "image_index": {
                            "type": "integer",
                            "description": "选择第几张图片（0-9，默认0）",
                            "minimum": 0,
                            "maximum": 9
                        },
                        "orientation": {
                            "type": "string",
                            "description": "图片方向（landscape/portrait/squarish）",
                            "enum": ["landscape", "portrait", "squarish"]
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（可选）"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（可选）"
                        },
                        "width": {
                            "type": "number",
                            "description": "图片宽度（可选）"
                        },
                        "height": {
                            "type": "number",
                            "description": "图片高度（可选）"
                        }
                    },
                    "required": ["slide_number", "query"]
                }
            ),
            Tool(
                name="get_random_unsplash_image",
                description="获取随机Unsplash图片并添加到幻灯片",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "slide_number": {
                            "type": "integer",
                            "description": "幻灯片编号"
                        },
                        "query": {
                            "type": "string",
                            "description": "搜索关键词（可选）"
                        },
                        "orientation": {
                            "type": "string",
                            "description": "图片方向（landscape/portrait/squarish）",
                            "enum": ["landscape", "portrait", "squarish"]
                        },
                        "x": {
                            "type": "number",
                            "description": "X坐标（可选）"
                        },
                        "y": {
                            "type": "number",
                            "description": "Y坐标（可选）"
                        },
                        "width": {
                            "type": "number",
                            "description": "图片宽度（可选）"
                        },
                        "height": {
                            "type": "number",
                            "description": "图片高度（可选）"
                        }
                    },
                    "required": ["slide_number"]
                }
            )
        ]
    
    async def search_unsplash_images(self, query: str, per_page: int = 10, orientation: Optional[str] = None, order_by: str = "relevant") -> List[TextContent]:
        """搜索Unsplash图片"""
        try:
            params = {
                "query": query,
                "per_page": min(per_page, 30),
                "order_by": order_by
            }
            
            if orientation:
                params["orientation"] = orientation
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/search/photos",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return [TextContent(
                            type="text",
                            text=f"❌ Unsplash API错误 ({response.status}): {error_text}"
                        )]
                    
                    data = await response.json()
                    photos = data.get("results", [])
                    
                    if not photos:
                        return [TextContent(
                            type="text",
                            text=f"❌ 没有找到关键词 '{query}' 的图片"
                        )]
                    
                    # 格式化搜索结果
                    result_text = f"🔍 找到 {len(photos)} 张图片（关键词：{query}）:\n\n"
                    
                    for i, photo in enumerate(photos):
                        photographer = photo.get("user", {}).get("name", "Unknown")
                        description = photo.get("description") or photo.get("alt_description") or "无描述"
                        width = photo.get("width", 0)
                        height = photo.get("height", 0)
                        likes = photo.get("likes", 0)
                        
                        result_text += f"[{i}] 📸 {description[:50]}{'...' if len(description) > 50 else ''}\n"
                        result_text += f"    👤 摄影师: {photographer}\n"
                        result_text += f"    📐 尺寸: {width}x{height}\n"
                        result_text += f"    ❤️ 点赞: {likes}\n"
                        result_text += f"    🔗 链接: {photo.get('links', {}).get('html', '')}\n\n"
                    
                    return [TextContent(
                        type="text",
                        text=result_text
                    )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 搜索图片失败: {str(e)}"
            )]
    
    async def add_unsplash_image_to_slide(self, slide_number: int, query: str, image_index: int = 0, 
                                        orientation: Optional[str] = None, x: Optional[float] = None, 
                                        y: Optional[float] = None, width: Optional[float] = None, 
                                        height: Optional[float] = None) -> List[TextContent]:
        """搜索Unsplash图片并添加到幻灯片"""
        try:
            validate_slide_number(slide_number)
            
            # 搜索图片
            params = {
                "query": query,
                "per_page": max(image_index + 1, 10),
                "order_by": "relevant"
            }
            
            if orientation:
                params["orientation"] = orientation
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/search/photos",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return [TextContent(
                            type="text",
                            text=f"❌ Unsplash API错误 ({response.status}): {error_text}"
                        )]
                    
                    data = await response.json()
                    photos = data.get("results", [])
                    
                    if not photos:
                        return [TextContent(
                            type="text",
                            text=f"❌ 没有找到关键词 '{query}' 的图片"
                        )]
                    
                    if image_index >= len(photos):
                        return [TextContent(
                            type="text",
                            text=f"❌ 图片索引 {image_index} 超出范围，共找到 {len(photos)} 张图片"
                        )]
                    
                    # 选择指定索引的图片
                    selected_photo = photos[image_index]
                    
                    # 获取图片信息
                    photographer = selected_photo.get("user", {}).get("name", "Unknown")
                    description = selected_photo.get("description") or selected_photo.get("alt_description") or "无描述"
                    
                    # 选择合适的图片尺寸（优先使用regular尺寸）
                    image_url = selected_photo.get("urls", {}).get("regular")
                    if not image_url:
                        image_url = selected_photo.get("urls", {}).get("full")
                    
                    if not image_url:
                        return [TextContent(
                            type="text",
                            text="❌ 无法获取图片下载链接"
                        )]
                    
                    # 下载图片
                    temp_dir = tempfile.gettempdir()
                    image_filename = f"unsplash_{selected_photo.get('id', 'unknown')}.jpg"
                    image_path = os.path.join(temp_dir, image_filename)
                    
                    async with session.get(image_url) as img_response:
                        if img_response.status != 200:
                            return [TextContent(
                                type="text",
                                text=f"❌ 下载图片失败: HTTP {img_response.status}"
                            )]
                        
                        async with aiofiles.open(image_path, 'wb') as f:
                            async for chunk in img_response.content.iter_chunked(8192):
                                await f.write(chunk)
                    
                    # 添加图片到幻灯片
                    await self._add_image_to_slide(slide_number, image_path, x, y, width, height)
                    
                    # 记录下载统计（按照Unsplash API要求）
                    download_url = selected_photo.get("links", {}).get("download_location")
                    if download_url:
                        try:
                            async with session.get(download_url, headers=self.headers) as _:
                                pass  # 只需要触发下载统计
                        except:
                            pass  # 忽略统计错误
                    
                    return [TextContent(
                        type="text",
                        text=f"✅ 成功添加图片到幻灯片 {slide_number}\n"
                             f"📸 图片: {description[:50]}{'...' if len(description) > 50 else ''}\n"
                             f"👤 摄影师: {photographer}\n"
                             f"📁 临时文件: {image_path}"
                    )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 添加图片失败: {str(e)}"
            )]
    
    async def get_random_unsplash_image(self, slide_number: int, query: Optional[str] = None, 
                                      orientation: Optional[str] = None, x: Optional[float] = None, 
                                      y: Optional[float] = None, width: Optional[float] = None, 
                                      height: Optional[float] = None) -> List[TextContent]:
        """获取随机Unsplash图片并添加到幻灯片"""
        try:
            validate_slide_number(slide_number)
            
            params = {}
            if query:
                params["query"] = query
            if orientation:
                params["orientation"] = orientation
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/photos/random",
                    headers=self.headers,
                    params=params
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        return [TextContent(
                            type="text",
                            text=f"❌ Unsplash API错误 ({response.status}): {error_text}"
                        )]
                    
                    photo = await response.json()
                    
                    # 获取图片信息
                    photographer = photo.get("user", {}).get("name", "Unknown")
                    description = photo.get("description") or photo.get("alt_description") or "无描述"
                    
                    # 选择合适的图片尺寸
                    image_url = photo.get("urls", {}).get("regular")
                    if not image_url:
                        image_url = photo.get("urls", {}).get("full")
                    
                    if not image_url:
                        return [TextContent(
                            type="text",
                            text="❌ 无法获取图片下载链接"
                        )]
                    
                    # 下载图片
                    temp_dir = tempfile.gettempdir()
                    image_filename = f"unsplash_random_{photo.get('id', 'unknown')}.jpg"
                    image_path = os.path.join(temp_dir, image_filename)
                    
                    async with session.get(image_url) as img_response:
                        if img_response.status != 200:
                            return [TextContent(
                                type="text",
                                text=f"❌ 下载图片失败: HTTP {img_response.status}"
                            )]
                        
                        async with aiofiles.open(image_path, 'wb') as f:
                            async for chunk in img_response.content.iter_chunked(8192):
                                await f.write(chunk)
                    
                    # 添加图片到幻灯片
                    await self._add_image_to_slide(slide_number, image_path, x, y, width, height)
                    
                    # 记录下载统计
                    download_url = photo.get("links", {}).get("download_location")
                    if download_url:
                        try:
                            async with session.get(download_url, headers=self.headers) as _:
                                pass
                        except:
                            pass
                    
                    return [TextContent(
                        type="text",
                        text=f"✅ 成功添加随机图片到幻灯片 {slide_number}\n"
                             f"📸 图片: {description[:50]}{'...' if len(description) > 50 else ''}\n"
                             f"👤 摄影师: {photographer}\n"
                             f"📁 临时文件: {image_path}"
                    )]
                    
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ 获取随机图片失败: {str(e)}"
            )]
    
    async def _add_image_to_slide(self, slide_number: int, image_path: str, x: Optional[int] = None, y: Optional[int] = None, width: Optional[int] = None, height: Optional[int] = None) -> None:
        """添加图片到指定幻灯片"""
        try:
            # 转换为绝对路径
            abs_path = os.path.abspath(image_path)
            
            # 构建位置参数
            position_params = ""
            if x is not None and y is not None:
                position_params = f", position:{{{x}, {y}}}"
            
            # 使用修正后的AppleScript语法（基于独立脚本中成功的实现）
            script = f'''
            tell application "Keynote"
                activate
                set targetDoc to front document
                
                tell targetDoc
                    tell slide {slide_number}
                        -- 使用修正后的语法
                        set imageFile to POSIX file "{abs_path}" as alias
                        
                        -- 方法1: 尝试标准image对象
                        try
                            set newImage to make new image with properties {{file:imageFile{position_params}}}
                            return "image_success"
                        on error
                            -- 方法2: 尝试movie对象
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
            '''
            
            # 执行AppleScript
            result = self.runner.run_inline_script(script)
            
        except Exception as e:
            error_msg = f"添加图片到幻灯片失败: {e}"
            raise Exception(error_msg) 