# 统一信息平台 - 集成详情

> 项目开始日期：2026-09-02
> 负责人：李奕兴
> 当前阶段：双平台 Bot 已接入 Dify + D365 MCP 集成 + Mysav 自动化流程

---

## 一、配置信息

### 飞书配置

| 项目 | 值 |
|------|-----|
| CLI 版本 | 1.0.92 |
| 应用 ID | cli_aa1d00640cf9dcd4 |
| 机器人名称 | 李奕兴的智能助手 |
| 测试群 ID | oc_a3154db1370d2421d74690a0dac270ed |

### 企业微信配置

| 项目 | 值 |
|------|-----|
| CLI 版本 | 1.2.0 |
| 安装方式 | `bun x @wecom/cli` |
| 机器人名称 | 李奕兴的机器人 |
| 机器人 ID | aibiW0wBHmD2iCO1VmDQXF1wSDdg3kMKzn1 |
| 用户 ID | wofFQbCAAA3-jKiVTXDlUnhCq8DqLxRA |
| 测试群 ID | wrfFQbCAAAA9OfAN75TfoobnpfVzsVJw |

### Dify Chat API 配置（飞书 / 企微 Bot 共用）

| 项目 | 值 |
|------|-----|
| API 端点 | `http://10.232.5.5/v1/chat-messages`（实际 URL 拼接 `/chat-messages`） |
| 环境变量 | `DIFY_API_URL`、`DIFY_API_KEY` |
| API Key 格式 | `app-xxxxxxxxxxxxxxxx`（在 Dify 应用 → 访问 API → API 密钥页获取） |
| 应用部署方式 | 内网自建（九号公司内网） |
| 知识库来源 | 仓库 Markdown 文档（README / unified-platform / integration-details / requirements）+ 业务 PDF/Office 文档 |
| 模型 | Dify 应用默认模型（未在文档中显式指定） |
| 多轮对话 | 按 user 字段（飞书 senderOpenId / 企微 userId）维护 conversation_id，30 分钟无活动自动重置 |
| 使用方 | feishu-bot（Blocking 模式）、wecom-bot（Streaming 模式） |

> 🔑 完整环境变量模板见 [feishu-bot/.env.example](feishu-bot/.env.example) 与 [wecom-bot/.env.example](wecom-bot/.env.example)。
> ⚠️ `DIFY_API_KEY` 已脱敏，使用前需在本地替换 `<REPLACE_ME>` 或 `your_dify_api_key_here` 为真实值。真实 Key 不得提交到公开仓库。

### D365 MCP 配置（SPP 运维助手）

| 环境 | 标识 | Dataverse URL | 风险等级 | 用途 |
|------|------|--------------|---------|------|
| 生产环境 | dataverse-prd | `https://eusegwayspp.crm4.dynamics.com` | 🔴 高风险 | 承载正式业务数据（EU SPP 项目） |
| 测试环境 | dataverse-uat2 | `https://eubvuat2.crm4.dynamics.com` | 🟢 低风险 | 验证和调试 |

> 🔑 **完整 MCP JSON 配置**（含 CLIENT_ID / TENANT_ID）：[d365-mcp-config.json](d365-mcp-config.json)
>
> ⚠️ `DATAVERSE_CLIENT_SECRET` 已脱敏，使用前需在本地替换 `<REPLACE_ME>` 为真实值。真实 Secret 不得提交到公开仓库。

### SMTP 邮件配置（网易企业邮箱）

| 项目 | 值 |
|------|-----|
| SMTP 服务器 | smtphz.qiye.163.com |
| SMTP 端口 | 994 (SSL) |
| 发件人邮箱 | yixing.li@ninebot.com |

---

## 二、功能状态对比

