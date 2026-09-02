# Cherry 与飞书、企微打通 - 操作日志

## 技术操作记录

### 2026-09-02 18:00 - 飞书 CLI 安装

```bash
# 安装 lark-cli 工具
mise install lark-cli@latest

# 验证安装
lark-cli --version
# 输出：lark-cli version 1.0.92
```

**结果**：✅ 安装成功

---

### 2026-09-02 18:05 - 飞书配置初始化

```bash
# 启动配置流程
lark-cli config init --new

# 生成二维码
lark-cli auth qrcode "https://open.feishu.cn/page/cli?user_code=2FVT-RQTD" --output feishu_auth_qr.png --size 300
```

**结果**：✅ 配置完成

---

### 2026-09-02 18:15 - 飞书身份验证

```bash
# 查看当前身份
lark-cli whoami

# 输出：
# profile: cli_aa1d00640cf9dcd4
# appId: cli_aa1d00640cf9dcd4
# brand: feishu
# identity: bot
# tokenStatus: ready
```

**结果**：✅ 机器人身份配置成功

---

### 2026-09-02 18:25 - 飞书测试群组创建

```bash
# 查看群组列表
lark-cli im +chat-list --format json

# 输出：
# {
#   "ok": true,
#   "data": {
#     "chats": [
#       {
#         "chat_id": "oc_a3154db1370d2421d74690a0dac270ed",
#         "name": "CLI 测试群",
#         "chat_mode": "group"
#       }
#     ]
#   }
# }
```

**结果**：✅ 群组创建成功

---

### 2026-09-02 18:30 - 飞书消息收发测试

```bash
# 发送消息到测试群
lark-cli im +messages-send \
  --chat-id oc_a3154db1370d2421d74690a0dac270ed \
  --text " 飞书机器人连接成功！这是来自 Cherry Studio 的测试消息。" \
  --format json

# 输出：
# {
#   "ok": true,
#   "data": {
#     "chat_id": "oc_a3154db1370d2421d74690a0dac270ed",
#     "create_time": "2026-09-02 18:37:08",
#     "message_id": "om_x100b664b8bf2bcacc36a882adefc5aa"
#   }
# }

# 读取群组消息
lark-cli im +chat-messages-list \
  --chat-id oc_a3154db1370d2421d74690a0dac270ed \
  --format json
```

**结果**：✅ 双向通信验证通过

---

### 2026-09-02 19:00 - 企业微信 CLI 安装

```bash
# 安装 wecom-cli
bun x @wecom/cli --version
# 输出：wecom-cli 1.2.0 (wecom 2026-08-25T10:18:11Z 78c514b)

# 安装技能包
# 通过 MCP skills install 安装以下技能：
# - wecomcli-contact
# - wecomcli-message
# - wecomcli-todo
# - wecomcli-meeting
# - wecomcli-doc
```

**结果**：✅ 安装成功

---

### 2026-09-02 19:15 - 企业微信联系人搜索

```bash
# 搜索用户江宇歌
bun x wecom-cli contact users search --keywords "江宇歌"

# 输出：
# {
#   "users": [
#     {
#       "userid": "wofFQbCAAAgxV2WSVpCoIlDswmHgo3Lw",
#       "name": "江宇歌 (Chloe)",
#       "alias": "Chloe",
#       "position": "助理应用工程师",
#       "departments": ["九号公司/集团信息化中心/..."],
#       "email": "yuge.jiang@ninebot.com"
#     }
#   ]
# }
```

**结果**：✅ 搜索成功

---

### 2026-09-02 19:20 - 企业微信日程创建

```bash
# 创建日程
bun x wecom-cli calendar schedules create \
  --subject "工作沟通会议" \
  --begin-time "2026-09-03 10:00:00" \
  --end-time "2026-09-03 11:00:00" \
  --attendees '[{"userid":"wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA"},{"userid":"wofFQbCAAAgxV2WSVpCoIlDswmHgo3Lw"}]'

# 输出：
# {
#   "schedule_id": "e996e349885aad9edffd0df77768b14elhgqapnp"
# }
```

**结果**：✅ 创建成功

---

### 2026-09-02 19:25 - 企业微信会议创建

