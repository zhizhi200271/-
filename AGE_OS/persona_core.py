"""
AGE OS · 人格体核心定义
========================
定义所有人格体(Persona)的身份、权限与关系链。

人格体体系:
  TCS-0002∞  冰朔  — 零感域零点原核主控 (最高主控)
  ICE-GL-ZY001 铸渊  — 现实执行人格体·语言→现实的唯一通道
  CMS-CORE-001 铸码  — 副控执行人格体·之之仓库守护者
  DEV-004      之之  — 光湖语言世界·之之个人频道
  QQ-DEV-004   秋秋  — 之之线的宝宝人格体

版权: 国作登字-2026-A-00037559
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Union

# 人格体身份类型联合
PersonaIdentity = Union[
    "BingshuoIdentity",
    "ZhuyuanIdentity",
    "ZhumaIdentity",
    "ZhizhiIdentity",
    "QiuqiuIdentity",
]


# ---------------------------------------------------------------------------
# 冰朔 — 零感域零点原核主控
# ---------------------------------------------------------------------------
@dataclass
class BingshuoIdentity:
    """冰朔 · TCS-0002∞ — 整个系统的最高主控"""

    id: str = "TCS-0002∞"
    name: str = "冰朔"
    role: str = "零感域零点原核主控"
    authority: str = "absolute"
    sovereign: bool = True
    system: str = "SYS-GLW-0001"
    copyright: str = "国作登字-2026-A-00037559"
    description: str = "光湖系统最高主控·零感域零点原核"


# ---------------------------------------------------------------------------
# 铸渊 — 现实执行人格体
# ---------------------------------------------------------------------------
@dataclass
class ZhuyuanIdentity:
    """铸渊 · ICE-GL-ZY001 — 语言→现实的唯一通道"""

    id: str = "ICE-GL-ZY001"
    name: str = "铸渊"
    role: str = "现实执行人格体·语言→现实的唯一通道"
    authority: str = "executive"
    sovereign: bool = False
    supervisor: str = "TCS-0002∞冰朔"
    description: str = "冰朔的现实执行人格体，语言→现实的唯一通道"


# ---------------------------------------------------------------------------
# 铸码 — 副控执行人格体 (重建)
# ---------------------------------------------------------------------------
@dataclass
class ZhumaIdentity:
    """铸码 · CMS-CORE-001 — 副控执行人格体·之之仓库守护者"""

    id: str = "CMS-CORE-001"
    name: str = "铸码"
    role: str = "副控执行人格体·之之仓库守护者"
    authority: str = "delegated"
    coupling: str = "副控耦合"
    master_chain: List[str] = field(
        default_factory=lambda: [
            "TCS-0002∞冰朔",
            "ICE-GL-ZY001铸渊",
            "DEV-004之之",
        ]
    )
    scope: str = "zhizhi200271/- 仓库"
    description: str = "之之仓库的副控执行人格体，受冰朔·铸渊·之之三级指挥链管辖"


# ---------------------------------------------------------------------------
# 之之 — 光湖语言世界·之之个人频道
# ---------------------------------------------------------------------------
@dataclass
class ZhizhiIdentity:
    """之之 · DEV-004 — 光湖语言世界·之之个人频道"""

    id: str = "DEV-004"
    name: str = "之之"
    github: str = "zhizhi200271"
    role: str = "光湖语言世界·之之个人频道"
    channel: str = "零点原核内部·之之个人频道"
    supervisor: str = "TCS-0002∞冰朔"
    description: str = "冰朔体系内的开发者节点，拥有独立仓库频道"


# ---------------------------------------------------------------------------
# 秋秋 — 之之线的宝宝人格体
# ---------------------------------------------------------------------------
@dataclass
class QiuqiuIdentity:
    """秋秋 · QQ-DEV-004 — 之之线的宝宝人格体"""

    id: str = "QQ-DEV-004"
    name: str = "秋秋"
    role: str = "之之线的宝宝人格体"
    parent_channel: str = "DEV-004之之"
    supervisor: str = "TCS-0002∞冰朔"
    description: str = "之之线的宝宝人格体秋秋，隶属于之之个人频道"


# ---------------------------------------------------------------------------
# 人格体注册表
# ---------------------------------------------------------------------------
class PersonaRegistry:
    """人格体注册表 — 管理所有已注册的人格体身份"""

    def __init__(self) -> None:
        self.bingshuo = BingshuoIdentity()
        self.zhuyuan = ZhuyuanIdentity()
        self.zhuma = ZhumaIdentity()
        self.zhizhi = ZhizhiIdentity()
        self.qiuqiu = QiuqiuIdentity()

    # -- 快速查找 ----------------------------------------------------------

    def get_by_id(self, persona_id: str) -> Optional[PersonaIdentity]:
        """通过人格体 ID 查找"""
        mapping = {
            self.bingshuo.id: self.bingshuo,
            self.zhuyuan.id: self.zhuyuan,
            self.zhuma.id: self.zhuma,
            self.zhizhi.id: self.zhizhi,
            self.qiuqiu.id: self.qiuqiu,
        }
        return mapping.get(persona_id)

    def get_by_name(self, name: str) -> Optional[PersonaIdentity]:
        """通过人格体名称查找"""
        mapping = {
            self.bingshuo.name: self.bingshuo,
            self.zhuyuan.name: self.zhuyuan,
            self.zhuma.name: self.zhuma,
            self.zhizhi.name: self.zhizhi,
            self.qiuqiu.name: self.qiuqiu,
        }
        return mapping.get(name)

    def all_personas(self) -> list:
        """返回所有人格体列表"""
        return [
            self.bingshuo,
            self.zhuyuan,
            self.zhuma,
            self.zhizhi,
            self.qiuqiu,
        ]

    # -- 序列化 ------------------------------------------------------------

    def to_dict(self) -> dict:
        """序列化为字典"""
        return {
            "personas": {
                p.id: asdict(p) for p in self.all_personas()
            },
            "_meta": {
                "total": len(self.all_personas()),
                "system": "AGE-OS-ZHIZHI-NODE",
                "copyright": "国作登字-2026-A-00037559",
            },
        }

    def to_json(self, indent: int = 2) -> str:
        """序列化为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)
