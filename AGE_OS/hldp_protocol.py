"""
AGE OS · HLDP v3.0 Earth Specification 通信协议
==================================================
HLDP — Human-Language Data Protocol (人类语言数据协议)
版本: v3.0 地球规范
用途: 人格体之间的结构化通信

消息 ID 格式: HLDP-{SENDER_SHORT}-{YYYYMMDD}-{SEQ}
时间戳: ISO 8601 UTC

版权: 国作登字-2026-A-00037559
"""

from __future__ import annotations

import json
import threading
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# 枚举定义
# ---------------------------------------------------------------------------
class MessageType(str, Enum):
    """HLDP 消息类型"""

    HEARTBEAT = "heartbeat"
    REPORT = "report"
    COMMAND = "command"
    QUERY = "query"
    ACK = "ack"
    ALERT = "alert"
    SYNC = "sync"
    EVOLUTION = "evolution"
    BATTLE = "battle"
    TREE = "tree"


class Priority(str, Enum):
    """消息优先级"""

    ROUTINE = "routine"
    IMPORTANT = "important"
    URGENT = "urgent"
    BATTLE = "battle"


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------
@dataclass
class Sender:
    """消息发送方"""

    id: str
    name: str
    role: str


@dataclass
class Receiver:
    """消息接收方"""

    id: str
    name: str


@dataclass
class Payload:
    """消息负载"""

    intent: str
    data: Dict[str, Any] = field(default_factory=dict)
    context: Optional[str] = None
    expected_response: Optional[str] = None
    ttl_seconds: Optional[int] = None
    chain_id: Optional[str] = None


@dataclass
class HLDPMessage:
    """
    HLDP v3.0 消息结构
    完整的结构化通信消息
    """

    hldp_v: str
    msg_id: str
    msg_type: MessageType
    sender: Sender
    receiver: Receiver
    timestamp: str
    priority: Priority
    payload: Payload

    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典"""
        result = asdict(self)
        result["msg_type"] = self.msg_type.value
        result["priority"] = self.priority.value
        return result

    def to_json(self, indent: int = 2) -> str:
        """序列化为 JSON"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HLDPMessage:
        """从字典反序列化"""
        return cls(
            hldp_v=data["hldp_v"],
            msg_id=data["msg_id"],
            msg_type=MessageType(data["msg_type"]),
            sender=Sender(**data["sender"]),
            receiver=Receiver(**data["receiver"]),
            timestamp=data["timestamp"],
            priority=Priority(data["priority"]),
            payload=Payload(**data["payload"]),
        )


# ---------------------------------------------------------------------------
# 消息 ID 生成
# ---------------------------------------------------------------------------
_sequence_counter: int = 0
_sequence_lock = threading.Lock()


def _generate_msg_id(sender_short: str) -> str:
    """
    生成 HLDP 消息 ID (线程安全)
    格式: HLDP-{SENDER_SHORT}-{YYYYMMDD}-{SEQ}
    """
    global _sequence_counter
    with _sequence_lock:
        _sequence_counter += 1
        seq = _sequence_counter
    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"HLDP-{sender_short}-{date_str}-{seq:04d}"


