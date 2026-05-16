@echo off
REM 占卜起卦 - 自动打包脚本
REM 此脚本简化了手机应用的编译过程

echo ========================================
echo   占卜起卦 - 手机应用编译工具
echo ========================================
echo.

echo 检查必要的工具...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Python，请先安装 Python 3.9+
    pause
    exit /b 1
)

java -version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到 Java，请先安装 Java JDK
    echo 下载地址: https://www.oracle.com/java/technologies/downloads/
    pause
    exit /b 1
)

echo ✓ Python 已安装
echo ✓ Java 已安装
echo.

echo 选择编译选项:
echo 1. 编译调试版本 (APK)
echo 2. 编译发布版本 (APK)
echo 3. 安装到手机
echo 4. 清除编译文件并重新编译
echo 5. 打开编译日志目录
echo 6. 退出
echo.

set /p choice="请选择 (1-6): "

if "%choice%"=="1" (
    echo.
    echo 开始编译调试版本...
    buildozer android debug
    echo.
    echo ✓ 编译完成！APK 位置: bin\divination-0.1-debug.apk
    pause
) else if "%choice%"=="2" (
    echo.
    echo 开始编译发布版本...
    buildozer android release
    echo.
    echo ✓ 编译完成！APK 位置: bin\divination-0.1-release-unsigned.apk
    pause
) else if "%choice%"=="3" (
    echo.
    echo 准备安装到手机...
    echo 确保手机已用 USB 连接并启用开发者模式
    pause
    adb install -r bin\divination-0.1-debug.apk
    pause
) else if "%choice%"=="4" (
    echo.
    echo 清除编译文件...
    rmdir /s /q .buildozer
    rmdir /s /q bin
    rmdir /s /q build
    echo 编译文件已清除，开始重新编译...
    buildozer android debug
    echo.
    echo ✓ 编译完成！APK 位置: bin\divination-0.1-debug.apk
    pause
) else if "%choice%"=="5" (
    if exist ".buildozer" (
        start explorer ".buildozer"
    ) else (
        echo 编译目录不存在，请先执行编译
    )
    pause
) else if "%choice%"=="6" (
    echo 再见！
    exit /b 0
) else (
    echo 无效选择，请重试
    pause
    goto menu
)