| 特性 | 飞书 | 企业微信 | D365 MCP | Dify |
|------|------|----------|----------|------|
| 联系人/表查询 | ✅ 联系人搜索 | ✅ 联系人搜索 | ✅ list_entities (1777 个表) | - |
| 消息发送 | ✅ 完整 | ⚠️ aibot 方式 | - | - |
| 消息读取 | ✅ 完整 | ❌ 需公司启用 | - | - |
| 日程管理 | ✅ | ✅ | - | - |
| 会议管理 | ✅ | ✅ | - | - |
| 待办管理 | ⚠️ 需权限 | ✅ | - | - |
| 文档管理 | ✅ | ✅ | - | - |
| 会话列表 | ✅ | ✅（仅摘要） | - | - |
| 数据查询 | - | - | ✅ query_records / fetchxml | - |
| 记录修改 | - | - | ✅ create / update / delete | - |
| 表结构管理 | - | - | ✅ DDL 操作（高危） | - |
| 发布自定义项 | - | - | ✅ PublishAllXml | - |
| **SMTP 邮件发送** | - | - | - | **✅ 带附件** |
| **实时 Bot 问答** | **✅ WebSocket** | **✅ WebSocket（流式）** | - | **✅ Chat API 引擎** |
| **邮件操作（IMAP/SMTP）** | **✅ Bot 端集成** | - | - | - |

### 企业微信已安装技能

| 技能 | 功能 | 状态 |
|------|------|------|
| wecomcli-contact | 联系人管理 | ✅ |
| wecomcli-message | 消息收发 | ✅ |
| wecomcli-todo | 待办事项 | ✅ |
| wecomcli-meeting | 会议管理 | ✅ |
| wecomcli-doc | 文档管理 | ✅ |
| wecomcli-calendar | 日程管理 | ✅ |
| wecomcli-sheet | 表格管理 | ✅ |

### D365 MCP 支持的操作（SPP）

| 类别 | 操作 | 风险 | 包含工具 |
|------|------|------|--------|
| 🔍 查询数据 | 查询记录、FetchXML、数据质量分析 | 🟢 只读 | query_records, execute_fetchxml, get_record_by_id, analyze_table_quality |
| ✏️ 修改数据 | 增删改记录 | 🟡 影响记录 | create_record, update_record, delete_record |
| 📋 表结构管理 | 查看/修改表与字段 | 🟢/🔴 | list_entities, get_entity_metadata, get_entity_attributes, create/delete_table, create/delete_attribute |
| 🚀 发布自定义项 | PublishAllXml | 🟠 影响所有用户 | publish_customizations |

### Cherry Studio 已安装 Skills

| Skill | 功能 | 绑定环境 |
|-------|------|--------|
| sppprd | SPP 生产环境运维助手 | dataverse-prd (`mcp__2de134c2-404e-465f-8170-8f6abb4ef943__*`) |
| sppuat2 | SPP 测试环境运维助手 | dataverse-uat2 (`mcp__1ef94522-4afe-4997-9c03-3145aa460b10__*`) |
| lark-mail | 飞书邮箱管理 | - |

> **注意**：原 `spp` skill 已拆分为 `sppprd` 和 `sppuat2` 两个独立 skill，用户无需在每次会话中选择环境。

### 二.五 飞书 / 企微实时监听 Bot（Dify 引擎）

#### 功能对照

| 能力 | feishu-bot | wecom-bot |
|------|-----------|----------|
| 连接模式 | WebSocket 长连接（@larksuiteoapi/node-sdk WSClient） | WebSocket 长连接（@wecom/aibot-node-sdk） |
| 触发条件 | 群聊 @机器人 | 群聊 @机器人 或 私聊 |
| 监听事件 | `im.message.receive_v1` | `message.text` |
| AI 引擎 | Dify Chat API（Blocking） | Dify Chat API（Streaming） |
| 多轮对话 | ✅ senderOpenId → conversation_id | ✅ userId → conversation_id |
| 会话超时 | 30 分钟无活动自动重置 | 30 分钟无活动自动重置 |
| 消息去重 | ✅ Set 缓存最近 1000 条 | ✅ Set 缓存最近 1000 条 |
| 知识库加载 | ✅ 本地文档热重载 | ✅ 本地文档热重载 |
| 回复方式 | 引用原消息回复（im.v1.message.reply） | replyStream 流式输出 |
| 流式回复 | ❌ | ✅（先回"🤔 思考中..."再流式填充） |
| 邮件操作 | ✅ IMAP 收件 / SMTP 发件（授权白名单） | ❌ |
| 贴表情 | ✅ LOVE ❤️ | ❌ |
| 监听配置 | ✅ monitored-chats.json（白名单 / 全量模式） | ❌（默认所有消息） |
| 环境变量 | `DIFY_API_URL` / `DIFY_API_KEY` | 共用（指向同一个 Dify 应用） |

