# 🇨🇳 GitHub Desktop 3.5.7 简体中文语言包

> 由 **铸码 CMS-CORE-001** 全自动构建 | 主控: 之之 (zhizhi200271)

---

## ⚡ 一键安装（复制粘贴即可）

### Windows

1. 先安装 [Node.js](https://nodejs.org/zh-cn/)（如果还没有的话）
2. 按 `Win + X`，选择 **"Windows PowerShell（管理员）"** 或 **"终端（管理员）"**
3. 粘贴以下命令，按回车：

```powershell
irm https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.ps1 | iex
```

4. 等待脚本自动完成（约 1~2 分钟）
5. **关闭并重新打开 GitHub Desktop** → 界面变为中文 ✅

### macOS

1. 先安装 [Node.js](https://nodejs.org/zh-cn/)（或通过 `brew install node`）
2. 打开"终端"，粘贴以下命令，按回车：

```bash
curl -fsSL https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.sh | bash
```

3. **关闭并重新打开 GitHub Desktop** → 界面变为中文 ✅

> 💡 **就这么简单！** 脚本会自动下载翻译文件、备份原文件、应用中文补丁。

---

## 📋 当前状态

| 项目 | 状态 |
|------|------|
| 翻译文件 | ✅ 已完成（500+ 条） |
| Windows 补丁脚本 | ✅ 已完成 |
| macOS/Linux 补丁脚本 | ✅ 已完成 |
| GitHub Actions 自动构建 | ✅ 已完成 |
| Release 自动发布 | ✅ 已完成 |

---

## 📦 其他安装方式

### 方式二：从 Release 下载离线安装包

1. 进入 [Releases 页面](https://github.com/zhizhi200271/-/releases)
2. 下载最新的 `github-desktop-zh-CN-v3.5.7.zip`
3. 解压后：
   - **Windows**：右键 `scripts/apply-patch.ps1` → 选择"使用 PowerShell 运行"
   - **macOS/Linux**：终端运行 `chmod +x scripts/apply-patch.sh && bash scripts/apply-patch.sh`
4. 重启 GitHub Desktop ✅

### 方式三：克隆仓库后本地运行

```bash
git clone https://github.com/zhizhi200271/-.git
cd -/github-desktop-zh-CN/scripts

# Windows (PowerShell 管理员)
.\apply-patch.ps1

# macOS/Linux
chmod +x apply-patch.sh && ./apply-patch.sh
```

---

## 🔄 更新后会怎样？

- ✅ **GitHub Desktop 自动更新后**：Windows 会通过系统计划任务**自动重新应用**中文补丁
- ✅ **翻译内容更新时**：GitHub Actions 自动重新构建并发布新的 Release
- ✅ **手动更新**：重新运行一次上面的一键安装命令即可

---

## 🔙 恢复英文界面

**Windows**（管理员 PowerShell）：

```powershell
irm https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/restore.ps1 | iex
```

**macOS/Linux**：

```bash
# 将备份文件复制回去（脚本安装时会自动告诉你备份路径）
cp "/Applications/GitHub Desktop.app/Contents/Resources/app.asar.zh-cn-backup" \
   "/Applications/GitHub Desktop.app/Contents/Resources/app.asar"
```

---

## ❓ 常见问题

### Q：运行命令时提示"找不到 Node.js"怎么办？

A：访问 https://nodejs.org/zh-cn/ → 下载 LTS 版本 → 安装 → 重新运行命令。

### Q：Windows 提示"无法运行脚本"或"执行策略"怎么办？

A：确保用 **管理员身份** 打开 PowerShell。如果仍有问题，先运行：
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### Q：Actions 构建失败怎么办？

A：
1. 进入 [Actions 页面](https://github.com/zhizhi200271/-/actions)
2. 找到失败的运行记录，点击查看错误信息
3. 如果显示等待审核，点击 **"Approve and run"**

### Q：想手动触发 Actions 构建？

A：进入 [Actions 页面](https://github.com/zhizhi200271/-/actions/workflows/build-zh-cn-patch.yml) → 点击 **"Run workflow"** → 选择 main 分支 → 点击绿色 **"Run workflow"** 按钮。

---

## 🔧 翻译覆盖范围

| 界面区域 | 状态 |
|---------|------|
| 菜单栏（文件/编辑/视图/仓库/分支/帮助） | ✅ 完整 |
| 工具栏（当前仓库/当前分支/推送/拉取/获取） | ✅ 完整 |
| 更改面板（提交/暂存/放弃） | ✅ 完整 |
| 历史面板（提交历史/还原/遴选） | ✅ 完整 |
| 分支面板（新建/合并/变基/重命名/删除） | ✅ 完整 |
| 所有对话框（克隆/新建/设置/登录等） | ✅ 完整 |
| 状态信息、通知、错误提示 | ✅ 完整 |

---

## 📁 文件结构

```
github-desktop-zh-CN/
├── README.md                    ← 本文档（使用说明）
├── translations/
│   └── zh-CN.json              ← 完整简体中文翻译（500+ 条）
└── scripts/
    ├── apply-patch.ps1         ← Windows 补丁脚本
    ├── apply-patch.sh          ← macOS/Linux 补丁脚本
    └── restore.ps1             ← 恢复英文版本脚本

.github/workflows/
└── build-zh-cn-patch.yml      ← 自动构建工作流（推送到 main 自动触发）
```

---

*🤖 铸码 · CMS-CORE-001 · 自动化语言包系统*
*👤 主控: 之之 (zhizhi200271)*

