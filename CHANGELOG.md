# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-09-04 14:22 (UTC+8)
- **修改文件**：`index.html`、`Tools/project-config.json`
- **变更类型**：重构
- **变更描述**：门户网站项目列表从手动配置改为自动发现。核心变更：1) 使用 GitHub Contents API 自动扫描 `Tools/` 目录下所有子目录，自动发现新项目；2) `project-config.json` 降级为可选的元数据补充（提供 icon、description、category），不再是必须项；3) 智能缓存机制：API 结果缓存 5 分钟 + ETag 304 优化，避免频繁请求；4) 新增「刷新」按钮可强制重新扫描；5) 自动根据目录名猜测分类和图标；6) API 失败时自动回退到本地缓存。同时为 `project-config.json` 中所有项目补充了 description 字段，并添加了 ai-test-tool 的元数据
- **影响范围**：门户网站项目列表加载逻辑。现在在 Tools/ 下新建子目录放入 index.html 后，门户网站会自动发现并展示，无需手动修改任何配置文件
- **关联请求**：用户反馈"现在有实现每次在tools下面新建html项目，都能够自动读取吗？如果不能，请修改"

### 2026-09-04 14:15 (UTC+8)
- **修改文件**：`Tools/ai-test-tool/index.html`（新增）、`Projects/AI API 测试工具.html`（删除）
- **变更类型**：重构
- **变更描述**：将 AI API 测试工具从 `Projects/` 目录移动到 `Tools/ai-test-tool/` 目录，与其他 HTML 项目保持一致的目录结构
- **影响范围**：AI API 测试工具的访问路径变更
- **关联请求**：用户反馈"这个html的目录不太对，我记得别的html项目都是在tools下面的"

### 2026-09-04 14:10 (UTC+8)
- **新增文件**：`Integration/feishu-bot/feishu-bot.js`、`Integration/feishu-bot/package.json`、`Integration/feishu-bot/.env.example`、`Integration/feishu-bot/README.md`、`Integration/feishu-bot/.gitignore`
- **变更类型**：新增
- **变更描述**：新增飞书实时监听机器人（WebSocket 长连接模式），替代原有的 2 分钟轮询方案
- **影响范围**：新增 `Integration/feishu-bot/` 目录
- **关联请求**：用户反馈"定时监听的时效性还是不够强，能不能做到实时的"

### 2026-09-04 13:50 (UTC+8)
- **修改文件**：`Projects/AI API 测试工具.html`
- **变更类型**：修复
- **变更描述**：修复输入消息后无法发送的问题
- **影响范围**：AI API 测试工具的发送交互流程
- **关联请求**：用户反馈"对话测试的时候，输入内容之后没法发送"
