# D365 日志同步系统 - 文件备份

本目录包含 D365 接口日志同步与告警系统的完整代码和文档备份。

## 目录结构

```
d365-log-sync/
├── scripts/                    # Python 脚本
│   ├── sync.py                # 核心同步脚本
│   ├── card.py                # 告警卡片生成
│   ├── rules.py               # 异常场景判定规则
│   ├── common.py              # 常量定义
│   ├── config_loader.py       # 配置加载器
│   ├── fetch_existing_ids.py  # 去重辅助
│   ├── rejudge_pending_records.py  # 重新判定待补充记录
│   ├── step1_query_service_store.py  # 查询 Service Store Name
│   ├── step2_update_base.py   # 批量更新多维表格
│   └── update_service_store_name.py  # 更新 Service Store Name
│
├── SKILL.md                   # Cherry Studio Skill 定义
├── fetchxml.md                # FetchXML 查询定义
├── card-generation-rules.md   # 卡片生成规则
├── README_local.md            # 本地 README（详细说明）
├── README.md                  # GitHub README（简要说明）
├── CHANGELOG.md               # 更新日志
├── flowchart.html             # 交互式流程图
└── BACKUP.md                  # 本文件
```

## 脚本说明

### 核心脚本

- **sync.py**: 主同步脚本，负责从 D365 拉取数据、异常场景判定、责任人赋值
- **card.py**: 生成告警卡片，支持配置化和聚合
- **rules.py**: 异常场景判定引擎
- **common.py**: 常量定义（表 ID、字段名等）
- **config_loader.py**: 统一配置加载器，读取告警卡片配置

### 辅助脚本

- **fetch_existing_ids.py**: 从多维表格拉取现有日志 ID，用于去重
- **rejudge_pending_records.py**: 重新判定"待补充"状态的记录
- **step1_query_service_store.py**: 从 D365 查询 Service Store Name
- **step2_update_base.py**: 批量更新多维表格中的 Service Store Name
- **update_service_store_name.py**: 完整的 Service Store Name 更新流程

## 配置文件

- **SKILL.md**: Cherry Studio Skill 定义，包含完整的执行流程
- **fetchxml.md**: D365 FetchXML 查询定义
- **card-generation-rules.md**: 告警卡片生成规则

## 运行环境

- Python 3.14+
- lark-cli 1.0.98+
- Cherry Studio（定时任务）
- Dataverse MCP 工具（D365 查询）

## 飞书多维表格

- Base Token: `MeCQbGQ5paCJBdsfRFwcfneznFb`
- 日志表: `tblTWNXVEKv0IScf`
- 迈创配置表: `tblePVTwOyMzPNG8`
- 非迈创配置表: `tblbscUEUlXSUQE4`
- 站点运营表: `tbl0Xiuz6KJ3SSC4`
- 告警卡片配置-迈创: `tblWugqhkySxdnlA`
- 告警卡片配置-非迈创: `tblcNZKfDloFgDPc`

## 备份日期

2026-10-23

## 维护者

Kevin Li (李奕兴)  
yixing.li@ninebot.com
