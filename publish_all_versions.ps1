#!/usr/bin/env pwsh

# 发布所有版本到PyPI的脚本
$versions = @("v1.0.0", "v1.0.1", "v1.1.0", "v1.1.1", "v1.1.2")
$apiToken = $env:PYPI_TOKEN

if (-not $apiToken) {
    Write-Host "错误: 未设置PYPI_TOKEN环境变量" -ForegroundColor Red
    exit 1
}

foreach ($version in $versions) {
    Write-Host "`n=== 发布版本: $version ===" -ForegroundColor Green
    
    # 创建临时目录
    $tempDir = Join-Path -Path "release_builds" -ChildPath $version
    if (Test-Path -Path $tempDir) {
        Remove-Item -Path $tempDir -Recurse -Force
    }
    New-Item -Path $tempDir -ItemType Directory | Out-Null
    
    # 检出标签代码
    Write-Host "检出标签代码..."
    git archive --format=tar $version | tar -x -C $tempDir
    
    # 进入临时目录
    Push-Location -Path $tempDir
    
    try {
        # 提取版本号（去掉v前缀）
        $versionNumber = $version.Substring(1)
        
        # 更新setup.py中的版本号
        Write-Host "更新版本号为: $versionNumber"
        $setupPyPath = Join-Path -Path $tempDir -ChildPath "setup.py"
        if (Test-Path -Path $setupPyPath) {
            $setupContent = Get-Content -Path $setupPyPath -Raw
            $setupContent = $setupContent -replace 'version="[^"]+"', "version=""$versionNumber"""
            Set-Content -Path $setupPyPath -Value $setupContent
        }
        
        # 更新pyproject.toml中的版本号
        $pyprojectPath = Join-Path -Path $tempDir -ChildPath "pyproject.toml"
        if (Test-Path -Path $pyprojectPath) {
            $pyprojectContent = Get-Content -Path $pyprojectPath -Raw
            $pyprojectContent = $pyprojectContent -replace 'version = "[^"]+"', "version = ""$versionNumber"""
            Set-Content -Path $pyprojectPath -Value $pyprojectContent
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
        # 回到原目录
        Pop-Location
    }
}

Write-Host "`n=== 所有版本发布完成 ===" -ForegroundColor Green