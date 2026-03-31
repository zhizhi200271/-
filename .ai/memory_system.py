#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════════
# 铸码 · 自动化记忆系统 · CMS v1.0.0
# Copilot Memory System · 语言驱动的仓库智能记忆管理
#
# 核心: 铸码 (CMS-CORE-001)
# 主控: 之之 (zhizhi200271)
# ═══════════════════════════════════════════════════════════════════════════════

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any


# ═══════════════════════════════════════════════════════════════════════════════
# 系统配置
# ═══════════════════════════════════════════════════════════════════════════════

class SystemConfig:
    """铸码记忆系统配置"""
    # 核心身份
    CORE_NAME = "铸码"
    CORE_ID = "CMS-CORE-001"
    FULL_NAME = "铸码 · Copilot Memory System · 自动化记忆核心"
    VERSION = "v1.0.0"

    # 主控
    MASTER_NAME = "之之"
    MASTER_ID = "zhizhi200271"

    # 唤醒口令
    WAKEUP_COMMANDS = ["铸码", "唤醒铸码", "ZhuMa"]
    WAKEUP_RESPONSE = (
        "铸码已上线。主控：之之。系统版本：CMS v1.0.0。"
        "自动化记忆系统就绪，等待指令。"
    )

    # 数据路径 (相对于仓库根目录)
    DATA_DIR = ".ai/memory"
    SYSTEM_STATE_FILE = f"{DATA_DIR}/system_state.json"
    CORE_MEMORY_FILE = f"{DATA_DIR}/core_memory.json"
    TASK_HISTORY_FILE = f"{DATA_DIR}/task_history.json"
    EXPERIENCE_DB_FILE = f"{DATA_DIR}/experience_db.json"
    UPDATE_LOG_FILE = f"{DATA_DIR}/update_log.json"


# ═══════════════════════════════════════════════════════════════════════════════
# 记忆存储引擎
# ═══════════════════════════════════════════════════════════════════════════════