#### Dify 调用流程（两侧共用）

```
用户在群里 @机器人 或私聊提问
        ↓ (~1秒)
平台通过 WebSocket 推送事件
        ↓
脚本接收 → 校验群聊 / 用户 / @机器人
        ↓
[飞书] 贴 LOVE 表情；[企微] 回复"🤔 思考中..."
        ↓
调用 Dify Chat API（/v1/chat-messages）
  - headers: Authorization: Bearer <DIFY_API_KEY>
  - body: { query, user, conversation_id?, response_mode }
        ↓
保存 conversation_id 用于后续多轮对话
        ↓
在原会话中回复答案
        ↓
总延迟：2-10 秒（视 Dify 响应速度）
```

#### Dify 应用配置（后台侧）

| 项 | 说明 |
|-----|------|
| 应用名 | 飞书 / 企微 Bot 共用同一个 Dify 应用 |
| 应用类型 | Chatbot（对话型） |
| 模型 | Dify 默认模型（未在代码中显式指定） |
| 知识库 | ① 仓库 Markdown 文档（README.md / unified-platform.md / integration-details.md / requirements.md）<br>② 业务 PDF/Office 文档（在 Dify 后台上传） |
| 用户标识 | 飞书端传 senderOpenId；企微端传 userId（Dify 通过 user 字段区分两端用户） |
| 会话标识 | conversation_id 由 Dify 返回，两端各自维护（不跨平台） |

### Cherry Studio AI 与 Dify 的定位区分

| 维度 | Cherry Studio AI | Dify |
|------|------------------|------|
| 角色 | 本地操作中枢（Kevin 本人使用） | 云端 AI 引擎（Bot 调用） |
| 部署 | 本地客户端 + MCP 集成 | 九号内网 http://10.232.5.5 |
| 使用者 | Kevin（本人） | 飞书 / 企微群里的提问用户 |
| 集成工具 | sppprd / sppuat2 / lark-mail 等 skill | Dify Chat API（/v1/chat-messages） |
| 数据来源 | 本地 Markdown + Dataverse MCP | Dify 后台知识库 |

---

## 三、任务清单

### 第一阶段：基础配置（2026-09-02）✅

- [x] 飞书：创建自建应用、获取凭证、配置机器人
- [x] 飞书：安装 lark-cli v1.0.92、配置认证
- [x] 飞书：创建测试群组、验证双向通信
- [x] 企微：安装 wecom-cli v1.2.0、配置凭证
- [x] 企微：联系人、日程、会议、待办、消息发送测试通过

### 第二阶段：核心功能开发

- [x] 企微：获取会话列表、aibot 消息发送
- [ ] 企微：消息内容读取（需公司启用，错误 853006）
- [x] 双平台：日程创建和查询
- [x] 双平台：会议创建和链接生成
- [x] 企微：待办读取/创建/完成
- [ ] 飞书：待办读取（需权限审批）
- [ ] 飞书：读取所有群组消息（需权限审批）
- [ ] 飞书：读取私聊消息（需权限审批）

### 第三阶段：D365 MCP 集成（2026-09-07）🔄

- [x] SPP 运维助手 Skill 安装与激活
- [x] 测试环境 (dataverse-uat2) 连接验证
- [x] 环境选择交互流程验证（铁律 1）
- [x] 操作分类菜单交互验证（铁律 2）
- [x] 高危操作二次确认流程验证（铁律 3）
- [x] 用户偏好记录：选项式参数收集（AskUserQuestion 替代手动输入）
- [x] MCP 配置模板归档（d365-mcp-config.json，secret 已脱敏）
- [x] SPP skill 拆分为 sppprd 和 sppuat2（2026-09-08）
- [ ] 表结构查询优化：list_entities 返回 1777 个表，需按 prefix 分组筛选
- [ ] create_attribute 完整流程验证

### 第四阶段：Mysav 自动化流程（2026-09-08）✅

