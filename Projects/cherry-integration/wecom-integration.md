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

## 测试记录

### 2026-09-02 测试

| 测试项 | 结果 | 备注 |
|--------|------|------|
| 搜索江宇歌 | ✅ 成功 | 找到用户信息 |
| 创建日程 | ✅ 成功 | 2026-09-03 10:00-11:00 |
| 创建会议 | ✅ 成功 | 生成会议号和链接 |
| 创建待办 | ✅ 成功 | 机器人创建的待办 |
| 完成待办 | ✅ 成功 | 机器人可完成自己创建的待办 |
| 创建表格 | ✅ 成功 | 生成在线表格链接 |
| 获取会话列表 | ✅ 成功 | 返回 2 个会话 |
| 发送消息 - 单聊 | ✅ 成功 | 发送给李奕兴 |
| 发送消息 - 群聊 | ✅ 成功 | 发送到测试群 |
| 发送消息 - 新用户 | ❌ 失败 | 江宇歌未和机器人对话过 |
| 读取消息内容 |  失败 | 需公司启用 API |

## 配置要求

### 个人/小团队（≤10 人）
- 消息、文档、事件、会议、待办功能可用

### 公司（>10 人）
- 文档 CLI 功能可用
- 其他功能需管理员启用

### 启用消息功能步骤
1. 登录企业微信管理后台
2. 进入 应用管理 → "李奕兴的机器人"
3. 在 API 权限 中启用：
   - 消息读取
   - 消息发送

## 常用命令

```bash
# 搜索用户
bun x wecom-cli contact users search --keywords "江宇歌"

# 创建日程
bun x wecom-cli calendar schedules create \
  --subject "会议标题" \
  --begin-time "2026-09-03 10:00:00" \
  --end-time "2026-09-03 11:00:00" \
  --attendees '[{"userid":"xxx"}]'

# 创建会议
bun x wecom-cli meeting create \
  --subject "会议标题" \
  --begin-time "2026-09-03 10:00:00" \
  --end-time "2026-09-03 10:30:00" \
  --attendees '[{"userid":"xxx"}]'

# 创建待办
bun x wecom-cli todo create \
  --items '[{"title":"待办标题","description":"描述"}]'

# 创建表格
bun x wecom-cli sheet create \
  --doc-name "表格名称" \
  --doc-type sheet

# 发送消息
bun x wecom-cli message aibot send \
  --chat-id "用户 ID 或群聊 ID" \
  --msg-type markdown \
  --markdown '{"content":"消息内容"}'

# 获取会话列表
bun x wecom-cli message aibot sessions list
```

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