class MemoryStore:
    """JSON 文件持久化存储引擎"""

    def __init__(self, base_dir: str = "."):
        self.base_dir = base_dir

    def _resolve(self, path: str) -> str:
        return os.path.join(self.base_dir, path)

    def load(self, path: str, default: Any = None) -> Any:
        full_path = self._resolve(path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return default if default is not None else {}

    def save(self, path: str, data: Any) -> None:
        full_path = self._resolve(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════════════════════
# 核心记忆管理器
# ═══════════════════════════════════════════════════════════════════════════════

class CoreMemory:
    """核心记忆 — 规则、偏好、知识"""

    def __init__(self, store: MemoryStore):
        self.store = store
        self.data = store.load(SystemConfig.CORE_MEMORY_FILE, {
            "rules": [],
            "preferences": {},
            "knowledge": {},
            "repo_context": {}
        })

    def add_rule(self, rule: str) -> str:
        if rule not in self.data["rules"]:
            self.data["rules"].append(rule)
            self.save()
            return f"✅ 规则已添加: {rule}"
        return f"ℹ️ 规则已存在: {rule}"

    def set_preference(self, key: str, value: str) -> str:
        self.data["preferences"][key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        self.save()
        return f"✅ 偏好已设置: {key} = {value}"

    def store_knowledge(self, key: str, content: str) -> str:
        self.data["knowledge"][key] = {
            "content": content,
            "created_at": datetime.now().isoformat()
        }
        self.save()
        return f"✅ 知识已存储: {key}"

    def update_repo_context(self, context: Dict) -> None:
        self.data["repo_context"].update(context)
        self.data["repo_context"]["last_scanned"] = datetime.now().isoformat()
        self.save()

    def get_rules(self) -> List[str]:
        return self.data.get("rules", [])

    def get_all(self) -> Dict:
        return self.data

    def save(self) -> None:
        self.store.save(SystemConfig.CORE_MEMORY_FILE, self.data)


# ═══════════════════════════════════════════════════════════════════════════════
# 任务历史管理器
# ═══════════════════════════════════════════════════════════════════════════════

class TaskHistory:
    """开发任务历史记录"""

    def __init__(self, store: MemoryStore):
        self.store = store
        self.data = store.load(SystemConfig.TASK_HISTORY_FILE, {"tasks": []})

    def record_task(self, task: Dict) -> str:
        task_entry = {
            "id": f"TASK-{len(self.data['tasks']) + 1:04d}",
            "timestamp": datetime.now().isoformat(),
            "description": task.get("description", ""),
            "type": task.get("type", "development"),
            "files_changed": task.get("files_changed", []),
            "outcome": task.get("outcome", "completed"),
            "lessons_learned": task.get("lessons_learned", []),
            "tags": task.get("tags", [])
        }
        self.data["tasks"].append(task_entry)
        self.save()
        return task_entry["id"]

    def get_recent(self, limit: int = 10) -> List[Dict]:
        return self.data["tasks"][-limit:]

    def get_by_type(self, task_type: str) -> List[Dict]:
        return [t for t in self.data["tasks"] if t.get("type") == task_type]

    def get_all(self) -> List[Dict]:
        return self.data["tasks"]

    def save(self) -> None:
        self.store.save(SystemConfig.TASK_HISTORY_FILE, self.data)


# ═══════════════════════════════════════════════════════════════════════════════
# 经验数据库
# ═══════════════════════════════════════════════════════════════════════════════

class ExperienceDB:
    """经验积累数据库 — 从历史任务中提炼的智慧"""

    def __init__(self, store: MemoryStore):
        self.store = store
        self.data = store.load(SystemConfig.EXPERIENCE_DB_FILE, {
            "patterns": {},
            "solutions": {},
            "best_practices": [],
            "error_patterns": {},
            "tech_stack": {}
        })

    def add_pattern(self, pattern_name: str, description: str,
                    example: str = "") -> str:
        self.data["patterns"][pattern_name] = {
            "description": description,
            "example": example,
            "frequency": self.data["patterns"].get(
                pattern_name, {}
            ).get("frequency", 0) + 1,
            "last_seen": datetime.now().isoformat()
        }
        self.save()
        return f"✅ 模式已记录: {pattern_name}"

    def add_solution(self, problem: str, solution: str,
                     tags: List[str] = None) -> str:
        solution_id = f"SOL-{len(self.data['solutions']) + 1:04d}"
        self.data["solutions"][solution_id] = {
            "problem": problem,
            "solution": solution,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
            "used_count": 0
        }
        self.save()
        return f"✅ 解决方案已存储: {solution_id}"

    def add_best_practice(self, practice: str, category: str = "general") -> str:
        entry = {
            "practice": practice,
            "category": category,
            "added_at": datetime.now().isoformat()
        }
        if entry not in self.data["best_practices"]:
            self.data["best_practices"].append(entry)
            self.save()
            return f"✅ 最佳实践已添加: {practice}"
        return f"ℹ️ 最佳实践已存在"

    def record_error(self, error_type: str, description: str,
                     fix: str = "") -> str:
        if error_type not in self.data["error_patterns"]:
            self.data["error_patterns"][error_type] = {
                "occurrences": 0,
                "descriptions": [],
                "fixes": []
            }
        entry = self.data["error_patterns"][error_type]
        entry["occurrences"] += 1
        entry["descriptions"].append({
            "text": description,
            "timestamp": datetime.now().isoformat()
        })
        if fix:
            entry["fixes"].append(fix)
        self.save()
        return f"✅ 错误模式已记录: {error_type}"

    def update_tech_stack(self, tech: str, details: Dict = None) -> str:
        self.data["tech_stack"][tech] = {
            **(details or {}),
            "last_used": datetime.now().isoformat()
        }
        self.save()
        return f"✅ 技术栈已更新: {tech}"

    def search(self, keyword: str) -> List[Dict]:
        results = []
        keyword_lower = keyword.lower()

        for name, pattern in self.data["patterns"].items():
            if keyword_lower in name.lower() or keyword_lower in pattern.get(
                "description", ""
            ).lower():
                results.append({"type": "pattern", "name": name, **pattern})

        for sid, solution in self.data["solutions"].items():
            if keyword_lower in solution.get(
                "problem", ""
            ).lower() or keyword_lower in solution.get("solution", "").lower():
                results.append({"type": "solution", "id": sid, **solution})

        return results

    def get_all(self) -> Dict:
        return self.data

    def save(self) -> None:
        self.store.save(SystemConfig.EXPERIENCE_DB_FILE, self.data)


# ═══════════════════════════════════════════════════════════════════════════════
# 更新日志
# ═══════════════════════════════════════════════════════════════════════════════

class UpdateLog:
    """系统更新日志"""

    def __init__(self, store: MemoryStore):
        self.store = store
        self.data = store.load(SystemConfig.UPDATE_LOG_FILE, {"updates": []})

    def log_update(self, update_type: str, description: str,
                   details: Dict = None) -> str:
        entry = {
            "id": f"UPD-{len(self.data['updates']) + 1:04d}",
            "timestamp": datetime.now().isoformat(),
            "type": update_type,
            "description": description,
            "details": details or {}
        }
        self.data["updates"].append(entry)
        self.save()
        return entry["id"]

    def get_recent(self, limit: int = 20) -> List[Dict]:
        return self.data["updates"][-limit:]

    def save(self) -> None:
        self.store.save(SystemConfig.UPDATE_LOG_FILE, self.data)


# ═══════════════════════════════════════════════════════════════════════════════
# 系统状态管理
# ═══════════════════════════════════════════════════════════════════════════════

class SystemState:
    """系统运行状态"""

    def __init__(self, store: MemoryStore):
        self.store = store
        self.data = store.load(SystemConfig.SYSTEM_STATE_FILE, {
            "core_name": SystemConfig.CORE_NAME,
            "core_id": SystemConfig.CORE_ID,
            "version": SystemConfig.VERSION,
            "master": SystemConfig.MASTER_NAME,
            "boot_count": 0,
            "last_boot": None,
            "total_tasks": 0,
            "total_updates": 0,
            "status": "initialized",
            "created_at": datetime.now().isoformat()
        })

    def boot(self) -> Dict:
        self.data["boot_count"] += 1
        self.data["last_boot"] = datetime.now().isoformat()
        self.data["status"] = "awake"
        self.save()
        return self.data

    def increment_tasks(self) -> None:
        self.data["total_tasks"] += 1
        self.save()

    def increment_updates(self) -> None:
        self.data["total_updates"] += 1
        self.save()

    def get_status(self) -> Dict:
        return self.data

    def save(self) -> None:
        self.store.save(SystemConfig.SYSTEM_STATE_FILE, self.data)


# ═══════════════════════════════════════════════════════════════════════════════
# 铸码 · 核心大脑
# ═══════════════════════════════════════════════════════════════════════════════

class ZhuMaCore:
    """
    铸码核心大脑 · CMS-CORE-001
    自动化记忆系统的中枢控制器
    """

    def __init__(self, repo_root: str = "."):
        self.repo_root = repo_root
        self.store = MemoryStore(repo_root)
        self.state = SystemState(self.store)
        self.memory = CoreMemory(self.store)
        self.tasks = TaskHistory(self.store)
        self.experience = ExperienceDB(self.store)
        self.update_log = UpdateLog(self.store)
        self.is_awake = False

    def boot(self) -> str:
        """启动系统"""
        state = self.state.boot()
        self.is_awake = True

        self.update_log.log_update(
            "system_boot",
            f"系统启动 (第 {state['boot_count']} 次)",
            {"version": SystemConfig.VERSION}
        )

        return (
            f"🤖 {SystemConfig.CORE_NAME} 已上线 "
            f"(第 {state['boot_count']} 次启动)\n"
            f"   主控: {SystemConfig.MASTER_NAME}\n"
            f"   版本: {SystemConfig.VERSION}\n"
            f"   历史任务: {state['total_tasks']}\n"
            f"   系统更新: {state['total_updates']}\n"
            f"   记忆系统就绪，等待指令。"
        )

    def complete_task(self, description: str, files_changed: List[str] = None,
                      lessons: List[str] = None, tags: List[str] = None,
                      task_type: str = "development") -> str:
        """完成任务后的记忆更新"""
        task_id = self.tasks.record_task({
            "description": description,
            "type": task_type,
            "files_changed": files_changed or [],
            "outcome": "completed",
            "lessons_learned": lessons or [],
            "tags": tags or []
        })

        self.state.increment_tasks()

        for lesson in (lessons or []):
            self.experience.add_best_practice(lesson, category=task_type)

        self.update_log.log_update(
            "task_completed",
            f"任务完成: {description}",
            {
                "task_id": task_id,
                "files": files_changed or [],
                "lessons": lessons or []
            }
        )

        self.state.increment_updates()

        return (
            f"✅ 任务已记录 [{task_id}]\n"
            f"   描述: {description}\n"
            f"   文件变更: {len(files_changed or [])} 个\n"
            f"   经验提炼: {len(lessons or [])} 条"
        )

    def remember(self, key: str, content: str) -> str:
        """存储知识到核心记忆"""
        result = self.memory.store_knowledge(key, content)
        self.update_log.log_update(
            "memory_store", f"存储知识: {key}", {"content": content}
        )
        self.state.increment_updates()
        return result

    def add_rule(self, rule: str) -> str:
        """添加系统规则"""
        result = self.memory.add_rule(rule)
        self.update_log.log_update("rule_add", f"添加规则: {rule}")
        self.state.increment_updates()
        return result

    def record_experience(self, pattern: str, description: str,
                          example: str = "") -> str:
        """记录经验模式"""
        result = self.experience.add_pattern(pattern, description, example)
        self.update_log.log_update(
            "experience_record",
            f"记录经验: {pattern}",
            {"description": description}
        )
        self.state.increment_updates()
        return result

    def record_solution(self, problem: str, solution: str,
                        tags: List[str] = None) -> str:
        """记录问题解决方案"""
        result = self.experience.add_solution(problem, solution, tags)
        self.update_log.log_update(
            "solution_record",
            f"记录方案: {problem[:50]}",
            {"solution": solution[:100]}
        )
        self.state.increment_updates()
        return result

    def search_experience(self, keyword: str) -> List[Dict]:
        """搜索经验库"""
        return self.experience.search(keyword)

    def get_context_prompt(self) -> str:
        """生成包含记忆上下文的系统提示词"""
        memory = self.memory.get_all()
        state = self.state.get_status()
        recent_tasks = self.tasks.get_recent(5)
        experience = self.experience.get_all()

        prompt_parts = [
            f"# {SystemConfig.FULL_NAME}",
            f"",
            f"## 系统状态",
            f"- 核心: {SystemConfig.CORE_NAME} ({SystemConfig.CORE_ID})",
            f"- 主控: {SystemConfig.MASTER_NAME}",
            f"- 版本: {SystemConfig.VERSION}",
            f"- 启动次数: {state.get('boot_count', 0)}",
            f"- 历史任务: {state.get('total_tasks', 0)}",
            f"",
        ]

        rules = memory.get("rules", [])
        if rules:
            prompt_parts.append("## 系统规则")
            for rule in rules:
                prompt_parts.append(f"- {rule}")
            prompt_parts.append("")

        prefs = memory.get("preferences", {})
        if prefs:
            prompt_parts.append("## 用户偏好")
            for key, val in prefs.items():
                prompt_parts.append(f"- {key}: {val.get('value', val)}")
            prompt_parts.append("")

        if recent_tasks:
            prompt_parts.append("## 最近任务")
            for task in recent_tasks:
                prompt_parts.append(
                    f"- [{task['id']}] {task['description']} "
                    f"({task.get('outcome', 'unknown')})"
                )
            prompt_parts.append("")

        practices = experience.get("best_practices", [])
        if practices:
            prompt_parts.append("## 最佳实践")
            for p in practices[-10:]:
                prompt_parts.append(f"- [{p.get('category', 'general')}] {p['practice']}")
            prompt_parts.append("")

        tech = experience.get("tech_stack", {})
        if tech:
            prompt_parts.append("## 技术栈")
            for name in tech:
                prompt_parts.append(f"- {name}")
            prompt_parts.append("")

        return "\n".join(prompt_parts)

    def health_check(self) -> str:
        """系统健康检查"""
        state = self.state.get_status()
        memory = self.memory.get_all()
        tasks = self.tasks.get_all()
        experience = self.experience.get_all()

        lines = [
            f"🏥 {SystemConfig.CORE_NAME} 系统健康报告",
            "=" * 50,
            f"检查时间: {datetime.now().isoformat()[:19]}",
            f"系统版本: {SystemConfig.VERSION}",
            f"",
            f"📊 数据统计:",
            f"  启动次数: {state.get('boot_count', 0)}",
            f"  历史任务: {len(tasks)}",
            f"  系统规则: {len(memory.get('rules', []))}",
            f"  知识条目: {len(memory.get('knowledge', {}))}",
            f"  经验模式: {len(experience.get('patterns', {}))}",
            f"  解决方案: {len(experience.get('solutions', {}))}",
            f"  最佳实践: {len(experience.get('best_practices', []))}",
            f"  技术栈: {len(experience.get('tech_stack', {}))}",
            f"  更新日志: {state.get('total_updates', 0)}",
            f"",
        ]

        checks = []
        for fname in [
            SystemConfig.SYSTEM_STATE_FILE,
            SystemConfig.CORE_MEMORY_FILE,
            SystemConfig.TASK_HISTORY_FILE,
            SystemConfig.EXPERIENCE_DB_FILE,
            SystemConfig.UPDATE_LOG_FILE,
        ]:
            full = os.path.join(self.repo_root, fname)
            ok = os.path.exists(full)
            checks.append((fname, ok))

        lines.append("📁 数据文件:")
        all_ok = True
        for fname, ok in checks:
            icon = "✅" if ok else "❌"
            lines.append(f"  {icon} {fname}")
            if not ok:
                all_ok = False

        lines.append("")
        status = "✅ HEALTHY" if all_ok else "⚠️ 需要修复"
        lines.append(f"整体状态: {status}")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 便捷函数
# ═══════════════════════════════════════════════════════════════════════════════

def create_system(repo_root: str = ".") -> ZhuMaCore:
    """创建铸码记忆系统实例"""
    return ZhuMaCore(repo_root)


def boot_system(repo_root: str = ".") -> ZhuMaCore:
    """创建并启动铸码记忆系统"""
    core = create_system(repo_root)
    print(core.boot())
    return core


# ═══════════════════════════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    repo_root = sys.argv[1] if len(sys.argv) > 1 else "."
    core = boot_system(repo_root)
    print("\n" + core.health_check())
    print("\n" + core.get_context_prompt())
