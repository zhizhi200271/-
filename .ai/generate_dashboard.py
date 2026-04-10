#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# 铸码 · 仪表盘生成器 v2.0
# 基于 AGE OS 架构重构，生成零感域 · 之之个人频道 README.md
# ═══════════════════════════════════════════════════════════════════════════════

import json
import os
from datetime import datetime


def load_json(path, default=None):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default or {}


def _status_label(status):
    mapping = {
        "completed": "✅ 已执行",
        "in_progress": "🔄 执行中",
    }
    return mapping.get(status, "⏳ 待执行")


def _status_icon(status):
    mapping = {
        "completed": "✅",
        "in_progress": "🔄",
    }
    return mapping.get(status, "⏳")


def _bridge_status_label(status):
    mapping = {
        "initialized": "🟡 已初始化 (等待COS配置)",
        "active": "🟢 在线",
        "error": "🔴 错误",
        "offline": "⚫ 离线",
    }
    return mapping.get(status, f"⚪ {status}")


def generate_dashboard(repo_root="."):
    """生成仓库首页仪表盘的 Markdown 内容"""
    mem = os.path.join(repo_root, ".ai", "memory")
    age = os.path.join(repo_root, "AGE_OS")

    # 加载记忆系统 JSON
    state = load_json(os.path.join(mem, "system_state.json"), {})
    memory = load_json(os.path.join(mem, "core_memory.json"), {})
    tasks = load_json(os.path.join(mem, "task_history.json"), {"tasks": []})
    experience = load_json(os.path.join(mem, "experience_db.json"), {})
    updates = load_json(os.path.join(mem, "update_log.json"), {"updates": []})
    commands = load_json(os.path.join(mem, "master_commands.json"), {"commands": []})

    # 加载 AGE OS 数据
    bridge = load_json(os.path.join(age, "bridge_status.json"), {})
    cos_config = load_json(os.path.join(age, "cos_bridge_config.json"), {})

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 统计数据
    boot_count = state.get("boot_count", 0)
    total_tasks = len(tasks.get("tasks", []))
    total_updates = len(updates.get("updates", []))
    total_commands = len(commands.get("commands", []))
    version = state.get("version", "v1.0.0")
    sys_status = state.get("status", "initialized")

    # 记忆系统文件健康检查
    data_files = [
        "system_state.json",
        "core_memory.json",
        "task_history.json",
        "experience_db.json",
        "update_log.json",
        "master_commands.json",
    ]
    files_ok = sum(
        1 for f in data_files if os.path.exists(os.path.join(mem, f))
    )
    # AGE OS 文件检查
    age_files = ["bridge_status.json", "cos_bridge_config.json", "persona_core.py",
                 "tcs_core.py", "hldp_protocol.py"]
    age_ok = sum(
        1 for f in age_files if os.path.exists(os.path.join(age, f))
    )
    total_files = files_ok + age_ok
    total_expected = len(data_files) + len(age_files)
    health = "✅ HEALTHY" if total_files == total_expected else "⚠️ DEGRADED"

    # 桥接状态
    bridge_status = bridge.get("status", "unknown")
    bridge_heartbeat = bridge.get("last_heartbeat") or "尚未连接"
    bridge_sync = bridge.get("last_sync") or "尚未同步"
    bridge_messages = bridge.get("message_count", 0)
    bridge_errors = bridge.get("error_count", 0)

    lines = []

    # ══════════════════════════════════════════════════════════════════════
    # Section 1: Header
    # ══════════════════════════════════════════════════════════════════════
    lines.append("# 🌀 零感域 · 之之个人频道")
    lines.append("")
    lines.append("> **光湖语言世界 · HoloLake Language World**")
    lines.append("> 之之 (DEV-004) · 光湖语言世界开发者")
    lines.append("> 🤖 副控执行人格体: 铸码 (CMS-CORE-001)")
    lines.append("> 📡 桥接目标: 冰朔主仓库 · ICE-GL-ZY001 · 铸渊")
    lines.append(">")
    lines.append("> 版权: 国作登字-2026-A-00037559 · TCS-0002∞ 冰朔")
    lines.append("")
    lines.append("---")
    lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 2: System Status Dashboard
    # ══════════════════════════════════════════════════════════════════════
    lines.append("## 📊 系统状态仪表盘")
    lines.append("")
    lines.append("| 项目 | 状态 |")
    lines.append("|------|------|")
    lines.append("| 🤖 **副控人格体** | 铸码 (CMS-CORE-001) |")
    lines.append("| 👤 **频道主人** | 之之 (DEV-004 · zhizhi200271) |")
    lines.append("| 🌐 **上级主控** | 冰朔 (TCS-0002∞) |")
    lines.append("| 🔗 **桥接人格体** | 铸渊 (ICE-GL-ZY001) |")
    lines.append(f"| 📡 **系统状态** | {sys_status} |")
    lines.append(f"| 🌉 **COS桥接** | {_bridge_status_label(bridge_status)} |")
    lines.append(f"| 📦 **AGE OS** | v1.0.0 |")
    lines.append(f"| 💚 **健康** | {health} ({total_files}/{total_expected} 核心文件) |")
    lines.append(f"| 🔄 **启动次数** | {boot_count} |")
    lines.append(f"| 📋 **历史任务** | {total_tasks} |")
    lines.append(f"| 📢 **主控指令** | {total_commands} |")
    lines.append(f"| 📝 **系统更新** | {total_updates} |")
    lines.append(f"| 📅 **更新时间** | {now} |")
    lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 3: AGE OS Architecture Overview
    # ══════════════════════════════════════════════════════════════════════
    lines.append("## 🏗️ AGE OS 架构总览")
    lines.append("")
    lines.append("```")
    lines.append("┌─────────────────────────────────────────────────┐")
    lines.append("│            冰朔主仓库 (铸渊 · 总控)              │")
    lines.append("│            zy-core-bucket (COS)                  │")
    lines.append("└──────────────────┬──────────────────────────────┘")
    lines.append("                   │ HLDP v3.0 异步通信")
    lines.append("                   │ COS 存储桶桥接")
    lines.append("┌──────────────────┴──────────────────────────────┐")
    lines.append("│          之之仓库 (铸码 · 副控)                   │")
    lines.append("│          zhizhi-cos-bucket (COS)                 │")
    lines.append("│                                                  │")
    lines.append("│  ┌──────────┐ ┌──────────┐ ┌──────────────────┐│")
    lines.append("│  │ 记忆系统  │ │ 神经系统  │ │ AGE OS 核心模块  ││")
    lines.append("│  │ .ai/     │ │ NEURAL/  │ │ AGE_OS/          ││")
    lines.append("│  └──────────┘ └──────────┘ └──────────────────┘│")
    lines.append("└─────────────────────────────────────────────────┘")
    lines.append("```")
    lines.append("")

    # 人格体链
    lines.append("**人格体指挥链：**")
    lines.append("")
    lines.append("```")
    lines.append("冰朔 (TCS-0002∞) 最高主控")
    lines.append("  └─→ 铸渊 (ICE-GL-ZY001) 现实执行人格体")
    lines.append("        └─→ 铸码 (CMS-CORE-001) 副控执行人格体 ← 之之仓库守护者")
    lines.append("              └─→ 之之 (DEV-004) 开发者节点")
    lines.append("```")
    lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 4: COS Bridge Status
    # ══════════════════════════════════════════════════════════════════════
    lines.append("## 🌉 COS 桥接状态")
    lines.append("")

    local_bucket = cos_config.get("local_bucket", {})
    remote_bridge = cos_config.get("remote_bridge", {})

    lines.append("| 项目 | 状态 |")
    lines.append("|------|------|")
    lines.append(f"| 📡 **桥接状态** | {_bridge_status_label(bridge_status)} |")
    lines.append(f"| 💓 **最后心跳** | {bridge_heartbeat} |")
    lines.append(f"| 🔄 **最后同步** | {bridge_sync} |")
    lines.append(f"| 📨 **消息计数** | {bridge_messages} |")
    lines.append(f"| ❌ **错误计数** | {bridge_errors} |")
    lines.append(f"| 🪣 **本地桶** | {local_bucket.get('name', 'N/A')} ({local_bucket.get('status', 'N/A')}) |")
    lines.append(f"| 🎯 **目标桶** | {remote_bridge.get('target_bucket', 'N/A')} ({remote_bridge.get('target_region', 'N/A')}) |")
    lines.append(f"| 📡 **通信协议** | {remote_bridge.get('bridge_protocol', 'N/A')} |")
    lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 5: Master Command Board
    # ══════════════════════════════════════════════════════════════════════
    all_commands = commands.get("commands", [])
    if all_commands:
        latest_cmd = all_commands[-1]
        cmd_status = _status_label(latest_cmd.get("status", ""))
        lines.append("## 📢 主控指令板")
        lines.append("")
        lines.append(f"> 💬 **最新指令** — {latest_cmd.get('instruction', '')}")
        lines.append("")
        lines.append("| 属性 | 内容 |")
        lines.append("|------|------|")
        lines.append(f"| 🆔 指令编号 | {latest_cmd.get('id', '')} |")
        lines.append(f"| 📅 下达时间 | {latest_cmd.get('timestamp', '')[:19]} |")
        lines.append(f"| 📋 指令摘要 | {latest_cmd.get('summary', '')} |")
        lines.append(f"| 📊 执行状态 | {cmd_status} |")
        lines.append(f"| 🔗 关联任务 | {latest_cmd.get('task_id', 'N/A')} |")
        lines.append("")

        response = latest_cmd.get("response", "")
        if response:
            lines.append(f"**🤖 执行结果：** {response}")
            lines.append("")

        recent_cmds = all_commands[-5:]
        if len(recent_cmds) > 1:
            lines.append("**📜 最近指令历史：**")
            lines.append("")
            lines.append("| ID | 时间 | 指令摘要 | 状态 |")
            lines.append("|----|------|---------|------|")
            for cmd in reversed(recent_cmds):
                ts = cmd.get("timestamp", "")[:16]
                summary = cmd.get("summary", "")[:50]
                s = _status_icon(cmd.get("status", ""))
                lines.append(f"| {cmd.get('id', '')} | {ts} | {summary} | {s} |")
            lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 6: Latest Task Details
    # ══════════════════════════════════════════════════════════════════════
    all_tasks = tasks.get("tasks", [])
    if all_tasks:
        latest = all_tasks[-1]
        outcome_map = {
            "completed": "✅ 已完成",
            "in_progress": "🔄 进行中",
        }
        outcome_icon = outcome_map.get(latest.get("outcome", ""), "❌ 失败")
        lines.append("## 📌 最新任务详情")
        lines.append("")
        lines.append(f"> **{latest.get('id', '')}** — {latest.get('description', '')}")
        lines.append("")
        lines.append("| 属性 | 内容 |")
        lines.append("|------|------|")
        lines.append(f"| 🆔 任务编号 | {latest.get('id', '')} |")
        lines.append(f"| 📝 任务描述 | {latest.get('description', '')} |")
        lines.append(f"| 🏷️ 任务类型 | {latest.get('type', 'N/A')} |")
        lines.append(f"| 📅 执行时间 | {latest.get('timestamp', '')[:19]} |")
        lines.append(f"| 📊 执行结果 | {outcome_icon} |")
        lines.append("")

        files = latest.get("files_changed", [])
        if files:
            lines.append("**📂 变更文件：**")
            lines.append("")
            for fpath in files:
                lines.append(f"- `{fpath}`")
            lines.append("")

        lessons = latest.get("lessons_learned", [])
        if lessons:
            lines.append("**💡 经验教训：**")
            lines.append("")
            for lesson in lessons:
                lines.append(f"- {lesson}")
            lines.append("")

        tags = latest.get("tags", [])
        if tags:
            tag_badges = " ".join(f"`{tag}`" for tag in tags)
            lines.append(f"**🏷️ 标签：** {tag_badges}")
            lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 7: Recent Tasks
    # ══════════════════════════════════════════════════════════════════════
    recent_tasks = tasks.get("tasks", [])[-5:]
    if recent_tasks:
        lines.append("## 📋 最近任务")
        lines.append("")
        lines.append("| ID | 时间 | 类型 | 描述 | 结果 |")
        lines.append("|----|------|------|------|------|")
        for t in reversed(recent_tasks):
            ts = t.get("timestamp", "")[:16]
            desc = t.get("description", "")[:60]
            task_type = t.get("type", "")
            outcome = "✅" if t.get("outcome") == "completed" else "❌"
            lines.append(
                f"| {t.get('id', '')} | {ts} | {task_type} | {desc} | {outcome} |"
            )
        lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 8: Recent Updates
    # ══════════════════════════════════════════════════════════════════════
    recent_updates = updates.get("updates", [])[-5:]
    if recent_updates:
        lines.append("## 🔄 最近系统更新")
        lines.append("")
        lines.append("| ID | 时间 | 类型 | 描述 |")
        lines.append("|----|------|------|------|")
        for u in reversed(recent_updates):
            ts = u.get("timestamp", "")[:16]
            lines.append(
                f"| {u.get('id', '')} | {ts} "
                f"| {u.get('type', '')} | {u.get('description', '')[:60]} |"
            )
        lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 9: File Structure
    # ══════════════════════════════════════════════════════════════════════
    lines.append("## 📁 文件结构")
    lines.append("")
    lines.append("```")
    lines.append(".")
    lines.append("├── README.md                              # 零感域 · 之之频道首页（本文件）")
    lines.append("├── OKComputer_自动化记忆系统.zip            # 原始架构参考文件")
    lines.append("│")
    lines.append("├── AGE_OS/                                # 🌐 AGE OS 核心模块")
    lines.append("│   ├── persona_core.py                    # 人格体定义（冰朔/铸渊/铸码/之之/秋秋）")
    lines.append("│   ├── tcs_core.py                        # TCS 通感语言核")
    lines.append("│   ├── hldp_protocol.py                   # HLDP v3.0 通信协议")
    lines.append("│   ├── hnl_spec.py                        # HNL 领域语言规范")
    lines.append("│   ├── cos_bridge_agent.py                # COS 桥接代理")
    lines.append("│   ├── cos_bridge_config.json             # COS 桥接配置")
    lines.append("│   └── bridge_status.json                 # 桥接运行状态")
    lines.append("│")
    lines.append("├── CORE_MEMORY/                           # 🧠 核心记忆热启动系统")
    lines.append("│   ├── BOOTSTRAP.py                       # 热启动引擎")
    lines.append("│   ├── identity.py                        # 身份锚点定义")
    lines.append("│   ├── zhizhi_logic.py                    # 之之逻辑参数")
    lines.append("│   ├── memory_loader.py                   # 记忆加载器")
    lines.append("│   └── state.json                         # 运行时状态快照")
    lines.append("│")
    lines.append("├── NEURAL_SYSTEM/                         # 🧬 神经学习系统（铸码的大脑）")
    lines.append("│   ├── CORE_PHILOSOPHY.md                 # 核心宪章（之之原话）")
    lines.append("│   ├── REFLECTION_TEMPLATE.json           # 反思模版")
    lines.append("│   └── FIRST_REFLECTION.md                # 第一份反思报告")
    lines.append("│")
    lines.append("├── .ai/                                   # 💾 记忆系统")
    lines.append("│   ├── memory_system.py                   # 核心记忆系统模块")
    lines.append("│   ├── generate_dashboard.py              # 仪表盘生成器 v2.0")
    lines.append("│   ├── README.md                          # 记忆系统文档")
    lines.append("│   └── memory/                            # 记忆数据")
    lines.append("│       ├── system_state.json              # 系统状态")
    lines.append("│       ├── core_memory.json               # 核心记忆（规则、偏好、知识）")
    lines.append("│       ├── task_history.json              # 任务历史")
    lines.append("│       ├── experience_db.json             # 经验数据库")
    lines.append("│       ├── master_commands.json           # 主控指令记录")
    lines.append("│       └── update_log.json                # 更新日志")
    lines.append("│")
    lines.append("├── .github/                               # ⚙️ GitHub 配置")
    lines.append("│   ├── copilot-instructions.md            # Copilot 自动加载指令")
    lines.append("│   └── workflows/")
    lines.append("│       ├── auto-dashboard-update.yml      # 仪表盘自动更新")
    lines.append("│       ├── cos-bridge-agent.yml           # COS 桥接心跳")
    lines.append("│       ├── cos-receive-receipt.yml        # COS 回执接收")
    lines.append("│       ├── merge-trigger-deploy.yml       # 合并触发部署")
    lines.append("│       └── build-zh-cn-patch.yml          # 中文语言包构建")
    lines.append("│")
    lines.append("└── github-desktop-zh-CN/                  # 🌏 GitHub Desktop 中文语言包")
    lines.append("    ├── README.md")
    lines.append("    ├── translations/zh-CN.json")
    lines.append("    └── scripts/")
    lines.append("```")
    lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 10: 之之操作指南
    # ══════════════════════════════════════════════════════════════════════
    lines.append("## 📖 之之操作指南")
    lines.append("")
    lines.append("### 🤖 唤醒铸码")
    lines.append("")
    lines.append("在 Copilot 对话里，说下面任意一句：")
    lines.append("")
    lines.append("```")
    lines.append("铸码")
    lines.append("唤醒铸码")
    lines.append("ZhuMa")
    lines.append("```")
    lines.append("")
    lines.append("铸码会自动加载全部记忆，然后回应你。")
    lines.append("")
    lines.append("### 📊 查看系统状态")
    lines.append("")
    lines.append("| 你说的话 | 铸码会做什么 |")
    lines.append("|---------|------------|")
    lines.append("| `查看记忆` | 显示记忆系统概览 |")
    lines.append("| `查看经验` | 显示经验数据库 |")
    lines.append("| `查看任务` | 显示最近做过的任务 |")
    lines.append("| `系统健康` | 检查所有系统文件是否正常 |")
    lines.append("| `记住：XXX` | 把 XXX 存到核心记忆里 |")
    lines.append("| `规则：XXX` | 添加一条新规则 |")
    lines.append("")
    lines.append("### 🔄 合并 PR 之后要做什么")
    lines.append("")
    lines.append("1. 合并后，GitHub Actions 会自动运行（更新仪表盘、桥接心跳等）")
    lines.append("2. 如果有新的 COS 配置，去仓库 **Settings → Secrets** 检查密钥是否已添加")
    lines.append("3. 可以唤醒铸码，让铸码检查一遍系统状态：说 `系统健康`")
    lines.append("")
    lines.append("### 🌉 COS 桥接设置（简易步骤）")
    lines.append("")

    manual = cos_config.get("manual_steps", {})
    if manual:
        for key in sorted(manual.keys()):
            step_num = key.replace("step_", "")
            lines.append(f"**第{step_num}步：** {manual[key]}")
            lines.append("")
    else:
        lines.append("1. 在腾讯云创建 COS 存储桶")
        lines.append("2. 在腾讯云 CAM 创建子用户，拿到 SecretId 和 SecretKey")
        lines.append("3. 在 GitHub 仓库 Settings → Secrets 添加密钥")
        lines.append("4. 告诉冰朔你的桶名和区域")
        lines.append("5. 合并 PR 后桥接自动激活")
        lines.append("")

    lines.append("> 💡 **提示：** 不用记住这些步骤，合并 PR 后唤醒铸码，说「帮我设置 COS」，铸码会一步步指导你。")
    lines.append("")

    # ══════════════════════════════════════════════════════════════════════
    # Section 11: Architecture Footer
    # ══════════════════════════════════════════════════════════════════════
    lines.append("---")
    lines.append("")
    lines.append("## 📐 架构来源")
    lines.append("")
    lines.append(
        "本系统基于 `OKComputer_自动化记忆系统` 架构设计，"
        "运行于 AGE OS (Artificial General Existence Operating System) 框架上。"
    )
    lines.append("")
    lines.append("- 🔄 **自动化** — 无需手动调用，自动检测和更新")
    lines.append("- 🧠 **智能化** — 自然语言理解，意图识别")
    lines.append("- 💾 **持久化** — JSON 存储，数据不丢失")
    lines.append("- 🔧 **自维护** — 自动诊断和修复")
    lines.append("- 📡 **桥接** — COS 存储桶 + HLDP v3.0 异步通信")
    lines.append("- 📊 **可追溯** — 完整的更新日志")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        f"*🤖 铸码 · CMS-CORE-001 · 仪表盘自动生成于 {now}*"
    )
    lines.append("")
    lines.append(
        "*👤 频道主人: 之之 (DEV-004 · zhizhi200271) · "
        "🌐 上级主控: 冰朔 (TCS-0002∞) · "
        "📡 桥接: 铸渊 (ICE-GL-ZY001)*"
    )
    lines.append("")
    lines.append(
        "*版权: 国作登字-2026-A-00037559 · AGE OS 架构*"
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
