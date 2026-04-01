# ============================================================
# GitHub Desktop 3.5.7 简体中文补丁脚本
# 铸码 CMS-CORE-001 | 主控: 之之 (zhizhi200271)
# ============================================================
# 使用方法: 以管理员身份运行此脚本（或直接双击 apply-patch.ps1）
# 功能: 自动汉化已安装的 GitHub Desktop 3.5.7
# ============================================================

param(
    [string]$TargetVersion = "3.5.7",
    [switch]$AutoRestore,
    [switch]$Silent
)

$ErrorActionPreference = "Stop"
$Host.UI.RawUI.WindowTitle = "GitHub Desktop 中文补丁 - 铸码 CMS"

# ── 颜色输出函数 ──────────────────────────────────────────────
function Write-Info  { param($msg) Write-Host "[信息] $msg" -ForegroundColor Cyan }
function Write-OK    { param($msg) Write-Host "[成功] $msg" -ForegroundColor Green }
function Write-Warn  { param($msg) Write-Host "[警告] $msg" -ForegroundColor Yellow }
function Write-Fail  { param($msg) Write-Host "[错误] $msg" -ForegroundColor Red }
function Write-Title { param($msg) Write-Host "`n$msg" -ForegroundColor Magenta }

Write-Title "════════════════════════════════════════════════════"
Write-Title "  GitHub Desktop $TargetVersion 简体中文汉化补丁"
Write-Title "  铸码 CMS-CORE-001 | 主控: 之之"
Write-Title "════════════════════════════════════════════════════`n"

# ── 检测 GitHub Desktop 安装路径 ─────────────────────────────
function Find-GitHubDesktop {
    param([string]$version)

    $searchPaths = @(
        "$env:LOCALAPPDATA\GitHubDesktop\app-$version",
        "$env:PROGRAMFILES\GitHub Desktop",
        "$env:PROGRAMFILES(x86)\GitHub Desktop"
    )

    foreach ($path in $searchPaths) {
        if (Test-Path $path) {
            return $path
        }
    }

    # 模糊搜索（版本号可能略有不同）
    $ghRoot = "$env:LOCALAPPDATA\GitHubDesktop"
    if (Test-Path $ghRoot) {
        $found = Get-ChildItem $ghRoot -Directory -Filter "app-$version*" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { return $found.FullName }
        # 列出所有版本供用户选择
        $allVersions = Get-ChildItem $ghRoot -Directory -Filter "app-*" | Sort-Object Name -Descending
        if ($allVersions) {
            Write-Warn "未找到 $version 版本，已找到以下版本:"
            $allVersions | ForEach-Object { Write-Host "  - $($_.Name)" -ForegroundColor Yellow }
            return $allVersions[0].FullName
        }
    }

    return $null
}

# ── 检测 Node.js ──────────────────────────────────────────────
function Test-NodeJs {
    $node = Get-Command node -ErrorAction SilentlyContinue
    if (-not $node) {
        # 检查 GitHub Desktop 自带的 node
        $ghNode = "$env:LOCALAPPDATA\GitHubDesktop\bin\node.exe"
        if (Test-Path $ghNode) { return $ghNode }
        return $null
    }
    return "node"
}

# ── 安装 asar 工具 ────────────────────────────────────────────
function Install-AsarTool {
    param([string]$nodeCmd)
    Write-Info "正在安装 @electron/asar 工具..."
    try {
        & npm install -g @electron/asar --silent 2>&1 | Out-Null
        $asar = Get-Command asar -ErrorAction SilentlyContinue
        if ($asar) {
            Write-OK "asar 工具安装成功"
            return "asar"
        }
        # 尝试 npx
        return "npx @electron/asar"
    } catch {
        Write-Warn "npm 全局安装失败，将使用 npx"
        return "npx --yes @electron/asar"
    }
}

