---
name: d365-log-sync-alert
description: |
  D365 接口日志同步与迈创问题告警自动化流程。每小时自动执行：查询 D365 生产环境报错日志 → 判定新增记录 → 写入飞书多维表格 → 筛选迈创-BOM/主数据异常 → 生成告警卡片发送到 scm-spp 沟通群 → 标记已发送。
  
  触发场景：
  - 用户说"执行 D365 日志同步"、"运行日志告警"、"同步 integration log"
  - 定时任务触发（Cron Job 每小时调用）
  - 用户说"检查 D365 报错"、"查看迈创问题"
  - 用户提到"D365 接口日志"、"integration log sync"
  
  关键特征：涉及 D365 生产环境 integrationlog 表、飞书多维表格 MeCQbGQ5paCJBdsfRFwcfneznFb、scm-spp 沟通群告警。
---

# D365 接口日志同步与迈创问题告警

## 环境要求（最高优先级）

**必须使用生产环境 Dataverse 工具**：`mcp__2de134c2-404e-465f-8170-8f6abb4ef943__execute_fetchxml`

**绝对禁止使用**：`mcp__1ef94522-4afe-4997-9c03-3145aa460b10__execute_fetchxml`（这是 UAT 环境，数据为空）

验证方法：执行查询后，确认返回的数据包含真实业务数据（如 WO 开头的工单号），而非空结果或测试数据。

## 执行流程

### 第 0 步：环境验证

在执行任何操作前，先用生产环境工具执行一次简单查询，确认：
1. 工具调用成功（无权限错误）
2. 返回的数据包含真实业务数据（`returnedCount > 0`，且记录中包含 `WO` 开头的工单号）

若验证失败，立即停止并报告错误，不要继续执行后续步骤。

### 第 1 步：查询 D365 生产环境

用生产环境工具查询 `new_integrationlogs`，FetchXML 定义在：
```
C:\Users\yixing.li\Desktop\Work\Work\4-EU SDS\运维\integration Log\d365-sync-pack\fetchxml.md
```

查询条件：
- `statecode=0`（Active）
- 8 个集成场景（Push WO to SCM、B2X Create/Update/Job Create/Job Cancel、MySav Create/Update、Update WO Request）
- `statuscode in [100000003 Failed, 100000001 Retry Failed]`
- `createdon=last-seven-days`

将完整 JSON 保存到：
```
C:\Users\yixing.li\Desktop\Work\Work\4-EU SDS\运维\integration Log\d365_fetchxml_YYYYMMDD_HHMM.json
```

### 第 2 步：判定新增记录

切换到脚本目录并执行：
```bash
cd "C:\Users\yixing.li\Desktop\Work\Work\4-EU SDS\运维\integration Log\d365-sync-pack"
python scripts/fetch_existing_ids.py ../existing_ids.txt
python scripts/sync.py ../d365_fetchxml_YYYYMMDD_HHMM.json --existing-ids ../existing_ids.txt --out ../
```

输出：
- `../d365_fetchxml_YYYYMMDD_HHMM.payload.json`（待写入 Base 的新增记录）
- `../d365_fetchxml_YYYYMMDD_HHMM.meta.json`（每条记录的元信息，含异常判定、报错、备件）

控制台会打印：`New records: N` 和 `Pending alert: M`

若 `New records: 0`，则无新增记录，跳到第 7 步（静默结束）。

### 第 3 步：写入多维表格（仅当 New records > 0）

**⚠️ 必须使用 `lark-cli` 写入**（MCP bitable 工具的 `fields` schema 限制为 `additionalProperties: false`，无法传入字段数据）。

```bash
cd "C:\Users\yixing.li\Desktop\Work\Work\4-EU SDS\运维\integration Log"
python -c "
import json, subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('d365_fetchxml_YYYYMMDD_HHMM.payload.json', 'r', encoding='utf-8') as f:
    payload = json.load(f)
data = json.dumps(payload, ensure_ascii=False)
cmd = ['lark-cli', 'base', '+record-batch-create',
       '--base-token', 'MeCQbGQ5paCJBdsfRFwcfneznFb',
       '--table-id', 'tblTWNXVEKv0IScf',
       '--json', data]
r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print(r.stdout)
if r.returncode != 0: print('STDERR:', r.stderr)
"
```

