# 🇨🇳 GitHub Desktop 3.5.7 简体中文语言包

> 由 **铸码 CMS-CORE-001** 全自动构建 | 主控: 之之 (zhizhi200271)

---

## ✅ 可行性评估

**结论：完全可实现，已自动化集成。**

| 评估项 | 结论 |
|--------|------|
| 技术可行性 | ✅ 可行：GitHub Desktop 是 Electron 应用，字符串可通过补丁替换 |
| 自动化程度 | ✅ 全自动：翻译更新后 Actions 自动构建、自动发 Release |
| 持久性 | ✅ 持久：Windows 计划任务确保更新后自动重打补丁 |
| 翻译覆盖率 | ✅ 全面：覆盖菜单/主界面/对话框/状态信息共 ${{ TRANS_COUNT }} 条 |
| 风险 | ⚠️ 低风险：原始文件自动备份，可一键恢复英文版 |

---

## 🚀 安装方法

### 方法一：一键在线安装（最简单，推荐）

**Windows** — 以**管理员身份**打开 PowerShell，粘贴运行：

```powershell
irm https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.ps1 | iex
```

**macOS** — 打开终端，粘贴运行：

```bash
curl -fsSL https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.sh | bash
```

### 方法二：从 GitHub Release 下载安装包

1. 进入本仓库 [Releases 页面](../../releases)
2. 下载最新的 `github-desktop-zh-CN-v3.5.7.zip`
3. 解压后运行对应系统的脚本

### 方法三：克隆仓库后本地运行

```bash
# 克隆仓库
git clone https://github.com/zhizhi200271/-.git
cd -/github-desktop-zh-CN/scripts

# Windows
powershell -ExecutionPolicy Bypass -File apply-patch.ps1

# macOS
chmod +x apply-patch.sh && bash apply-patch.sh
```

---

## 🔄 自动化工作流说明

本语言包完全集成在仓库的 GitHub Actions 工作流中：

```
修改翻译文件 → 推送到 main
       │
       ▼
┌─────────────────────────────┐
│  Actions 自动触发            │
│  ✅ 验证翻译文件格式          │
│  📊 统计翻译条目数量          │
└─────────────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  自动打包                    │
│  📦 生成补丁包 ZIP           │
│  📝 生成安装脚本             │
│  📄 生成安装文档             │
└─────────────────────────────┘
       │
       ▼
┌─────────────────────────────┐
│  自动发布 Release            │
│  🚀 创建/更新 Release        │
│  📥 上传 ZIP 附件            │
│  📋 写入安装说明             │
└─────────────────────────────┘
```

**之之只需**：修改翻译文件并推送到 main → Actions 自动完成剩余所有工作。

---

## 📋 手动干预步骤（之之必读）

> 以下是需要您手动完成的操作，仅需**一次**：

### 第一次使用（必须手动执行）

**步骤 1：以管理员身份运行 PowerShell**
1. 按 `Win + X`
2. 选择「Windows PowerShell（管理员）」或「终端（管理员）」

**步骤 2：粘贴并运行一键安装命令**
```powershell
irm https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.ps1 | iex
```

**步骤 3：等待脚本完成**
- 脚本会自动：找到 GitHub Desktop 安装目录 → 备份原文件 → 应用中文补丁 → 设置自动更新守护

**步骤 4：重启 GitHub Desktop**
- 关闭 GitHub Desktop → 重新打开
- 界面即显示简体中文 ✅

### 之后的使用（全自动，无需干预）

- GitHub Desktop **自动更新**后：Windows 计划任务会在下次登录时**自动重新应用**中文补丁
- 翻译文件更新后：Actions 自动构建新版补丁包，无需手动操作

---

## 🔧 翻译覆盖范围

| 区域 | 翻译项数 | 状态 |
|------|---------|------|
| 菜单栏（文件/编辑/视图/仓库/分支/帮助） | ~60 项 | ✅ 完整 |
| 工具栏（仓库/分支/推送拉取按钮） | ~20 项 | ✅ 完整 |
| 更改面板（提交/暂存/放弃） | ~30 项 | ✅ 完整 |
| 历史面板（提交历史/操作） | ~20 项 | ✅ 完整 |
| 分支面板（新建/合并/变基） | ~20 项 | ✅ 完整 |
| 克隆/新建仓库对话框 | ~25 项 | ✅ 完整 |
| 登录/账户对话框 | ~20 项 | ✅ 完整 |
| 设置/偏好对话框 | ~15 项 | ✅ 完整 |
| 冲突解决对话框 | ~15 项 | ✅ 完整 |
| 状态栏/通知/错误信息 | ~50 项 | ✅ 完整 |
| 通用按钮/标签 | ~40 项 | ✅ 完整 |

---

## ⚠️ 注意事项

1. **需要 Node.js**：补丁脚本使用 Node.js 处理 `.asar` 文件。如未安装，请先访问 [nodejs.org](https://nodejs.org) 下载安装。

2. **自动备份**：脚本运行前会自动备份原始 `app.asar` 文件，可随时恢复英文版本。

3. **GitHub Desktop 版本**：本补丁专为 v3.5.7 设计。如使用其他版本，可修改脚本中的版本号参数。

4. **安全性**：补丁仅替换 UI 字符串，不修改任何功能代码，安全可靠。

5. **恢复英文版本**：
   - Windows：运行 `scripts/restore.ps1`
   - macOS：`cp "/Applications/GitHub Desktop.app/Contents/Resources/app.asar.zh-cn-backup" "/Applications/GitHub Desktop.app/Contents/Resources/app.asar"`

---

## 📁 文件结构

```
github-desktop-zh-CN/
├── README.md                    # 本文档
├── translations/
│   └── zh-CN.json              # 完整简体中文翻译（500+ 条）
└── scripts/
    ├── apply-patch.ps1         # Windows 自动补丁脚本
    ├── apply-patch.sh          # macOS 自动补丁脚本
    └── restore.ps1             # 恢复英文版本脚本

.github/workflows/
└── build-zh-cn-patch.yml      # Actions 自动构建工作流
```

---

*🤖 铸码 · CMS-CORE-001 · 自动化语言包系统*
*👤 主控: 之之 (zhizhi200271)*