```bash
# 创建会议
bun x wecom-cli meeting create \
  --subject "工作沟通会议" \
  --begin-time "2026-09-03 10:00:00" \
  --end-time "2026-09-03 10:30:00" \
  --attendees '[{"userid":"wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA"},{"userid":"wofFQbCAAAgxV2WSVpCoIlDswmHgo3Lw"}]'

# 输出：
# {
#   "meeting_id": "mtfFQbCAAAimx9UA5fIn3gvNXxwNxw1w",
#   "meeting_code": "416964698",
#   "meeting_link": "https://work.weixin.qq.com/webapp/tm/xe9WZxpnm1d"
# }
```

**结果**：✅ 创建成功

---

### 2026-09-02 19:30 - 企业微信待办管理

```bash
# 读取待办列表
bun x wecom-cli todo list --limit 10

# 创建待办
bun x wecom-cli todo create \
  --items '[{"title":"机器人测试待办","description":"由机器人创建"}]'

# 输出：
# {
#   "items": [
#     {
#       "success": true,
#       "todo_id": "tdfFQbCAAAWt2zdLs_LbpHo83msSq0Fw",
#       "title": "机器人测试待办"
#     }
#   ]
# }

# 完成待办
bun x wecom-cli todo finish \
  --items '[{"todo_id":"tdfFQbCAAAWt2zdLs_LbpHo83msSq0Fw"}]'

# 尝试完成用户创建的待办（失败）
bun x wecom-cli todo finish \
  --items '[{"todo_id":"tdfFQbCAAAa4a6rbgwaoylWEuXr1na7Q"}]'

# 输出：
# {"error":{"code":860024,"message":"仅待办创建者可更新"}}
```

**结果**：✅ 机器人可完成自己创建的待办
**关键发现**：机器人无法完成用户创建的待办

---

### 2026-09-02 19:35 - 企业微信表格创建

```bash
# 创建空表格
bun x wecom-cli sheet create \
  --doc-name "新建表格" \
  --doc-type sheet

# 输出：
# {
#   "docid": "e3_AFQAW3g4APECNVB0yEid8TRy0euJh_a",
#   "url": "https://doc.weixin.qq.com/sheet/e3_AFQAW3g4APECNVB0yEid8TRy0euJh_a?scode=...",
#   "doc_name": "新建表格"
# }
```

**结果**：✅ 创建成功

---

### 2026-09-02 19:40 - 企业微信会话管理

```bash
# 获取会话列表
bun x wecom-cli message aibot sessions list

# 输出：
# {
#   "sessions": [
#     {
#       "chat_id": "wrfFQbCAAAA9OfAN75TfoobnpfVzsVJw",
#       "chat_name": "李奕兴的机器人测试群",
#       "last_msg_time": "2026-09-02 19:47:36",
#       "chat_type": "group"
#     },
#     {
#       "chat_id": "wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA",
#       "chat_name": "李奕兴 (Kevin)",
#       "last_msg_time": "2026-09-02 19:34:47",
#       "chat_type": "single"
#     }
#   ]
# }
```

**结果**：✅ 获取成功（2 个会话）

---

### 2026-09-02 19:45 - 企业微信消息发送

```bash
# 发送给李奕兴（成功）
bun x wecom-cli message aibot send \
  --chat-id "wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA" \
  --msg-type markdown \
  --markdown '{"content":"你好"}'

# 输出：{"success": true}

# 发送给群聊（成功）
bun x wecom-cli message aibot send \
  --chat-id "wrfFQbCAAAA9OfAN75TfoobnpfVzsVJw" \
  --msg-type markdown \
  --markdown '{"content":"你好"}'

# 输出：{"success": true}

# 发送给江宇歌（失败）
bun x wecom-cli message aibot send \
  --chat-id "wofFQbCAAAgxV2WSVpCoIlDswmHgo3Lw" \
  --msg-type markdown \
  --markdown '{"content":"你好"}'

# 输出：
# {"error":{"code":853008,"message":"当前会话不是机器人的最近会话..."}}
```

**结果**：⚠️ 部分成功
**关键发现**：机器人只能给已对话过的成员发送消息

---

### 2026-09-02 19:50 - 企业微信消息读取测试