- `base_token`: `MeCQbGQ5paCJBdsfRFwcfneznFb`
- `table_id`: `tblTWNXVEKv0IScf`（D365 接口日志表）
- `--json`: 从 `payload.json` 直接读取（payload 的 `create_records` 格式与 lark-cli 要求一致）

字段映射（中文 key，已在 payload.json 中准备好）：
| 中文字段名 | 取值来源 |
|------------|----------|
| Work Order | D365 link-entity workorder 的 FormattedValue（WO 开头格式） |
| Created On | createdon 转北京时间(UTC+8)，格式 `yyyy-MM-dd HH:mm:ss`，必须带时分秒 |
| Integration Scenario | 场景 GUID→名称映射 |
| Target System | link-entity integrationscenario 的 new_targetsystem |
| Source System | link-entity integrationscenario 的 new_sourcesystem |
| Request JSON | new_requestjson |
| Response JSON | new_responsejson |
| 报错 | 迈创-BOM：`errorCodeDesc + "\n超BOM物料: " + otherDesc`；其他：仅 errorCodeDesc |
| 日志ID | new_integrationlogid（唯一键，判重用） |
| 异常场景 | 按 rules.py 规则判定（迈创-数据问题-BOM/主数据、B2X-接口问题-必填等） |
| 责任人 | 迈创-BOM/主数据 → 贡梦夏 `ou_527f81f1af862f57e62694e229640812`；其他留空 |
| 已发送告警 | 新写入为 false |

单批 ≤200 条，超了分批。写后按日志ID回读验证。

### 第 3.5 步：配置表自动补录（异常场景未命中时）

**配置表**：`tblIqZ9T8Ekj9h8y`（异常场景判定配置）

当新增记录的异常场景为「待补充」（即非迈创场景且 rules.py 未命中）时，需在配置表新增规则记录：

1. **从 Response JSON 提取关键词**：取最能代表报错特征的短语（如 `is Closed`、`timeout exceeded`）
2. **查重**：用 `lark-cli base +record-search` 或 MCP search 按「Integration Scenario + Response JSON 关键词」查询配置表，若已存在则跳过
3. **新增**（仅当不存在时）：
```bash
lark-cli base +record-batch-create \
  --base-token MeCQbGQ5paCJBdsfRFwcfneznFb \
  --table-id tblIqZ9T8Ekj9h8y \
  --json '{"create_records":[{"Integration Scenario":["<场景名>"],"Response JSON 关键词":"<关键词>","异常场景":["待补充"],"备注":"自动新增：<时间> 轮次未命中，待人工补充规则"}]}'
```

**迈创场景（Push WO to SCM）特殊兜底**：匹配不到 → 异常场景赋值为「迈创-接口问题-其他」，**不**新增配置表记录。

**注意**：此步骤已由 `sync.py` 自动实现（`fetch_config_existing()` 查重 + `write_config_records()` 写入），无需手动执行。

### 第 4 步：筛选待发送（仅当 Pending alert > 0）

待发送 = 异常场景为以下三类、且「已发送告警」未勾选的记录：
- 「迈创-数据问题-BOM」
- 「迈创-数据问题-主数据」
- 「迈创-接口问题-其他」（含 Push WO to SCM + 无 errorCodeDesc 的场景 + 迈创兜底记录）

若 `Pending alert: 0`，则无待发送告警，跳到第 7 步（静默结束）。

### 第 5 步：生成并发送告警卡片

生成卡片：
```bash
python scripts/card.py ../d365_fetchxml_YYYYMMDD_HHMM.meta.json --out ../
```

`--now`/`--next`/`--range` 三个参数为可选，未传入时 `card.py` 自动取系统当前北京时间计算：
- `--now`：默认当前时间，格式 `yyyy-MM-dd HH:mm:ss (UTC+8)`
- `--next`：默认当前时间 +1h 整点
- `--range`：默认近 7 天，格式 `yyyy-MM-dd ~ yyyy-MM-dd (近7天)`

输出：`card_0.json`、`card_1.json`…（自动拆卡：每张表格数≤5、体积≤25KB）

