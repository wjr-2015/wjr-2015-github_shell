#!/usr/bin/env pwsh

# 发布所有版本到PyPI的PowerShell脚本

# 版本标签列表
$versions = @("v1.0.0", "v1.0.1", "v1.1.0", "v1.1.1", "v1.1.2")

# PyPI API令牌
$apiToken = $env:PYPI_TOKEN

if (-not $apiToken) {
    Write-Host "错误: 未设置PYPI_TOKEN环境变量" -ForegroundColor Red
    exit 1
}

# 主目录
$mainDir = Get-Location

foreach ($version in $versions) {
    Write-Host "`n=== 发布版本: $version ===" -ForegroundColor Green
    
    # 创建临时目录
    $tempDir = Join-Path -Path $mainDir -ChildPath "release_builds" | Join-Path -ChildPath $version
    if (Test-Path -Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force
    }
    New-Item -Path $tempDir -ItemType Directory | Out-Null
    
    # 进入临时目录
    Push-Location -Path $tempDir
    
    try {
        # 提取版本号（去掉v前缀）
        $versionNumber = $version.Substring(1)
        Write-Host "版本号: $versionNumber"
        
        # 检出标签代码到临时目录
        Write-Host "检出标签代码..."
        git -C $mainDir archive --format=tar $version | tar -x
        
        # 更新setup.py中的版本号
        Write-Host "更新setup.py版本号..."
        $setupPyPath = Join-Path -Path $tempDir -ChildPath "setup.py"
        if (Test-Path -Path $setupPyPath) {
            $setupContent = Get-Content -Path $setupPyPath -Raw
            $setupContent = $setupContent -replace 'version="[^"]+"', "version=""$versionNumber"""
            Set-Content -Path $setupPyPath -Value $setupContent -Encoding UTF8
        }
        
        # 更新pyproject.toml中的版本号
        Write-Host "更新pyproject.toml版本号..."
        $pyprojectPath = Join-Path -Path $tempDir -ChildPath "pyproject.toml"
        if (Test-Path -Path $pyprojectPath) {
            $pyprojectContent = Get-Content -Path $pyprojectPath -Raw
            $pyprojectContent = $pyprojectContent -replace 'version = "[^"]+"', "version = ""$versionNumber"""
            Set-Content -Path $pyprojectPath -Value $pyprojectContent -Encoding UTF8
        }
        
        # 构建项目
        Write-Host "构建项目..."
        python -m build
        
        # 发布到PyPI
        Write-Host "发布到PyPI..."
        python -m twine upload dist/* -u __token__ -p $apiToken
        
        Write-Host "`n✅ 版本 $version 发布成功!" -ForegroundColor Green
    }
    catch {
        Write-Host "`n❌ 版本 $version 发布失败: $_" -ForegroundColor Red
    }
    finally {
        # 回到主目录
        Pop-Location
    }
}

Write-Host "`n=== 所有版本发布完成 ===" -ForegroundColor Green