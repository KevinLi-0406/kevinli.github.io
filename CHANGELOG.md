# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-09-20 16:30 (UTC+8)
- **修改文件**：`Integration/` 目录结构重组
- **变更类型**：重构
- **变更描述**：
  1. **新建 presentations/ 目录**：
     - 整合所有演示文稿（feishu-bot、kevin-li-presentation）
     - 避免 PPT 与 Bot 代码混在一起
  2. **新建 docs/ 目录**：
     - 整合所有技术文档（unified-platform、integration-details、requirements 等）
     - 整合配置文件（d365-mcp-config、monitored-chats）
     - 整合架构图（architecture.svg）
  3. **更新 README.md**：
     - 反映新目录结构
     - 更新快速链接指向新路径
- **影响范围**：Integration 目录结构、文档链接
- **Commit**：`1ee2825` - refactor: 重组 Integration 目录结构

### 2026-09-20 16:00 (UTC+8)
- **修改文件**：`Knowledge/`、`Integration/feishu-bot-presentation/`
- **变更类型**：重构
- **变更描述**：
  1. **清理 Knowledge 目录**：
     - 删除空子目录（01-SPP-SDS、02-FAQ、04-Meeting-Notes、05-Personal）
     - 删除重复文件 cron-feishu-notification-misroute.md（内容与 Integration Bot 文档重复）
  2. **调整 PPT 位置**：
     - 将 feishu-bot-presentation（PPT + HTML）从 feishu-bot/ 子目录移到 Integration/ 根目录
     - 避免演示文稿与 Bot 代码混在一起
  3. **保留 architecture.svg**：
     - 保留在 Integration/ 根目录，与 unified-platform.md 配套
- **影响范围**：仓库目录结构
- **Commit**：`6274d17` - refactor: 清理仓库结构

### 2026-09-20 15:00 (UTC+8)
- **修改文件**：`Integration/assets/`（70 个文件）
- **变更类型**：新增
- **变更描述**：
  1. **PPT 演示文稿共享资源**：
     - 添加 CSS 基础样式（base.css, fonts.css）
     - 添加 JavaScript 运行时（runtime.js）
     - 添加动画效果库（animations/ 目录，24 个动画脚本）
     - 添加 30+ 主题样式（themes/ 目录）
     - 添加演示图片资源（demo-images/）
  2. **修复问题**：
     - 解决 HTML PPT 访问 404 问题（缺少依赖的 assets 资源）
     - 支持完整的演讲者模式、主题切换、动画效果等功能
- **影响范围**：所有 HTML PPT 演示文稿
- **关联请求**："点击提示404"
- **Commit**：`3001156` - feat: 添加 PPT 演示文稿所需的共享资源文件


### 2026-09-20 14:55 (UTC+8)
- **修改文件**：`Integration/feishu-bot/feishu-bot-presentation.pptx`、`Integration/feishu-bot/feishu-bot-presentation/`
- **变更类型**：新增
- **变更描述**：
  1. **飞书机器人方案演示文稿**：
     - 新增 PowerPoint 格式演示文稿（8 页，含演讲者备注）
     - 新增 HTML 格式演示文稿（演讲者模式，带逐字稿，支持 S 键切换演讲者视图）
     - 内容覆盖：背景痛点、方案价值、技术架构、核心功能、实施成果、后续优化、Q&A
     - 配色方案：Ocean Gradient 技术风（深蓝 + 青色 + 薄荷绿）
     - 每页配备 150-300 字演讲者备注，按"提示信号"方式编写
  2. **使用方式**：
     - PowerPoint：双击 `feishu-bot-presentation.pptx`，按 F5 放映，Alt+F5 进入演讲者视图
     - HTML：打开 `feishu-bot-presentation/index.html`，按 S 进入演讲者模式，T 切换主题
- **影响范围**：飞书 Bot 项目文档与演示材料
- **关联请求**："读一下github中，飞书机器人相关的材料，输出一份ppt供我给大家讲解这个方案的价值、实施、后续优化等方面"
- **Commit**：`dd56610` - docs: 新增飞书机器人方案演示文稿（PPT + HTML）
### 2026-09-16 18:38 (UTC+8)
- **修改文件**：`Integration/integration-details.md`
- **变更类型**：文档更新
- **变更描述**：
  1. **EU SDS 知识库构建进度报告**：
     - 自动重推逻辑分析与验证（B2X/Mysav流程图）
     - QA知识库构建：60→200+ QA对，24个章节，1300+行
     - Dify Bot问答验证：修正22个关键点（接口方向、状态定义、术语准确性等）
     - 文件整理：桌面50→8个文件，4-EU SDS按项目管理维度重组
     - 知识库拆分：1个大文件→22个小文件，216个Q&A对，格式化为Dify兼容格式
     - 企微机器人排查与修复：进程未运行，手动启动恢复
  2. **经验总结**：
     - 成功做法：先验证逻辑再写文档、用Bot问答验证、拆分文档、格式化适配
     - 踩过的坑：Q&A被拆开、Q&A分段选不上、机器人进程退出、术语不准确
