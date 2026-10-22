# Changelog

All notable changes to this project will be documented in this file.

## 2026-10-22

### 19:45 (UTC+8)
- **修改文件**：`Integration/d365-log-sync/README.md`
- **变更类型**：新增
- **变更描述**：新增 D365 接口日志同步与告警系统文档，包含系统架构、数据流程、配置表说明、关键脚本说明、部署运维指南
- **影响范围**：Integration 目录新增 d365-log-sync 子项目
- **关联请求**：用户要求将今天的修改内容写入 GitHub 仓库
- **Commit**：`ac4cda8` - feat: 新增 D365 接口日志同步与告警系统文档

#### 详细变更

**D365 日志同步系统重构（2026-10-22）**

1. **配置表拆分**
   - 原单表 `tblIqZ9T8Ekj9h8y` 拆分为：
     - 迈创配置表 `tblePVTwOyMzPNG8`（Push WO to SCM 场景）
     - 非迈创配置表 `tblbscUEUlXSUQE4`（B2X/MySav/Update 等场景）
   
2. **新增 Service Store Name 字段**
   - 在 D365接口日志表新增 `Service Store Name` 字段
   - FetchXML 扩展：关联查询 `new_servicestore` 实体
   - 批量更新 614 条历史记录的 Service Store Name

3. **异常场景命名统一**
   - 从中文前缀（迈创-）改为英文前缀（Maitrox-）
   - 示例：`Maitrox-数据问题-BOM`、`B2X-接口问题-必填为空`

4. **告警卡片配置化**
   - 新增「告警卡片配置-迈创」表 `tblWugqhkySxdnlA`
   - 新增「告警卡片配置-非迈创」表 `tblcNZKfDloFgDPc`
   - 支持按场景配置不同的卡片样式、颜色、艾特规则

5. **迈创站点运营表**
   - 新增 `tbl0Xiuz6KJ3SSC4`，存储 Service Store Name → 负责人映射
   - 16 条记录，覆盖所有 RC（维修中心）

6. **卡片聚合功能**
   - 按聚合组代码（GROUP_DATA、GROUP_INTERFACE 等）合并记录
   - 同一聚合组的记录合并到一张卡片中

7. **自动 @责任人**
   - 迈创场景根据 Service Store Name 匹配负责人
   - 自动 @对应的负责人

8. **告警规则配置表**
   - 新增 `tblRa4IDCJ6ylCOz`，存储特殊优先级规则、字段显示逻辑、标红规则

---

**维护者**：Kevin Li (李奕兴)  
**最后更新**：2026-10-22