发送卡片到 scm-spp 沟通群（直接发送）：
- `chat_id`: `oc_f1890b5bed23c01839dfb517c63bec48`
- `msg_type`: `interactive`
- `content`: 从 `card_N.json` 读取
- 卡片内已用 `<at id=ou_527f81f1af862f57e62694e229640812></at>` 艾特贡梦夏

发送命令（使用 `lark-sppqabot` MCP）：
```
mcp__bb1bd24d-983f-48b1-a11b-3a7d59421f2c__im_v1_message_create
receive_id_type: chat_id
receive_id: oc_f1890b5bed23c01839dfb517c63bec48
msg_type: interactive
content: <card_N.json 的 JSON 字符串>
```

### 第 6 步：标记已发送

将已发送记录的「已发送告警」(`fld2bx9x7p`) 更新为 `true`，避免下次重复发送。

用 `lark-cli base +record-batch-update` 批量更新：
- `base_token`: `MeCQbGQ5paCJBdsfRFwcfneznFb`
- `table_id`: `tblTWNXVEKv0IScf`
- 从 meta.json 读取 `record_id` 列表
- 构造更新 payload：每条记录 `{"已发送告警": true}`

```bash
lark-cli base +record-batch-update \
  --base-token MeCQbGQ5paCJBdsfRFwcfneznFb \
  --table-id tblTWNXVEKv0IScf \
  --json '{"update_records":[{"record_id":"<rec_id>","fields":{"已发送告警":true}},...]}'
```

> **注意**：此步骤也可用 MCP `bitable_v1_appTableRecord_update` 逐条更新（因为只更新单个 checkbox 字段，不涉及 `additionalProperties` 限制）。

### 第 7 步：执行结束

简要汇报：
```
查询 N 条、新增 M 条、待发送 K 条
```

若 `New records: 0` 或 `Pending alert: 0`，静默结束，不发送任何消息。

## 关键常量

