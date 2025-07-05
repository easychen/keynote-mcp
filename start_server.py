#!/usr/bin/env python3
"""
Keynote-MCP 服务器启动脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def select_language():
    """选择语言"""
    print("Please select your language / 请选择您的语言:")
    print("1. English")
    print("2. 中文")
    
    while True:
        try:
            choice = input("Enter your choice (1 or 2) / 请输入您的选择 (1 或 2): ").strip()
            if choice == "1":
                return "en"
            elif choice == "2":
                return "zh"
            else:
                print("Invalid choice. Please enter 1 or 2. / 无效选择，请输入 1 或 2。")
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye / 再见")
            sys.exit(0)

def get_messages(lang):
    """获取对应语言的消息"""
    if lang == "zh":
        return {
            "starting": "🚀 启动 Keynote-MCP 服务器...",
            "ensure_keynote": "📝 确保 Keynote 应用已安装",
            "ensure_permissions": "🔒 确保已授予必要的系统权限",
            "mcp_ready": "🔌 MCP 客户端可以连接到此服务器",
            "unsplash_enabled": "🖼️  Unsplash配图功能已启用",
            "unsplash_disabled": "⚠️  未检测到 UNSPLASH_KEY 环境变量",
            "unsplash_note1": "   Unsplash配图功能将不可用",
            "unsplash_note2": "   获取API密钥: https://unsplash.com/developers",
            "env_loaded": "📄 已加载环境变量文件",
            "env_not_found": "📄 未找到 .env 文件，使用系统环境变量",
            "dotenv_not_installed": "⚠️  python-dotenv 未安装，仅使用系统环境变量",
            "server_stopped": "\n👋 服务器已停止",
            "server_failed": "\n❌ 服务器启动失败"
        }
    else:  # English
        return {
            "starting": "🚀 Starting Keynote-MCP Server...",
            "ensure_keynote": "📝 Ensure Keynote application is installed",
            "ensure_permissions": "🔒 Ensure necessary system permissions are granted",
            "mcp_ready": "🔌 MCP clients can connect to this server",
            "unsplash_enabled": "🖼️  Unsplash image feature is enabled",
            "unsplash_disabled": "⚠️  UNSPLASH_KEY environment variable not detected",
            "unsplash_note1": "   Unsplash image feature will be unavailable",
            "unsplash_note2": "   Get API key: https://unsplash.com/developers",
            "env_loaded": "📄 Environment variables loaded from file",
            "env_not_found": "📄 .env file not found, using system environment variables",
            "dotenv_not_installed": "⚠️  python-dotenv not installed, using system environment variables only",
            "server_stopped": "\n👋 Server stopped",
            "server_failed": "\n❌ Server startup failed"
        }

# 选择语言
language = select_language()
messages = get_messages(language)

# 加载环境变量
try:
    from dotenv import load_dotenv
    # 优先加载 .env 文件
    env_path = project_root / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"{messages['env_loaded']}: {env_path}")
    else:
        print(messages['env_not_found'])
except ImportError:
    print(messages['dotenv_not_installed'])

# 导入并运行服务器
from src.server import main

if __name__ == "__main__":
    print(messages['starting'])
    print("=" * 50)
    print(messages['ensure_keynote'])
    print(messages['ensure_permissions'])
    print(messages['mcp_ready'])
    
    # 检查Unsplash配置
    if os.getenv('UNSPLASH_KEY'):
        print(messages['unsplash_enabled'])
    else:
        print(messages['unsplash_disabled'])
        print(messages['unsplash_note1'])
        print(messages['unsplash_note2'])
    
    print("=" * 50)
    
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print(messages['server_stopped'])
    except Exception as e:
        print(f"{messages['server_failed']}: {e}")
        sys.exit(1) 