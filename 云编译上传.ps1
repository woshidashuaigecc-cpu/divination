# 云编译 - 快速上传脚本
# 将项目上传到 GitHub，自动触发云编译

param(
    [string]$GitHubUsername = "",
    [string]$RepositoryName = "divination"
)

function Show-Header {
    Write-Host ""
    Write-Host "========================================"
    Write-Host "   占卜起卦 - GitHub 云编译助手"
    Write-Host "========================================"
    Write-Host ""
}

function Check-Git {
    Write-Host "检查 Git 安装..."
    $gitCheck = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Git 已安装: $gitCheck"
        return $true
    } else {
        Write-Host "✗ Git 未安装"
        Write-Host ""
        Write-Host "请先安装 Git:"
        Write-Host "1. 访问 https://git-scm.com/download/win"
        Write-Host "2. 下载并安装"
        Write-Host "3. 重启 PowerShell"
        return $false
    }
}

function Get-GitHub-Info {
    Write-Host ""
    Write-Host "【第 1 步】输入你的 GitHub 信息"
    Write-Host ""
    Write-Host "如果你还没有 GitHub 账号，请先访问 https://github.com 注册"
    Write-Host ""
    
    $username = Read-Host "请输入 GitHub 用户名"
    if ([string]::IsNullOrEmpty($username)) {
        Write-Host "✗ 用户名不能为空"
        return $null
    }
    
    Write-Host ""
    Write-Host "接下来请前往 GitHub:"
    Write-Host "1. 登录 https://github.com"
    Write-Host "2. 点击右上角 '+' 选择 'New repository'"
    Write-Host "3. 输入仓库名: $RepositoryName"
    Write-Host "4. 选择 'Public'"
    Write-Host "5. 点击 'Create repository'"
    Write-Host ""
    
    $continue = Read-Host "创建完成后按 Enter 继续..."
    
    return $username
}

function Initialize-Git {
    Write-Host ""
    Write-Host "【第 2 步】初始化本地 Git 仓库"
    Write-Host ""
    
    # 检查是否已初始化
    if (Test-Path .git) {
        Write-Host "⚠ 本地 Git 仓库已存在，跳过初始化"
        return $true
    }
    
    Write-Host "正在初始化 Git..."
    git init
    git config user.name "Divination App Builder"
    git config user.email "builder@example.com"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Git 初始化成功"
        return $true
    } else {
        Write-Host "✗ Git 初始化失败"
        return $false
    }
}

function Add-Files {
    Write-Host ""
    Write-Host "【第 3 步】添加项目文件"
    Write-Host ""
    
    # 创建 .gitignore
    $gitignore = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
.venv
env/

# Buildozer
.buildozer/
bin/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Local configs
local.properties
"@
    
    $gitignore | Out-File -Encoding UTF8 -FilePath ".gitignore"
    Write-Host "✓ 已创建 .gitignore"
    
    Write-Host "正在添加项目文件..."
    git add .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 文件添加成功"
        return $true
    } else {
        Write-Host "✗ 文件添加失败"
        return $false
    }
}

function Commit-Changes {
    Write-Host ""
    Write-Host "【第 4 步】提交更改"
    Write-Host ""
    
    Write-Host "正在创建初始提交..."
    git commit -m "Initial commit: Divination app"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 提交成功"
        return $true
    } else {
        Write-Host "✗ 提交失败（可能没有更改）"
        return $true
    }
}

function Setup-Remote {
    param(
        [string]$Username,
        [string]$RepoName
    )
    
    Write-Host ""
    Write-Host "【第 5 步】关联远程仓库"
    Write-Host ""
    
    $remoteUrl = "https://github.com/$Username/$RepoName.git"
    Write-Host "远程仓库地址: $remoteUrl"
    
    # 检查是否已有 remote
    $hasRemote = git remote -v 2>&1 | Select-String origin
    if ($hasRemote) {
        Write-Host "⚠ 已存在远程配置，删除后重新添加"
        git remote remove origin 2>&1 | Out-Null
    }
    
    git remote add origin $remoteUrl
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 远程仓库配置成功"
        return $true
    } else {
        Write-Host "✗ 远程仓库配置失败"
        return $false
    }
}

function Push-Code {
    param(
        [string]$Username
    )
    
    Write-Host ""
    Write-Host "【第 6 步】推送代码到 GitHub"
    Write-Host ""
    
    # 检查当前分支
    $branch = git rev-parse --abbrev-ref HEAD
    Write-Host "当前分支: $branch"
    
    # 如果是 master，重命名为 main
    if ($branch -eq "master") {
        git branch -M main
        $branch = "main"
    }
    
    Write-Host ""
    Write-Host "正在推送代码..."
    Write-Host "（如果提示输入密码，请使用 Personal Access Token）"
    Write-Host "获取 Token: https://github.com/settings/tokens"
    Write-Host ""
    
    git push -u origin $branch
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ 代码推送成功！"
        Write-Host ""
        Write-Host "📱 GitHub 已自动开始编译，请访问:"
        Write-Host "https://github.com/$Username/divination/actions"
        Write-Host ""
        Write-Host "编译通常需要 5-20 分钟，请耐心等待..."
        return $true
    } else {
        Write-Host ""
        Write-Host "✗ 推送失败，可能的原因:"
        Write-Host "1. 网络连接问题"
        Write-Host "2. GitHub 凭证错误"
        Write-Host "3. 仓库权限问题"
        return $false
    }
}

function Show-Next-Steps {
    param(
        [string]$Username
    )
    
    Write-Host ""
    Write-Host "========================================"
    Write-Host "   ✓ 上传完成！下一步"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "1️⃣  访问 GitHub Actions:"
    Write-Host "   https://github.com/$Username/divination/actions"
    Write-Host ""
    Write-Host "2️⃣  观看编译进度:"
    Write-Host "   - 点击最新的 'Build Android APK' 工作流"
    Write-Host "   - 实时查看编译日志"
    Write-Host ""
    Write-Host "3️⃣  下载编译结果:"
    Write-Host "   - 编译完成后点击工作流进入详情"
    Write-Host "   - 向下滚动找到 'Artifacts' 部分"
    Write-Host "   - 点击 'divination-apk' 下载"
    Write-Host ""
    Write-Host "4️⃣  安装到手机:"
    Write-Host "   - APK 文件位置: bin/divination-0.1-debug.apk"
    Write-Host "   - 复制到手机或用 adb install 安装"
    Write-Host ""
    Write-Host "需要帮助? 查看: 云编译使用说明.md"
    Write-Host ""
}

# 主程序
Show-Header

# 检查 Git
if (-not (Check-Git)) {
    Write-Host ""
    Read-Host "按 Enter 退出"
    exit 1
}

# 获取 GitHub 信息
$githubUsername = Get-GitHub-Info
if ($null -eq $githubUsername) {
    exit 1
}

Write-Host ""

# 初始化 Git
if (-not (Initialize-Git)) {
    Write-Host "按 Enter 退出"
    Read-Host
    exit 1
}

# 添加文件
if (-not (Add-Files)) {
    Write-Host "按 Enter 退出"
    Read-Host
    exit 1
}

# 提交更改
Commit-Changes

# 关联远程
if (-not (Setup-Remote $githubUsername $RepositoryName)) {
    Write-Host ""
    Write-Host "按 Enter 退出"
    Read-Host
    exit 1
}

# 推送代码
if (Push-Code $githubUsername) {
    Show-Next-Steps $githubUsername
}

Write-Host ""
Read-Host "按 Enter 结束"
