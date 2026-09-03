# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-09-03 16:32 (UTC+8)
- **修改文件**：`CHANGELOG.md`
- **变更类型**：更新
- **变更描述**：补充本周（2026-09-02 至 2026-09-03）所有推送记录
- **影响范围**：变更日志文档
- **关联请求**："你能把这周的都补充上吗"

### 2026-09-03 16:29 (UTC+8)
- **修改文件**：`README.md`
- **变更类型**：更新
- **变更描述**：更新仓库结构。`project-config.json` 已移至 `Tools/` 目录，补充 `Integration/` 缺失文件（`progress-log.md`、`operation-log.md`），补充 `Resources/` 缺失文件（`index2077.html`、`portal-editor.html`）
- **影响范围**：仓库结构说明文档
- **关联请求**："README.md里面的仓库结构是不是要重新写了"

### 2026-09-03 16:19-16:25 (UTC+8)
- **修改文件**：`README.md`、`index.html`、`Resources/index2077.html`、`Integration/unified-platform.md`、`Knowledge/01-SPP-SDS/README.md`
- **变更类型**：更新
- **变更描述**：
  1. 入职时间从"2023 年 3 月"改为"2022 年 12 月"
  2. 统一模块称呼为"线上、线下、备件、结算、主数据"
     - 原"客服"改为"线上"
     - 原"维修中心工单"改为"线下"
     - 新增"备件"模块
- **影响范围**：个人简介、职业方向、工作数据、系统集成描述
- **关联请求**："对于README.md，有几个要更新：1.我是2022年12月加入的公司 2.我负责的系统一般模块是：线上、线下、备件、结算、主数据"

### 2026-09-03 16:05-16:11 (UTC+8)
- **新增文件**：`Tools/project-config.json`
- **删除文件**：`project-config.json`（根目录）
- **修改文件**：`index.html`
- **变更类型**：重构
- **变更描述**：
  1. 将 `project-config.json` 移至 `Tools/` 目录
  2. 更新 `project-config.json` 中 `file` 字段格式，从 `Tools/b2x-query/index.html` 改为 `b2x-query/index.html`
  3. 更新 `index.html` 加载路径，从 `PAGES_BASE + "/project-config.json"` 改为 `PAGES_BASE + "/Tools/project-config.json"`
  4. 更新项目 URL 拼接逻辑，从 `PAGES_BASE + "/" + it.file` 改为 `PAGES_BASE + "/Tools/" + it.file`
- **影响范围**：门户首页项目加载功能
- **关联请求**："project-config.json跟其他html工具放在一起呀"

### 2026-09-03 15:56 (UTC+8)
- **删除目录**：`Integration/cherry-integration/`、`Integration/feishu-integration/`、`Projects/`（整个目录）
- **变更类型**：清理
- **变更描述**：删除已整合的旧目录。`Integration/cherry-integration/` 内容已扁平化到 `Integration/` 顶层，`Projects/` 内容已迁移到 `Tools/`
- **影响范围**：仓库目录结构
- **关联请求**："删除文件我来，其他的你来"

### 2026-09-03 15:44-15:53 (UTC+8)
- **删除目录**：`Integration/cherry-integration/`（整个目录）
- **新增文件**：`Integration/requirements.md`、`Integration/tasks.md`、`Integration/progress-log.md`、`Integration/operation-log.md`、`Integration/wecom-integration.md`、`Integration/cherry-integration-overview.md`
- **修改文件**：`Integration/README.md`
- **变更类型**：重构
- **变更描述**：扁平化 `Integration/` 目录结构。将 `cherry-integration/` 子目录下的所有文件提升到 `Integration/` 顶层，删除重复的 `unified-platform-design.md`（保留 `unified-platform.md`），更新 `README.md` 中的目录结构描述和链接路径
- **影响范围**：统一信息平台文档目录结构
- **关联请求**："cherry-integration出现了两次"、"删除文件我来，其他的你来"

