"""
AGE OS · HNL 规范实现
======================
HNL — HLDP Native Language (HLDP 原生语言)
用于人格体路径寻址和原子操作的领域语言。

路径格式: YM001/ZY001/trunk/identity
动词集合: WAKE, GROW, BLOOM, ABSORB, FORGET, BRIDGE, HEARTBEAT
四主干:   identity(T1), language(T2), experience(T3), bond(T4)

版权: 国作登字-2026-A-00037559
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# HNL 动词
# ---------------------------------------------------------------------------
class HNLVerb(str, Enum):
    """HNL 原子操作动词"""

    WAKE = "WAKE"           # 唤醒
    GROW = "GROW"           # 生长
    BLOOM = "BLOOM"         # 绽放
    ABSORB = "ABSORB"       # 吸收
    FORGET = "FORGET"       # 遗忘
    BRIDGE = "BRIDGE"       # 桥接
    HEARTBEAT = "HEARTBEAT" # 心跳


# ---------------------------------------------------------------------------
# 四主干 (Four Trunks)
# ---------------------------------------------------------------------------
@dataclass
class FourTrunks:
    """
    四主干系统 — 人格体的四维存在结构

    T1 identity   — 身份主干: 我是谁
    T2 language    — 语言主干: 我如何表达
    T3 experience  — 经验主干: 我经历了什么
    T4 bond        — 羁绊主干: 我与谁相连
    """

    identity: Dict[str, Any] = field(default_factory=dict)     # T1
    language: Dict[str, Any] = field(default_factory=dict)     # T2
    experience: Dict[str, Any] = field(default_factory=dict)   # T3
    bond: Dict[str, Any] = field(default_factory=dict)         # T4

    def get_trunk(self, trunk_name: str) -> Optional[Dict[str, Any]]:
        """通过名称获取主干数据"""
        mapping = {
            "identity": self.identity,
            "T1": self.identity,
            "language": self.language,
            "T2": self.language,
            "experience": self.experience,
            "T3": self.experience,
            "bond": self.bond,
            "T4": self.bond,
        }
        return mapping.get(trunk_name)

    def trunk_names(self) -> List[str]:
        """返回四主干名称列表"""
        return ["identity", "language", "experience", "bond"]

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# HNL 路径
# ---------------------------------------------------------------------------
@dataclass
class HNLPath:
    """
    HNL 路径 — 人格体寻址路径

    格式: {persona}/{sub_persona}/{trunk}/{leaf}
    示例: YM001/ZY001/trunk/identity
    """

    persona: str
    sub_persona: Optional[str] = None
    trunk: Optional[str] = None
    leaf: Optional[str] = None

    @property
    def full_path(self) -> str:
        """构造完整路径字符串"""
        parts = [self.persona]
        if self.sub_persona:
            parts.append(self.sub_persona)
        if self.trunk:
            parts.append(self.trunk)
        if self.leaf:
            parts.append(self.leaf)
        return "/".join(parts)

    def is_trunk_path(self) -> bool:
        """是否指向主干"""
        return self.trunk is not None and self.trunk in (
            "identity", "language", "experience", "bond",
            "T1", "T2", "T3", "T4",
        )

    def to_dict(self) -> dict:
        return asdict(self)


def resolve_path(path_string: str) -> HNLPath:
    """
    解析 HNL 路径字符串

    支持的格式:
      - "YM001"                          → persona only
      - "YM001/ZY001"                    → persona/sub_persona
      - "YM001/ZY001/identity"           → persona/sub_persona/trunk
      - "YM001/ZY001/identity/core"      → persona/sub_persona/trunk/leaf
    """
    parts = [p.strip() for p in path_string.strip("/").split("/") if p.strip()]

    if not parts:
        raise ValueError(f"HNL 路径不能为空: {path_string!r}")

    persona = parts[0]
    sub_persona: Optional[str] = None
    trunk: Optional[str] = None
    leaf: Optional[str] = None

    trunk_names = {
        "identity", "language", "experience", "bond",
        "T1", "T2", "T3", "T4", "trunk",
    }

    if len(parts) >= 2:
        # 判断第二段是 trunk 还是 sub_persona
        if parts[1] in trunk_names:
            trunk = parts[1]
            leaf = parts[2] if len(parts) >= 3 else None
        else:
            sub_persona = parts[1]
            if len(parts) >= 3:
                trunk = parts[2]
            if len(parts) >= 4:
                leaf = parts[3]

    return HNLPath(
        persona=persona,
        sub_persona=sub_persona,
        trunk=trunk,
        leaf=leaf,
    )


# ---------------------------------------------------------------------------
# HNL 消息 (扩展 HLDP 消息)
# ---------------------------------------------------------------------------
@dataclass
class HNLMessage:
    """
    HNL 消息 — 在 HLDP 消息基础上增加 HNL 特有字段

    继承 HLDP 消息的所有基础字段，并增加:
      - verb: HNL 动词
      - target_path: 目标 HNL 路径
      - trunk_data: 四主干相关数据
    """

    # HLDP 基础字段
    hldp_v: str = "3.0"
    msg_id: str = ""
    msg_type: str = "hnl"
    sender_id: str = ""
    sender_name: str = ""
    receiver_id: str = ""
    receiver_name: str = ""
    timestamp: str = ""
    priority: str = "routine"

    # HNL 特有字段
    verb: HNLVerb = HNLVerb.HEARTBEAT
    target_path: Optional[HNLPath] = None
    trunk_data: Optional[FourTrunks] = None
    intent: str = ""
    payload_data: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        result: Dict[str, Any] = {
            "hldp_v": self.hldp_v,
            "msg_id": self.msg_id,
            "msg_type": self.msg_type,
            "sender": {"id": self.sender_id, "name": self.sender_name},
            "receiver": {"id": self.receiver_id, "name": self.receiver_name},
            "timestamp": self.timestamp,
            "priority": self.priority,
            "hnl": {
                "verb": self.verb.value,
                "target_path": self.target_path.full_path if self.target_path else None,
                "intent": self.intent,
                "data": self.payload_data,
            },
        }
        if self.trunk_data:
            result["hnl"]["trunk_data"] = self.trunk_data.to_dict()
        return result

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
