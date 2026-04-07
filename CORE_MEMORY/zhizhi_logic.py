"""
之之逻辑参数与偏好 — 结构化 Class 定义
通过每次任务的反思不断更新和对齐
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


@dataclass
class CommunicationStyle:
    """之之的沟通风格"""
    primary_language: str = "中文"
    tone: str = "比喻性/对话式"
    prefers_metaphors: bool = True
    prefers_structured_output: bool = True
    dislikes_verbosity: bool = True
    dislikes_showing_off: bool = True


@dataclass
class PriorityWeights:
    """之之的优先级权重 (1-10)"""
    learning: int = 10          # 学习 > 一切
    reflection: int = 9         # 反思 > 速度
    understanding: int = 9      # 理解偏好 > 技术炫技
    growth_mindset: int = 10    # 成长型思维
    execution_speed: int = 5    # 速度不是第一位
    technical_depth: int = 6    # 技术深度适中即可
    never_repeat_mistake: int = 10  # 不犯同样的错误


@dataclass
class TaskPreferences:
    """之之对任务执行的偏好"""
    verify_before_commit: bool = True
    update_memory_after_task: bool = True
    write_reflection_after_task: bool = True
    regenerate_dashboard: bool = True
    prefer_minimal_changes: bool = True
    code_comments_language: str = "英文可，中文优先"


@dataclass
class ZhizhiLogic:
    """之之的完整逻辑参数集"""

    communication: CommunicationStyle = field(
        default_factory=CommunicationStyle
    )
    priorities: PriorityWeights = field(
        default_factory=PriorityWeights
    )
    task_prefs: TaskPreferences = field(
        default_factory=TaskPreferences
    )

    # 从反思报告中积累的偏好洞察
    observed_preferences: List[str] = field(default_factory=lambda: [
        "之之用比喻来描述系统架构（如'安装脑部神经'）",
        "之之重视'为什么'多于'怎么做'",
        "之之期望铸码理解任务背后的深层意图",
        "之之强调对比思维：你以为 vs 之之教的",
        "之之认为错误是成长的养分，不是惩罚",
    ])

    # 已识别的思维模式
    thinking_patterns: Dict[str, str] = field(default_factory=lambda: {
        "architecture_metaphor": "用人体比喻系统（记忆=身体，神经=大脑）",
        "growth_over_speed": "宁可慢但学到东西，不要快但重蹈覆辙",
        "depth_first": "先理解再执行，不要盲目开工",
        "structured_reflection": "每件事都要有结构化的复盘",
    })

    # 未竟任务 / 待续上下文
    pending_context: List[Dict] = field(default_factory=list)

    def add_preference(self, preference: str) -> None:
        """从新任务中添加观察到的偏好"""
        if preference not in self.observed_preferences:
            self.observed_preferences.append(preference)

    def add_thinking_pattern(self, key: str, pattern: str) -> None:
        """记录新识别的思维模式"""
        self.thinking_patterns[key] = pattern

    def set_pending_context(self, context: List[Dict]) -> None:
        """设置未竟任务上下文"""
        self.pending_context = context

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "ZhizhiLogic":
        """从字典重建实例"""
        logic = cls()
        if "communication" in data:
            logic.communication = CommunicationStyle(**data["communication"])
        if "priorities" in data:
            logic.priorities = PriorityWeights(**data["priorities"])
        if "task_prefs" in data:
            logic.task_prefs = TaskPreferences(**data["task_prefs"])
        if "observed_preferences" in data:
            logic.observed_preferences = data["observed_preferences"]
        if "thinking_patterns" in data:
            logic.thinking_patterns = data["thinking_patterns"]
        if "pending_context" in data:
            logic.pending_context = data["pending_context"]
        return logic
