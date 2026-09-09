# Integration - 统一信息平台

本目录包含**统一信息平台**项目的所有技术文档与 Bot 代码。

> 核心理念：**一个大脑，五个触角** —— Cherry Studio AI 整合企微、飞书、Teams、邮箱、D365；Dify 作为云端 AI 引擎支撑 Bot 实时问答。

## 目录结构

```
Integration/
├── README.md                 # 本文件
├── unified-platform.md       # 统一平台架构设计（需求 + 方案 + 路线图）
├── requirements.md           # 功能需求文档
├── integration-details.md    # 集成详情（配置、功能状态、任务、进度、错误记录）
├── d365-mcp-config.json      # D365 MCP 配置模板（secret 已脱敏）
├── monitored-chats.json      # 飞书消息监听配置
├── sync-log.md               # GitHub 仓库同步日志
├── feishu-bot/               # 飞书实时监听机器人（WebSocket + Dify）
│   ├── feishu-bot.js
│   ├── package.json
│   ├── .env.example
│   └── README.md
└── wecom-bot/                # 企微智能机器人（WebSocket + Dify）
    ├── wecom-bot.js
    ├── package.json
    ├── .env.example
    └── README.md
```

## 集成状态

| 平台 | 工具/入口 | 消息读取 | 消息发送 | 日程/会议 | 待办 | 联系人 | 备注 |
|------|----------|---------|---------|----------|------|--------|------|
| 飞书 | lark-cli v1.0.92 + Bot | ✅ | ✅ | ✅ | ⚠️ | ✅ | Bot 端已接入 Dify（WebSocket 实时监听） |
| 企业微信 | wecom-cli v1.2.0 + Bot | ❌ (需启用) | ✅ (aibot/Bot) | ✅ | ✅ | ✅ | Bot 端已接入 Dify（流式回复） |
| Teams | 待开发 |  | ⏳ | ⏳ |  | ⏳ |  |
| 邮箱 | 网易 SMTP / Bot IMAP | ✅ (IMAP) | ✅ (SMTP) | - | - | - | 飞书 Bot 已集成邮件收发 |
| **D365 MCP** | **SPP 运维助手** | - | - | - | - | ✅ (1777 表) | Dataverse 运维（查询/修改/DDL/发布） |
| **Dify** | **http://10.232.5.5** | - | - | - | - | - | **AI 引擎（飞书+企微 Bot 共用）** |

## 快速链接

- [统一平台架构设计](unified-platform.md)
- [功能需求文档](requirements.md)
- [集成详情](integration-details.md) — 配置信息、功能状态、任务清单、进度日志、错误记录
  - [D365 MCP 集成详情](integration-details.md#六d365-mcp-集成详情spp-运维助手) — SPP 运维助手环境配置、操作分类、铁律机制
  - [飞书 / 企微 Bot 集成详情](integration-details.md#二五飞书企微实时监听-botdify-引擎) — Dify Chat API 接入、多轮对话、邮件操作
- [D365 MCP 配置模板](d365-mcp-config.json) — 生产/测试环境 MCP JSON（secret 已脱敏）
- [飞书 Bot 子项目](feishu-bot/) — WebSocket 实时监听 + Dify + IMAP/SMTP 邮件
- [企微 Bot 子项目](wecom-bot/) — WebSocket 长连接 + Dify（流式回复）
