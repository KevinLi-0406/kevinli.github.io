# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-09-09 18:44 (UTC+8)
- **修改文件**：`Integration/wecom-bot/wecom-bot.js`、`Integration/wecom-bot/README.md`、`Integration/integration-details.md`、`Integration/README.md`、`index.html`、`CHANGELOG.md`
- **变更类型**：Bug 修复 + 功能新增 + 文档更新
- **变更描述**：
  1. **wecom-bot 会话隔离修复（commit `5cd93bf`）**：
     - Bug：`conversations` Map 的 key 仅用 `userId`，导致同一用户在不同聊天场景（群聊 vs 私聊）共享 Dify `conversation_id`
     - 现象：用户在群里问了 B2X 问题后，切到私聊发"回答我的问题"，机器人回复了群里的 B2X 答案
     - Fix：session key 从 `userId` 改为 `${chatType}:${chatId}:${userId}`，确保每个聊天场景有独立对话上下文
     - 影响函数：`getConversationId()`、`setConversationId()`、`callDify()`、`wsClient.on('message.text')` 回调
  2. **门户首页嵌入 Dify Chatbot（commit `2c3c321`）**：
     - `index.html` 新增 `#knowledge` section，嵌入 `http://10.232.5.5/chatbot/p5ugRUuzsibsNbJn` iframe
     - 导航栏新增「知识库」链接
     - 卡片式包裹，700px 高度，与门户风格一致
  3. **文档同步更新**：
     - `Integration/wecom-bot/README.md`：多轮对话 key 从 `userId → conversation_id` 更新为 `sessionKey(chatType:chatId:userId) → conversation_id`
     - `Integration/README.md`：同上
     - `Integration/integration-details.md`：新增 2026-09-09 进度日志
  4. **知识库诊断与建议**（未写入代码，已口头告知用户）：
     - 根因：Dify 知识库文档不足（36 个文档大部分召回次数为 0）
     - 建议：补充 B2X 集成文档、调高相似度阈值到 0.6~0.7、优化 System Prompt
  5. **企微机器人简介撰写**（未推送到 GitHub，仅本地生成）
- **影响范围**：企微 Bot 多轮对话隔离、门户首页知识库展示
- **关联请求**：用户反馈"机器人在私聊里回复了群里的问题" + "把 Dify Chatbot 嵌入门户"

### 2026-09-09 12:15 (UTC+8)