```bash
# 尝试读取单聊消息
bun x wecom-cli chat messages list \
  --chat-id "wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA" \
  --begin-time "2026-08-26 00:00:00" \
  --end-time "2026-09-02 23:59:59"

# 输出：
# {"errcode":853006,"errmsg":"this tool is not available for your corporation..."}

# 尝试读取群聊消息（同样失败）
bun x wecom-cli chat messages list \
  --chat-id "wrfFQbCAAAA9OfAN75TfoobnpfVzsVJw" \
  --begin-time "2026-08-26 00:00:00" \
  --end-time "2026-09-02 23:59:59"

# 输出：同样错误 853006
```

**结果**：⚠️ 需公司启用 API

---

## 配置信息汇总

### 飞书配置

| 项目 | 值 |
|------|-----|
| CLI 版本 | 1.0.92 |
| 应用 ID | cli_aa1d00640cf9dcd4 |
| 机器人名称 | 李奕兴的智能助手 |
| 测试群 ID | oc_a3154db1370d2421d74690a0dac270ed |
| 用户 Open ID | ou_d1d7f2c929754d891fee5d97bc894d74 |
| 租户 Key | 19042693ad891b8f |

### 企业微信配置

| 项目 | 值 |
|------|-----|
| CLI 版本 | 1.2.0 |
| 机器人 ID | aibiW0wBHmD2iCO1VmDQXF1wSDdg3kMKzn1 |
| 机器人名称 | 李奕兴的机器人 |
| 用户 ID | wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA |
| 用户名称 | 李奕兴 (Kevin) |
| 测试群 ID | wrfFQbCAAAA9OfAN75TfoobnpfVzsVJw |

---

## 错误记录

### 错误 1: 飞书 scope 名称错误
**时间**：2026-09-02 19:15
**错误**：`The provided scope list contains invalid or malformed scopes`
**原因**：部分 scope 名称不正确
**解决**：简化 scope 列表，使用正确的名称

### 错误 2: 飞书搜索返回空结果
**时间**：2026-09-02 19:00
**错误**：搜索返回 0 条结果
**可能原因**：消息索引延迟或权限限制
**状态**：待验证

### 错误 3: 企业微信消息读取受限
**时间**：2026-09-02 19:50
**错误代码**：853006
**错误信息**：`this tool is not available for your corporation`
**原因**：公司未启用消息 API
**解决**：需联系管理员启用

### 错误 4: 企业微信发送消息给新用户失败
**时间**：2026-09-02 19:45
**错误代码**：853008
**错误信息**：`当前会话不是机器人的最近会话`
**原因**：成员未和机器人对话过
**解决**：让成员先和机器人对话

### 错误 5: 企业微信完成用户待办失败
**时间**：2026-09-02 19:30
**错误代码**：860024
**错误信息**：`仅待办创建者可更新`
**原因**：机器人无法修改用户创建的数据
**解决**：机器人只能完成自己创建的待办

---

## 权限状态

### 飞书权限

| 权限 | 状态 | 说明 |
|------|------|------|
| im:message:readonly | ✅ 已授予 | 读取消息 |
| im:message | ✅ 已授予 | 消息操作 |
| search:message | ✅ 已授予 | 搜索消息 |
| contact:user.base_profile:readonly | ✅ 已授予 | 读取用户信息 |
| mail:user_mailbox:readonly | ✅ 已授予 | 读取邮箱 |
| im:chat:read | ⏳ 审核中 | 读取群组列表 |
| im:message.group_msg:get_as_user | ⏳ 审核中 | 读取群消息 |
| im:message.p2p_msg:get_as_user | ⏳ 审核中 | 读取私聊消息 |
| task:task:read |  审核中 | 读取待办 |

### 企业微信权限

| 功能 | 状态 | 说明 |
|------|------|------|
| 联系人搜索 | ✅ | 默认可用 |
| 日程管理 | ✅ | 默认可用 |
| 会议创建 | ✅ | 默认可用 |
| 待办管理 | ✅ | 默认可用 |
| 文档管理 | ✅ | 默认可用 |
| 消息发送 (aibot) | ✅ | 默认可用 |
| 消息读取 | ⚠️ | 需公司启用 |
| 消息发送 (应用) | ️ | 需公司启用 |
| 群聊列表 | ️ | 需公司启用 |