| 项 | 值 |
|----|-----|
| 生产环境 Dataverse 工具 | `mcp__2de134c2-404e-465f-8170-8f6abb4ef943__execute_fetchxml` |
| Base token | `MeCQbGQ5paCJBdsfRFwcfneznFb` |
| 日志表 | `tblTWNXVEKv0IScf` |
| 迈创异常场景判定配置表 | `tblePVTwOyMzPNG8` |
| 非迈创异常场景判定配置表 | `tblbscUEUlXSUQE4` |
| 迈创站点运营表 | `tbl0Xiuz6KJ3SSC4` |
| 告警卡片配置-迈创表 | `tblWugqhkySxdnlA` |
| 告警卡片配置-非迈创表 | `tblcNZKfDloFgDPc` |
| 告警规则配置表 | `tblRa4IDCJ6ylCOz` |
| scm-spp 沟通群（直接发送） | `oc_f1890b5bed23c01839dfb517c63bec48` |
| 贡梦夏 open_id | `ou_527f81f1af862f57e62694e229640812` |
| D365 环境 | `https://eusegwayspp.crm4.dynamics.com` |
| 脚本目录 | `C:\Users\yixing.li\Desktop\Work\Work\4-EU SDS\运维\integration Log\d365-sync-pack\` |
| 归档目录 | `C:\Users\yixing.li\Desktop\Work\Work\4-EU SDS\运维\integration Log\` |

## 异常场景判定规则（动态读取配置表）

**核心机制**：`scripts/sync.py` 每次执行时通过 `fetch_config_rules()` **实时拉取飞书多维表格「迈创异常场景判定配置」表（`tblePVTwOyMzPNG8`）和「非迈创异常场景判定配置」表（`tblbscUEUlXSUQE4`）**的全部规则，`rules.py` 的 `judge_abnormal(scenario, response, config_rules)` 逐条匹配「场景+关键词」，首次命中即返回。

- 配置表是规则**唯一真源**，更新配置表后下次执行立即生效，无需改代码。
- **配置表拆分**：迈创场景（Push WO to SCM）和非迈创场景（B2X/MySav/Update 等）分别存储在两张表中，便于管理。
- **异常场景命名规范**：统一使用英文前缀，如 `Maitrox-数据问题-BOM`、`B2X-接口问题-必填为空`、`MySav-接口问题-状态` 等。
- **特殊优先级（代码层）**：Push WO to SCM + Response 中无 `errorCodeDesc`（报错列为空）→ 直接判定为「Maitrox-接口问题-其他」，优先级高于配置表规则（因为「缺少字段」无法用关键词 `in` 匹配）。此场景同样触发告警卡片，卡片中不显示报错信息但保留备件申请列表。
- **兜底**：迈创匹配不到 → `Maitrox-接口问题-其他`（不写配置表）；其他场景匹配不到 → `待补充`（自动写入配置表提醒用户，先按「场景+关键词」查重）。
- **告警触发场景**：从「告警卡片配置-迈创」表和「告警卡片配置-非迈创」表中读取启用的场景，每个场景可配置不同的卡片样式、颜色、艾特规则等。
- **艾特规则**：
  - 迈创场景：根据 Work Order 的 Service Store Name 匹配「迈创站点运营」表（`tbl0Xiuz6KJ3SSC4`）中的负责人，自动 @对应的负责人。
  - 非迈创场景：根据配置表中的「是否艾特」和「艾特用户ID」字段决定。
- **责任人自动赋值**（2026-10-23 新增）：
  - `sync.py` 的 `parse_record()` 函数现在自动为每条记录赋值责任人
  - **迈创场景**：根据 Service Store Name 从「迈创站点运营」表（`tbl0Xiuz6KJ3SSC4`）读取对应的负责人
  - **非迈创场景**：从配置表（`tblePVTwOyMzPNG8` 或 `tblbscUEUlXSUQE4`）的「责任人」字段读取
  - 新增 `fetch_site_ops_mapping()` 函数，实时加载 Service Store Name → 负责人映射
  - 配置表的「责任人」字段已改为 user 类型（`fldh7gslGr`），支持直接存储飞书用户
- **最终兜底**：配置表拉取失败时，`judge_abnormal_fallback()` 提供本地静态规则作为最后安全网。

以下为配置表快照（**实际以多维表格实时内容为准**）：

| # | 场景 | Response JSON 含关键词 | 异常场景 |
|---|------|------------------------|----------|
| 1 | Push WO to SCM | `BOM` | 迈创-数据问题-BOM |
| 2 | Push WO to SCM | `ERR_000090` | 迈创-数据问题-BOM |
| 3 | B2X Update WO Request | `Cannot skip` | B2X-接口问题-必填 |
| 4 | Push WO to SCM | `Product SKU` | 迈创-数据问题-主数据 |
| 5 | MySav Update WO Request | ` is empty` | MySav-接口问题-必填 |
| 6 | B2X Update WO Request | ` is empty` | B2X-接口问题-必填 |
| 7 | MySav Update WO Request | `Cannot skip` | MySav-接口问题-状态 |
| 8 | B2X Create WO Request | `is empty` | B2X-接口问题-必填 |
| 9 | B2X Create WO Request | `Existing active SWAP/Refund` | B2X-接口问题-工单重复 |
| 10 | MySav Update WO Request | `[WoClosedDateTime] invalid format` | MySav-接口问题-必填 |
| 11 | B2X Update WO Request | `status cannot move back` | B2X-接口问题-数据 |
| 12 | B2X Update WO Request | `is Cancelled` | B2X-接口问题-数据 |
| 13 | B2X Update WO Request | `open Send-In order` | B2X-接口问题-工单重复 |
| 14 | B2X Update WO Request | `is Closed` | B2X-接口问题-数据 |

## 卡片格式规范

Card 2.0 中文版，支持配置化和聚合：

### 配置化参数
从「告警卡片配置」表（迈创 `tblWugqhkySxdnlA` / 非迈创 `tblcNZKfDloFgDPc`）读取：
- **卡片标题**：如「D365 集成报错告警」
- **卡片副标题模板**：支持 `{scenario}` 占位符，如 `{scenario}` → 「Maitrox-数据问题-BOM」
- **卡片颜色**：red / orange / yellow / blue / green / grey 等
- **是否艾特**：true/false
- **艾特用户ID**：飞书 open_id（如 `ou_527f81f1af862f57e62694e229640812`）
- **发送目标群聊**：group_chat 类型字段，选择飞书群
- **最大展示条数**：单卡最多展示几条记录（默认 5）
- **数据来源范围天数**：卡片中显示的数据来源时间范围（默认 7 天）
- **聚合组代码**：如 `GROUP_DATA`、`GROUP_INTERFACE`、`GROUP_OTHER`、`GROUP_B2X`、`GROUP_MYSAV`
- **聚合后副标题**：聚合后显示的副标题，如「Maitrox-数据问题」、「B2X-接口问题」

### 聚合逻辑
- 同一聚合组代码的记录会合并到一张卡片中
- 聚合后使用第一条记录的配置（颜色、艾特规则、发送目标等）
- 聚合后副标题替换为「聚合后副标题」字段的值
- 卡片内容中每条记录仍显示各自的异常场景

### Service Store Name 与负责人匹配
- **数据来源**：D365 workorder 实体的 `new_servicestoreid` 关联查询 `new_servicestore.new_name`
- **FetchXML 扩展**：在 `link-entity name="new_workorder"` 内部新增：
  ```xml
  <link-entity name="new_servicestore" from="new_servicestoreid" to="new_servicestoreid" link-type="outer" alias="a_servicestore" visible="false">
    <attribute name="new_name"/>
    <attribute name="new_servicestorecode"/>
  </link-entity>
  ```
- **负责人匹配**：对于迈创场景，根据 Work Order 的 Service Store Name 匹配「迈创站点运营」表（`tbl0Xiuz6KJ3SSC4`）中的「负责人」字段（user 类型），自动 @对应的负责人
- **批量更新**：已编写脚本 `update_service_store_name.py`，使用 D365 OData API 批量查询并更新所有历史记录的 Service Store Name

### 卡片结构
- header：标题 + 副标题 + 颜色 + icon
- body：
  1. 运行元信息（本次运行/下次运行/数据来源范围）
  2. 汇总 markdown（本次新增 X 条告警记录）
  3. 每条工单一个 collapsible_panel（默认折叠，展开后显示工单号/B2X单号/异常场景/创建时间/类型/整车物料号/报错信息/备件申请列表）
  4. 底部多维表格链接

详细规范见 `card-generation-rules.md`。

## 常见坑

1. **环境错误**：使用了 UAT 环境工具（`mcp__1ef94522...`），导致查询返回 0 条
2. **场景 GUID**：`_new_integrationscenarioid_value` 是**不带花括号**的 GUID
3. **工单号**：写 link-entity workorder 的 FormattedValue（WO 开头格式），不写 new_name 的 GUID
4. **Created On**：转北京时间(UTC+8)，格式 `yyyy-MM-dd HH:mm:ss`，带时分秒
5. **Base checkbox 筛选**：用 `['已发送告警','==',False]`，不认 isNot
6. **报错字段**：迈创-BOM 类拼接 `errorCodeDesc + "\n超BOM物料: " + otherDesc`；其他场景仅 errorCodeDesc
7. **卡片格式**：必须使用 Card 2.0 格式，collapsible_panel 的 header 用 `{"title": {"tag": "markdown", "content": "..."}}`，子元素用 `elements` 而非 `children`
8. **MCP bitable 工具限制**：MCP 的 `bitable__0a9b882c96cb`（create）和 `bitable__c754af1e8760`（update）的 `fields` schema 定义为 `additionalProperties: false`，无法传入任意字段名。**所有 Base 写入必须改用 `lark-cli base +record-batch-create` 命令**，通过 `--json` 传入完整记录 JSON
9. **配置表查重**：新增配置表记录前必须按「Integration Scenario + Response JSON 关键词」查重，避免重复插入。用 MCP search 或 `lark-cli base +record-search` 查询

## 发送规则

1. 每次先写 Base，再判定待发送
2. 存量已处理（2026-10-12 全量 23 条已勾选），后续只发本轮新增且 BOM/主数据未勾选的
3. 发送后立即勾选已发送，防重复
4. 无待发送则静默

## 约束

- 全程用中文回复
- 无新增或无待发送则静默，不发送任何消息
- 所有新增记录必须写入 Base
- 异常场景判定必须按 rules.py 规则执行
