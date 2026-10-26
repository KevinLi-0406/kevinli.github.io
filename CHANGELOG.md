# Changelog

All notable changes to this project will be documented in this file.

## 2026-10-26

### 仓库结构整理
- **修改文件**：`README.md`、`Tools/README.md`、`Tools/project-config.json`、`Tools/stickman-adventure/`（新）、`Tools/travel-planner/beijing-weekend-drive.html`（移入）、`Knowledge/`（删除）
- **变更类型**：重构 + 清理
- **变更描述**：
  1. 归位散落文件：`Tools/stickman-adventure.html` 移入 `Tools/stickman-adventure/index.html`（门户可自动扫描发现）；`docs/beijing-weekend-drive.html` 移入 `Tools/travel-planner/`
  2. 清理废弃文件：删除 `Knowledge/` 空壳目录（知识库已迁移至 Dify）
  3. 更新 `README.md` 仓库结构树（Knowledge 移除、Integration 修正为实际结构、Tools 补全 4 个缺失项目、Resources 修正 portal-editor 引用）
  4. 更新 `Tools/README.md` 项目索引（补充 ai-test-tool、portal-editor、project-weekly-report、stickman-adventure）
  5. `project-config.json` 新增 stickman-adventure 配置（🎮 趣味互动）
- **影响范围**：门户展示（火柴人游戏新增可见）；原 `Tools/stickman-adventure.html` 与 `docs/beijing-weekend-drive.html` 直链失效
- **关联请求**：用户要求"整理下github"
- **Commit**：`6d6de4f` - chore: 仓库结构整理

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
