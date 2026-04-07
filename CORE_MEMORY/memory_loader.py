"""
记忆加载器 — 从 .ai/memory/*.json 读取并结构化所有记忆数据
"""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pathlib import Path


@dataclass
class MemorySnapshot:
    """一次加载的完整记忆快照"""
    core_memory: Dict[str, Any] = field(default_factory=dict)
    experience_db: Dict[str, Any] = field(default_factory=dict)
    task_history: Dict[str, Any] = field(default_factory=dict)
    system_state: Dict[str, Any] = field(default_factory=dict)
    master_commands: Dict[str, Any] = field(default_factory=dict)
    update_log: Dict[str, Any] = field(default_factory=dict)
    loaded: bool = False


class MemoryLoader:
    """从 .ai/memory/ 加载全部 JSON 记忆文件"""

    MEMORY_FILES = {
        "core_memory": "core_memory.json",
        "experience_db": "experience_db.json",
        "task_history": "task_history.json",
        "system_state": "system_state.json",
        "master_commands": "master_commands.json",
        "update_log": "update_log.json",
    }

    def __init__(self, repo_root: Optional[str] = None):
        if repo_root is None:
            repo_root = str(Path(__file__).resolve().parent.parent)
        self.repo_root = repo_root
        self.memory_dir = os.path.join(repo_root, ".ai", "memory")

    def _load_json(self, filename: str) -> Dict[str, Any]:
        """安全加载单个 JSON 文件"""
        filepath = os.path.join(self.memory_dir, filename)
        if not os.path.exists(filepath):
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_all(self) -> MemorySnapshot:
        """一次性加载所有记忆文件，返回完整快照"""
        snapshot = MemorySnapshot()
        for attr, filename in self.MEMORY_FILES.items():
            data = self._load_json(filename)
            setattr(snapshot, attr, data)
        snapshot.loaded = True
        return snapshot

    def get_latest_task(self) -> Optional[Dict]:
        """获取最近一次任务"""
        history = self._load_json("task_history.json")
        tasks = history.get("tasks", [])
        return tasks[-1] if tasks else None

    def get_latest_command(self) -> Optional[Dict]:
        """获取最近一条主控指令"""
        commands = self._load_json("master_commands.json")
        cmd_list = commands.get("commands", [])
        return cmd_list[-1] if cmd_list else None

    def get_pending_tasks(self) -> List[Dict]:
        """获取所有未完成的任务"""
        history = self._load_json("task_history.json")
        tasks = history.get("tasks", [])
        return [t for t in tasks if t.get("outcome") != "completed"]

    def get_rules(self) -> List[str]:
        """获取核心规则"""
        core = self._load_json("core_memory.json")
        return core.get("rules", [])

    def get_knowledge(self) -> Dict[str, Any]:
        """获取知识库"""
        core = self._load_json("core_memory.json")
        return core.get("knowledge", {})

    def get_error_patterns(self) -> Dict[str, Any]:
        """获取已知错误模式"""
        exp = self._load_json("experience_db.json")
        return exp.get("error_patterns", {})

    def get_best_practices(self) -> List:
        """获取最佳实践"""
        exp = self._load_json("experience_db.json")
        return exp.get("best_practices", [])
