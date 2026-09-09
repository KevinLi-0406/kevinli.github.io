# 定时任务通知渠道误投问题

**日期**：2026-09-09  
**严重程度**：中  
**分类**：Cherry Studio / 定时任务 / 飞书

---

## 问题描述

两个 Mysav 定时任务（Daily Export、Daily Email）执行后，通知消息被发送到了一个用户未指定的飞书群，而非用户期望的私有群。

### 具体表现

- 定时任务配置中 `channelIds` 设为 `5de9998d-be06-4b1a-acd2-960a3ca5a915`（Cherry Studio 飞书频道"飞书-李奕兴"）
- 该频道默认投递到一个包含其他成员的群，而非用户单独与机器人的群
- 用户发现后要求：创建专属群 + 定时任务只发到该群

---

## 根因分析

### 1. `channelIds` 字段理解偏差

- Cherry Studio 的 cron `channelIds` 接收的是 **Cherry Studio 频道 ID**（如 `5de9998d-...`），而非飞书 chat_id（如 `oc_xxx`）
- 频道 ID 对应的是一个 Cherry 配置的 IM 通道，该通道有自己的投递目标（可能是一个群、可能是多个群）
- 直接传入飞书 chat_id 会报错：`Channel "oc_xxx" not found`

### 2. 频道默认投递行为

- 当 cron 任务设置 `channelIds` 后，任务执行结果会投递到该 Cherry 频道
- 频道再根据其配置将消息转发到关联的飞书群
- 如果频道配置关联了非预期的群，消息就会投递到错误的地方

---

## 解决方案

### 方案核心：绕过 Cherry 频道投递，任务内部直接调用飞书 API

1. **创建专属飞书群**
   - 群名：`Mysav定时任务通知`
   - 成员：仅用户（李奕兴）+ 机器人
   - chat_id：`oc_710bbf75e761c08ac769499cff2719a8`

2. **修改定时任务配置**
   - 将 `channelIds` 设为空数组 `[]`（不通过 Cherry 频道投递）
   - 在任务 prompt 中添加步骤：执行完成后，显式调用 `im_v1_message_create` 发送通知到指定 chat_id

3. **消息格式要求**
   - 飞书 text 消息的 `content` 必须是 JSON 字符串：`{"text":"消息内容"}`
   - 不能用普通字符串，否则报错 `content is not a string in json format`

---

## 关键代码/配置示例

### 定时任务 prompt 中的通知步骤

```markdown
## 任务二：通知到新飞书群

导出完成后，使用飞书 MCP 工具 `im_v1_message_create` 向指定群发送通知：
- receive_id_type: "chat_id"
- receive_id: "oc_710bbf75e761c08ac769499cff2719a8"
- msg_type: "text"
- content: 必须是 JSON 字符串格式，例如：{"text":"[Mysav Export 完成] 昨日导出 N 条记录，文件已保存"}

如果导出失败，也要向该群发送失败通知。
```

### 重建定时任务的参数

```json
{
  "name": "Mysav Error Logs Daily Export (UAT2)",
  "cron": "0 10 * * *",
  "channel_ids": [],
  "timeout_minutes": 30,
  "message": "..."
}
```

---

## 经验教训

1. **区分 Cherry 频道 ID 和飞书 chat_id**
   - Cherry 频道 ID：UUID 格式（如 `5de9998d-be06-4b1a-acd2-960a3ca5a915`）
   - 飞书 chat_id：`oc_` 前缀（如 `oc_710bbf75e761c08ac769499cff2719a8`）
   - cron 的 `channelIds` 只接受前者

2. **需要精确控制投递目标时，绕过频道投递**
   - 将 `channelIds` 设为 `[]`
   - 在任务内部使用 MCP 工具直接调用目标 IM API

3. **飞书消息格式易错点**
   - text 类型消息的 content 必须是 `{"text":"..."}` 格式的 JSON 字符串
   - 不能直接传普通字符串

4. **定时任务重建而非更新**
   - Cherry cron 工具没有 update 动作，只有 add/remove
   - 修改配置需要先 remove 再 add

---

## 相关文件/配置

- 定时任务 ID：`1e92a20d-e73e-4ba6-ac25-cffed21a16a6`（Export）、`9c47cb4c-3c3a-456f-a3f7-17eb7284364a`（Email）
- 飞书群 chat_id：`oc_710bbf75e761c08ac769499cff2719a8`
- 飞书群名：Mysav定时任务通知
