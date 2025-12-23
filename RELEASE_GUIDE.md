# GitHub Simulation Shell 发布指南

## 发布工具

本项目包含以下发布工具：

1. `release.py` - 版本管理和GitHub发布脚本
2. `.github/workflows/release.yml` - GitHub Actions自动化发布工作流

## 使用方法

### 1. 使用发布脚本 (`release.py`)

**功能**：
- 版本号管理
- 更新版本文件
- 自动提交更改
- 推送到GitHub
- 创建Git标签

**使用步骤**：

```bash
# 1. 确保Git工作树干净
# 2. 运行发布脚本
python release.py

# 3. 按照提示输入新版本号和发布说明
```

**示例**：
```
GitHub Simulation Shell 发布工具
==================================================
当前版本: 1.0.0
输入新版本号 (默认: 1.0.0): 1.1.0
✅ 版本已更新为 1.1.0
请输入发布说明 (Ctrl+D结束输入):
本次更新添加了以下功能：
- 新增命令测试功能
- 支持中英文切换
- 修复语言全局语言问题
- 增加账号、邮箱输入功能
- 增加令牌自动连接功能
✅ 代码已推送到GitHub
✅ 已创建标签 v1.1.0

==================================================
🎉 发布成功！
版本: 1.1.0
发布说明:
本次更新添加了以下功能：
- 新增命令测试功能
- 支持中英文切换
- 修复语言全局语言问题
- 增加账号、邮箱输入功能
- 增加令牌自动连接功能
==================================================
```

### 2. GitHub Actions 自动发布

**功能**：
- 当推送带有 `v*` 前缀的标签时自动触发
- 构建Python包
- 运行测试
- 发布到PyPI
- 创建GitHub Release

**使用步骤**：

```bash
# 1. 使用release.py脚本或手动创建标签
python release.py

# 或手动创建标签
git tag -a v1.1.0 -m "Release version 1.1.0"
git push origin v1.1.0
```

**注意事项**：
- 需在GitHub仓库设置中添加 `PYPI_USERNAME` 和 `PYPI_PASSWORD` 密钥
- 确保 `.github/workflows/release.yml` 文件存在

## 发布流程

### 完整发布流程

1. **更新代码**：完成所有功能开发和测试
2. **运行测试**：确保所有测试通过
   ```bash
   python -m pytest github_shell/tests/ -v
   ```
3. **使用发布脚本**：运行 `release.py` 脚本
4. **验证发布**：
   - 检查GitHub仓库是否有新标签
   - 检查GitHub Releases是否有新发布
   - 检查PyPI是否有新版本

### 手动发布到PyPI

如果需要手动发布到PyPI，可以使用以下命令：

```bash
# 1. 安装必要工具
pip install setuptools wheel twine

# 2. 构建包
python setup.py sdist bdist_wheel

# 3. 发布到PyPI
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```

## 版本号规则

项目使用语义化版本号（Semantic Versioning）：

- **主版本号**：重大变化，不兼容的API更改
- **次版本号**：新功能，向下兼容
- **修订号**：bug修复，向下兼容

示例：
- `1.0.0` - 初始版本
- `1.1.0` - 添加新功能
- `1.1.1` - 修复bug
- `2.0.0` - 重大更改

## 注意事项

1. **确保代码质量**：发布前运行所有测试
2. **更新文档**：确保README.md和其他文档是最新的
3. **检查依赖**：确保setup.py中的依赖正确
4. **更新版本号**：确保版本号符合语义化版本规则
5. **添加发布说明**：清晰描述本次发布的更改内容

## 故障排除

### 发布脚本失败

- **Git工作树不干净**：先提交或撤销所有更改
- **无法推送到GitHub**：检查Git远程配置和权限
- **标签已存在**：使用新的版本号

### GitHub Actions失败

- **测试失败**：修复测试失败的问题
- **PyPI认证失败**：检查PyPI密钥是否正确
- **构建失败**：检查setup.py和项目结构

## 联系信息

如果遇到问题，请联系项目维护者：
- 邮箱：wangjinrui_150328@126.com
- GitHub：https://github.com/wjr-2015
