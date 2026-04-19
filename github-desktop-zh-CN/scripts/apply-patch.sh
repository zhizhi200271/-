#!/bin/bash
# ============================================================
# GitHub Desktop 3.5.7 简体中文补丁脚本 (macOS)
# 铸码 CMS-CORE-001 | 主控: 之之 (zhizhi200271)
# ============================================================
# 使用方法: chmod +x apply-patch.sh && ./apply-patch.sh
# ============================================================

set -e

TARGET_VERSION="3.5.7"
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
NC='\033[0m'

info()  { echo -e "${CYAN}[信息] $1${NC}"; }
ok()    { echo -e "${GREEN}[成功] $1${NC}"; }
warn()  { echo -e "${YELLOW}[警告] $1${NC}"; }
fail()  { echo -e "${RED}[错误] $1${NC}"; }
title() { echo -e "${MAGENTA}\n$1${NC}"; }

title "════════════════════════════════════════════════════"
title "  GitHub Desktop ${TARGET_VERSION} 简体中文汉化补丁"
title "  铸码 CMS-CORE-001 | 主控: 之之"
title "════════════════════════════════════════════════════"

# ── 检测操作系统和安装路径 ────────────────────────────────────
title "步骤 1/5: 检测 GitHub Desktop 安装路径"

ASAR_PATH=""
APP_DIR=""

if [ "$(uname)" = "Darwin" ]; then
    # macOS
    if [ -f "/Applications/GitHub Desktop.app/Contents/Resources/app.asar" ]; then
        ASAR_PATH="/Applications/GitHub Desktop.app/Contents/Resources/app.asar"
        APP_DIR="/Applications/GitHub Desktop.app/Contents/Resources"
        ok "找到 GitHub Desktop: /Applications/GitHub Desktop.app"
    elif [ -d "/Applications/GitHub Desktop.app/Contents/Resources/app" ]; then
        APP_DIR="/Applications/GitHub Desktop.app/Contents/Resources/app"
        ok "找到 GitHub Desktop (未打包模式): $APP_DIR"
    else
        fail "未找到 GitHub Desktop！请确认已安装。"
        fail "默认安装位置: /Applications/GitHub Desktop.app"
        exit 1
    fi
elif [ "$(uname)" = "Linux" ]; then
    # Linux（非官方 shiftkey/desktop 分支）
    LINUX_PATHS=(
        "/usr/lib/github-desktop/resources/app.asar"
        "/usr/share/github-desktop/resources/app.asar"
        "/opt/GitHub Desktop/resources/app.asar"
        "/snap/github-desktop/current/resources/app.asar"
    )
    for lpath in "${LINUX_PATHS[@]}"; do
        if [ -f "$lpath" ]; then
            ASAR_PATH="$lpath"
            APP_DIR="$(dirname "$lpath")"
            ok "找到 GitHub Desktop: $APP_DIR"
            break
        fi
    done
    if [ -z "$ASAR_PATH" ] && [ -z "$APP_DIR" ]; then
        fail "未找到 GitHub Desktop！"
        warn "Linux 用户请确认已安装 GitHub Desktop (shiftkey/desktop 分支)"
        warn "已搜索路径: ${LINUX_PATHS[*]}"
        exit 1
    fi
else
    fail "此脚本仅支持 macOS 和 Linux。Windows 用户请使用 apply-patch.ps1"
    exit 1
fi

# ── 检测是否需要管理员权限 ─────────────────────────────────────
SUDO=""
if [ -n "$ASAR_PATH" ]; then
    WRITE_TEST_DIR="$(dirname "$ASAR_PATH")"
else
    WRITE_TEST_DIR="$APP_DIR"
fi
if ! [ -w "$WRITE_TEST_DIR" ]; then
    SUDO="sudo"
    warn "修改 GitHub Desktop 文件需要管理员权限，可能会要求输入密码"
    if ! sudo -v 2>/dev/null; then
        fail "无法获取管理员权限！"
        warn "请尝试以下方式运行："
        warn "  curl -fsSL https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.sh -o /tmp/apply-patch.sh && sudo bash /tmp/apply-patch.sh"
        exit 1
    fi
