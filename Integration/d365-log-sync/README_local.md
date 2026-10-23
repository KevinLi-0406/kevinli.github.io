# D365 接口日志同步与迈创问题告警 · 本地运行手册

本目录是自包含交付包，供**本地电脑的 agent** 独立运行。所有脚本、规则、命令已固化，无需额外推理。

> **配套文档**：本手册 + `fetchxml.md`（FetchXML）+ `rules.md`（异常判定规则）+ `card.md`/`card-generation-rules.md`（卡片生成）+ **`SUPPLEMENT.md`（补充操作细节，必读）**。

## 一、前置依赖

- **本地电脑 + dataverse-prd 连接器**（豆包自定义连接器，仅本地可用）。执行前确认当前会话能检索到 dataverse 工具（tool_search 关键词 `execute_fetchxml`），否则停止并提示"未在本地环境"。
- **lark-cli**（写飞书多维表格、发卡片）。
- **python3**。

## 二、目标

工作日 10:00–18:00 每小时：把 D365 生产环境新增的集成报错日志写入飞书多维表格「D365接口日志管理系统」，并对「迈创-数据问题-BOM/主数据」记录向 scm-spp 沟通群发艾特贡梦夏的告警卡片。

## 三、工作流（严格按此顺序执行）

### 第 1 步：查询 D365 新增数据
用 dataverse-prd 连接器的 `execute_fetchxml`，`entitySetName=new_integrationlogs`，**FetchXML 见 `fetchxml.md`**（原样复制）。
- 若返回被截断，用 `curl.exe -L '<url>' -o <文件>.json` 下载完整原文再解析。

### 第 2 步：判定新增记录
```bash
python scripts/fetch_existing_ids.py <existing_ids.txt>
python scripts/sync.py <d365_json> --existing-ids <existing_ids.txt> --out <输出目录>
```
- `fetch_existing_ids.py` 拉取 Base 现有全部日志ID。
- `sync.py` 输出：`<d365_json>.payload.json`（待写入的新增记录）+ `<d365_json>.meta.json`（每条记录元信息，含异常判定/报错/备件）。控制台打印 `New records: N` 和 `Pending alert: M`。

### 第 3 步：写入多维表格
```bash
lark-cli base +record-batch-create --base-token MeCQbGQ5paCJBdsfRFwcfneznFb --table-id tblTWNXVEKv0IScf --json @<payload.json> --format json
```
- 单批 ≤200 条，超了分批。
- 写后回读验证：按日志ID筛选，确认 Created On 为北京时间带时分秒、异常场景正确。

### 第 4 步：异常场景判定
由 `rules.py` 实现（sync.py 自动调用）。**每次执行实时读取多维表格「异常场景判定配置」表（tblIqZ9T8Ekj9h8y）的全部规则**，用配置表判定异常场景——配置表更新后立即生效，不依赖本地静态规则。规则见 `rules.md`。
- 迈创（Push WO to SCM）配置表未命中 → 兜底「迈创-接口问题-其他」。
- 其他场景配置表未命中 → 标「待补充」，并自动把该「场景+关键词」组合新增到配置表（含查重，见 SUPPLEMENT.md 第一节）。
- 配置表拉取失败/为空时，回退到 `rules.py` 的本地静态规则兜底。

### 第 5 步：筛选待发送
待发送 = 异常场景「迈创-数据问题-BOM/主数据」+「已发送告警」(fld2bx9x7p) 未勾选。若 `Pending alert` 为 0，**静默结束，不发送任何消息**。

### 第 6 步：发送告警卡片到群
```bash
python scripts/card.py <meta.json> --out <目录> --now <本次运行> --next <下次运行> --range "<近7天时间段>"
lark-cli im +messages-send --chat-id oc_f1890b5bed23c01839dfb517c63bec48 --msg-type interactive --content @card_N.json --as user
```
- card.py 自动拆卡（表格≤5、体积≤25KB），生成 card_0.json、card_1.json…
- 卡片超 32KB 时改走 api POST（见 `card.md`）。
- 卡片自动艾特贡梦夏。发送命令/结构详见 `card.md`。

### 第 7 步：标记已发送
把已发送记录的「已发送告警」(fld2bx9x7p) 更新为 `true`，避免下次重复。

## 四、关键常量（在 scripts/common.py）

| 项 | 值 |
|---|---|
| Base | MeCQbGQ5paCJBdsfRFwcfneznFb |
| 日志表 | tblTWNXVEKv0IScf |
| scm-spp 群 | oc_f1890b5bed23c01839dfb517c63bec48 |
| 贡梦夏 | ou_527f81f1af862f57e62694e229640812 |
| D365 环境 | https://eusegwayspp.crm4.dynamics.com |

## 五、发送规则

1. 先写 Base，再判定待发送。
2. 存量已处理（2026-10-12 全量 23 条已勾选），后续只发本轮新增且 BOM/主数据未勾选的。
3. 发送后立即勾选已发送，防重复。
4. 无待发送则静默。

## 六、常见坑（务必遵守）

1. **环境**：必须在本地会话执行，确认 dataverse 工具可检索到；云端会失败。
2. **场景 GUID**：`_new_integrationscenarioid_value` 是**不带花括号**的 GUID；映射字典键也不带花括号。
3. **工单号**：写 `link-entity workorder` 的 FormattedValue（WO 开头格式），不写 new_name 的 GUID。
4. **Created On**：转北京时间(UTC+8)，格式 `yyyy-MM-dd HH:mm:ss`，带时分秒。
5. **PowerShell**：`curl` 须用 `curl.exe`；`lark-cli --json @file` 的 `@` 会触发 splatting，须用 Python `subprocess` 传参。
6. **Base checkbox 筛选**：用 `['已发送告警','==',False]`，不认 isNot。
7. **报错字段**：迈创-BOM 类拼接 `errorCodeDesc + "\n超BOM物料: " + otherDesc`；其他场景仅 errorCodeDesc（纯文本留空）。

## 七、交付物归档

中间/归档文件建议放：
`C:\Users\yixing.li\Desktop\Work\Work\4-EU SDS\运维\integration Log\`
（脚本、d365_fetchxml_*.json、payload/meta、card_*.json 等）