# ── 获取翻译文件路径 ──────────────────────────────────────────
function Get-TranslationsPath {
    # 优先从仓库本地读取（如果用户克隆了仓库）
    $scriptDir = Split-Path -Parent $MyInvocation.ScriptName
    $localPath = Join-Path $scriptDir "..\translations\zh-CN.json"
    if (Test-Path $localPath) {
        return (Resolve-Path $localPath).Path
    }

    # 从脚本同级目录读取
    $samePath = Join-Path $scriptDir "zh-CN.json"
    if (Test-Path $samePath) { return $samePath }

    # 从 GitHub 下载最新翻译
    Write-Info "正在从 GitHub 下载最新翻译文件..."
    $tempTrans = "$env:TEMP\github-desktop-zh-cn-translations.json"
    try {
        $url = "https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/translations/zh-CN.json"
        Invoke-WebRequest -Uri $url -OutFile $tempTrans -UseBasicParsing
        Write-OK "翻译文件下载成功"
        return $tempTrans
    } catch {
        Write-Fail "无法下载翻译文件: $_"
        return $null
    }
}

# ── 核心补丁函数 ──────────────────────────────────────────────
function Apply-StringPatches {
    param(
        [string]$filePath,
        [hashtable]$translations,
        [int]$replacedCount = 0
    )

    $content = [System.IO.File]::ReadAllText($filePath, [System.Text.Encoding]::UTF8)
    $originalLength = $content.Length
    $count = 0

    foreach ($entry in $translations.GetEnumerator()) {
        $en = $entry.Key
        $zh = $entry.Value

        # 跳过元信息键
        if ($en -eq "_meta") { continue }
        if ($en -match "^\[") { continue }

        # 处理嵌套对象（递归展平已在 Load-Translations 中完成）
        if ($zh -is [hashtable] -or $zh -is [System.Collections.Specialized.OrderedDictionary]) { continue }
        if (-not ($zh -is [string])) { continue }
        if ([string]::IsNullOrWhiteSpace($en) -or [string]::IsNullOrWhiteSpace($zh)) { continue }
        if ($en -eq $zh) { continue }

        # 构建正则表达式，匹配带引号的字符串
        $escaped = [regex]::Escape($en)

        # 双引号字符串匹配
        $before = $content.Length
        $content = $content -replace "(?<=[""'])$escaped(?=[""'])", $zh
        if ($content.Length -ne $before -or $content.Contains($zh)) {
            $occurrences = ([regex]::Matches($content, [regex]::Escape($zh))).Count
            if ($occurrences -gt 0) { $count++ }
        }
    }

    if ($count -gt 0 -or $content.Length -ne $originalLength) {
        [System.IO.File]::WriteAllText($filePath, $content, [System.Text.Encoding]::UTF8)
        Write-OK "  已替换 $count 处字符串: $(Split-Path -Leaf $filePath)"
    }

    return $count
}

# ── 展平嵌套翻译 JSON ─────────────────────────────────────────
function Flatten-Translations {
    param($obj, [string]$prefix = "")

    $result = @{}

    if ($obj -is [System.Collections.Hashtable] -or $obj -is [PSCustomObject]) {
        $props = if ($obj -is [PSCustomObject]) { $obj.PSObject.Properties } else { $obj.GetEnumerator() }
        foreach ($prop in $props) {
            $key = $prop.Name
            $val = $prop.Value
            if ($key -eq "_meta") { continue }
            if ($val -is [string]) {
                $result[$key] = $val
            } elseif ($val -is [PSCustomObject] -or $val -is [System.Collections.Hashtable]) {
                $nested = Flatten-Translations -obj $val -prefix "$key."
                foreach ($n in $nested.GetEnumerator()) {
                    $result[$n.Key] = $n.Value
                }
            }
        }
    }
    return $result
}

