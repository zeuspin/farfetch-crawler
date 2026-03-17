# FARFETCH 爬虫功能清单

## 核心功能

### 1. 分类提取
自动提取 FARFETCH 分类并生成任务文件。

**使用方法：**
```bash
make extract
```

**输出：** `output/服装分类_所有二级类目.csv`

---

### 2. 批量爬取
根据 CSV 文件批量爬取商品数据。

**使用方法：**
```bash
# 服装类目
make quick          # 快速测试（10个示例）
make full           # 完整爬取（88个分类）

# 女鞋类目
make quick-shoes    # 快速测试（3个示例）
make full-shoes     # 完整爬取（26个分类）

# 自定义
python3 -m playwright_crawler.batch_crawler your_file.csv
```

**特性：**
- ✅ 断点续传
- ✅ 智能反爬
- ✅ 详细日志

---

### 3. 断点续传
自动跳过已爬取的页面，支持中断后继续。

**说明：**
- 无需额外配置
- 自动生效
- 基于文件是否存在判断

---

## 配置管理

### 4. 交互式配置
智能推荐配置参数。

**使用方法：**
```bash
make setup-config
```

**配置选项：**
- 使用场景
- 浏览器模式（有头/无头）
- 网络环境
- 懒加载策略
- 自定义参数

---

### 5. 配置查看
显示当前配置参数。

**使用方法：**
```bash
make show-config
```

---

## 测试工具

### 6. 环境验证
验证环境和依赖是否正常。

**使用方法：**
```bash
make test
```

**检查内容：**
- Python 版本
- Playwright 模块
- Chromium 浏览器
- 数据文件
- 配置文件

---

### 7. 超时测试
测试不同的超时时间，找出最优值。

**使用方法：**
```bash
make test-timeout
```

**测试选项：**
- 60秒 - 快速
- 90秒 - 推荐
- 120秒 - 默认
- 180秒 - 保守
- 240秒 - 极保守
- 自定义值

---

## 日志和统计

### 8. 日志监控
实时查看和监控运行日志。

**使用方法：**
```bash
make log          # 实时查看（Ctrl+C 退出）
make log-last     # 查看最后 50 行
```

---

### 9. 输出统计
查看输出目录的统计信息。

**使用方法：**
```bash
make stats
```

**统计内容：**
- 输出目录大小
- CSV 文件数量
- 分类目录数量
- 各分类文件数

---

## 工具脚本

### 10. 交互式菜单
提供友好的交互式菜单界面。

**使用方法：**
```bash
make interactive
```

---

### 11. 清理工具
清理输出文件和日志。

**使用方法：**
```bash
make clean-output   # 清理输出文件（保留日志）
make clean-all      # 清理所有输出
```

---

## 环境管理

### 12. 环境初始化
一键安装和配置环境。

**使用方法：**
```bash
make setup         # 初始化环境
make install       # 安装依赖
make install-browser  # 安装浏览器
make check         # 检查环境
```

---

### 13. 配置恢复
恢复配置文件备份。

**使用方法：**
```bash
make restore-config
```

---

## 快速参考

### Makefile 命令速查

| 命令 | 说明 |
|------|------|
| `make help` | 查看所有命令 |
| `make setup` | 初始化环境 |
| `make test` | 验证环境 |
| `make quick` | 快速测试服装 |
| `make full` | 完整爬取服装 |
| `make quick-shoes` | 快速测试女鞋 |
| `make full-shoes` | 完整爬取女鞋 |
| `make extract` | 提取分类 |
| `make log` | 查看日志 |
| `make stats` | 查看统计 |
| `make clean-output` | 清理输出 |
| `make show-config` | 查看配置 |

---

## 详细文档

- [README.md](README.md) - 完整使用文档
- [USAGE.md](USAGE.md) - 快速使用指南
- [CONFIG_GUIDE.md](CONFIG_GUIDE.md) - 配置指南
- [SHOES_GUIDE.md](SHOES_GUIDE.md) - 女鞋类目使用指南
- [MAKEFILE_GUIDE.md](MAKEFILE_GUIDE.md) - Makefile 使用指南
- [TIMEOUT_TEST_REPORT.md](TIMEOUT_TEST_REPORT.md) - 超时测试报告

---

**版本:** 2.0  
**最后更新:** 2026-03-17