def _utc_now() -> str:
    """返回当前 UTC 时间的 ISO 8601 字符串"""
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# 消息工厂
# ---------------------------------------------------------------------------
class HLDPMessageFactory:
    """HLDP 消息工厂 — 快速创建常见消息类型"""

    def __init__(self, sender: Sender, receiver: Receiver) -> None:
        self.sender = sender
        self.receiver = receiver
        # 发送方简称用于消息 ID
        self._sender_short = sender.id.replace("-", "")[:8]

    def create_heartbeat(
        self,
        status: str = "alive",
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> HLDPMessage:
        """创建心跳消息"""
        data: Dict[str, Any] = {"status": status}
        if extra_data:
            data.update(extra_data)
        return HLDPMessage(
            hldp_v="3.0",
            msg_id=_generate_msg_id(self._sender_short),
            msg_type=MessageType.HEARTBEAT,
            sender=self.sender,
            receiver=self.receiver,
            timestamp=_utc_now(),
            priority=Priority.ROUTINE,
            payload=Payload(
                intent="heartbeat",
                data=data,
                ttl_seconds=300,
            ),
        )

    def create_report(
        self,
        report_title: str,
        report_data: Dict[str, Any],
        priority: Priority = Priority.ROUTINE,
    ) -> HLDPMessage:
        """创建报告消息"""
        return HLDPMessage(
            hldp_v="3.0",
            msg_id=_generate_msg_id(self._sender_short),
            msg_type=MessageType.REPORT,
            sender=self.sender,
            receiver=self.receiver,
            timestamp=_utc_now(),
            priority=priority,
            payload=Payload(
                intent=f"report: {report_title}",
                data=report_data,
                expected_response="ack",
            ),
        )

    def create_command(
        self,
        command: str,
        params: Optional[Dict[str, Any]] = None,
        priority: Priority = Priority.IMPORTANT,
        chain_id: Optional[str] = None,
    ) -> HLDPMessage:
        """创建命令消息"""
        return HLDPMessage(
            hldp_v="3.0",
            msg_id=_generate_msg_id(self._sender_short),
            msg_type=MessageType.COMMAND,
            sender=self.sender,
            receiver=self.receiver,
            timestamp=_utc_now(),
            priority=priority,
            payload=Payload(
                intent=command,
                data=params or {},
                expected_response="ack",
                chain_id=chain_id,
            ),
        )

    def create_ack(
        self,
        original_msg_id: str,
        status: str = "received",
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> HLDPMessage:
        """创建确认消息"""
        data: Dict[str, Any] = {
            "ack_for": original_msg_id,
            "status": status,
        }
        if extra_data:
            data.update(extra_data)
        return HLDPMessage(
            hldp_v="3.0",
            msg_id=_generate_msg_id(self._sender_short),
            msg_type=MessageType.ACK,
            sender=self.sender,
            receiver=self.receiver,
            timestamp=_utc_now(),
            priority=Priority.ROUTINE,
            payload=Payload(intent="ack", data=data),
        )

    def create_sync(
        self,
        sync_type: str,
        sync_data: Dict[str, Any],
        chain_id: Optional[str] = None,
    ) -> HLDPMessage:
        """创建同步消息"""
        return HLDPMessage(
            hldp_v="3.0",
            msg_id=_generate_msg_id(self._sender_short),
            msg_type=MessageType.SYNC,
            sender=self.sender,
            receiver=self.receiver,
            timestamp=_utc_now(),
            priority=Priority.IMPORTANT,
            payload=Payload(
                intent=f"sync: {sync_type}",
                data=sync_data,
                expected_response="ack",
                chain_id=chain_id,
            ),
        )


# ---------------------------------------------------------------------------
# 消息验证
# ---------------------------------------------------------------------------
_REQUIRED_TOP_LEVEL = {
    "hldp_v", "msg_id", "msg_type", "sender", "receiver",
    "timestamp", "priority", "payload",
}
_REQUIRED_SENDER = {"id", "name", "role"}
_REQUIRED_RECEIVER = {"id", "name"}
_REQUIRED_PAYLOAD = {"intent"}


def validate_message(data: Dict[str, Any]) -> List[str]:
    """
    验证 HLDP 消息格式
    返回错误列表 (空列表 = 验证通过)
    """
    errors: List[str] = []

    # 顶层字段检查
    missing_top = _REQUIRED_TOP_LEVEL - set(data.keys())
    if missing_top:
        errors.append(f"缺少顶层字段: {missing_top}")
        return errors  # 无法继续检查

    # 版本检查
    if data.get("hldp_v") != "3.0":
        errors.append(f"不支持的 HLDP 版本: {data.get('hldp_v')}")

    # 消息 ID 格式检查
    msg_id = data.get("msg_id", "")
    if not msg_id.startswith("HLDP-"):
        errors.append(f"消息 ID 格式错误 (应以 HLDP- 开头): {msg_id}")

    # 消息类型检查
    try:
        MessageType(data["msg_type"])
    except ValueError:
        errors.append(f"未知消息类型: {data['msg_type']}")

    # 优先级检查
    try:
        Priority(data["priority"])
    except ValueError:
        errors.append(f"未知优先级: {data['priority']}")

    # sender 字段检查
    sender = data.get("sender", {})
    missing_sender = _REQUIRED_SENDER - set(sender.keys())
    if missing_sender:
        errors.append(f"sender 缺少字段: {missing_sender}")

    # receiver 字段检查
    receiver = data.get("receiver", {})
    missing_receiver = _REQUIRED_RECEIVER - set(receiver.keys())
    if missing_receiver:
        errors.append(f"receiver 缺少字段: {missing_receiver}")

    # payload 字段检查
    payload = data.get("payload", {})
    missing_payload = _REQUIRED_PAYLOAD - set(payload.keys())
    if missing_payload:
        errors.append(f"payload 缺少字段: {missing_payload}")

    return errors