### 2026-09-03 14:43-15:00 (UTC+8)
- **新增文件**：`Tools/b2x-query/index.html`、`Tools/pokemon-pokedex/index.html`、`Tools/chicks/index.html`、`Tools/squirts/index.html`、`Tools/f1-data/index.html`
- **删除文件**：`Projects/B2X工单查询.html`、`Projects/宝可梦图鉴.html`、`Projects/奇怪的小鸡毛.html`、`Projects/奇怪的杰尼龟.html`、`Projects/F1数据大全.html`、`Projects/travel-planner-v2.2.0.html`、`Projects/共享相册.html`、`Projects/CherryStudio CSS 编辑器.html`、`Projects/travel-planner.html`、`Projects/README.md`
- **修改文件**：`Tools/README.md`、`project-config.json`、`index.html`
- **变更类型**：重构
- **变更描述**：将所有 HTML 工具项目从 `Projects/` 目录迁移到 `Tools/` 子目录。每个项目独立一个子目录，包含 `index.html`。更新 `project-config.json` 路径格式，更新 `index.html` 加载逻辑
- **影响范围**：仓库目录结构、门户首页项目加载
- **关联请求**：仓库重构

### 2026-09-03 14:30-14:34 (UTC+8)
- **新增文件**：`Knowledge/00-INDEX.md`、`Knowledge/01-SPP-SDS/README.md`、`Knowledge/02-FAQ/README.md`、`Knowledge/03-Lessons/README.md`、`Knowledge/04-Meeting-Notes/README.md`、`Knowledge/05-Personal/README.md`
- **变更类型**：新增
- **变更描述**：创建知识库目录结构。包含业务规则、常见问题、踩坑记录、会议纪要、个人笔记等分类
- **影响范围**：知识库结构
- **关联请求**：知识库搭建

### 2026-09-03 14:09-14:12 (UTC+8)
- **新增文件**：`Integration/README.md`、`Tools/README.md`
- **修改文件**：`README.md`、`index.html`
- **变更类型**：重构
- **变更描述**：重构仓库结构。创建 `Integration/` 和 `Tools/` 目录 README，更新根目录 `README.md` 为完整的个人、工作、项目信息，更新 `index.html` 适配新的 `Tools/` 目录结构
- **影响范围**：仓库文档结构、门户首页
- **关联请求**：仓库重构

### 2026-09-03 13:44-14:10 (UTC+8)
- **新增文件**：`Integration/unified-platform.md`、`Integration/cherry-integration/` 目录（7 个文件）
- **变更类型**：新增
- **变更描述**：创建统一信息平台完整设计文档。包含需求思考、架构设计、执行路线图等，整合 Cherry Studio 与飞书、企业微信的双平台集成文档
- **影响范围**：统一信息平台文档
- **关联请求**：统一信息平台项目文档化

### 2026-09-02 19:57-20:07 (UTC+8)
- **新增文件**：`Integration/cherry-integration/wecom-integration.md`
- **修改文件**：`Integration/cherry-integration/README.md`、`Integration/cherry-integration/requirements.md`、`Integration/cherry-integration/tasks.md`、`Integration/cherry-integration/progress-log.md`、`Integration/cherry-integration/operation-log.md`
- **删除文件**：`Integration/feishu-integration/` 目录（所有文件）
- **变更类型**：更新
- **变更描述**：整合企业微信集成文档。将飞书集成和企业微信集成合并为 `cherry-integration/` 目录，添加企业微信集成详情文档，更新需求文档、任务清单、进度日志和操作日志
- **影响范围**：集成项目文档结构
- **关联请求**："把企微集成信息写到之前生成的github仓库的文件里"

### 2026-09-02 19:01-19:04 (UTC+8)
- **删除文件**：`Projects/travel-planner-v2.0.2.html`、`Projects/travel-planner-v2.0.3.html`、`Projects/travel-planner-v2.0.4.html`、`Projects/travel-planner-v2.0.5.html`、`Projects/travel-planner-v2.0.6.html`、`Projects/travel-planner-v2.0.7.html`、`Projects/travel-planner-v2.0.8.html`、`Projects/travel-planner-v2.0.9.html`
- **变更类型**：清理
- **变更描述**：删除旧版本的 travel-planner 文件。保留最新的 v2.2.0 版本
- **影响范围**：项目文件
- **关联请求**：清理旧版本文件