- [x] FetchXML 查询验证（Mysav 集成错误日志）
- [x] Excel 导出脚本开发（16 个字段映射）
- [x] SMTP 邮件发送验证（带附件）
- [x] 定时任务配置（数据导出 + 邮件发送）
- [ ] 邮件收件人确认（paul.gimay@mysav.eu, somsanouk.hoang@mysav.eu）

### 第五阶段：飞书 / 企微 Bot Dify 接入（2026-09-09）✅

- [x] feishu-bot WebSocket 长连接实现（@larksuiteoapi/node-sdk WSClient）
- [x] feishu-bot 接入 Dify Chat API（/v1/chat-messages）+ 多轮对话
- [x] feishu-bot 邮件 IMAP/SMTP 操作（授权白名单机制）
- [x] feishu-bot 贴 LOVE 表情、消息去重、知识库热重载
- [x] wecom-bot WebSocket 长连接实现（@wecom/aibot-node-sdk）
- [x] wecom-bot 接入 Dify Chat API（流式回复）+ 多轮对话
- [x] 两端共用同一个 Dify 应用，通过 user 字段区分提问来源
- [x] monitored-chats.json 支持白名单 / 全量监听两种模式

### 任务统计

| 阶段 | 总任务 | 已完成 | 进行中 | 待开始 | 完成率 |
|------|--------|--------|--------|--------|--------|
| 第一阶段 | 5 | 5 | 0 | 0 | 100% |
| 第二阶段 | 8 | 5 | 0 | 3 | 63% |
| 第三阶段 | 10 | 8 | 0 | 2 | 80% |
| 第四阶段 | 5 | 4 | 0 | 1 | 80% |
| 第五阶段 | 8 | 8 | 0 | 0 | 100% |
| **总计** | **36** | **30** | **0** | **6** | **83%** |

---

## 四、错误记录

| 错误 | 代码 | 原因 | 解决方案 |
|------|------|------|----------|
| 企微消息读取受限 | 853006 | 公司未启用消息 API | 联系管理员在后台启用 |
| 企微发送消息给新用户失败 | 853008 | 成员未和机器人对话过 | 让成员先和机器人对话 |
| 企微完成用户待办失败 | 860024 | 仅创建者可更新 | 机器人只能完成自己创建的待办 |
| 飞书 scope 名称错误 | - | 部分 scope 名称不正确 | 简化 scope 列表 |
| D365 list_entities 数据过大 | - | 返回 1777 个表（470KB），无法直接展示 | 需按 IsCustomEntity 过滤或提取 prefix 分组 |
| jq 不可用 | - | Cherry Studio 环境未安装 jq | 改用 Read + offset/limit 分段处理 |
| UAT2 权限不足 | 0x80040220 | si-eu-crm-dw 应用缺少 new_integrationlog 读取权限 | 在 UAT2 环境添加 prvReadnew_integrationlog 权限 |
| 飞书邮箱未激活 | 1234013 | user mailbox not found | 需要在飞书App中开通邮箱功能 |

---

## 五、进度日志

### 2026-09-09（星期二）

**飞书 Bot Dify 接入（commit 4d705b2）：**
- 将 AI 调用从 OpenAI 兼容格式切换到 Dify Chat API（/v1/chat-messages）
- 新增多轮对话管理（按 sender_id 维护 conversation_id，30 分钟超时自动重置）
- 环境变量：`AI_API_URL/AI_API_KEY/AI_MODEL` → `DIFY_API_URL/DIFY_API_KEY`
- 保留全部原有功能：WebSocket 监听、邮件 IMAP/SMTP、白名单、贴表情、热重载

**企微 Bot Dify 接入：**
- 基于 @wecom/aibot-node-sdk 实现 WebSocket 长连接
- 接入 Dify Chat API，支持流式回复（先回"🤔 思考中..."再 fill 最终答案）
- 与飞书 Bot 共用同一个 Dify 应用，conversation_id 在两端独立管理
- 文档：wecom-bot/README.md 详细记录架构对比与常见问题

**文档全量对齐：**
- Integration 顶层 7 个文档 + 2 个子项目 README 全部更新到最新状态
- 明确"五个触角（企微/飞书/Teams/邮箱/D365 MCP）+ Dify AI 引擎"架构
- 新增 §2.5 飞书/企微 Bot 集成详情、§2.6 Cherry Studio 与 Dify 定位区分

