# 告警卡片生成规则 · 交接文档

本文档规定「D365接口日志同步与迈创问题告警」系统**告警卡片的完整生成规则**。凡生成卡片，必须严格遵循本规则，不得擅自改动结构、颜色、间距、字段或文案。

## 一、触发条件

仅当有**待发送记录**时才生成并发送卡片。待发送记录 = 异常场景为「迈创-数据问题-BOM」或「迈创-数据问题-主数据」、且「已发送告警」字段未勾选的记录。

- 待发送数为 0 → **不生成、不发送，静默结束**。
- 每张卡片都会**艾特贡梦夏**（open_id=`ou_527f81f1af862f57e62694e229640812`）。

## 二、卡片整体结构（Card 2.0 中文版）

| 项 | 值 |
|---|---|
| schema | `2.0` |
| config | `update_multi: true` |
| width_mode | `default` |
| body | `direction: vertical`，`padding: 12px 12px 20px 12px`，`vertical_spacing: 12px` |

**header（红色告警头）**
- 标题（title，plain_text）：`D365 集成报错告警`
- 副标题（subtitle，plain_text）：`Push WO to SCM · 迈创`
- template：`red`
- icon：standard_icon，token `warning_outlined`
- text_tag_list：「需核实」，color `red`

**body 元素顺序**
1. 运行元信息 div.fields
2. 汇总 markdown（顶部艾特贡梦夏）
3. 每条工单一个 collapsible_panel（默认折叠）
4. 底部多维表格链接 markdown

## 三、运行元信息（body 顶部 div.fields）

两两并排（is_short: true），共三项：

| 字段 | 内容 | 说明 |
|---|---|---|
| 本次运行 | 当前执行时间 | 北京时间 UTC+8，格式 `yyyy-MM-dd HH:mm:ss`，标注 `(UTC+8)` |
| 下次运行 | 定时任务下一次触发时间 | 北京时间 UTC+8，标注 `(UTC+8)` |
| 数据来源范围 | 近 7 天时间段 | **必须是时间段**，格式 `yyyy-MM-dd ~ yyyy-MM-dd (近7天)`，每次运行动态计算，**禁止写单个时间点** |

## 四、汇总 markdown

```
<at id=ou_527f81f1af862f57e62694e229640812></at>
本次待发送 N 条迈创数据问题记录，<font color=red>▸ 点击工单标题可展开</font>详情与备件。
```
- 顶部必须用 `<at id=ou_527f81f1af862f57e62694e229640812></at>` 艾特贡梦夏
- N = 本卡片包含的记录数

## 五、每条工单 collapsible_panel

**header（折叠时显示）**
- `expanded: false`（默认折叠）
- 内容：红色 `▸` + 工单号 + 异常场景 + 灰色「点击展开」
- 示例：`<font color=red>▸</font> **WO26082620285** · 迈创-数据问题-BOM <font color=grey>点击展开</font>`

**展开后 elements（按顺序）**

1. **div.fields 字段区**（is_short: true，两两并排，三组）：

| 行 | 左 | 右 |
|---|---|---|
| 第 1 行 | 工单号（**可点击 D365 工单链接**） | B2X单号 |
| 第 2 行 | 异常场景（**红色**） | 创建时间（**原始 UTC 值 + (UTC+0) 注明**，格式 `yyyy-MM-dd HH:mm:ss`） |
| 第 3 行 | 类型（service_order.status，如 UserConfirm） | 整车物料号（goodsId，来自 Request JSON 的 service_order.items.goodsId） |

   - 工单号链接：`https://eusegwayspp.crm4.dynamics.com/main.aspx?appid=296808a8-ebd5-f011-8543-000d3adcfa64&newWindow=true&pagetype=entityrecord&etn=new_workorder&id={woid}`
   - 异常场景统一用 `<font color=red>{异常场景}</font>` 标红
   - 创建时间必须写**D365 原始 UTC 值**，并标注 `(UTC+0)`，**不转北京时间**

2. **报错信息 markdown**
   - 迈创-数据问题-BOM 类：显示 `errorCodeDesc` + 换行 + `超BOM物料: {otherDesc}`（otherDesc 逗号分隔，展示时转 `, ` 分隔）
   - 其他异常场景：仅显示 `errorCodeDesc`
   - **此处为纯文本，不标红**
   - 无报错则不显示该块

3. **备件申请列表 markdown 表格**
   - 表头：`| 序号 | 物料号 | 数量 |`
   - 数据：来自 Request JSON `service_order.items.hasMaterialList`，取 `Index` / `applyMacId` / `quantity`
   - 表格标题可加数量，如 `**备件申请列表**（18 项）`
   - **超BOM物料号标红**：凡物料号属于 Response JSON `data.otherDesc` 集合的，用 `<font color=red>{物料号}</font>` 标红；其余不标红

**间距规范**
- 块间间距统一 `12px`
- 每个元素：`margin: 0px 0px 12px 0px`
- 每行行间距保持一致，不得有大小不一

## 六、底部 footer

```
完整字段请查看[多维表格「D365 接口日志」](https://segway-ninebot.feishu.cn/base/MeCQbGQ5paCJBdsfRFwcfneznFb)。
```
- text_size: `notation`

## 七、多卡拆分

单卡元素/体积超限时（**表格数 > 5** 或 **体积 > 25KB**），将记录拆成多张卡片逐张发送：
- 每张卡片都独立包含：运行元信息 + 汇总 markdown（**每张都在顶部艾特贡梦夏**）+ 若干工单 panel + footer
- 每张卡片 panel 数控制在表格数 ≤ 5、体积 ≤ 25KB

## 八、禁止事项

- **禁止中英对照**，卡片纯中文
- 禁止在「报错信息」处标红（只在备件表格的超BOM物料号标红）
- 禁止写单个时间点作为「数据来源范围」，必须写时间段
- 禁止改动 header 模板（红色「需核实」）
- 禁止在卡片中暴露日志ID/系统ID等非展示字段
