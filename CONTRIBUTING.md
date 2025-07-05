# 贡献指南

感谢您对 Keynote-MCP 项目的关注！我们欢迎并感谢所有形式的贡献。

## 🎯 贡献方式

### 报告问题
- 使用 [GitHub Issues](https://github.com/easychen/keynote-mcp/issues) 报告 bug
- 提供尽可能详细的信息，包括：
  - 操作系统版本
  - Python 版本
  - Keynote 版本
  - 错误信息和步骤重现

### 提出功能请求
- 在 Issues 中使用 "Feature Request" 模板
- 详细描述您希望的功能
- 说明使用场景和价值

### 代码贡献
- Fork 本项目
- 创建功能分支 (`git checkout -b feature/AmazingFeature`)
- 提交更改 (`git commit -m 'Add some AmazingFeature'`)
- 推送到分支 (`git push origin feature/AmazingFeature`)
- 创建 Pull Request

## 🔧 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/easychen/keynote-mcp.git
cd keynote-mcp
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 开发依赖
```

### 4. 配置环境变量
```bash
cp env.example .env
# 编辑 .env 文件，设置必要的环境变量
```

### 5. 运行测试
```bash
pytest tests/
```

## 📝 编码规范

### Python 代码风格
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用 4 个空格缩进
- 行长度不超过 88 字符
- 使用有意义的变量名和函数名

### 代码格式化
我们使用以下工具进行代码格式化：
```bash
# 代码格式化
black .

# 导入排序
isort .

# 代码检查
flake8 .

# 类型检查
mypy src/
```

### 注释和文档
- 为所有公共函数和类添加文档字符串
- 使用中文编写注释和文档
- 复杂逻辑添加行内注释

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_presentation.py

# 运行带覆盖率的测试
pytest --cov=src tests/
```

### 编写测试
- 为新功能编写单元测试
- 测试文件放在 `tests/` 目录下
- 测试文件名以 `test_` 开头
- 使用 pytest 框架

## 📋 提交规范

### 提交信息格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 示例
```
feat(unsplash): 添加图片搜索功能

- 实现 Unsplash API 集成
- 支持关键词搜索
- 支持图片方向筛选

Closes #123
```

## 🔍 Pull Request 流程

### 提交前检查
- [ ] 代码通过所有测试
- [ ] 代码符合格式规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 提交信息符合规范

### PR 描述
请在 PR 中包含：
- 更改的简要描述
- 相关的 Issue 编号
- 测试说明
- 截图（如适用）

### 代码审查
- 所有 PR 都需要通过代码审查
- 至少需要一个维护者的批准
- 自动化测试必须通过

## 🏗️ 项目结构

```
keynote-mcp/
├── src/                    # 源代码
│   ├── server.py          # MCP 服务器
│   ├── tools/             # 工具模块
│   ├── applescript/       # AppleScript 脚本
│   └── utils/             # 工具函数
├── tests/                 # 测试文件
├── docs/                  # 文档
├── examples/              # 示例代码
└── scripts/               # 构建脚本
```

## 📚 开发资源

### 文档
- [MCP 协议文档](https://modelcontextprotocol.io/)
- [AppleScript 语言指南](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [Keynote 自动化指南](https://developer.apple.com/library/archive/documentation/LanguagesUtilities/Conceptual/MacAutomationScriptingGuide/)

### 工具
- [Visual Studio Code](https://code.visualstudio.com/) - 推荐的编辑器
- [Python 扩展](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [AppleScript 扩展](https://marketplace.visualstudio.com/items?itemName=idleberg.applescript)

## 🤝 社区准则

### 行为准则
- 尊重所有参与者
- 使用包容性语言
- 接受建设性批评
- 专注于对社区最有利的事情

### 沟通
- 使用 GitHub Issues 进行公开讨论
- 保持友善和专业的态度
- 及时回应评论和反馈

## 📞 联系方式

如有任何问题，请通过以下方式联系：

- 创建 [GitHub Issue](https://github.com/easychen/keynote-mcp/issues)
- 发送邮件至 [your-email@example.com](mailto:your-email@example.com)

## 🎉 致谢

感谢所有为 Keynote-MCP 项目做出贡献的开发者！

---

再次感谢您的贡献！每一个 PR、Issue 和建议都让这个项目变得更好。 