- **影响范围**：EU SDS知识库文档、企微机器人
- **Commit**：`f9bfbc8` - docs: 更新集成详情 - 添加EU SDS知识库构建进度（2026-09-16）

### 2026-09-16 12:00 (UTC+8)
- **修改文件**：`Integration/b2x-mysav-auto-repush/README.md`、`Integration/b2x-mysav-auto-repush/b2x-auto-repush.html`、`Integration/b2x-mysav-auto-repush/mysav-auto-repush.html`
- **变更类型**：新增
- **变更描述**：
  1. **B2X & Mysav 自动重推逻辑文档**：
     - 记录 B2X 和 Mysav 工单状态推送失败后的自动重推策略
     - 包含完整背景说明：状态流转、库存扣减机制、问题场景
     - B2X 方案：无 WO 状态查询接口，依赖错误信息路由（盲推 USB → 根据报错转 RC）
     - Mysav 方案：有 WO 状态查询接口，精准路由（先查状态 → 直达 USB 或 RC）
     - 两套方案的详细对比表和差异分析
  2. **交互式流程图**：
     - 两个独立 HTML 文件，使用 Mermaid 渲染流程图
     - 包含背景说明、逻辑解释、关键结论
     - 方便分别给 B2X 和 Mysav 的 IT 团队讲解
  3. **关键结论**：
     - 库存扣减最多 1 分钟，24H 间隔充足
     - 无重复扣减风险（24H ≫ 1min）
     - Out of stock 时 RC 重推循环，人工调整库存后自动恢复
- **影响范围**：B2X/Mysav 自动重推机制实施
- **关联请求**：用户需要为 B2X 和 Mysav 分别设计自动重推方案，并输出可视化流程图供 IT 团队参考
- **Commit**：`d062030` - docs: 添加 B2X 和 Mysav 自动重推逻辑文档

### 2026-09-15 (UTC+8)
- **修改文件**：`Resources/cars/` 目录下多个重复图片文件
- **变更类型**：清理
- **变更描述**：删除 Teams/ 目录下已存在的重复 F1 赛车图片（2026williamscar.png、2026redbullracingcar.png 等 12 个文件）
- **影响范围**：无功能影响，仅清理重复资源
- **Commits**：`a208cca`~`e3c025a` - chore: remove duplicate cars

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
- **修改文件**：`Integration/feishu-bot/`、`Integration/wecom-bot/`、`Integration/integration-details.md`、`Integration/requirements.md`、`Integration/sync-log.md`
- **变更类型**：功能新增 + 文档更新
- **变更描述**：
  1. **新增飞书和企微智能机器人**：
     - 基于 `@wecom/aibot-node-sdk` 和飞书 WebSocket SDK
     - WebSocket 长连接模式，无需公网 URL/内网穿透
     - 集成 Dify Chat API，支持多轮对话和流式回复
     - 架构与 Cherry Studio 本地 Agent 对称
  2. **统一信息平台架构图**：
     - 新增 `architecture.svg`，展示"一个大脑，五个触角"架构
     - 大脑：Cherry Studio + Dify；触角：企微/飞书/Teams/邮箱/D365
  3. **OpenAI 兼容格式调整**：
     - feishu-bot 从 Dify 原生格式改为 OpenAI 兼容格式
     - 统一与 wecom-bot 的 API 调用方式
  4. **文档同步**：
     - `sync-log.md`：补齐 9-5 至 9-9 同步记录
     - `requirements.md`：同步 Dify 接入 + F1 WebSocket 实时模式需求
- **影响范围**：企微/飞书 Bot 实时监听、统一信息平台架构
- **Commits**：`0c470e3`、`e0dca39`、`40b6d98`、`7ecd037`、`63a0bfe`

### 2026-09-05 (UTC+8)
- **修改文件**：`Tools/portal-editor/`、`Resources/`、`project-config.json`、`index.html`
- **变更类型**：重构 + Bug 修复
- **变更描述**：
  1. **portal-editor 迁移**：
     - 从 `Resources/portal-editor.html` 移到 `Tools/portal-editor/portal-editor.html`
     - 更新 `project-config.json` 配置
  2. **cyberpunk portal 扫描路径修复**：
     - Bug：删除 Projects/ 目录后，portal 扫描路径失效
     - Fix：改为扫描 Tools/ 目录
  3. **Projects 目录删除**：
     - 清理空的 Projects/ 目录
     - 更新顶层 README 反映 Bot + Dify AI 问答能力和门户 Chatbot 集成
- **影响范围**：门户编辑器、cyberpunk portal 扫描逻辑
- **Commits**：`526ae33`、`e9ae888`、`a48abb6`、`0414e49`、`2ce7618`、`1ef5864`
