# FARFETCH 爬虫 Makefile
# 常用命令管理

.PHONY: help install install-browser setup test quick full extract clean log restore-config

# 默认目标
.DEFAULT_GOAL := help

# 颜色定义
GREEN  := \033[0;32m
YELLOW := \033[0;33m
BLUE   := \033[0;34m
NC     := \033[0m # No Color

# 项目根目录
PROJECT_ROOT := $(shell pwd)

help: ## 显示帮助信息
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  FARFETCH 爬虫 - 常用命令$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "$(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## 安装 Python 依赖
	@echo "$(GREEN)📦 安装 Python 依赖...$(NC)"
	@pip3 install -r requirements.txt

install-browser: ## 安装 Playwright 浏览器
	@echo "$(GREEN)🎭 安装 Playwright 浏览器...$(NC)"
	@python3 -m playwright install chromium

setup: ## 初始化环境（安装依赖 + 安装浏览器）
	@echo "$(GREEN)🚀 初始化环境...$(NC)"
	@make install
	@make install-browser
	@echo "$(GREEN)✅ 环境初始化完成！$(NC)"

setup-config: ## 运行配置引导工具
	@echo "$(GREEN)⚙️  运行配置引导工具...$(NC)"
	@python3 setup_config.py

test: ## 运行验证测试
	@echo "$(GREEN)🔍 运行验证测试...$(NC)"
	@python3 test.py

quick: ## 快速测试（10个示例分类）
	@echo "$(GREEN)🚀 快速测试（10个示例分类）...$(NC)"
	@python3 -m playwright_crawler.batch_crawler data/服装分类_示例.csv

quick-shoes: ## 快速测试女鞋类目（3个示例分类）
	@echo "$(GREEN)🚀 快速测试女鞋类目...$(NC)"
	@head -4 data/女鞋类目.csv | tail -3 > /tmp/女鞋类目_示例.csv
	@python3 -m playwright_crawler.batch_crawler /tmp/女鞋类目_示例.csv

full: ## 完整爬取（88个分类）
	@echo "$(GREEN)🚀 完整爬取（88个分类）...$(NC)"
	@echo "$(YELLOW)⚠️  此操作可能需要 1-2 小时，请确保网络稳定$(NC)"
	@read -p "确认继续？[y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		python3 -m playwright_crawler.batch_crawler data/服装分类_完整版.csv; \
	else \
		echo "$(YELLOW)❌ 已取消$(NC)"; \
	fi

full-shoes: ## 完整爬取女鞋类目（26个分类）
	@echo "$(GREEN)🚀 完整爬取女鞋类目（26个分类）...$(NC)"
	@echo "$(YELLOW)⚠️  此操作可能需要 2-4 小时，请确保网络稳定$(NC)"
	@read -p "确认继续？[y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		python3 -m playwright_crawler.batch_crawler data/女鞋类目.csv; \
	else \
		echo "$(YELLOW)❌ 已取消$(NC)"; \
	fi

extract: ## 重新提取分类
	@echo "$(GREEN)📊 提取分类...$(NC)"
	@python3 -m playwright_crawler.extract_categories

test-timeout: ## 测试超时时间
	@echo "$(GREEN)🧪 超时时间测试工具...$(NC)"
	@python3 test_timeout.py

test-shoes-quick: ## 测试女鞋（3条）使用当前超时设置
	@echo "$(GREEN)🧪 测试女鞋类目（3条）...$(NC)"
	@python3 -m playwright_crawler.batch_crawler data/女鞋类目_测试3条.csv

interactive: ## 交互式菜单
	@echo "$(GREEN)🎮 启动交互式菜单...$(NC)"
	@python3 quick_start.py

log: ## 查看运行日志（实时）
	@echo "$(GREEN)📝 查看运行日志（按 Ctrl+C 退出）...$(NC)"
	@if [ -f output/batch_crawler.log ]; then \
		tail -f output/batch_crawler.log; \
	else \
		echo "$(YELLOW)⚠️  日志文件不存在，请先运行爬虫$(NC)"; \
	fi

log-last: ## 查看最后 50 行日志
	@echo "$(GREEN)📝 查看最后 50 行日志...$(NC)"
	@if [ -f output/batch_crawler.log ]; then \
		tail -n 50 output/batch_crawler.log; \
	else \
		echo "$(YELLOW)⚠️  日志文件不存在，请先运行爬虫$(NC)"; \
	fi

stats: ## 查看输出统计
	@echo "$(GREEN)📊 输出统计...$(NC)"
	@echo ""
	@if [ -d output ]; then \
		echo "输出目录大小："; \
		du -sh output 2>/dev/null || echo "  计算中..."; \
		echo ""; \
		echo "CSV 文件数量："; \
		find output -name "*.csv" 2>/dev/null | wc -l | awk '{print "  " $$1 " 个文件"}'; \
		echo ""; \
		echo "分类目录数量："; \
		find output -type d -mindepth 1 -maxdepth 1 2>/dev/null | wc -l | awk '{print "  " $$1 " 个分类"}'; \
		echo ""; \
		echo "各分类文件数："; \
		for dir in output/*/; do \
			if [ -d "$$dir" ]; then \
				count=$$(find "$$dir" -name "*.csv" 2>/dev/null | wc -l); \
				echo "  $$(basename "$$dir"): $$count 个文件"; \
			fi; \
		done; \
	else \
		echo "$(YELLOW)⚠️  输出目录不存在$(NC)"; \
	fi

clean-output: ## 清理输出文件（保留日志）
	@echo "$(YELLOW)⚠️  将删除所有爬取的数据文件（保留日志）$(NC)"
	@read -p "确认继续？[y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		find output -name "*.csv" -type f -delete 2>/dev/null; \
		find output -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} + 2>/dev/null; \
		echo "$(GREEN)✅ 输出文件已清理$(NC)"; \
	else \
		echo "$(YELLOW)❌ 已取消$(NC)"; \
	fi

clean-all: ## 清理所有输出（包括日志）
	@echo "$(YELLOW)⚠️  将删除所有输出文件和日志$(NC)"
	@read -p "确认继续？[y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf output/* 2>/dev/null; \
		rm -rf logs/* 2>/dev/null; \
		echo "$(GREEN)✅ 所有输出已清理$(NC)"; \
	else \
		echo "$(YELLOW)❌ 已取消$(NC)"; \
	fi

restore-config: ## 恢复配置文件备份
	@if [ -f playwright_crawler/config.py.backup ]; then \
		cp playwright_crawler/config.py.backup playwright_crawler/config.py; \
		echo "$(GREEN)✅ 配置文件已恢复$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  备份文件不存在$(NC)"; \
	fi

show-config: ## 显示当前配置
	@echo "$(GREEN)⚙️  当前配置：$(NC)"
	@echo ""
	@grep -E "^(HEADLESS|PAGE_LOAD_WAIT|SCROLL_COUNT|SCROLL_INTERVAL|BETWEEN_PAGES|BETWEEN_TASKS|TIMEOUT)" playwright_crawler/config.py | sed 's/^/  /'

check: ## 检查环境和依赖
	@echo "$(GREEN)🔍 检查环境...$(NC)"
	@echo ""
	@echo "Python 版本："
	@python3 --version | sed 's/^/  /'
	@echo ""
	@echo "Playwright 模块："
	@python3 -c "import playwright" 2>/dev/null && echo "  ✅ 已安装" || echo "  ❌ 未安装"
	@echo ""
	@echo "Chromium 浏览器："
	@python3 -m playwright install --dry-run chromium 2>&1 | grep -q "chromium" && echo "  ✅ 已安装" || echo "  ❌ 未安装"
	@echo ""
	@echo "数据文件："
	@[ -f data/服装分类_示例.csv ] && echo "  ✅ 示例文件存在" || echo "  ❌ 示例文件不存在"
	@[ -f data/服装分类_完整版.csv ] && echo "  ✅ 完整文件存在" || echo "  ❌ 完整文件不存在"
	@echo ""
	@echo "配置文件："
	@[ -f playwright_crawler/config.py ] && echo "  ✅ 配置文件存在" || echo "  ❌ 配置文件不存在"

docs: ## 查看文档
	@echo "$(GREEN)📚 可用文档：$(NC)"
	@echo ""
	@echo "$(YELLOW)README.md$(NC) - 完整使用文档"
	@echo "$(YELLOW)USAGE.md$(NC) - 快速使用指南"
	@echo "$(YELLOW)CONFIG_GUIDE.md$(NC) - 配置指南"
	@echo "$(YELLOW)DELIVERY.md$(NC) - 交付说明"
	@echo ""
	@echo "使用 'make <target> 查看文档'，例如："
	@echo "  make README.md (在终端查看)"
	@echo "  或直接打开文档文件"

update-browser: ## 更新 Playwright 浏览器
	@echo "$(GREEN)🔄 更新 Playwright 浏览器...$(NC)"
	@python3 -m playwright install --force chromium
	@echo "$(GREEN)✅ 浏览器更新完成$(NC)"

# 文档快捷方式
README.md:
	@cat README.md

USAGE.md:
	@cat USAGE.md

CONFIG_GUIDE.md:
	@cat CONFIG_GUIDE.md

DELIVERY.md:
	@cat DELIVERY.md
