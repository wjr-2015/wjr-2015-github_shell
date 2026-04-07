#!/bin/bash

# 发布版本到PyPI
VERSION=$1
API_TOKEN=$PYPI_TOKEN

if [ -z "$API_TOKEN" ]; then
    echo "错误: 未设置PYPI_TOKEN环境变量"
    exit 1
fi

echo "=== 发布版本: $VERSION ==="

# 提取版本号（去掉v前缀）
VERSION_NUMBER=${VERSION:1}
echo "版本号: $VERSION_NUMBER"

# 检出标签
git checkout $VERSION

# 更新版本号
sed -i "s/version=\"[^\"]*/version=\"$VERSION_NUMBER/" setup.py
sed -i "s/version = \"[^\"]*/version = \"$VERSION_NUMBER/" pyproject.toml

# 构建
python -m build

# 发布
python -m twine upload dist/* -u __token__ -p "$API_TOKEN"

# 切回main分支
git checkout main