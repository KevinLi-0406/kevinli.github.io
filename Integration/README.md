# Integration - 统一信息平台

本目录包含**统一信息平台**项目的所有技术文档。

> 核心理念：**一个大脑，五个触角** —— Cherry Studio AI 整合企微、飞书、Teams、邮箱、D365

## 目录结构

```
Integration/
├── README.md                 # 本文件
├── unified-platform.md       # 统一平台架构设计（需求 + 方案 + 路线图）
├── requirements.md           # 功能需求文档
├── integration-details.md    # 集成详情（配置、功能状态、任务、进度、错误记录）
└── d365-mcp-config.json      # D365 MCP 配置模板（secret 已脱敏）
```

## 集成状态

| 平台 | CLI 工具 | 消息读取 | 消息发送 | 日程/会议 | 待办 | 联系人 |
|------|---------|---------|---------|----------|------|--------|
| 飞书 | lark-cli v1.0.92 | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| 企业微信 | wecom-cli v1.2.0 | ❌ (需启用) | ✅ (aibot) | ✅ | ✅ | ✅ |
| Teams | 待开发 |  | ⏳ | ⏳ |  | ⏳ |
| 邮箱 | 待开发 | ⏳ | ⏳ | - | - | - |
| **D365 MCP** | **SPP 运维助手** | **-** | **-** | **-** | **-** | **✅ (1777 表)** |

## 快速链接

- [统一平台架构设计](unified-platform.md)
- [功能需求文档](requirements.md)
- [集成详情](integration-details.md) — 配置信息、功能状态、任务清单、进度日志、错误记录
  - [D365 MCP 集成详情](integration-details.md#六d365-mcp-集成详情spp-运维助手) — SPP 运维助手环境配置、操作分类、铁律机制
- [D365 MCP 配置模板](d365-mcp-config.json) — 生产/测试环境 MCP JSON（secret 已脱敏）
