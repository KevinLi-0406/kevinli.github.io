# 飞书多平台消息集成项目

## 项目概述

将飞书、企业微信、邮件等多平台消息整合到 Cherry Studio AI 助手中，实现一站式消息管理和智能总结。

## 项目目标

1. **消息整合**：在一个界面中处理所有平台的消息
2. **智能总结**：AI 自动总结和分类消息内容
3. **待办管理**：跨平台待办事项统一管理
4. **邮件集成**：读取和管理飞书邮件

## 技术架构

```
Cherry Studio (AI 中枢)
    ↓ MCP 协议
飞书 lark-cli (命令行工具)
    ↓ API 调用
飞书开放平台
    ↓
消息 / 任务 / 联系人 / 邮件
```

## 项目状态

- **开始日期**：2026-09-02
- **当前阶段**：权限配置和基础功能测试
- **预计完成**：待权限审批通过后继续开发

## 文档索引

- [需求文档](requirements.md) - 详细功能需求
- [任务清单](tasks.md) - 开发任务跟踪
- [进度日志](progress-log.md) - 每日进度记录
- [操作日志](operation-log.md) - 技术操作记录

## 快速链接

- GitHub 仓库：https://github.com/KevinLi-0406/kevinli.github.io
- 飞书开放平台：https://open.feishu.cn
- Cherry Studio 文档：https://docs.cherry-ai.com
