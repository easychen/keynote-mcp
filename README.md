# Keynote-MCP

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![macOS](https://img.shields.io/badge/platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)

> ⚠️ **Development Notice**: This project was developed using Cursor AI without human code review. It's provided for educational and experimental purposes only. Please use with caution in production environments and conduct thorough testing before deployment.

A Model Context Protocol (MCP) server that enables AI assistants to control Keynote presentations through AppleScript automation.

**[中文文档](README_zh.md)** | **[English](README.md)**

## ✨ Features

- 🎨 **Complete Presentation Management** - Create, open, save, and close presentations
- 📊 **Rich Slide Operations** - Add, delete, duplicate, and move slides
- 📝 **Powerful Content Management** - Add text, images, shapes, tables, and charts
- 📸 **Flexible Export Options** - Screenshot slides, export to PDF and images
- 🖼️ **Unsplash Integration** - Automatically search and add high-quality images
- 🔒 **Secure & Reliable** - Comprehensive error handling and permission management
- 🧪 **Well Tested** - Unit and integration test coverage

---

## 🚀 Quick Start

### Prerequisites

- macOS 10.14 or later
- Keynote application
- Python 3.8 or later

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/easychen/keynote-mcp.git
   cd keynote-mcp
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment (optional for Unsplash features)**
   ```bash
   cp env.example .env
   # Edit .env file and add your Unsplash API key
   ```

4. **Set up macOS permissions**
   - Go to **System Preferences** > **Security & Privacy** > **Privacy**
   - Add Terminal and Python to **Accessibility** permissions
   - Add Python to **Automation** permissions for Keynote

### Usage with MCP Clients

#### Gemini CLI Configuration

Add this configuration to your MCP client:

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

#### Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

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

#### Other MCP Clients

For other MCP-compatible clients, use these connection details:
- **Command**: `python`
- **Args**: `["start_server.py"]`
- **Working Directory**: `/path/to/keynote-mcp`
- **Environment**: `{"UNSPLASH_KEY": "your_api_key"}` (optional)

## 📖 Available Tools

The server provides comprehensive tools for Keynote automation:

### 🎨 Presentation Management
- Create, open, save, and close presentations
- Set themes and get presentation information
- List all open presentations

### 📊 Slide Operations  
- Add, delete, duplicate, and move slides
- Set slide layouts and get slide information
- Navigate between slides

### 📝 Content Management
- Add text boxes, titles, and subtitles
- Insert images from files or Unsplash
- Create bullet lists and numbered lists
- Add code blocks and quotes

### 📸 Export & Screenshot
- Take screenshots of individual slides
- Export presentations to PDF
- Export as image sequences

### 🖼️ Unsplash Integration (Optional)
- Search high-quality images
- Automatically add images to slides
- Support for different orientations and styles

## 💡 Usage Examples

Once connected to your MCP client, you can use natural language to control Keynote:

- *"Create a new presentation about AI trends"*
- *"Add a slide with the title 'Machine Learning Basics'"*
- *"Insert an image about technology on slide 2"*
- *"Export the presentation as PDF"*

## 🔧 Unsplash Configuration (Optional)

To use Unsplash image features:

1. **Get API Key**: Visit [Unsplash Developers](https://unsplash.com/developers)
2. **Configure**: Add your API key to the `.env` file:
   ```bash
   UNSPLASH_KEY=your_unsplash_access_key_here
   ```

## 📚 Documentation

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [Technical Documentation](TECH.md) - API reference and architecture
- [Examples](examples/) - Usage examples and demos

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) - Standardized tool calling protocol for AI models
- [Unsplash](https://unsplash.com/) - High-quality free images
- [AppleScript](https://developer.apple.com/documentation/applescript) - Powerful macOS automation

## 📞 Contact

- 🐛 Issues: [GitHub Issues](https://github.com/easychen/keynote-mcp/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/easychen/keynote-mcp/discussions)

## ⭐ Support

If this project helps you, please give it a ⭐️!

---

*Empowering AI assistants to create and manage Keynote presentations effortlessly.*
