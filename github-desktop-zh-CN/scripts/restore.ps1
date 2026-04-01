# ============================================================
# GitHub Desktop 恢复英文版本脚本
# 铸码 CMS-CORE-001 | 主控: 之之 (zhizhi200271)
# ============================================================

param(
    [string]$TargetVersion = "3.5.7"
)

$Host.UI.RawUI.WindowTitle = "GitHub Desktop 恢复英文版 - 铸码 CMS"

function Write-Info  { param($msg) Write-Host "[信息] $msg" -ForegroundColor Cyan }
function Write-OK    { param($msg) Write-Host "[成功] $msg" -ForegroundColor Green }
function Write-Fail  { param($msg) Write-Host "[错误] $msg" -ForegroundColor Red }
function Write-Title { param($msg) Write-Host "`n$msg" -ForegroundColor Magenta }

Write-Title "════════════════════════════════════════════════════"
Write-Title "  GitHub Desktop $TargetVersion 恢复英文版本"
Write-Title "  铸码 CMS-CORE-001 | 主控: 之之"
Write-Title "════════════════════════════════════════════════════`n"

# 查找 asar 和备份文件
$searchRoots = @(
    "$env:LOCALAPPDATA\GitHubDesktop\app-$TargetVersion\resources\app.asar",
    "$env:LOCALAPPDATA\GitHubDesktop"
)

$asarPath = $null
foreach ($path in $searchRoots) {
    if (Test-Path $path -PathType Leaf) {
        $asarPath = $path
        break
    }
    if (Test-Path $path -PathType Container) {
        $found = Get-ChildItem $path -Recurse -Filter "app.asar" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { $asarPath = $found.FullName; break }
    }
}

if (-not $asarPath) {
    Write-Fail "未找到 GitHub Desktop 安装目录！"
    Read-Host "按 Enter 键退出"
    exit 1
}

$backupPath = "$asarPath.zh-cn-backup"

if (-not (Test-Path $backupPath)) {
    Write-Fail "未找到英文版备份文件: $backupPath"
    Write-Info "可能从未应用过中文补丁，或备份已被删除"
    Read-Host "按 Enter 键退出"
    exit 1
}

Write-Info "找到备份文件: $backupPath"
Write-Info "正在恢复英文版本..."

Copy-Item $backupPath $asarPath -Force

# 移除计划任务
Unregister-ScheduledTask -TaskName "GitHubDesktop-ZhCN-AutoPatch" -Confirm:$false -ErrorAction SilentlyContinue

Write-Title "════════════════════════════════════════════════════"
Write-OK "GitHub Desktop 已恢复为英文版本！"
Write-Title "════════════════════════════════════════════════════"
Write-Host ""
Write-Host "  📌 请重新启动 GitHub Desktop 以使更改生效" -ForegroundColor Yellow
Write-Host ""

Read-Host "按 Enter 键退出"