fi

# ── 备份 ──────────────────────────────────────────────────────
title "步骤 2/5: 创建原始文件备份"
if [ -n "$ASAR_PATH" ]; then
    BACKUP_PATH="${ASAR_PATH}.zh-cn-backup"
    if [ ! -f "$BACKUP_PATH" ]; then
        $SUDO cp "$ASAR_PATH" "$BACKUP_PATH"
        ok "备份已创建: $BACKUP_PATH"
    else
        warn "备份已存在，跳过"
    fi
else
    BACKUP_PATH="${APP_DIR}.zh-cn-backup"
    if [ ! -d "$BACKUP_PATH" ]; then
        info "正在备份 app 目录..."
        $SUDO cp -R "$APP_DIR" "$BACKUP_PATH"
        ok "备份已创建: $BACKUP_PATH"
    else
        warn "备份已存在，跳过"
    fi
fi

# ── 检测 Node.js ──────────────────────────────────────────────
title "步骤 3/5: 检测 Node.js 环境"
if ! command -v node &> /dev/null; then
    fail "未找到 Node.js！"
    warn "请从 https://nodejs.org 安装 Node.js 后重新运行此脚本"
    warn "或使用 Homebrew: brew install node"
    exit 1
fi
NODE_VER=$(node --version)
ok "Node.js 已就绪: $NODE_VER"

# ── 获取翻译文件 ──────────────────────────────────────────────
title "步骤 4/5: 加载翻译文件"

# 获取脚本所在目录（兼容 curl | bash 管道调用）
SCRIPT_DIR=""
if [ -n "${BASH_SOURCE[0]}" ] && [ "${BASH_SOURCE[0]}" != "bash" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
fi

TRANS_PATH=""
if [ -n "$SCRIPT_DIR" ]; then
    if [ -f "$SCRIPT_DIR/../translations/zh-CN.json" ]; then
        TRANS_PATH="$SCRIPT_DIR/../translations/zh-CN.json"
    elif [ -f "$SCRIPT_DIR/zh-CN.json" ]; then
        TRANS_PATH="$SCRIPT_DIR/zh-CN.json"
    fi
fi

if [ -z "$TRANS_PATH" ] || [ ! -f "$TRANS_PATH" ]; then
    info "正在从 GitHub 下载翻译文件..."
    TEMP_TRANS="/tmp/github-desktop-zh-CN.json"
    if curl -fsSL "https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/translations/zh-CN.json" -o "$TEMP_TRANS"; then
        TRANS_PATH="$TEMP_TRANS"
        ok "翻译文件下载成功"
    else
        fail "无法下载翻译文件！"
        exit 1
    fi
fi
ok "翻译文件: $TRANS_PATH"

# ── 应用补丁 ──────────────────────────────────────────────────
title "步骤 5/5: 应用中文补丁"

# Node.js 补丁脚本（内嵌）
NODE_PATCH_SCRIPT=$(cat << 'NODEJS_EOF'
const fs = require('fs');
const path = require('path');

const transPath = process.argv[2];
const targetDir = process.argv[3];

if (!transPath || !targetDir) {
    console.error('用法: node patch.js <翻译文件> <目标目录>');
    process.exit(1);
}

// 加载并展平翻译
const raw = JSON.parse(fs.readFileSync(transPath, 'utf8'));
const translations = {};

function flatten(obj, prefix) {
    for (const [key, val] of Object.entries(obj)) {
        if (key === '_meta') continue;
        if (typeof val === 'string') {
            translations[key] = val;
        } else if (typeof val === 'object') {
            flatten(val, prefix ? `${prefix}.${key}` : key);
        }
    }
}
flatten(raw, '');
console.log(`[信息] 已加载 ${Object.keys(translations).length} 条翻译`);

// 遍历 JS 文件
let totalReplaced = 0;
function patchDir(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            patchDir(fullPath);
        } else if (entry.isFile() && entry.name.endsWith('.js')) {
            const stat = fs.statSync(fullPath);
            if (stat.size < 1024 || stat.size > 50 * 1024 * 1024) continue;

            let content = fs.readFileSync(fullPath, 'utf8');
            let count = 0;

            for (const [en, zh] of Object.entries(translations)) {
                if (!en || !zh || en === zh) continue;
                const escaped = en.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                // 匹配双引号和单引号包裹的字符串
                const regex = new RegExp(`(?<=[\"'])${escaped}(?=[\"'])`, 'g');
                const newContent = content.replace(regex, zh);
                if (newContent !== content) {
                    count++;
                    content = newContent;
                }
            }

            if (count > 0) {
                fs.writeFileSync(fullPath, content, 'utf8');
                console.log(`[成功]   已替换 ${count} 处: ${path.basename(fullPath)}`);
                totalReplaced += count;
            }
        }
    }
}

