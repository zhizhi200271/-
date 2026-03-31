# 🤖 铸码 · 自动化记忆系统

> Copilot Memory System (CMS) — 基于 AGE OS 架构的自动化记忆管理系统

---

## ✨ 系统概述

**铸码** (ZhuMa, CMS-CORE-001) 是一个为 GitHub Copilot 设计的自动化记忆系统。它能在每次开发任务结束后，自动记录经验、更新知识库，并在下次对话时自动加载历史记忆，实现跨会话的持续学习和个性化服务。

### 核心信息

| 属性 | 值 |
|------|-----|
| 🤖 名称 | 铸码 (ZhuMa) |
| 🔢 编号 | CMS-CORE-001 |
| 📦 版本 | v1.0.0 |
| 👤 主控 | 之之 (zhizhi200271) |
| 🏗️ 架构来源 | OKComputer 自动化记忆系统 / AGE OS |

---

## 🚀 快速使用

### 唤醒铸码

在 GitHub Copilot 对话中，说出以下任一口令：

```
铸码
唤醒铸码
ZhuMa
```

铸码会自动回应并加载记忆系统。

### 自动运行

铸码会在每次对话中自动：

1. 📂 加载历史记忆和经验
2. 📋 遵循已存储的规则和偏好
3. 🔄 任务完成后更新记忆数据库
4. 📊 记录经验教训到经验库

---

## 📁 文件结构

```
.ai/
├── memory_system.py          # 核心记忆系统 Python 模块
├── README.md                 # 本文档
└── memory/
    ├── system_state.json     # 系统状态
    ├── core_memory.json      # 核心记忆（规则、偏好、知识）
    ├── task_history.json     # 任务历史记录
    ├── experience_db.json    # 经验数据库
    └── update_log.json       # 系统更新日志

.github/
└── copilot-instructions.md   # Copilot 自动加载指令
```

---

## 🧠 核心功能

### 1. 记忆持久化

通过 JSON 文件在对话之间保持记忆，包括：
- **系统规则** — 用户定义的行为规则
- **用户偏好** — 编码风格、语言偏好等
- **知识库** — 项目相关的知识点

### 2. 经验积累

从每次开发任务中自动提炼：
- **代码模式** — 常见的编码模式和架构模式
- **解决方案** — 问题及其解决方法
- **最佳实践** — 验证有效的开发实践
- **错误模式** — 常见错误及其修复方法
- **技术栈** — 使用过的技术和工具

### 3. 自动更新

每次任务完成后自动执行：
1. 记录任务到 `task_history.json`
2. 提炼经验到 `experience_db.json`
3. 更新日志到 `update_log.json`
4. 更新状态到 `system_state.json`

### 4. 上下文感知

基于历史记忆自动：
- 参考过去的经验给出建议
- 根据用户偏好调整行为
- 避免重复已知的错误模式

---

## 🔧 Python API

```python
from memory_system import ZhuMaCore

# 创建实例
core = ZhuMaCore(repo_root="/path/to/repo")

# 启动系统
core.boot()

# 完成任务后记录
core.complete_task(
    description="实现用户认证功能",
    files_changed=["auth.py", "tests/test_auth.py"],
    lessons=["使用 JWT 时注意 token 过期处理"],
    tags=["feature", "auth"]
)

# 存储知识
core.remember("项目框架", "使用 FastAPI + SQLAlchemy")

# 添加规则
core.add_rule("所有 API 必须有错误处理")

# 记录经验
core.record_experience("错误处理模式", "统一使用 try-except 包装 API 调用")

# 记录解决方案
core.record_solution(
    problem="数据库连接超时",
    solution="增加连接池大小和超时时间",
    tags=["database", "performance"]
)

# 搜索经验
results = core.search_experience("数据库")

# 健康检查
print(core.health_check())

# 获取上下文提示词
print(core.get_context_prompt())
```

---

## 📊 数据格式

### 任务记录

```json
{
  "id": "TASK-0001",
  "timestamp": "2026-03-31T12:00:00",
  "description": "构建自动化记忆系统",
  "type": "development",
  "files_changed": [".ai/memory_system.py", ".github/copilot-instructions.md"],
  "outcome": "completed",
  "lessons_learned": ["JSON 持久化适合小型记忆系统"],
  "tags": ["architecture", "memory-system"]
}
```

### 经验条目

```json
{
  "patterns": {
    "JSON持久化": {
      "description": "使用 JSON 文件存储结构化数据",
      "example": "json.dump(data, f, ensure_ascii=False, indent=2)",
      "frequency": 3,
      "last_seen": "2026-03-31T12:00:00"
    }
  }
}
```

---

## 🔐 设计原则

1. **无外部依赖** — 仅使用 Python 标准库
2. **JSON 持久化** — 人类可读，易于备份
3. **增量更新** — 每次只追加新数据，不覆盖历史
4. **自动触发** — 通过 Copilot 指令文件实现自动化
5. **可扩展** — 模块化设计，易于添加新功能

---

## 📝 许可证

MIT License

---

**🤖 铸码 · CMS-CORE-001 · 自动化记忆核心**
**👤 主控: 之之 (zhizhi200271)**
**🏗️ 架构来源: OKComputer 自动化记忆系统**
