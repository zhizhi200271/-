# 🇨🇳 GitHub Desktop 3.5.7 简体中文语言包

> 由 **铸码 CMS-CORE-001** 全自动构建 | 主控: 之之 (zhizhi200271)

---

## 📋 当前状态

| 项目 | 状态 |
|------|------|
| 翻译文件 | ✅ 已完成（500+ 条） |
| Windows 补丁脚本 | ✅ 已完成 |
| macOS 补丁脚本 | ✅ 已完成 |
| 自动构建工作流 | ✅ 已完成 |

---

## 🚀 之之的使用步骤（按顺序操作）

### 第一步：合并 PR，让代码进入主分支

1. 打开浏览器，进入：**https://github.com/zhizhi200271/-/pull/2**
2. 如果看到 **"This pull request is still a draft"**，先点击 **"Ready for review"** 按钮
3. 然后点击绿色的 **"Merge pull request"** → **"Confirm merge"**
4. 合并完成，页面显示 "Pull request successfully merged and closed" ✅

---

### 第二步：等待 Actions 自动构建（约 1 分钟）

合并后，GitHub Actions 会自动运行，步骤如下：

1. 进入：**https://github.com/zhizhi200271/-/actions**
2. 找到 **"🇨🇳 构建 GitHub Desktop 中文语言包"** 这条记录
3. 等待它变成绿色 ✅（表示构建成功）
4. 构建完成后，会自动在 Releases 页面发布中文安装包

---

### 第三步：在你的电脑上运行安装（一次性操作）

**Windows 系统（推荐方法）：**

1. 按 `Win + X`，选择 **"Windows PowerShell（管理员）"** 或 **"终端（管理员）"**
2. 粘贴以下命令，按回车：

```powershell
irm https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.ps1 | iex
```

3. 脚本会自动完成所有操作（需要约 1~2 分钟）
4. **关闭并重新打开 GitHub Desktop** → 界面变为中文 ✅

> ⚠️ **前置条件**：需要安装 [Node.js](https://nodejs.org/zh-cn/)（免费，直接下一步安装即可）。如果没有安装，脚本会提示你。

**macOS 系统：**

打开"终端"，粘贴以下命令，按回车：

```bash
curl -fsSL https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/apply-patch.sh | bash
```

---

### 第四步：之后无需任何操作

- ✅ GitHub Desktop **自动更新**后：Windows 会通过系统计划任务**自动重新应用**中文
- ✅ 翻译内容更新：Actions 自动重新构建，你只需重新运行一次第三步命令

---

## ❓ 常见问题

### Q：运行命令时提示"找不到 Node.js"怎么办？

A：访问 https://nodejs.org/zh-cn/ → 下载 LTS 版本 → 安装完成后重新运行命令。

### Q：想恢复回英文界面怎么办？

A：以管理员身份运行 PowerShell，执行：

```powershell
irm https://raw.githubusercontent.com/zhizhi200271/-/main/github-desktop-zh-CN/scripts/restore.ps1 | iex
```

### Q：Actions 构建失败或显示"action required"怎么办？

A：
1. 进入 https://github.com/zhizhi200271/-/actions
2. 找到失败或等待审核的运行记录，点击进入
3. 点击 **"Approve and run"** 按钮批准运行

### Q：PR 合并后 Actions 没有自动运行？

A：手动触发：进入 https://github.com/zhizhi200271/-/actions/workflows/build-zh-cn-patch.yml → 点击 **"Run workflow"** → 点击绿色 **"Run workflow"** 按钮。

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
    ├── apply-patch.sh          ← macOS 补丁脚本
    └── restore.ps1             ← 恢复英文版本脚本

.github/workflows/
└── build-zh-cn-patch.yml      ← 自动构建工作流（合并到 main 自动触发）
```

---

*🤖 铸码 · CMS-CORE-001 · 自动化语言包系统*
*👤 主控: 之之 (zhizhi200271)*

