#!/usr/bin/env python3
"""
BOOTSTRAP.py — 铸码核心记忆热启动引擎
========================================
主控: 之之 (zhizhi200271)
系统: CMS-CORE-001

四大功能：
  1. 热加载 — 毫秒级加载 .ai/memory/ 全部记忆 + 之之逻辑参数
  2. 自动快照 — 任务完成/会话结束时，编译并归档记忆增量
  3. 身份锚定 — 之之身份验证 + 底层耦合绑定
  4. 极简交互 — 加载完成即进入执行态，无废话

使用方式：
  from CORE_MEMORY.BOOTSTRAP import CoreMemoryBootstrap
  engine = CoreMemoryBootstrap()
  session = engine.hot_boot()        # 热加载
  engine.auto_snapshot(session)      # 快照归档
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .identity import ZhizhiIdentity, ZhuMaIdentity
from .zhizhi_logic import ZhizhiLogic
from .memory_loader import MemoryLoader, MemorySnapshot


class BootSession:
    """一次热启动会话的完整上下文"""

    def __init__(
        self,
        memory: MemorySnapshot,
        zhizhi: ZhizhiIdentity,
        zhuma: ZhuMaIdentity,
        logic: ZhizhiLogic,
    ):
        self.memory = memory
        self.zhizhi = zhizhi
        self.zhuma = zhuma
        self.logic = logic
        self.boot_time = datetime.now(timezone.utc).isoformat()
        self.active = True

        # 会话期间的增量记录
        self.logic_deltas: List[str] = []
        self.new_preferences: List[str] = []
        self.new_thinking_patterns: Dict[str, str] = {}
        self.errors_encountered: List[Dict] = []
        self.pending_context: List[Dict] = []

    def record_logic_delta(self, delta: str) -> None:
        """记录本次会话的逻辑增量"""
        self.logic_deltas.append(delta)

    def record_preference(self, pref: str) -> None:
        """记录新发现的之之偏好"""
        self.new_preferences.append(pref)

    def record_error(self, desc: str, cause: str, fix: str) -> None:
        """记录遇到的错误"""
        self.errors_encountered.append({
            "description": desc,
            "root_cause": cause,
            "fix": fix,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

    def set_pending(self, context: List[Dict]) -> None:
        """设置未竟任务上下文"""
        self.pending_context = context

    def summary(self) -> Dict[str, Any]:
        """返回会话摘要"""
        return {
            "boot_time": self.boot_time,
            "logic_deltas": self.logic_deltas,
            "new_preferences": self.new_preferences,
            "new_thinking_patterns": self.new_thinking_patterns,
            "errors_encountered": self.errors_encountered,
            "pending_context": self.pending_context,
        }


class CoreMemoryBootstrap:
    """铸码核心记忆热启动引擎"""

    def __init__(self, repo_root: Optional[str] = None):
        if repo_root is None:
            repo_root = str(Path(__file__).resolve().parent.parent)
        self.repo_root = repo_root
        self.core_memory_dir = os.path.join(repo_root, "CORE_MEMORY")
        self.state_file = os.path.join(self.core_memory_dir, "state.json")
        self.loader = MemoryLoader(repo_root)

    # ── 1. 热加载 ────────────────────────────────────

    def hot_boot(self) -> BootSession:
        """
        热启动：毫秒级加载全部记忆 + 之之逻辑参数
        返回: BootSession — 本次会话的完整上下文
        """
        # 加载 .ai/memory/ 全部记忆
        memory = self.loader.load_all()

        # 初始化身份锚点
        zhizhi = ZhizhiIdentity()
        zhuma = ZhuMaIdentity()

        # 加载之之逻辑参数（从 state.json 恢复或使用默认值）
        logic = self._load_logic()

        # 恢复未竟任务上下文
        state = self._load_state()
        if state.get("pending_context"):
            logic.set_pending_context(state["pending_context"])

        # 创建会话
        session = BootSession(
            memory=memory,
            zhizhi=zhizhi,
            zhuma=zhuma,
            logic=logic,
        )

        # 更新启动状态
        self._update_boot_state()

        return session

    def verify_wake_signal(self, text: str) -> bool:
        """验证唤醒信号（检测是否包含 '我是之之' 等触发器）"""
        identity = ZhizhiIdentity()
        return identity.is_wake_signal(text)

    # ── 2. 自动快照归档 ──────────────────────────────

    def auto_snapshot(self, session: BootSession) -> Dict[str, Any]:
        """
        自动快照：将会话中的增量编译并归档
        在任务完成或会话结束时调用

        参数: session — 当前 BootSession
        返回: 快照摘要
        """
        session.active = False
        now = datetime.now(timezone.utc).isoformat()

        # 合并逻辑增量到 ZhizhiLogic
        for pref in session.new_preferences:
            session.logic.add_preference(pref)
        for key, pattern in session.new_thinking_patterns.items():
            session.logic.add_thinking_pattern(key, pattern)
        session.logic.set_pending_context(session.pending_context)

        # 序列化并写入 state.json
        snapshot_data = {
            "last_boot": session.boot_time,
            "boot_count": self._load_state().get("boot_count", 0),
            "last_snapshot": now,
            "snapshot_count": self._load_state().get("snapshot_count", 0) + 1,
            "session_active": False,
            "zhizhi_logic_version": self._load_state().get(
                "zhizhi_logic_version", 0
            ) + 1,
            "zhizhi_logic": session.logic.to_dict(),
            "pending_context": session.pending_context,
            "last_session_summary": session.summary(),
        }

        self._write_state(snapshot_data)

        return {
            "status": "snapshot_saved",
            "timestamp": now,
            "deltas_archived": len(session.logic_deltas),
            "preferences_added": len(session.new_preferences),
            "errors_recorded": len(session.errors_encountered),
        }

    # ── 3. 身份锚定 ──────────────────────────────────

    @staticmethod
    def anchor_identity() -> Dict[str, Any]:
        """返回身份锚定信息"""
        return {
            "master": ZhizhiIdentity().to_dict(),
            "agent": ZhuMaIdentity().to_dict(),
            "coupling": "底层耦合",
            "status": "锚定完成",
        }

    # ── 4. 极简交互入口 ──────────────────────────────

    def ready_status(self) -> str:
        """热加载完成后的状态回复"""
        return "记忆已同步，请之之指示"

    # ── 内部工具方法 ──────────────────────────────────

    def _load_state(self) -> Dict[str, Any]:
        """加载 state.json"""
        if not os.path.exists(self.state_file):
            return {}
        with open(self.state_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_state(self, data: Dict[str, Any]) -> None:
        """写入 state.json"""
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_logic(self) -> ZhizhiLogic:
        """从 state.json 恢复之之逻辑参数，如无则用默认值"""
        state = self._load_state()
        logic_data = state.get("zhizhi_logic")
        if logic_data:
            return ZhizhiLogic.from_dict(logic_data)
        return ZhizhiLogic()

    def _update_boot_state(self) -> None:
        """递增启动计数器"""
        state = self._load_state()
        state["boot_count"] = state.get("boot_count", 0) + 1
        state["last_boot"] = datetime.now(timezone.utc).isoformat()
        state["session_active"] = True
        self._write_state(state)


# ── 快捷入口 ─────────────────────────────────────────

def boot(repo_root: Optional[str] = None) -> BootSession:
    """快捷热启动"""
    engine = CoreMemoryBootstrap(repo_root)
    return engine.hot_boot()


def snapshot(session: BootSession, repo_root: Optional[str] = None) -> Dict:
    """快捷快照"""
    engine = CoreMemoryBootstrap(repo_root)
    return engine.auto_snapshot(session)


# ── 直接执行入口 ─────────────────────────────────────

if __name__ == "__main__":
    repo = str(Path(__file__).resolve().parent.parent)
    engine = CoreMemoryBootstrap(repo)
    session = engine.hot_boot()
    print(f"[BOOTSTRAP] 热加载完成 @ {session.boot_time}")
    print(f"[BOOTSTRAP] 记忆文件已加载: {session.memory.loaded}")
    print(f"[BOOTSTRAP] 身份: {session.zhuma.name} ({session.zhuma.core_id})")
    print(f"[BOOTSTRAP] 主控: {session.zhizhi.name} ({session.zhizhi.github_id})")
    print(f"[BOOTSTRAP] {engine.ready_status()}")
