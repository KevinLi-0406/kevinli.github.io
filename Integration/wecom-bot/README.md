# 企微智能机器人（WebSocket 长连接模式）

基于 **企微官方 SDK `@wecom/aibot-node-sdk`** 的 WebSocket 长连接方案。当用户在群里 @机器人 或私聊提问时，自动调用 Dify Chat API 生成回复，支持多轮对话和流式回复。

**对比 Webhook（短连接）方案的优势：**

| 维度 | Webhook（短连接） | 长连接（本方案） |
|------|------------------|------------------|
| 公网地址 | **必须**（需要配置回调 URL） | **不需要**（纯出站连接） |
| 内网穿透 | 必须（如果在内网部署）| **不需要** |
| 响应延迟 | 5 秒同步超时限制 | **无限制** |
| 部署复杂度 | 高（HTTP 服务 + 签名校验 + 加解密）| 低（SDK 自动处理一切）|
| 与飞书侧对称性 | 不对称（HTTP 回调） | **完全对称**（WebSocket） |
| 流式回复 | 不支持 | **支持**（SDK 原生能力）|

---

## 快速开始

### 1. 企微管理后台配置（必须先完成）

登录企微管理后台 → 应用管理 → 智能机器人 → 找到"李奕兴的机器人"：

1. 记录 **机器人 ID**（Bot ID，格式：`aibi...`）
2. 记录或重置 **机器人 Secret**（仅显示一次，请妥善保存）

### 2. 本地安装

```bash
cd Integration/wecom-bot
npm install
cp .env.example .env
```

### 3. 编辑 .env 配置

填入 `WECOM_BOT_ID`、`WECOM_BOT_SECRET`、`DIFY_API_URL`、`DIFY_API_KEY`。

### 4. 启动

```bash
npm start       # 正常启动
npm run dev     # 开发模式（Node.js 22+，文件修改自动重启）
```

---

## 工作原理

```
用户在群里 @机器人 或私聊提问
        ↓ (~1秒)
企微通过 WebSocket 推送 message.text 事件
        ↓
SDK 自动处理：认证 / 心跳 / 解密 / 消息解析
        ↓
脚本接收 → 立即回复"🤔 思考中..."（流式占位）
        ↓
调用 Dify Chat API 生成回复（支持多轮对话）
        ↓
通过 replyStream 发送最终答案（finish=true 结束流）
        ↓
总延迟：2-10 秒（视 Dify 响应速度，无超时限制）
```

---

## 文件结构

```
Integration/wecom-bot/
├── wecom-bot.js      # 主脚本（~280 行）
├── package.json       # 依赖管理
├── .env.example       # 配置模板
├── .env               # 你的实际配置（不提交到 Git）
├── .gitignore         # Git 忽略规则
└── README.md          # 本文档
```

---

## 与飞书侧架构对比

| 维度 | 飞书 feishu-bot | 企微 wecom-bot |
|------|----------------|----------------|
| 官方 SDK | `@larksuiteoapi/node-sdk` | `@wecom/aibot-node-sdk` |
| 连接方式 | WebSocket 长连接 | WebSocket 长连接 |
| 入站端口 | 不需要 | 不需要 |
| 监听事件 | `im.message.receive_v1` | `message.text` |
| 回复方式 | `client.im.v1.message.reply`（引用回复）| `wsClient.replyStream`（流式回复）|
| Dify 调用 | 共用 `http://10.232.5.5/v1/chat-messages` | 共用 |
| 多轮对话 | ✅（senderOpenId → conversation_id）| ✅（userId → conversation_id）|
| 流式回复 | ❌ | ✅（"思考中..." → 最终答案）|
| 消息去重 | ✅（Set 缓存最近 1000 条）| ✅（Set 缓存最近 1000 条）|

两端共享同一个 Dify 应用，可以在飞书群提问，然后在企微私聊继续同一话题（Dify 通过 user 字段区分用户，conversation_id 在两端独立管理）。

---

## 常见问题

**Q: 连接失败怎么办？**
A: 检查 `WECOM_BOT_ID` 和 `WECOM_BOT_SECRET` 是否正确。Secret 仅显示一次，如果丢失需要在企微管理后台重置。

**Q: 收到消息但不回复？**
A: 检查 `DIFY_API_KEY` 是否配置正确，Dify 服务是否可达。查看控制台日志中的 Dify 调用响应。

**Q: 如何后台常驻运行？**
A: 推荐使用 pm2：
```bash
npm install -g pm2
pm2 start wecom-bot.js --name wecom-bot
pm2 save
pm2 startup
```

**Q: 机器人能收到图片/文件消息吗？**
A: 当前版本仅处理文本消息（`message.text`），其他类型会打印日志但不回复。可以根据需要扩展（参考 SDK 文档的 `message.image` / `message.file` 事件）。

**Q: 企微用户 ID 是加密的怎么办？**
A: 如果机器人创建者不是企业超级管理员，`from.userid` 字段会是加密 userid。可以通过"自建应用与智能机器人的对接"文档转换为明文 userid。多轮对话不受影响（SDK 用加密 userid 作为 key 也能正常工作）。
