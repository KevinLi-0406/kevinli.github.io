# 企业微信集成详情

## 概述

企业微信 CLI (wecom-cli) 集成，版本 1.2.0

## 安装信息

| 项目 | 详情 |
|------|------|
| **CLI 版本** | 1.2.0 |
| **安装方式** | `bun x @wecom/cli` |
| **机器人名称** | 李奕兴的机器人 |
| **机器人 ID** | `aibiW0wBHmD2iCO1VmDQXF1wSDdg3kMKzn1` |

## 已安装技能

| 技能名称 | 功能 | 状态 |
|---------|------|------|
| wecomcli-contact | 联系人管理 | ✅ |
| wecomcli-message | 消息收发 | ✅ |
| wecomcli-todo | 待办事项 | ✅ |
| wecomcli-meeting | 会议管理 | ✅ |
| wecomcli-doc | 文档管理 | ✅ |
| wecomcli-calendar | 日程管理 | ✅ |
| wecomcli-sheet | 表格管理 | ✅ |

## 功能状态

### ✅ 已验证可用

| 功能 | 命令 |
|------|------|
| 联系人搜索 | `wecom-cli contact users search` |
| 日程创建/查询 | `wecom-cli calendar schedules create/list` |
| 会议创建 | `wecom-cli meeting create` |
| 待办读取/创建/完成 | `wecom-cli todo list/create/finish` |
| 表格创建 | `wecom-cli sheet create` |
| 会话列表 | `wecom-cli message aibot sessions list` |
| 消息发送 | `wecom-cli message aibot send` |

### ⚠️ 受限功能

| 功能 | 错误代码 | 说明 |
|------|---------|------|
| 消息读取 | 853006 | 需公司在管理后台启用 |
| 应用消息发送 | 853006 | 需公司在管理后台启用 |

## 与飞书集成对比

| 特性 | 飞书 | 企业微信 |
|------|------|----------|
| 消息发送 | ✅ 完整 | ⚠️ aibot |
| 消息读取 | ✅ 完整 | ⚠️ 需启用 |
| 日程管理 | ✅ | ✅ |
| 会议管理 | ✅ | ✅ |
| 待办管理 | ⚠️ 需权限 | ✅ |
| 文档管理 | ✅ | ✅ |
