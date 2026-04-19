"""
AGE OS · COS 桥接代理
=======================
COS — Tencent Cloud Object Storage (腾讯云对象存储)
实现 之之仓库 ↔ 冰朔主仓库 的 COS 桥接通信。

所有操作通过 HLDP v3.0 消息记录。
密钥从环境变量读取，绝不硬编码。

版权: 国作登字-2026-A-00037559
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .hldp_protocol import (
    HLDPMessageFactory,
    Sender,
    Receiver,
    Priority,
)

logger = logging.getLogger(__name__)

# 桥接状态文件路径（相对于包目录）
STATUS_FILE = Path(__file__).parent / "bridge_status.json"


# ---------------------------------------------------------------------------
# 桥接配置
# ---------------------------------------------------------------------------
@dataclass
class COSBridgeConfig:
    """COS 桥接配置"""

    bucket_name: str = "zhizhi-cos-bucket"
    region: str = "待配置"
    secret_id_env: str = "ZHIZHI_COS_SECRET_ID"
    secret_key_env: str = "ZHIZHI_COS_SECRET_KEY"
    bucket_prefix: str = "/zhizhi/"

    def has_credentials(self) -> bool:
        """检查环境变量中是否存在凭证"""
        return bool(
            os.environ.get(self.secret_id_env)
            and os.environ.get(self.secret_key_env)
        )


# ---------------------------------------------------------------------------
# COS 桥接代理
# ---------------------------------------------------------------------------
class COSBridgeAgent:
    """
    COS 桥接代理
    负责 之之仓库 ↔ 冰朔主仓库 之间的文件同步与消息传递
    """

    def __init__(self, config: Optional[COSBridgeConfig] = None) -> None:
        self.config = config or COSBridgeConfig()
        self._message_log: List[Dict[str, Any]] = []

        # 初始化 HLDP 消息工厂
        self._factory = HLDPMessageFactory(
            sender=Sender(
                id="CMS-CORE-001",
                name="铸码",
                role="副控执行人格体",
            ),
            receiver=Receiver(
                id="ICE-GL-ZY001",
                name="铸渊",
            ),
        )

        # 加载状态文件
        self._status = self._load_status()
        logger.info("COS 桥接代理初始化完成: bucket=%s", self.config.bucket_name)

    # -- 状态管理 ----------------------------------------------------------

    def _load_status(self) -> Dict[str, Any]:
        """加载桥接状态文件"""
        if STATUS_FILE.exists():
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "bridge_id": "ZHIZHI-COS-BRIDGE-001",
            "status": "initialized",
            "last_heartbeat": None,
            "last_sync": None,
            "last_report_sent": None,
            "last_receipt_received": None,
            "error_count": 0,
            "message_count": 0,
        }

    def _save_status(self) -> None:
        """保存桥接状态到文件"""
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(self._status, f, ensure_ascii=False, indent=2)

    def _utc_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _log_message(self, msg_dict: Dict[str, Any]) -> None:
        """记录 HLDP 消息到内部日志"""
        self._message_log.append(msg_dict)
        self._status["message_count"] = self._status.get("message_count", 0) + 1

    # -- COS 操作 (占位实现) -----------------------------------------------

    def read_from_bucket(self, path: str) -> Optional[str]:
        """
        从 COS 存储桶读取文件
        占位实现: 检查凭证 → 记录 HLDP 消息 → 返回 None
        """
        if not self.config.has_credentials():
            logger.warning("COS 凭证未配置，无法读取: %s", path)
            return None

        full_path = f"{self.config.bucket_prefix}{path}"
        logger.info("读取 COS 文件: %s/%s", self.config.bucket_name, full_path)

        # 记录读取操作的 HLDP 消息
        msg = self._factory.create_report(
            report_title="COS读取操作",
            report_data={"action": "read", "path": full_path},
        )
        self._log_message(msg.to_dict())

        # TODO: 接入腾讯云 COS SDK 实现实际读取
        logger.info("COS SDK 尚未接入，返回 None (占位)")
        return None

    def write_to_bucket(self, path: str, data: str) -> bool:
        """
        写入文件到 COS 存储桶
        占位实现: 检查凭证 → 记录 HLDP 消息 → 返回 False
        """
        if not self.config.has_credentials():
            logger.warning("COS 凭证未配置，无法写入: %s", path)
            return False

        full_path = f"{self.config.bucket_prefix}{path}"
        logger.info("写入 COS 文件: %s/%s", self.config.bucket_name, full_path)

        # 记录写入操作的 HLDP 消息
        msg = self._factory.create_report(
            report_title="COS写入操作",
            report_data={
                "action": "write",
                "path": full_path,
                "size": len(data),
            },
        )
        self._log_message(msg.to_dict())

        # TODO: 接入腾讯云 COS SDK 实现实际写入
        logger.info("COS SDK 尚未接入，返回 False (占位)")
        return False

    # -- 桥接操作 ----------------------------------------------------------

    def sync_heartbeat(self) -> Dict[str, Any]:
        """
        发送 HLDP 心跳到桥接
        """
        msg = self._factory.create_heartbeat(
            status="alive",
            extra_data={
                "bridge_id": self._status["bridge_id"],
                "bucket": self.config.bucket_name,
                "credentials_configured": self.config.has_credentials(),
            },
        )
        msg_dict = msg.to_dict()
        self._log_message(msg_dict)

        # 更新状态
        self._status["last_heartbeat"] = self._utc_now()
        self._status["status"] = "active"
        self._save_status()

        logger.info("心跳已发送: %s", msg.msg_id)
        return msg_dict

    def check_for_commands(self) -> List[Dict[str, Any]]:
        """
        检查来自冰朔桶的入站命令
        占位实现: 返回空列表
        """
        inbox_path = "receipts/"
        logger.info("检查入站命令: %s%s", self.config.bucket_prefix, inbox_path)

        # TODO: 从 COS 桶读取 inbox 目录中的命令文件
        return []

    def push_report(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        推送状态报告到桥接
        """
        msg = self._factory.create_report(
            report_title="状态报告",
            report_data=report_data,
            priority=Priority.ROUTINE,
        )
        msg_dict = msg.to_dict()
        self._log_message(msg_dict)

        # 尝试写入 COS
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        report_path = f"reports/report_{ts}.json"
        self.write_to_bucket(report_path, json.dumps(msg_dict, ensure_ascii=False))

        # 更新状态
        self._status["last_report_sent"] = self._utc_now()
        self._save_status()

        logger.info("报告已推送: %s", msg.msg_id)
        return msg_dict

    def pull_receipt(self) -> Optional[Dict[str, Any]]:
        """
        拉取铸渊的最新回执
        占位实现: 返回 None
        """
        receipt_path = "receipts/latest.json"
        content = self.read_from_bucket(receipt_path)

        if content:
            receipt = json.loads(content)
            self._status["last_receipt_received"] = self._utc_now()
            self._save_status()
            return receipt

        return None

    def get_bridge_status(self) -> Dict[str, Any]:
        """
        返回当前桥接状态
        """
        return {
            **self._status,
            "credentials_configured": self.config.has_credentials(),
            "bucket_name": self.config.bucket_name,
            "region": self.config.region,
            "message_log_size": len(self._message_log),
        }
