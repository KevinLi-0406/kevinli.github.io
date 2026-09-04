# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-09-04 14:15 (UTC+8)
- **修改文件**：`Tools/ai-test-tool/index.html`（新增）、`Projects/AI API 测试工具.html`（删除）
- **变更类型**：重构
- **变更描述**：将 AI API 测试工具从 `Projects/` 目录移动到 `Tools/ai-test-tool/` 目录，与其他 HTML 项目（travel-planner、css-editor、photo-album 等）保持一致的目录结构
- **影响范围**：AI API 测试工具的访问路径变更
- **关联请求**：用户反馈"这个html的目录不太对，我记得别的html项目都是在tools下面的"

### 2026-09-04 14:10 (UTC+8)
- **新增文件**：`Integration/feishu-bot/feishu-bot.js`、`Integration/feishu-bot/package.json`、`Integration/feishu-bot/.env.example`、`Integration/feishu-bot/README.md`、`Integration/feishu-bot/.gitignore`
- **变更类型**：新增
- **变更描述**：新增飞书实时监听机器人（WebSocket 长连接模式），替代原有的 2 分钟轮询方案。核心功能：1) 基于 @larksuiteoapi/node-sdk WSClient 与飞书建立 WebSocket 长连接，实时接收 im.message.receive_v1 事件；2) 收到 @机器人 消息后自动贴 LOVE 表情表示已收到；3) 从本地仓库文档读取知识库，调用 AI API（OpenAI 兼容格式）生成回复并 @提问人发送；4) 支持消息去重、知识库文件热更新（watchFile）、监听配置热刷新（60秒轮询）、自动重连；5) 延迟从轮询的 0-2 分钟降低到 2-5 秒
- **影响范围**：新增 `Integration/feishu-bot/` 目录，不影响其他模块
- **关联请求**：用户反馈"定时监听的时效性还是不够强，能不能做到实时的"
- **调试记录**：修复了飞书 mentions 数据结构差异（id 为对象而非字符串，需用 mentioned_type === 'bot' 判断）；通过逐一测试确认 LOVE 为有效的 emoji_type

### 2026-09-04 13:50 (UTC+8)
- **修改文件**：`Projects/AI API 测试工具.html`
- **变更类型**：修复
- **变更描述**：修复输入消息后无法发送的问题。根因：发送按钮 disabled 条件包含 `state.selectedModels.size === 0`，用户未手动选择模型时按钮永远灰色不可点击，且 `sendMessage()` 在无模型时静默 return 无任何提示。修复：1) 发送按钮只检查是否有文本；2) 获取模型/测试连通后自动全选所有模型；3) 无模型时点击发送给出 toast 警告；4) 新增全选/取消全选按钮；5) 模型卡片增加选中勾选标记；6) 对话区标题显示已选模型数量
- **影响范围**：AI API 测试工具的发送交互流程
- **关联请求**：用户反馈"对话测试的时候，输入内容之后没法发送"
