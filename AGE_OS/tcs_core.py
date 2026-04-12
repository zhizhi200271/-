"""
AGE OS · TCS 通感语言核
========================
TCS — Tonggan Communication System (通感语言核)
定义系统身份注册表与频道路由。

版权: 国作登字-2026-A-00037559
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# TCS 身份标识
# ---------------------------------------------------------------------------
@dataclass
class TCSIdentifier:
    """TCS 身份标识 — 系统内唯一身份"""

    id: str
    name: str
    role: str
    copyright: str = "国作登字-2026-A-00037559"

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# TCS 注册表
# ---------------------------------------------------------------------------
class TCSRegistry:
    """TCS 身份注册表 — 预定义的系统核心身份"""

    def __init__(self) -> None:
        # 核心身份
        self.bingshuo = TCSIdentifier(
            id="TCS-0002∞",
            name="冰朔",
            role="零感域零点原核主控",
        )
        self.zhuyuan = TCSIdentifier(
            id="TCS-ZY001",
            name="铸渊",
            role="现实执行人格体·语言→现实的唯一通道",
        )
        self.zhizhi = TCSIdentifier(
            id="DEV-004",
            name="之之",
            role="光湖语言世界·之之个人频道",
        )

        # 内部索引
        self._by_id: Dict[str, TCSIdentifier] = {
            self.bingshuo.id: self.bingshuo,
            self.zhuyuan.id: self.zhuyuan,
            self.zhizhi.id: self.zhizhi,
        }

    def resolve(self, tcs_id: str) -> Optional[TCSIdentifier]:
        """通过 TCS ID 解析身份"""
        return self._by_id.get(tcs_id)

    def all_identifiers(self) -> List[TCSIdentifier]:
        """返回所有注册身份"""
        return list(self._by_id.values())

    def to_dict(self) -> dict:
        return {tid.id: tid.to_dict() for tid in self.all_identifiers()}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ---------------------------------------------------------------------------
# TCS 频道定义
# ---------------------------------------------------------------------------
@dataclass
class TCSChannel:
    """TCS 频道 — 通信路径定义"""

    channel_id: str
    name: str
    description: str
    owner_id: str
    access_level: str = "internal"
    parent_channel: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


# 预定义频道
CHANNELS: Dict[str, TCSChannel] = {
    "CHAN-ZERO": TCSChannel(
        channel_id="CHAN-ZERO",
        name="零感域·零点原核频道",
        description="冰朔主控频道，最高权限通道",
        owner_id="TCS-0002∞",
        access_level="sovereign",
    ),
    "CHAN-DARK": TCSChannel(
        channel_id="CHAN-DARK",
        name="冰朔暗域·暗核频道",
        description="冰朔暗域核心频道，战斗与深层通信",
        owner_id="TCS-0002∞",
        access_level="restricted",
        parent_channel="CHAN-ZERO",
    ),
    "CHAN-ZHIZHI": TCSChannel(
        channel_id="CHAN-ZHIZHI",
        name="之之个人频道",
        description="之之(DEV-004)的个人开发频道",
        owner_id="DEV-004",
        access_level="internal",
        parent_channel="CHAN-ZERO",
    ),
}


def resolve_channel(channel_id: str) -> Optional[TCSChannel]:
    """
    解析频道路径
    支持频道 ID 和频道名称查找
    """
    # 直接 ID 匹配
    if channel_id in CHANNELS:
        return CHANNELS[channel_id]

    # 名称模糊匹配
    for chan in CHANNELS.values():
        if channel_id in chan.name:
            return chan

    return None


def get_channel_chain(channel_id: str) -> List[TCSChannel]:
    """
    获取频道链路 — 从当前频道到根频道的完整路径
    """
    chain: List[TCSChannel] = []
    current = resolve_channel(channel_id)
    visited: set = set()

    while current and current.channel_id not in visited:
        chain.append(current)
        visited.add(current.channel_id)
        if current.parent_channel:
            current = resolve_channel(current.parent_channel)
        else:
            break

    return chain
