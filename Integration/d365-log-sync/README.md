# D365 接口日志同步与告警系统

## 项目概述

D365 接口日志同步与告警系统是一个自动化的监控和告警平台，用于实时监控 Dynamics 365 生产环境中的集成接口报错，并通过飞书多维表格和群聊卡片进行可视化展示和即时通知。

### 核心功能

- **实时监控**：每小时自动查询 D365 生产环境的集成接口报错日志
- **智能判定**：基于配置表规则自动判定异常场景（支持 60+ 种异常类型）
- **配置化管理**：所有告警规则、卡片样式、通知对象均可通过飞书多维表格动态配置
- **自动告警**：根据异常场景自动生成告警卡片并发送到指定飞书群
- **责任人匹配**：迈创场景根据 Service Store Name 自动匹配并 @对应的负责人

---

## 系统架构

（见原文档）

---

## 完整数据流程

### 第1步：定时触发

**工具**：Cherry Studio Cron Job  
**频率**：每小时整点  
**Cron Job ID**: a09e0a38-f275-4903-bd2d-839827902978

### 第2步：查询 D365 生产环境

**工具**：Dataverse MCP 工具  
**查询方式**：FetchXML  
**输出**：d365_fetchxml_YYYYMMDD_HHMM.json

### 第3步：数据同步与异常判定

**脚本**：scripts/sync.py

- 去重：fetch_existing_ids_from_base()
- 异常判定：judge_abnormal()
- 责任人赋值：迈创根据 Service Store Name，非迈创从配置表读取

### 第4步：写入飞书多维表格

**工具**：lark-cli base +record-batch-create  
**目标表**：tblTWNXVEKv0IScf  
**批次限制**：≤200 条/批

### 第5步：读取配置表

**脚本**：config_loader.py  
**读取内容**：告警卡片配置（是否启用、卡片样式、聚合规则等）

### 第6步：生成告警卡片

**脚本**：scripts/card.py  
**逻辑**：按异常场景分组 → 按聚合组合并 → 生成 Card 2.0 JSON

### 第7步：发送告警卡片

**工具**：飞书 MCP 工具  
**目标群**：scm-spp 沟通群

### 第8步：标记已发送

**工具**：lark-cli base +record-batch-update  
**更新字段**：已发送告警 = true

---

## 多维表格结构

### D365接口日志表 (tblTWNXVEKv0IScf) - 28个字段

核心字段：Work Order, Created On, Integration Scenario, 异常场景, 责任人, Service Store Name, 已发送告警

### 异常场景判定配置表

- 迈创 (tblePVTwOyMzPNG8) - 5个字段
- 非迈创 (tblbscUEUlXSUQE4) - 6个字段（含责任人）

### 迈创站点运营表 (tbl0Xiuz6KJ3SSC4) - 8个字段

Service Store Name → 负责人 映射

### 告警卡片配置表 - 13个字段

- 迈创 (tblWugqhkySxdnlA)
- 非迈创 (tblcNZKfDloFgDPc)

关键字段：是否启用、卡片颜色、是否艾特、聚合组代码

---

## 脚本说明

- sync.py：核心同步脚本
- rules.py：异常场景判定
- card.py：告警卡片生成
- config_loader.py：配置加载器
- common.py：常量定义

---

## 部署与运维

### 环境要求

- Python 3.14+
- lark-cli 1.0.98+
- Cherry Studio
- Dataverse MCP 工具

### 定时任务

每小时整点执行 d365-log-sync-alert skill

---

## 常见问题

1. 配置表更新后立即生效
2. 取消勾选"是否启用"可禁用告警
3. Service Store Name 为空时运行批量更新脚本

---

**维护者**：Kevin Li (李奕兴)  
**最后更新**：2026-10-23
