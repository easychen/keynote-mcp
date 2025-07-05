"""
Utility modules for Keynote-MCP
"""

from .applescript_runner import AppleScriptRunner
from .error_handler import (
    KeynoteError, 
    AppleScriptError, 
    FileOperationError, 
    ParameterError,
    validate_slide_number,
    validate_coordinates,
    validate_file_path
)

__all__ = [
    'AppleScriptRunner', 
    'KeynoteError', 
    'AppleScriptError', 
    'FileOperationError',
    'ParameterError',
    'validate_slide_number',
    'validate_coordinates', 
    'validate_file_path'
] 