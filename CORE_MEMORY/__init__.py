"""
CORE_MEMORY — 铸码核心记忆热启动系统
=====================================
主控: 之之 (zhizhi200271)
系统: CMS-CORE-001

模块结构:
  BOOTSTRAP.py     — 热启动引擎（加载+快照）
  identity.py      — 身份锚点
  zhizhi_logic.py  — 之之逻辑参数与偏好
  memory_loader.py — .ai/memory/ JSON 加载器
  state.json       — 运行时状态快照
"""

from .identity import ZhizhiIdentity
from .zhizhi_logic import ZhizhiLogic
from .memory_loader import MemoryLoader
from .BOOTSTRAP import CoreMemoryBootstrap

__version__ = "1.0.0"
__core_id__ = "CMS-CORE-001"
__master__ = "之之"