### 2026-09-08（星期一）

**SPP Skill 拆分：**
- 原 `spp` skill 拆分为 `sppprd`（生产环境）和 `sppuat2`（测试环境）
- 明确 MCP 工具前缀绑定：
  - `mcp__1ef94522-4afe-4997-9c03-3145aa460b10__*` → dataverse-uat2
  - `mcp__2de134c2-404e-465f-8170-8f6abb4ef943__*` → dataverse-prd

**Mysav 集成日志自动化：**
- 10:00 创建数据导出定时任务（FetchXML → Excel）
- 12:00 创建邮件发送定时任务（SMTP 带附件）
- 收件人：paul.gimay@mysav.eu, somsanouk.hoang@mysav.eu
- 抄送：yixing.li@ninebot.com
- 附件：Mysav Error Integration Logs YYYYMMDD.xlsx

**SMTP 邮件配置：**
- 使用网易企业邮箱 SMTP (smtphz.qiye.163.com:994)
- 成功发送带附件邮件

**飞书邮箱尝试：**
- 尝试通过飞书邮箱发送带附件邮件
- 飞书邮箱未激活（user mailbox not found）
- 改用 SMTP 方案

### 2026-09-07（星期日）

**D365 MCP 集成（SPP 运维助手）：**

**初始化流程验证：**
- 触发 spp skill，输出环境选择卡片（铁律 1）
- 用户选择：🧪 测试环境 (dataverse-uat2)
- 锁定环境后输出操作分类菜单（铁律 2）

**操作流程：**
1. 用户选择「📋 表结构管理」
2. 进一步区分「👁️ 查看」 vs 「✏️ 修改」
3. 用户选择「✏️ 修改表结构」→「➕ 创建字段 (create_attribute)」

**关键发现：**
- **数据量问题**：list_entities 返回 1777 个表（含系统表），数据量达 470KB / 12444 行，无法直接在 AskUserQuestion 中展示
- **工具限制**：Cherry Studio 环境无 jq，无法快速提取 prefix 进行分组
- **交互偏好**：用户明确要求所有涉及选项的参数必须使用 AskUserQuestion 工具点选，不允许手动输入。已记录到 USER.md
- **高危操作确认**：铁律 3 的二次确认机制设计合理，DDL 操作需明确环境、操作、对象、影响
- **配置归档**：MCP JSON 配置模板已归档到 `d365-mcp-config.json`，client_secret 已脱敏

**待解决：**
- 大表数量下的 entityName 选择交互优化（需提取 custom entity prefix 列表）
- create_attribute 完整流程验证
- 考虑在本地缓存表列表以减少重复查询

### 2026-09-02（星期三）

**飞书集成：**
- 18:00 安装 lark-cli v1.0.92，配置应用 cli_aa1d00640cf9dcd4
- 18:25 创建测试群组 oc_a3154db1370d2421d74690a0dac270ed
- 18:30 消息收发测试通过
- 18:40 权限申请提交，部分待审批

**企业微信集成：**
- 19:00 安装 wecom-cli v1.2.0
- 19:15 联系人搜索测试通过
- 19:20 日程创建测试通过
- 19:25 会议创建测试通过（会议号 416964698）
- 19:30 待办管理测试通过（发现机器人只能完成自己创建的待办）
- 19:40 会话管理测试通过
- 19:45 消息发送测试通过（只能给已对话过的成员发消息）
- 19:50 消息读取测试失败（需公司启用 API，错误 853006）

**关键发现：**
- 机器人只能完成自己创建的待办
- 企微消息读取需公司管理员在后台启用
- 机器人只能给已对话过的成员发消息

---

## 六、D365 MCP 集成详情（SPP 运维助手）

### 6.1 核心机制

SPP 运维助手通过 5 条铁律规范操作流程：

| 铁律 | 内容 | 说明 |
|------|------|------|
| 铁律 1 | ~~强制选择环境~~ 环境已锁定 | 拆分为 sppprd/sppuat2 后无需选择 |
| 铁律 2 | 操作分类菜单 | 查询 / 修改 / 表结构管理 / 发布自定义项 |
| 铁律 3 | 高危操作二次确认 | DDL 操作、删除记录、发布自定义项需确认卡片 |
| 铁律 4 | 结果可视化展示 | 表格 / ASCII 进度条 / Mermaid 图表，禁止原始 JSON |
| 铁律 5 | 环境切换 | 支持会话中切换环境，重新走铁律 1 |

