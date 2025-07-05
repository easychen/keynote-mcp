# Keynote-MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

> ⚠️ **开发声明**: 本项目使用 Cursor AI 开发，代码未经人工审查，仅供学习和实验使用。请在生产环境中谨慎使用，建议先进行充分测试。

一个专为大模型设计的 MCP (Model Context Protocol) 服务器，通过 AppleScript 实现对 Keynote 演示文稿的全面控制。

## ✨ 主要特性

- 🎨 **完整的演示文稿管理** - 创建、打开、保存、关闭演示文稿
- 📊 **丰富的幻灯片操作** - 添加、删除、复制、移动幻灯片
- 📝 **强大的内容管理** - 文本、图片、形状、表格、图表
- 📸 **灵活的导出功能** - 截图、PDF、图片序列
- 🖼️ **Unsplash 配图集成** - 自动搜索和添加高质量图片
- 🔒 **安全可靠** - 完善的错误处理和权限管理
- 🧪 **完整测试** - 单元测试和集成测试覆盖

---

## 🚀 快速开始

### 系统要求

- macOS 10.14 或更高版本
- Keynote 应用程序
- Python 3.8 或更高版本

### 安装步骤

1. **克隆仓库**
   ```bash
   git clone https://github.com/easychen/keynote-mcp.git
   cd keynote-mcp
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置环境（可选，用于 Unsplash 功能）**
   ```bash
   cp env.example .env
   # 编辑 .env 文件，添加您的 Unsplash API 密钥
   ```

4. **设置 macOS 权限**
   - 进入 **系统偏好设置** > **安全性与隐私** > **隐私**
   - 将终端和 Python 添加到 **辅助功能** 权限
   - 将 Python 添加到 **自动化** 权限（用于 Keynote）

### 在 MCP 客户端中使用

#### Gemini CLI 配置

在您的 MCP 客户端中添加以下配置：

```json
{
  "KeynoteServer": {
    "command": "python",
    "args": ["start_server.py"],
    "env": {
      "UNSPLASH_KEY": "your_unsplash_api_key_here"
    },
    "cwd": "/path/to/keynote-mcp",
    "timeout": 5000
  }
}
```

#### Claude Desktop 配置

在您的 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "keynote": {
      "command": "python",
      "args": ["/path/to/keynote-mcp/start_server.py"],
      "env": {
        "UNSPLASH_KEY": "your_unsplash_api_key_here"
      }
    }
  }
}
```

#### 其他 MCP 客户端

对于其他兼容 MCP 的客户端，使用以下连接详情：
- **命令**: `python`
- **参数**: `["start_server.py"]`
- **工作目录**: `/path/to/keynote-mcp`
- **环境变量**: `{"UNSPLASH_KEY": "your_api_key"}` (可选)

---

## 📖 可用工具

服务器提供全面的 Keynote 自动化工具：

### 🎨 演示文稿管理
- 创建、打开、保存和关闭演示文稿
- 设置主题并获取演示文稿信息
- 列出所有打开的演示文稿

### 📊 幻灯片操作
- 添加、删除、复制和移动幻灯片
- 设置幻灯片布局并获取幻灯片信息
- 在幻灯片之间导航

### 📝 内容管理
- 添加文本框、标题和副标题
- 插入来自文件或 Unsplash 的图片
- 创建项目符号列表和编号列表
- 添加代码块和引用

### 📸 导出和截图
- 截取单个幻灯片的屏幕截图
- 将演示文稿导出为 PDF
- 导出为图片序列

### 🖼️ Unsplash 集成（可选）
- 搜索高质量图片
- 自动将图片添加到幻灯片
- 支持不同方向和样式

## 💡 使用示例

连接到您的 MCP 客户端后，您可以使用自然语言控制 Keynote：

- *"创建一个关于 AI 趋势的新演示文稿"*
- *"添加一个标题为'机器学习基础'的幻灯片"*
- *"在第 2 张幻灯片上插入一张关于技术的图片"*
- *"将演示文稿导出为 PDF"*

## 🔧 Unsplash 配置（可选）

要使用 Unsplash 图片功能：

1. **获取 API 密钥**: 访问 [Unsplash Developers](https://unsplash.com/developers)
2. **配置**: 将您的 API 密钥添加到 `.env` 文件：
   ```bash
   UNSPLASH_KEY=your_unsplash_access_key_here
   ```

## 📚 文档

- [安装指南](docs/installation.md) - 详细的设置说明
- [技术文档](TECH.md) - API 参考和架构
- [示例](examples/) - 使用示例和演示

## 🤝 贡献

我们欢迎各种形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何参与项目。

### 贡献步骤

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🏆 致谢

- [Model Context Protocol](https://modelcontextprotocol.io/) - 为大模型提供标准化的工具调用协议
- [Unsplash](https://unsplash.com/) - 提供高质量的免费图片
- [AppleScript](https://developer.apple.com/documentation/applescript) - 强大的 macOS 自动化工具

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 🐛 提交 Issue: [GitHub Issues](https://github.com/easychen/keynote-mcp/issues)
- 💬 讨论: [GitHub Discussions](https://github.com/easychen/keynote-mcp/discussions)

## ⭐ 支持项目

如果这个项目对您有帮助，请给我们一个 ⭐️！

---

*让 AI 助手能够轻松创建和管理 Keynote 演示文稿。* 