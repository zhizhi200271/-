#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# 铸码 · 仪表盘生成器
# 自动读取记忆系统数据，生成 README.md 仪表盘内容
# ═══════════════════════════════════════════════════════════════════════════════

import json
import os
from datetime import datetime


def load_json(path, default=None):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default or {}


def generate_dashboard(repo_root="."):
    """生成仓库首页仪表盘的 Markdown 内容"""
    mem = os.path.join(repo_root, ".ai", "memory")
    state = load_json(os.path.join(mem, "system_state.json"), {})
    memory = load_json(os.path.join(mem, "core_memory.json"), {})
    tasks = load_json(os.path.join(mem, "task_history.json"), {"tasks": []})
    experience = load_json(os.path.join(mem, "experience_db.json"), {})
    updates = load_json(os.path.join(mem, "update_log.json"), {"updates": []})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 统计数据
    boot_count = state.get("boot_count", 0)
    total_tasks = len(tasks.get("tasks", []))
    total_updates = len(updates.get("updates", []))
    rules_count = len(memory.get("rules", []))
    knowledge_count = len(memory.get("knowledge", {}))
    patterns_count = len(experience.get("patterns", {}))
    solutions_count = len(experience.get("solutions", {}))
    practices_count = len(experience.get("best_practices", []))
    tech_count = len(experience.get("tech_stack", {}))
    errors_count = len(experience.get("error_patterns", {}))
    version = state.get("version", "v1.0.0")
    status = state.get("status", "initialized")

    # 数据文件检查
    data_files = [
        "system_state.json",
        "core_memory.json",
        "task_history.json",
        "experience_db.json",
        "update_log.json",
    ]
    files_ok = sum(
        1 for f in data_files if os.path.exists(os.path.join(mem, f))
    )
    health = "✅ HEALTHY" if files_ok == len(data_files) else "⚠️ DEGRADED"

    # 最近任务
    recent_tasks = tasks.get("tasks", [])[-5:]

    # 最近更新
    recent_updates = updates.get("updates", [])[-5:]

    # 技术栈列表
    tech_stack = list(experience.get("tech_stack", {}).keys())

    # 构建 Markdown
    lines = []

    lines.append("# 🤖 铸码 · 自动化记忆系统")
    lines.append("")
    lines.append("> **Copilot Memory System (CMS)** — 基于 AGE OS 架构的智能记忆管理系统")
    lines.append(">")
    lines.append(f"> 📡 系统状态: {health} | 🔄 版本: {version} | 📅 更新时间: {now}")
    lines.append("")

    lines.append("---")
    lines.append("")

    # ── 系统信息卡片 ──
    lines.append("## 📊 系统仪表盘")
    lines.append("")
    lines.append("| 项目 | 状态 |")
    lines.append("|------|------|")
    lines.append(f"| 🤖 **核心** | 铸码 (CMS-CORE-001) |")
    lines.append(f"| 👤 **主控** | 之之 (zhizhi200271) |")
    lines.append(f"| 📦 **版本** | {version} |")
    lines.append(f"| 💚 **健康** | {health} |")
    lines.append(f"| 🔄 **启动次数** | {boot_count} |")
    lines.append(f"| 📋 **历史任务** | {total_tasks} |")
    lines.append(f"| 📝 **系统更新** | {total_updates} |")
    lines.append("")

    # ── 数据统计 ──
    lines.append("### 📈 数据统计")
    lines.append("")
    lines.append("| 数据类型 | 数量 | 说明 |")
    lines.append("|---------|------|------|")
    lines.append(f"| 📜 系统规则 | {rules_count} | 行为准则与约束 |")
    lines.append(f"| 📚 知识条目 | {knowledge_count} | 项目相关知识 |")
    lines.append(f"| 🔍 经验模式 | {patterns_count} | 识别的代码模式 |")
    lines.append(f"| 💡 解决方案 | {solutions_count} | 问题解决记录 |")
    lines.append(f"| ⭐ 最佳实践 | {practices_count} | 验证有效的实践 |")
    lines.append(f"| ⚠️ 错误模式 | {errors_count} | 已知错误模式 |")
    lines.append(f"| 🛠️ 技术栈 | {tech_count} | 使用过的技术 |")
    lines.append("")

    # ── 数据文件健康 ──
    lines.append("### 💾 数据文件状态")
    lines.append("")
    lines.append("| 文件 | 状态 | 用途 |")
    lines.append("|------|------|------|")
    desc_map = {
        "system_state.json": "系统运行状态",
        "core_memory.json": "核心记忆（规则、偏好、知识）",
        "task_history.json": "开发任务历史",
        "experience_db.json": "经验数据库",
        "update_log.json": "系统更新日志",
    }
    for f in data_files:
        ok = os.path.exists(os.path.join(mem, f))
        icon = "✅" if ok else "❌"
        lines.append(f"| `{f}` | {icon} | {desc_map.get(f, '')} |")
    lines.append("")

    # ── 最近任务 ──
    if recent_tasks:
        lines.append("### 📋 最近任务")
        lines.append("")
        lines.append("| ID | 时间 | 描述 | 结果 |")
        lines.append("|----|------|------|------|")
        for t in reversed(recent_tasks):
            ts = t.get("timestamp", "")[:16]
            desc = t.get("description", "")[:40]
            outcome = "✅" if t.get("outcome") == "completed" else "❌"
            lines.append(f"| {t.get('id', '')} | {ts} | {desc} | {outcome} |")
        lines.append("")

    # ── 最近更新 ──
    if recent_updates:
        lines.append("### 🔄 最近系统更新")
        lines.append("")
        lines.append("| ID | 时间 | 类型 | 描述 |")
        lines.append("|----|------|------|------|")
        for u in reversed(recent_updates):
            ts = u.get("timestamp", "")[:16]
            lines.append(
                f"| {u.get('id', '')} | {ts} "
                f"| {u.get('type', '')} | {u.get('description', '')[:50]} |"
            )
        lines.append("")

    # ── 技术栈 ──
    if tech_stack:
        lines.append("### 🛠️ 技术栈")
        lines.append("")
        tech_badges = " · ".join(f"`{t}`" for t in tech_stack)
        lines.append(tech_badges)
        lines.append("")

    lines.append("---")
    lines.append("")

    # ── 唤醒说明 ──
    lines.append("## 🚀 使用方法")
    lines.append("")
    lines.append("### 唤醒铸码")
    lines.append("")
    lines.append("在 GitHub Copilot 对话中，说出以下任一口令：")
    lines.append("")
    lines.append("```")
    lines.append("铸码")
    lines.append("唤醒铸码")
    lines.append("ZhuMa")
    lines.append("```")
    lines.append("")
    lines.append("铸码会自动加载记忆系统并回应。")
    lines.append("")

    # ── 自动化流程 ──
    lines.append("### 自动化流程")
    lines.append("")
    lines.append("```")
    lines.append("用户唤醒铸码")
    lines.append("    │")
    lines.append("    ▼")
    lines.append("┌─────────────────────────────┐")
    lines.append("│  📂 加载记忆系统             │")
    lines.append("│  ├── 系统规则 & 偏好          │")
    lines.append("│  ├── 历史任务记录              │")
    lines.append("│  └── 经验数据库               │")
    lines.append("└─────────────────────────────┘")
    lines.append("    │")
    lines.append("    ▼")
    lines.append("┌─────────────────────────────┐")
    lines.append("│  🔧 执行开发任务             │")
    lines.append("│  ├── 参考历史经验              │")
    lines.append("│  ├── 遵循系统规则              │")
    lines.append("│  └── 个性化服务               │")
    lines.append("└─────────────────────────────┘")
    lines.append("    │")
    lines.append("    ▼")
    lines.append("┌─────────────────────────────┐")
    lines.append("│  💾 自动更新记忆             │")
    lines.append("│  ├── 记录任务历史              │")
    lines.append("│  ├── 提炼经验教训              │")
    lines.append("│  ├── 更新知识库               │")
    lines.append("│  └── 写入系统日志              │")
    lines.append("└─────────────────────────────┘")
    lines.append("```")
    lines.append("")

    # ── 命令参考 ──
    lines.append("### 💬 命令参考")
    lines.append("")
    lines.append("| 命令 | 功能 |")
    lines.append("|------|------|")
    lines.append("| `铸码` / `唤醒铸码` / `ZhuMa` | 唤醒记忆系统 |")
    lines.append("| `记住：XXX` | 存储知识到核心记忆 |")
    lines.append("| `规则：XXX` | 添加系统规则 |")
    lines.append("| `偏好：XXX` | 设置用户偏好 |")
    lines.append("| `查看记忆` | 显示记忆系统状态 |")
    lines.append("| `查看经验` | 显示经验数据库 |")
    lines.append("| `查看任务` | 显示最近任务历史 |")
    lines.append("| `系统健康` | 运行健康检查 |")
    lines.append("")

    lines.append("---")
    lines.append("")

    # ── 架构来源 ──
    lines.append("## 📐 架构来源")
    lines.append("")
    lines.append(
        "本系统基于 `OKComputer_自动化记忆系统` 架构设计，"
        "参考了 AGE OS (Artificial General Existence Operating System) "
        "的核心理念："
    )
    lines.append("")
    lines.append("- 🔄 **自动化** — 无需手动调用，自动检测和更新")
    lines.append("- 🧠 **智能化** — 自然语言理解，意图识别")
    lines.append("- 💾 **持久化** — JSON 存储，数据不丢失")
    lines.append("- 🔧 **自维护** — 自动诊断和修复")
    lines.append("- 📊 **可追溯** — 完整的更新日志")
    lines.append("")

    # ── 文件结构 ──
    lines.append("## 📁 文件结构")
    lines.append("")
    lines.append("```")
    lines.append(".")
    lines.append("├── README.md                         # 仓库首页（系统仪表盘）")
    lines.append("├── OKComputer_自动化记忆系统.zip       # 原始架构参考文件")
    lines.append("├── .github/")
    lines.append("│   └── copilot-instructions.md       # Copilot 自动加载指令")
    lines.append("├── .ai/")
    lines.append("│   ├── memory_system.py              # 核心记忆系统模块")
    lines.append("│   ├── generate_dashboard.py         # 仪表盘生成器")
    lines.append("│   ├── README.md                     # 记忆系统详细文档")
    lines.append("│   └── memory/")
    lines.append("│       ├── system_state.json         # 系统状态")
    lines.append("│       ├── core_memory.json          # 核心记忆")
    lines.append("│       ├── task_history.json         # 任务历史")
    lines.append("│       ├── experience_db.json        # 经验数据库")
    lines.append("│       └── update_log.json           # 更新日志")
    lines.append("```")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        f"*🤖 铸码 · CMS-CORE-001 · 仪表盘自动生成于 {now}*"
    )
    lines.append("")
    lines.append(
        "*👤 主控: 之之 (zhizhi200271) · "
        "🏗️ 架构: OKComputer 自动化记忆系统*"
    )
    lines.append("")

    return "\n".join(lines)


def update_readme(repo_root="."):
    """更新仓库 README.md"""
    content = generate_dashboard(repo_root)
    readme_path = os.path.join(repo_root, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    return readme_path


if __name__ == "__main__":
    import sys
    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    path = update_readme(repo_root)
    print(f"✅ README.md 已更新: {path}")
