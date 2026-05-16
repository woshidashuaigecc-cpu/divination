# 占卜起卦 - 手机应用打包说明

## 前置要求

### Windows 系统上开发：
1. **安装 Java JDK**（必需）
   - 下载 JDK 11 或 17: https://www.oracle.com/java/technologies/downloads/
   - 设置环境变量 JAVA_HOME

2. **安装 Android SDK**
   - 下载 Android Studio: https://developer.android.com/studio
   - 或单独下载 Android SDK

3. **安装 Python 3.9+**
   - 确保已安装 Python 3.9 或更高版本

4. **安装 Buildozer**
   ```bash
   pip install buildozer
   ```

5. **安装其他必要工具**
   ```bash
   pip install cython
   ```

## 打包步骤

### 方法一：使用 Buildozer（推荐）

1. **在项目目录中打开命令行**
   ```bash
   cd c:\Users\黎呈君\Desktop\python_code
   ```

2. **初始化 Buildozer**（如果还没有完整配置）
   ```bash
   buildozer android debug
   ```
   首次运行会下载必要的 SDK 和工具，可能需要 10-30 分钟

3. **编译 APK**
   ```bash
   buildozer android debug
   ```
   编译完成后，APK 文件会在 `bin` 文件夹中

4. **安装到手机**
   ```bash
   # 确保手机已用 USB 连接并启用开发者模式
   adb install bin/divination-0.1-debug.apk
   ```

### 方法二：发布版本（有签名）

1. **编译发布版本**
   ```bash
   buildozer android release
   ```

2. **签名 APK**
   ```bash
   jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/divination-0.1-release-unsigned.apk alias_name
   ```

## 配置说明

已更新的 `buildozer.spec` 配置：

- **应用名称**: 占卜起卦
- **包名**: org.example.divination
- **最小 API 级别**: 21（Android 5.0）
- **目标 API 级别**: 33（Android 13）
- **架构**: arm64-v8a（64位，兼容现代安卓手机）

## 常见问题

### 1. "Java not found" 错误
- 检查 JAVA_HOME 环境变量是否正确设置
- 重启 PowerShell/CMD

### 2. "Android SDK not found" 错误
- 检查 Android SDK 路径
- 在环境变量中设置 ANDROID_SDK_ROOT

### 3. 首次编译很慢
- Buildozer 会下载约 5-10GB 的 SDK、NDK 等工具
- 需要良好的网络连接
- 耐心等待，只需首次如此

### 4. 编译失败
- 检查所有依赖包是否正确安装
- 尝试运行 `buildozer android debug --verbose` 获取详细日志
- 可能需要更新 buildozer 或 python-for-android

## APK 最后位置

编译成功后，APK 文件位置：
```
c:\Users\黎呈君\Desktop\python_code\bin\divination-0.1-debug.apk
```

## 在手机上安装

1. **启用未知来源安装**
   - 进入手机设置 → 安全 → 允许安装未知来源应用

2. **使用 USB 安装（推荐）**
   ```bash
   adb install bin/divination-0.1-debug.apk
   ```

3. **直接安装**
   - 将 APK 传到手机
   - 用文件管理器打开，选择安装

## 优化建议

如果要进一步优化应用：

1. **添加应用图标**
   - 在 `buildozer.spec` 中取消注释 `icon.filename`
   - 使用 512x512px 的 PNG 图片

2. **添加启动屏幕**
   - 在 `buildozer.spec` 中取消注释 `presplash.filename`

3. **减少 APK 大小**
   - 在 `buildozer.spec` 中添加优化选项

## 联系支持

如遇问题，可查看：
- Kivy 文档: https://kivy.org/doc/stable/
- Buildozer 文档: https://buildozer.readthedocs.io/
