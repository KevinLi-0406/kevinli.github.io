# lark-cli 飞书任务自动化踩坑记录

**日期**：2026-09-20  
**严重程度**：低  
**分类**：Cherry Studio / lark-cli / 飞书任务 / 定时任务

---

## 背景

需要定时检查 Cherry Studio 中 lark-cli 的 User token 是否过期，过期时自动提醒用户重新授权。最初方案是发飞书私聊，但私聊消息太多容易漏看，改为创建飞书任务作为提醒。

---

## 问题描述

### 问题 1：Bot 创建的任务用户看不到

用 `--as bot` 创建任务后，用户在飞书任务中打开显示"暂无权限查看该任务"。

**原因**：任务归属在 Bot 名下，用户没有权限查看 Bot 创建的任务。

**解决**：用 `+assign --add "ou_xxx"` 将用户添加为任务成员。

### 问题 2：User token 过期导致无法创建任务

User token 的 refresh token 7 天到期，过期后 `--as user` 创建任务会失败。

### 问题 3：授权链接每次不同且 10 分钟过期

`lark-cli auth login --no-wait` 每次生成新的 `flow_id` 和 `user_code`，链接有效期仅 600 秒（10 分钟）。不能把链接硬编码到定时任务中。

### 问题 4：Bot 无法访问用户的 tasklist

Bot 不能直接往用户的 tasklist 创建任务（`permission_denied`），也不能被加入用户的 tasklist（`+tasklist-members` 只接受 open_id，不接受 app_id）。

### 问题 5：Bot 创建的任务不在用户的分组下

Bot 创建的任务只能放在 Bot 自己的 tasklist 里，分配给用户后出现在"默认分组"，不在用户自定义的「 机器人运维」分组下。

---

## 根因分析

### 1. User vs Bot 身份差异

| 特性 | User 身份 | Bot 身份 |
|------|-----------|----------|
| token 有效期 | refresh token 7 天 | 永不过期 |
| 创建任务归属 | 用户自己 | Bot |
| 访问用户 tasklist | 可以 | 不可以 |
| 分配用户为成员 | 可以 | 可以（通过 +assign） |
| 任务分组 | 正确 | 默认分组 |

### 2. 飞书任务 API 限制

- `tasklists` 成员管理只支持 open_id（用户），不支持 app_id（应用）
- Bot 无法被添加到用户的 tasklist
- 没有 API 可以将任务从一个 tasklist 移到另一个

### 3. OAuth device flow 限制

- 每次调用生成新的 device_code 和 verification_url
- 链接有效期 10 分钟，超时需重新生成
- 用户必须在浏览器中手动完成授权，无法自动化

---

## 解决方案

### 最终方案：双身份降级策略

```
定时任务（每天 09:00）
    ↓
检查 User token 状态
    ↓
├─ 未过期 → 用 User 身份创建任务 → 放到用户的「 机器人运维」tasklist → 分组正确 ✅
└─ 已过期 → 生成新授权链接 → 用 Bot 身份创建任务 → 分配到用户 → 分组为默认 ️
```

### 关键配置

```bash
# 正常路径：User 身份创建
lark-cli task +create \
  --summary "【授权过期】重新授权飞书任务 [verification_url]" \
  --description "在浏览器中打开上述链接，完成授权后告知我即可。" \
  --tasklist-id "843a958e-d26b-4013-b2f5-0c4df65479f7" \
  --assignee "ou_d1d7f2c929754d891fee5d97bc894d74" \
  --due "+3d" \
  --data '{"start":{"timestamp":"<computed>","is_all_day":true}}' \
  --as user

# 兜底路径：Bot 身份创建 + 分配
lark-cli task +create \
  --summary "【授权过期】重新授权飞书任务 [verification_url]" \
  --description "在浏览器中打开上述链接，完成授权后告知我即可。" \
  --tasklist-id "7ca05e52-187e-4cb4-8117-bc9260ad9ee9" \
  --due "+3d" \
  --data '{"start":{"timestamp":"<computed>","is_all_day":true}}' \
  --as bot

lark-cli task +assign \
  --task-id "<task_guid>" \
  --add "ou_d1d7f2c929754d891fee5d97bc894d74" \
  --as bot
```

### 开始时间格式

飞书任务 API 的 `start` 字段是对象格式，不是简单字符串：

```json
{
  "start": {
    "timestamp": "1758326400000",
    "is_all_day": true
  }
}
```

`timestamp` 是毫秒级时间戳，`is_all_day: true` 表示全天事件。

---

## 经验教训

1. **不要擅自行动**
   - 用户问"链接会变吗？"只是确认事实，不是要求修改方案
   - 只回答问题，等用户给出明确指示后再行动

2. **区分 User 和 Bot 身份的能力边界**
   - Bot 永不过期但权限受限（无法访问用户 tasklist）
   - User 权限完整但 token 会过期
   - 设计自动化方案时必须考虑两种身份的降级策略

3. **飞书任务 tasklist 的访问控制**
   - tasklist 成员只接受 open_id，不接受 app_id
   - Bot 无法被加入用户的 tasklist
   - Bot 创建的任务无法移动到用户的 tasklist

4. **授权链接不能硬编码**
   - 每次 `auth login --no-wait` 生成新链接
   - 链接 10 分钟过期
   - 必须在运行时动态获取

5. **飞书任务 start 字段格式**
   - 是对象 `{"timestamp": "ms", "is_all_day": bool}`，不是简单字符串
   - 用 `--data` 参数传递 JSON

---

## 相关文件/配置

- 用户 tasklist ID：`843a958e-d26b-4013-b2f5-0c4df65479f7`（「 机器人运维」）
- Bot tasklist ID：`7ca05e52-187e-4cb4-8117-bc9260ad9ee9`（兜底用）
- 用户 open_id：`ou_d1d7f2c929754d891fee5d97bc894d74`
- 定时任务 cron：`0 9 * * *`（每天 09:00）
