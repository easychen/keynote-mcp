"""
Error handling utilities for Keynote-MCP
"""

import re
from typing import Optional


class KeynoteError(Exception):
    """Keynote 操作基础异常"""
    pass


class AppleScriptError(KeynoteError):
    """AppleScript 执行异常"""
    pass


class FileOperationError(KeynoteError):
    """文件操作异常"""
    pass


class ParameterError(KeynoteError):
    """参数验证异常"""
    pass


def handle_applescript_error(error_output: str) -> None:
    """处理 AppleScript 错误输出"""
    if not error_output:
        return
    
    error_output = error_output.strip()
    
    # Keynote 应用错误
    if "Keynote got an error" in error_output:
        raise AppleScriptError(f"Keynote error: {error_output}")
    
    # 对象不存在错误
    elif "Can't get" in error_output:
        raise AppleScriptError(f"Object not found: {error_output}")
    
    # 权限错误
    elif "not allowed" in error_output or "permission" in error_output.lower():
        raise AppleScriptError(f"Permission denied: {error_output}")
    
    # 文件操作错误
    elif "file" in error_output.lower() and ("not found" in error_output.lower() or "doesn't exist" in error_output.lower()):
        raise FileOperationError(f"File operation error: {error_output}")
    
    # 语法错误
    elif "syntax error" in error_output.lower():
        raise AppleScriptError(f"AppleScript syntax error: {error_output}")
    
    # 其他错误
    else:
        raise AppleScriptError(f"Unknown AppleScript error: {error_output}")


def validate_slide_number(slide_number: Optional[int], max_slides: Optional[int] = None) -> int:
    """验证幻灯片编号"""
    if slide_number is None:
        raise ParameterError("Slide number is required")
    
    if not isinstance(slide_number, int) or slide_number < 1:
        raise ParameterError(f"Invalid slide number: {slide_number}. Must be a positive integer.")
    
    if max_slides is not None and slide_number > max_slides:
        raise ParameterError(f"Slide number {slide_number} exceeds maximum slides {max_slides}")
    
    return slide_number


def validate_coordinates(x: Optional[float], y: Optional[float]) -> tuple[float, float]:
    """验证坐标值"""
    if x is not None and (not isinstance(x, (int, float)) or x < 0):
        raise ParameterError(f"Invalid x coordinate: {x}")
    
    if y is not None and (not isinstance(y, (int, float)) or y < 0):
        raise ParameterError(f"Invalid y coordinate: {y}")
    
    return float(x) if x is not None else 0.0, float(y) if y is not None else 0.0


def validate_file_path(file_path: str) -> str:
    """验证文件路径"""
    if not file_path or not isinstance(file_path, str):
        raise ParameterError("File path is required and must be a string")
    
    # 基本路径验证
    if not file_path.strip():
        raise ParameterError("File path cannot be empty")
    
    return file_path.strip() 