# ── 主流程 ────────────────────────────────────────────────────
Write-Title "步骤 1/6: 检测 GitHub Desktop 安装路径"
$appDir = Find-GitHubDesktop -version $TargetVersion
if (-not $appDir) {
    Write-Fail "未找到 GitHub Desktop $TargetVersion 安装目录！"
    Write-Warn "请确认已安装 GitHub Desktop，或检查安装位置："
    Write-Warn "  默认位置: $env:LOCALAPPDATA\GitHubDesktop\app-$TargetVersion"
    Read-Host "按 Enter 键退出"
    exit 1
}
Write-OK "找到 GitHub Desktop: $appDir"

# ── 检测 asar 文件 ────────────────────────────────────────────
$asarPath = "$appDir\resources\app.asar"
$appUnpacked = "$appDir\resources\app"
$useAsar = $false

if (Test-Path $asarPath) {
    $useAsar = $true
    Write-OK "检测到 app.asar 归档文件"
} elseif (Test-Path $appUnpacked) {
    Write-OK "检测到未打包的 app 目录（开发模式）"
} else {
    Write-Fail "未找到应用资源文件 (app.asar 或 app/)！"
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Title "步骤 2/6: 创建原始文件备份"
if ($useAsar) {
    $backupPath = "$asarPath.zh-cn-backup"
    if (-not (Test-Path $backupPath)) {
        Copy-Item $asarPath $backupPath
        Write-OK "备份已创建: $backupPath"
    } else {
        Write-Warn "备份已存在，跳过（如需重新备份，请先删除 .zh-cn-backup 文件）"
    }
}

Write-Title "步骤 3/6: 检测 Node.js 环境"
$nodeCmd = Test-NodeJs
if (-not $nodeCmd -and $useAsar) {
    Write-Fail "未找到 Node.js！处理 .asar 文件需要 Node.js。"
    Write-Warn "请从 https://nodejs.org 下载安装 Node.js，然后重新运行此脚本"
    Read-Host "按 Enter 键退出"
    exit 1
}
if ($nodeCmd) {
    Write-OK "Node.js 已就绪: $nodeCmd"
}

Write-Title "步骤 4/6: 加载翻译文件"
$transPath = Get-TranslationsPath
if (-not $transPath) {
    Write-Fail "无法获取翻译文件！"
    Read-Host "按 Enter 键退出"
    exit 1
}
Write-OK "翻译文件: $transPath"

$transJson = Get-Content $transPath -Raw -Encoding UTF8 | ConvertFrom-Json
$translations = Flatten-Translations -obj $transJson
Write-OK "已加载 $($translations.Count) 条翻译"

Write-Title "步骤 5/6: 应用中文补丁"

$tempDir = "$env:TEMP\github-desktop-zh-cn-$TargetVersion"

if ($useAsar) {
    # 解包 asar
    Write-Info "正在解包 app.asar..."
    if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }

    # 使用 npx asar 解包
    $asarCmd = "npx --yes @electron/asar extract `"$asarPath`" `"$tempDir`""
    Write-Info "执行: $asarCmd"
    $result = cmd /c $asarCmd 2>&1
    if ($LASTEXITCODE -ne 0 -and -not (Test-Path $tempDir)) {
        Write-Fail "解包失败: $result"
        Write-Warn "请手动安装 Node.js 后重试，或联系铸码获取支持"
        Read-Host "按 Enter 键退出"
        exit 1
    }
    Write-OK "解包完成: $tempDir"
    $patchDir = $tempDir
} else {
    $patchDir = $appUnpacked
}

# 查找所有 JS 文件进行补丁
$jsFiles = Get-ChildItem $patchDir -Recurse -Filter "*.js" -File |
    Where-Object { $_.Length -gt 1KB -and $_.Length -lt 50MB } |
    Sort-Object Length -Descending

Write-Info "找到 $($jsFiles.Count) 个 JS 文件待处理..."
$totalReplaced = 0
foreach ($jsFile in $jsFiles) {
    $replaced = Apply-StringPatches -filePath $jsFile.FullName -translations $translations
    $totalReplaced += $replaced
}

