"""
AppleScript execution utilities for Keynote-MCP
"""

import subprocess
import os
import json
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

from .error_handler import handle_applescript_error, AppleScriptError


class AppleScriptRunner:
    """AppleScript 执行器"""
    
    def __init__(self, script_dir: Optional[str] = None):
        """
        初始化 AppleScript 执行器
        
        Args:
            script_dir: AppleScript 脚本目录路径
        """
        if script_dir is None:
            # 默认脚本目录
            current_dir = Path(__file__).parent.parent
            script_dir = current_dir / "applescript"
        
        self.script_dir = Path(script_dir)
        self._ensure_script_dir()
    
    def _ensure_script_dir(self) -> None:
        """确保脚本目录存在"""
        if not self.script_dir.exists():
            self.script_dir.mkdir(parents=True, exist_ok=True)
    
    def run_script(self, script_name: str, function_name: str, *args) -> str:
        """
        运行 AppleScript 脚本中的指定函数
        
        Args:
            script_name: 脚本文件名（不含扩展名）
            function_name: 函数名
            *args: 函数参数
            
        Returns:
            脚本执行结果
            
        Raises:
            AppleScriptError: 脚本执行错误
        """
        script_path = self.script_dir / f"{script_name}.scpt"
        
        if not script_path.exists():
            raise AppleScriptError(f"Script file not found: {script_path}")
        
        # 构建 AppleScript 调用命令
        script_args = self._format_args(*args)
        applescript_code = f"""
        set scriptFile to "{script_path}"
        set scriptObj to load script POSIX file scriptFile
        tell scriptObj to {function_name}({script_args})
        """
        
        return self._execute_applescript(applescript_code)
    
    def run_inline_script(self, script_code: str) -> str:
        """
        运行内联 AppleScript 代码
        
        Args:
            script_code: AppleScript 代码
            
        Returns:
            脚本执行结果
        """
        return self._execute_applescript(script_code)
    
    def _execute_applescript(self, script_code: str) -> str:
        """
        执行 AppleScript 代码
        
        Args:
            script_code: AppleScript 代码
            
        Returns:
            执行结果
        """
        try:
            # 使用 osascript 执行 AppleScript
            result = subprocess.run(
                ["osascript", "-e", script_code],
                capture_output=True,
                text=True,
                timeout=30  # 30秒超时
            )
            
            if result.returncode != 0:
                handle_applescript_error(result.stderr)
            
            return result.stdout.strip()
            
        except subprocess.TimeoutExpired:
            raise AppleScriptError("AppleScript execution timed out")
        except subprocess.SubprocessError as e:
            raise AppleScriptError(f"Failed to execute AppleScript: {e}")
    
    def _format_args(self, *args) -> str:
        """
        格式化函数参数为 AppleScript 格式
        
        Args:
            *args: 参数列表
            
        Returns:
            格式化后的参数字符串
        """
        formatted_args = []
        
        for arg in args:
            if arg is None:
                formatted_args.append('""')
            elif isinstance(arg, bool):
                formatted_args.append("true" if arg else "false")
            elif isinstance(arg, (int, float)):
                formatted_args.append(str(arg))
            elif isinstance(arg, str):
                # 转义字符串中的引号
                escaped_arg = arg.replace('"', '\\"')
                formatted_args.append(f'"{escaped_arg}"')
            elif isinstance(arg, (list, tuple)):
                # 处理列表参数
                list_items = [self._format_single_arg(item) for item in arg]
                formatted_args.append(f"{{{', '.join(list_items)}}}")
            else:
                # 其他类型转为字符串
                formatted_args.append(f'"{str(arg)}"')
        
        return ", ".join(formatted_args)
    
    def _format_single_arg(self, arg: Any) -> str:
        """格式化单个参数"""
        if arg is None:
            return '""'
        elif isinstance(arg, bool):
            return "true" if arg else "false"
        elif isinstance(arg, (int, float)):
            return str(arg)
        elif isinstance(arg, str):
            escaped_arg = arg.replace('"', '\\"')
            return f'"{escaped_arg}"'
        else:
            return f'"{str(arg)}"'
    
    def check_keynote_running(self) -> bool:
        """检查 Keynote 是否正在运行"""
        script = '''
        tell application "System Events"
            return (name of processes) contains "Keynote"
        end tell
        '''
        
        try:
            result = self._execute_applescript(script)
            return result.lower() == "true"
        except AppleScriptError:
            return False
    
    def launch_keynote(self) -> None:
        """启动 Keynote 应用"""
        script = '''
        tell application "Keynote"
            activate
        end tell
        '''
        
        self._execute_applescript(script)
    
    def quit_keynote(self) -> None:
        """退出 Keynote 应用"""
        script = '''
        tell application "Keynote"
            quit
        end tell
        '''
        
        self._execute_applescript(script)
    
    def get_keynote_version(self) -> str:
        """获取 Keynote 版本"""
        script = '''
        tell application "Keynote"
            return version
        end tell
        '''
        
        return self._execute_applescript(script)
    
    def compile_script(self, script_source: str, output_path: str) -> None:
        """
        编译 AppleScript 源码为 .scpt 文件
        
        Args:
            script_source: AppleScript 源码
            output_path: 输出文件路径
        """
        try:
            # 使用 osacompile 编译脚本
            result = subprocess.run(
                ["osacompile", "-o", output_path],
                input=script_source,
                text=True,
                capture_output=True,
                timeout=10
            )
            
            if result.returncode != 0:
                raise AppleScriptError(f"Failed to compile script: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            raise AppleScriptError("Script compilation timed out")
        except subprocess.SubprocessError as e:
            raise AppleScriptError(f"Failed to compile script: {e}")
    
    def list_available_scripts(self) -> List[str]:
        """列出可用的脚本文件"""
        if not self.script_dir.exists():
            return []
        
        scripts = []
        for script_file in self.script_dir.glob("*.scpt"):
            scripts.append(script_file.stem)
        
        return sorted(scripts) 