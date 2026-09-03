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
| **授权用户** | 李奕兴 (Kevin) |
| **用户 ID** | `wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA` |

## 已安装技能

| 技能名称 | 功能 | 状态 |
|---------|------|------|
| wecomcli-contact | 联系人管理 | ✅ 已安装 |
| wecomcli-message | 消息收发 | ✅ 已安装 |
| wecomcli-todo | 待办事项 | ✅ 已安装 |
| wecomcli-meeting | 会议管理 | ✅ 已安装 |
| wecomcli-doc | 文档管理 | ✅ 已安装 |
| wecomcli-calendar | 日程管理 | ✅ 已安装 |
| wecomcli-sheet | 表格管理 | ✅ 已安装 |

## 功能状态

### ✅ 已验证可用功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 联系人搜索 | `wecom-cli contact users search` | 可按姓名搜索用户 |
| 日程创建 | `wecom-cli calendar schedules create` | 创建日程并添加参与人 |
| 日程查询 | `wecom-cli calendar schedules list` | 查询指定时间范围的日程 |
| 会议创建 | `wecom-cli meeting create` | 创建会议并生成会议链接 |
| 待办读取 | `wecom-cli todo list` | 读取待办列表 |
| 待办创建 | `wecom-cli todo create` | 创建待办事项 |
| 待办完成 | `wecom-cli todo finish` | 完成机器人创建的待办 |
| 表格创建 | `wecom-cli sheet create` | 创建在线表格文档 |
| 会话列表 | `wecom-cli message aibot sessions list` | 获取机器人最近会话 |
| 消息发送 | `wecom-cli message aibot send` | 发送消息到单聊/群聊 |

### ⚠️ 受限功能（需公司启用 API）

| 功能 | 错误代码 | 说明 |
|------|---------|------|
| 消息读取 | 853006 | 需公司在管理后台启用 |
| 应用消息发送 | 853006 | 需公司在管理后台启用 |
| 群聊列表 | 853006 | 需公司在管理后台启用 |

## 关键发现

### 1. 消息发送限制

| 发送方式 | 状态 | 说明 |
|---------|------|------|
| `message send` | ️ 受限 | 需公司启用 API 权限 |
| `message aibot send` | ✅ 可用 | 智能机器人消息发送 |

### 2. 待办管理规则

| 待办创建者 | 机器人可操作？ |
|-----------|--------------|
| 机器人 | ✅ 可读取/完成/更新 |
| 真人用户 | ✅ 可读取/查询 |
| 真人用户 | ❌ 不可完成/更新/删除 |

### 3. 消息发送规则

| 成员状态 | 机器人可发送？ |
|---------|--------------|
| 已和机器人对话过 | ✅ 可以发送 |
| 未和机器人对话过 | ❌ 不能主动发送 |
| 在同一个群聊中 | ✅ 可通过群发送 |

## 与飞书集成对比

| 特性 | 飞书 | 企业微信 |
|------|------|---------|
| CLI 工具 | lark-cli | wecom-cli |
| 安装方式 | mise/cherry-tools | bun x |
| 认证方式 | OAuth + 扫码 | Bot ID + Secret |
| 消息发送 | ✅ 完整支持 | ⚠️ aibot 方式可用 |
| 消息读取 | ✅ 完整支持 | ⚠️ 需公司启用 |
| 日程管理 | ✅ 完整支持 | ✅ 完整支持 |
| 会议管理 | ✅ 完整支持 | ✅ 完整支持 |
| 待办管理 | ⚠️ 需权限 | ✅ 完整支持 |
| 文档管理 | ✅ 完整支持 | ✅ 完整支持 |