Write-OK "共替换 $totalReplaced 处字符串"

if ($useAsar -and $totalReplaced -gt 0) {
    Write-Info "正在重新打包 app.asar..."
    # 备份原始 asar 并替换
    $newAsarCmd = "npx --yes @electron/asar pack `"$tempDir`" `"$asarPath`""
    $result = cmd /c $newAsarCmd 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "重新打包失败: $result"
        Write-Warn "正在恢复备份..."
        Copy-Item $backupPath $asarPath -Force
        Write-OK "已恢复英文版本"
        Read-Host "按 Enter 键退出"
        exit 1
    }
    Write-OK "app.asar 重新打包完成"

    # 清理临时目录
    Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
} elseif ($totalReplaced -eq 0) {
    Write-Warn "未找到可替换的字符串（可能已经是中文版，或版本不匹配）"
}

Write-Title "步骤 6/6: 设置自动重打补丁（GitHub Desktop 更新后自动恢复中文）"

# 创建自动重打补丁的计划任务
$taskScript = @"
# 自动重打补丁检测脚本 - 由铸码生成
`$asarPath = "$asarPath"
`$backupPath = "$($asarPath).zh-cn-backup"
`$patchScript = "$($MyInvocation.MyCommand.Path)"

# 如果 asar 比备份新（说明 GitHub Desktop 已更新），重新应用补丁
if ((Test-Path `$asarPath) -and (Test-Path `$backupPath)) {
    `$asarTime = (Get-Item `$asarPath).LastWriteTime
    `$backupTime = (Get-Item `$backupPath).LastWriteTime
    if (`$asarTime -gt `$backupTime) {
        Start-Process powershell -ArgumentList "-File `"`$patchScript`" -Silent" -Verb RunAs
    }
}
"@

$autoScriptPath = "$env:APPDATA\github-desktop-zh-cn-auto.ps1"
$taskScript | Out-File $autoScriptPath -Encoding UTF8

# 注册计划任务（登录时检查）
try {
    $trigger = New-ScheduledTaskTrigger -AtLogOn
    $action = New-ScheduledTaskAction -Execute "powershell" -Argument "-WindowStyle Hidden -File `"$autoScriptPath`""
    $settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
    $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest
    Register-ScheduledTask -TaskName "GitHubDesktop-ZhCN-AutoPatch" -Trigger $trigger -Action $action -Settings $settings -Principal $principal -Force -ErrorAction SilentlyContinue | Out-Null
    Write-OK "已注册开机自动重打补丁任务"
} catch {
    Write-Warn "无法注册计划任务（需要管理员权限）: $_"
    Write-Warn "GitHub Desktop 更新后请手动重新运行此脚本"
}

Write-Title "`n════════════════════════════════════════════════════"
Write-OK "GitHub Desktop $TargetVersion 中文汉化补丁已成功应用！"
Write-Title "════════════════════════════════════════════════════"
Write-Host ""
Write-Host "  ✅ 翻译条目: $($translations.Count) 条" -ForegroundColor White
Write-Host "  ✅ 已替换字符串: $totalReplaced 处" -ForegroundColor White
Write-Host "  ✅ 备份文件: $backupPath" -ForegroundColor White
Write-Host ""
Write-Host "  📌 下一步操作:" -ForegroundColor Yellow
Write-Host "  1. 重新启动 GitHub Desktop" -ForegroundColor White
Write-Host "  2. 界面将显示简体中文" -ForegroundColor White
Write-Host "  3. GitHub Desktop 更新后将自动重新应用中文补丁" -ForegroundColor White
Write-Host ""
Write-Host "  📌 如需恢复英文版本:" -ForegroundColor Yellow
Write-Host "  运行 restore.ps1 脚本" -ForegroundColor White
Write-Host ""

if (-not $Silent) {
    Read-Host "按 Enter 键退出"
}
