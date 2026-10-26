# Tools 项目索引

本目录包含所有 HTML 工具项目。每个子目录对应一个独立项目。

## 项目列表

| 项目 | 文件 | 说明 |
|------|------|------|
| AI API 测试工具 | `ai-test-tool/index.html` | 多模型对比与性能基准测试 |
| B2X 工单查询 | `b2x-query/index.html` | 工作中用到的工单查询工具 |
| CherryStudio CSS 编辑器 | `css-editor/index.html` | Cherry Studio 的 CSS 编辑器 |
| F1 数据大全 | `f1-data/index.html` | 个人兴趣 - F1 赛车数据 |
| 城市漫游行程助手 | `travel-planner/index.html` | 旅行规划工具 (v2.2.0) |
| 共享相册 | `photo-album/index.html` | 图片分享工具 |
| 宝可梦全国图鉴 | `pokemon-pokedex/index.html` | 个人兴趣 - 宝可梦 |
| 门户可视化编辑器 | `portal-editor/index.html` | 点击元素修改 index.html 并发布到 GitHub |
| 项目周报管理 | `project-weekly-report/index.html` | 按周管理项目进度、风险和拉通事项 |
| 火柴人冒险 | `stickman-adventure/index.html` | 趣味横版闯关小游戏 |
| 奇怪的杰尼龟 | `squirts/index.html` | 个人兴趣 - 虚拟宠物 |
| 奇怪的小鸡毛 | `chicks/index.html` | 个人兴趣 - 虚拟宠物 |

## 约定

- 每个项目一个子目录，入口文件统一为 `index.html`，门户会自动扫描发现。
- 图标、分类等元数据配置在 `project-config.json`。

## 迁移说明

> [!NOTE]
> 原 `Projects/` 目录中的 HTML 工具文件已迁移到 `Tools/` 下的各自子目录中。
> 原文件名保留为 `index.html`，通过子目录隔离，避免命名冲突。
