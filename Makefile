# Keynote-MCP Makefile

.PHONY: help install install-dev test lint format clean build upload docs

# 默认目标
help: ## 显示帮助信息
	@echo "Keynote-MCP 开发工具"
	@echo ""
	@echo "可用命令:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# 安装相关
install: ## 安装项目依赖
	pip install -r requirements.txt

install-dev: ## 安装开发依赖
	pip install -r requirements-dev.txt
	pip install -e .

install-all: install install-dev ## 安装所有依赖

# 代码质量
lint: ## 运行代码检查
	@echo "运行 flake8..."
	flake8 src/ tests/
	@echo "运行 mypy..."
	mypy src/
	@echo "运行 bandit..."
	bandit -r src/
	@echo "运行 safety..."
	safety check

format: ## 格式化代码
	@echo "运行 black..."
	black src/ tests/
	@echo "运行 isort..."
	isort src/ tests/

format-check: ## 检查代码格式
	@echo "检查 black..."
	black --check src/ tests/
	@echo "检查 isort..."
	isort --check-only src/ tests/

# 测试相关
test: ## 运行测试
	pytest tests/ -v

test-cov: ## 运行测试并生成覆盖率报告
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-unit: ## 运行单元测试
	pytest tests/ -v -m "unit"

test-integration: ## 运行集成测试
	pytest tests/ -v -m "integration"

# 构建和发布
clean: ## 清理构建文件
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## 构建包
	python -m build

upload-test: build ## 上传到测试 PyPI
	twine upload --repository testpypi dist/*

upload: build ## 上传到 PyPI
	twine upload dist/*

# 文档相关
docs: ## 生成文档
	@if [ -d "docs" ]; then \
		cd docs && make html; \
	else \
		echo "docs 目录不存在"; \
	fi

docs-serve: docs ## 启动文档服务器
	@if [ -d "docs/_build/html" ]; then \
		cd docs/_build/html && python -m http.server 8000; \
	else \
		echo "请先运行 make docs"; \
	fi

# 开发相关
dev-setup: ## 设置开发环境
	python -m venv venv
	@echo "请运行: source venv/bin/activate"
	@echo "然后运行: make install-all"

server: ## 启动 MCP 服务器
	python start_server.py

demo: ## 运行演示
	python examples/basic_usage.py

# 检查相关
check-all: format-check lint test ## 运行所有检查

pre-commit: format lint test ## 提交前检查

# 版本相关
version: ## 显示版本信息
	@python -c "import src; print(f'Version: {src.__version__}')"

# 环境相关
env-check: ## 检查环境配置
	@echo "Python 版本:"
	@python --version
	@echo "虚拟环境:"
	@which python
	@echo "已安装包:"
	@pip list | grep -E "(keynote|mcp|aiohttp|pytest)"

# Git 相关
git-clean: ## 清理 Git 仓库
	git clean -fd
	git reset --hard HEAD

# 帮助信息
info: ## 显示项目信息
	@echo "项目: Keynote-MCP"
	@echo "描述: 一个专为大模型设计的 MCP 套件"
	@echo "版本: $(shell python -c 'import src; print(src.__version__)')"
	@echo "Python: $(shell python --version)"
	@echo "路径: $(shell pwd)" 