### 6.2 环境绑定（已修正）

| 环境 | Skill | MCP 工具前缀 |
|------|-------|-------------|
| dataverse-prd | sppprd | `mcp__2de134c2-404e-465f-8170-8f6abb4ef943__*` |
| dataverse-uat2 | sppuat2 | `mcp__1ef94522-4afe-4997-9c03-3145aa460b10__*` |

### 6.3 与统一信息平台的关系

D365 MCP 是统一信息平台的**第五个触角**（业务系统运维），与飞书/企微/Teams/邮箱的消息集成互补：

```
统一大脑（Cherry Studio AI + Dify 引擎）
├── 触角 1：企业微信（消息集成）
├── 触角 2：飞书（消息集成）
├── 触角 3：Teams（消息集成）
├── 触角 4：邮箱（消息集成）
├── 触角 5：D365 MCP（业务系统运维）
└── AI 引擎：Dify（飞书 / 企微 Bot 共用，云端 AI 回答）
```

D365 MCP 主要负责 EU SPP 项目的 Dataverse 数据运维，包括表结构管理、数据查询、记录修改等，是日常工作中不可或缺的工具集成。Dify 则为飞书 / 企微 Bot 提供 Chat API 引擎，让群聊 @机器人 的提问能得到智能回答（含多轮对话与知识库检索）。

---

## 七、Mysav 集成日志自动化

### 7.1 定时任务配置

| 任务 | 执行时间 | 说明 |
|------|---------|------|
| Mysav Error Logs Daily Export (UAT2) | 每天北京时间 10:00 | 从 UAT2 环境导出 Mysav 集成错误日志到桌面 |
| Mysav Error Logs Daily Email (SMTP) | 每天北京时间 12:00 | 使用 SMTP 发送带附件邮件 |

### 7.2 数据导出流程

1. 使用 Dataverse MCP (UAT2) 执行 FetchXML 查询
2. 查询条件：`new_integrationscenarioidname` 包含 "mysav%"，状态非成功，创建时间为昨天
3. 导出 16 个字段到 Excel 文件
4. 文件保存到桌面：`Mysav Error Integration Logs YYYYMMDD.xlsx`

### 7.3 邮件发送配置

| 字段 | 内容 |
|------|------|
| 收件人 | paul.gimay@mysav.eu, somsanouk.hoang@mysav.eu |
| 抄送 | yixing.li@ninebot.com |
| 主题 | Mysav Error Integration Logs - YYYY-MM-DD |
| 附件 | Mysav Error Integration Logs YYYYMMDD.xlsx |
| SMTP 服务器 | smtphz.qiye.163.com:994 (SSL) |
| 发件人 | yixing.li@ninebot.com |

### 7.4 FetchXML 查询示例

```xml
<fetch version="1.0" output-format="xml-platform" mapping="logical" distinct="true" count="5000">
  <entity name="new_integrationlog">
    <attribute name="new_integrationlogid"/>
    <attribute name="createdon"/>
    <attribute name="new_responsejson"/>
    <attribute name="new_requestjson"/>
    <attribute name="new_extensionfield4"/>
    <attribute name="new_integrationscenarioid"/>
    <attribute name="new_extensionfield5"/>
    <attribute name="new_workorder"/>
    <attribute name="new_extensionfield1"/>
    <attribute name="new_extensionfield2"/>
    <attribute name="new_extensionfield3"/>
    <filter type="and">
      <condition attribute="new_integrationscenarioidname" operator="like" value="%mysav%"/>
      <condition attribute="statuscode" operator="not-in">
        <value>100000002</value>
        <value>100000000</value>
      </condition>
      <condition attribute="createdon" operator="yesterday"/>
    </filter>
    <link-entity name="new_workorder" from="new_workorderid" to="new_workorder" link-type="outer" alias="wo">
      <attribute name="new_exceptionscenario"/>
      <attribute name="statuscode"/>
    </link-entity>
  </entity>
</fetch>
```
