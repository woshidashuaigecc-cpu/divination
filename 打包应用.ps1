# 占卜起卦 - PowerShell 打包脚本
# 简化手机应用的编译和安装过程

function Show-Menu {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "   占卜起卦 - 手机应用编译工具"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "选择编译选项:"
    Write-Host "1. 检查打包环境"
    Write-Host "2. 编译调试版本 (APK)"
    Write-Host "3. 编译发布版本 (APK)"
    Write-Host "4. 安装到手机 (USB)"
    Write-Host "5. 清除编译文件并重新编译"
    Write-Host "6. 打开编译输出目录"
    Write-Host "0. 退出"
    Write-Host ""
}

function Check-Environment {
    Write-Host "检查必要的工具..."
    Write-Host ""
    
    # 检查 Python
    $pythonCheck = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python: 已安装 ($pythonCheck)"
    } else {
        Write-Host "✗ Python: 未找到，请先安装 Python 3.9+"
        return
    }
    
    # 检查 Java
    $javaCheck = java -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Java: 已安装"
    } else {
        Write-Host "✗ Java: 未找到，请先安装 Java JDK"
        return
    }
    
    # 检查 buildozer
    $buildozerCheck = buildozer --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Buildozer: 已安装"
    } else {
        Write-Host "✗ Buildozer: 未安装，正在安装..."
        pip install buildozer
    }
    
    # 检查 Android SDK
    $androidSdk = $env:ANDROID_SDK_ROOT
    if ($androidSdk) {
        Write-Host "✓ Android SDK: 已配置 ($androidSdk)"
    } else {
        Write-Host "⚠ Android SDK: 环境变量未设置，但 buildozer 可能会自动下载"
    }
    
    Write-Host ""
    Write-Host "✓ 环境检查完成！"
}

function Build-Debug {
    Write-Host "开始编译调试版本..."
    Write-Host "这可能需要 5-30 分钟，请耐心等待..."
    Write-Host ""
    
    buildozer android debug
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ 编译成功！"
        Write-Host "APK 位置: $(Get-Location)\bin\divination-0.1-debug.apk"
    } else {
        Write-Host ""
        Write-Host "✗ 编译失败，请检查错误日志"
    }
}

function Build-Release {
    Write-Host "开始编译发布版本..."
    Write-Host "这可能需要 5-30 分钟，请耐心等待..."
    Write-Host ""
    
    buildozer android release
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ 编译成功！"
        Write-Host "APK 位置: $(Get-Location)\bin\divination-0.1-release-unsigned.apk"
    } else {
        Write-Host ""
        Write-Host "✗ 编译失败，请检查错误日志"
    }
}

function Install-ToPhone {
    Write-Host "准备安装到手机..."
    Write-Host ""
    Write-Host "操作步骤:"
    Write-Host "1. 用 USB 线连接安卓手机到电脑"
    Write-Host "2. 在手机上启用开发者模式和 USB 调试"
    Write-Host "3. 按任意键开始安装..."
    Write-Host ""
    
    Read-Host "按 Enter 继续"
    
    $apkPath = ".\bin\divination-0.1-debug.apk"
    if (Test-Path $apkPath) {
        adb install -r $apkPath
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ 安装成功！应用已安装到手机"
        } else {
            Write-Host ""
            Write-Host "✗ 安装失败，请检查手机连接"
        }
    } else {
        Write-Host "✗ APK 文件未找到，请先执行编译"
    }
}

function Clean-And-Build {
    Write-Host "清除编译文件..."
    Remove-Item -Path ".buildozer" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "bin" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-Host "清除完成，开始重新编译..."
    Write-Host ""
    
    Build-Debug
}

function Open-Output {
    $outputPath = ".\bin"
    if (Test-Path $outputPath) {
        Invoke-Item $outputPath
    } else {
        Write-Host "输出目录不存在，请先执行编译"
    }
}

# 主程序循环
do {
    Show-Menu
    $choice = Read-Host "请选择 (0-6)"
    
    switch ($choice) {
        "1" { Check-Environment }
        "2" { Build-Debug }
        "3" { Build-Release }
        "4" { Install-ToPhone }
        "5" { Clean-And-Build }
        "6" { Open-Output }
        "0" { Write-Host "再见！"; break }
        default { Write-Host "✗ 无效选择，请重试" }
    }
    
    if ($choice -ne "0") {
        Write-Host ""
        Read-Host "按 Enter 继续"
    }
} while ($choice -ne "0")