patchDir(targetDir);
console.log(`[成功] 共替换 ${totalReplaced} 处字符串`);
NODEJS_EOF
)

TEMP_PATCH="/tmp/github-desktop-patch-$$.js"
echo "$NODE_PATCH_SCRIPT" > "$TEMP_PATCH"

if [ -n "$ASAR_PATH" ]; then
    # 解包 asar
    TEMP_EXTRACT="/tmp/github-desktop-extracted-$$"
    info "正在解包 app.asar..."
    if ! npx --yes @electron/asar extract "$ASAR_PATH" "$TEMP_EXTRACT" 2>/dev/null; then
        fail "解包 asar 失败！"
        rm -f "$TEMP_PATCH"
        exit 1
    fi
    ok "解包完成"

    # 应用补丁
    node "$TEMP_PATCH" "$TRANS_PATH" "$TEMP_EXTRACT"

    # 重新打包
    info "正在重新打包 app.asar..."
    TEMP_ASAR="/tmp/github-desktop-patched-$$.asar"
    if npx --yes @electron/asar pack "$TEMP_EXTRACT" "$TEMP_ASAR" 2>/dev/null; then
        $SUDO cp -f "$TEMP_ASAR" "$ASAR_PATH"
        rm -f "$TEMP_ASAR"
        ok "app.asar 重新打包完成"
    else
        fail "重新打包失败！正在恢复备份..."
        $SUDO cp -f "$BACKUP_PATH" "$ASAR_PATH"
        ok "已恢复英文版本"
        rm -rf "$TEMP_EXTRACT" "$TEMP_PATCH" "$TEMP_ASAR"
        exit 1
    fi

    rm -rf "$TEMP_EXTRACT"
else
    # 未打包模式：复制到临时目录打补丁，再复制回去
    TEMP_APP="/tmp/github-desktop-unpacked-$$"
    info "正在复制 app 目录到临时目录..."
    cp -R "$APP_DIR" "$TEMP_APP"

    node "$TEMP_PATCH" "$TRANS_PATH" "$TEMP_APP"

    info "正在将补丁后的文件复制回原位..."
    $SUDO cp -Rf "$TEMP_APP/." "$APP_DIR/"
    ok "补丁文件已复制回原位"

    rm -rf "$TEMP_APP"
fi

rm -f "$TEMP_PATCH"

title "════════════════════════════════════════════════════"
ok "GitHub Desktop ${TARGET_VERSION} 中文汉化补丁已成功应用！"
title "════════════════════════════════════════════════════"
echo ""
echo "  📌 下一步操作:"
echo "  1. 重新启动 GitHub Desktop"
echo "  2. 界面将显示简体中文"
echo ""
echo "  📌 如需恢复英文版本:"
if [ -n "$ASAR_PATH" ]; then
    echo "  ${SUDO:+sudo }cp \"${BACKUP_PATH}\" \"${ASAR_PATH}\""
else
    echo "  ${SUDO:+sudo }rm -rf \"${APP_DIR}\" && ${SUDO:+sudo }cp -R \"${BACKUP_PATH}\" \"${APP_DIR}\""
fi
echo ""
