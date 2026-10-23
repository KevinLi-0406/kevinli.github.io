# -*- coding: utf-8 -*-
"""D365 日志同步 - 常量定义（单一事实来源，勿改动，除非字段/规则变化）"""

# ---- 多维表格 ----
BASE_TOKEN = "MeCQbGQ5paCJBdsfRFwcfneznFb"
LOG_TABLE = "tblTWNXVEKv0IScf"          # D365 接口日志 表

# ---- 配置表（拆分为迈创和非迈创）----
CONFIG_TABLE_MAITUO = "tblePVTwOyMzPNG8"       # 迈创异常场景判定配置 表
CONFIG_TABLE_NON_MAITUO = "tblbscUEUlXSUQE4"   # 非迈创异常场景判定配置 表

# ---- 其他数据表 ----
SITE_OPS_TABLE = "tbl0Xiuz6KJ3SSC4"            # 迈创站点运营 表
CARD_CONFIG_TABLE = "tblWugqhkySxdnlA"         # 告警卡片配置 - 迈创 表
CARD_CONFIG_TABLE_NON_MAITUO = "tblcNZKfDloFgDPc"  # 告警卡片配置 - 非迈创 表
ALERT_RULES_TABLE = "tblRa4IDCJ6ylCOz"         # 告警规则配置 表

# ---- 字段名（用中文名写入，与 Base 一致）----
# 只列出可写存储字段；系统/公式/lookup/附件字段不写

# ---- 场景 GUID -> 名称映射（不带花括号）----
SCENARIO_MAP = {
    "38aed1be-7e62-f111-a825-7c1e52fcf3e4": "Push WO to SCM",
    "f651f305-e26a-f111-a826-7ced8d484f6b": "B2X Create WO Request",
    "11fe084c-7d62-f111-a825-7c1e52fcf3e4": "B2X Job Cancel",
    "21c2330b-7d62-f111-a825-7c1e52fcf3e4": "B2X Job Create",
    "7324fd48-e26a-f111-a826-7ced8d484f6b": "B2X Update WO Request",
    "ec7cdf10-746b-f111-ab0e-7c1e5237236a": "MySav Create WO Request",
    "0431d823-746b-f111-ab0e-7c1e5237236a": "MySav Update WO Request",
    "5221da59-756b-f111-ab0e-7c1e5237236a": "Update WO Request",
}

# ---- 日志表字段（中文名 -> 类型）----
# 写入 batch-create 时 key 用中文名
FIELD_WORKORDER = "Work Order"
FIELD_CREATED = "Created On"
FIELD_SCENARIO = "Integration Scenario"
FIELD_TARGET = "Target System"
FIELD_SOURCE = "Source System"
FIELD_REQJSON = "Request JSON"
FIELD_RESPJSON = "Response JSON"
FIELD_ERROR = "报错"
FIELD_STATION = "Station"
FIELD_STATUS = "Status"
FIELD_STATUS_REASON = "Status Reason"
FIELD_B2X = "B2X Order ID"
FIELD_LOGID = "日志ID"
FIELD_WOID = "工单ID"
FIELD_LOGLINK = "日志链接"
FIELD_WOLINK = "工单链接"
FIELD_ABNORMAL = "异常场景"
FIELD_OWNER = "责任人"
FIELD_SENT = "已发送告警"
FIELD_WOSTATUS = "Work Order Status"
FIELD_EXT4 = "Extension Field 4"
FIELD_MAITUO_CODE = "迈创单号"
FIELD_SERVICE_TYPE = "Service Type"
FIELD_WO_SOURCE = "Work Order Source"
FIELD_SERVICE_STORE_NAME = "Service Store Name"  # 新增字段

# ---- 已发送告警 字段ID (用于筛选) ----
FIELD_SENT_ID = "fld2bx9x7p"

# ---- 异常场景判定配置 表 字段（中文名 -> 类型）----
CFG_FIELD_SCENARIO = "Integration Scenario"   # select
CFG_FIELD_KEYWORD = "Response JSON 关键词"    # text
CFG_FIELD_ABNORMAL = "异常场景"                 # select
CFG_FIELD_NOTE = "备注"                          # text

# ---- D365 链接模板 ----
LOG_URL_TPL = "https://eusegwayspp.crm4.dynamics.com/main.aspx?appid=296808a8-ebd5-f011-8543-000d3adcfa64&pagetype=entityrecord&etn=new_integrationlog&id={logid}"
WO_URL_TPL = "https://eusegwayspp.crm4.dynamics.com/main.aspx?appid=296808a8-ebd5-f011-8543-000d3adcfa64&newWindow=true&pagetype=entityrecord&etn=new_workorder&id={woid}"

# ---- 告警相关 ----
GROUP_CHAT = "oc_f1890b5bed23c01839dfb517c63bec48"          # scm-spp 沟通群
OWNER_GONG = "ou_527f81f1af862f57e62694e229640812"          # 贡梦夏
BASE_URL = "https://segway-ninebot.feishu.cn/base/MeCQbGQ5paCJBdsfRFwcfneznFb"

# ---- 异常场景可选值（英文前缀）----
ABNORMAL_OPTIONS = [
    "B2X-接口问题-必填为空", "Maitrox-数据问题-out of SBOM", "Maitrox-数据问题-主数据缺失",
    "Maitrox-接口问题-其他", "MySav-接口问题-必填为空", "B2X-接口问题-状态",
    "MySav-接口问题-状态", "B2X-接口问题-数据", "B2X-接口问题-工单重复", "待补充",
]
