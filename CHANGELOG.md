# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-08-19 16:59 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：
  1. 修复搜索自动推荐功能：将 `AMap.AutoComplete` 替换为 `AMap.PlaceSearch`，因为 `AutoComplete` 不支持 `setLocation()` 和 `setRadius()` 方法，导致 JS 报错且搜索不工作
  2. 修复地铁详情显示：`extractTransitDetail()` 函数从 `seg.transit.onstation` 改为正确读取 `seg.bus.buslines[0].departure_stop.name`（起点站）、`arrival_stop.name`（终点站）、`via_num`（途径站数）
- **影响范围**：地图搜索功能、地铁路线详情展示
- **关联请求**：用户反馈"搜索地点功能不好使了"、"地铁起点站和终点站没显示，途径的站点数也没显示"

### 2026-08-19 16:30 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：
  1. 修复搜索框 location 参数传递：在 `doAutoComplete()` 中使用 `new AMap.LngLat()` 正确传递当前位置
  2. 将"💾 保存方案"按钮移到地点列表页顶部
  3. 修复方案页滚动问题：`.tab-content` 添加 `height: 100%; overflow-y: auto`
  4. 交通按钮 z-index 提升至 60
- **影响范围**：搜索功能、方案保存、方案页滚动、交通方式切换

### 2026-08-19 16:00 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：
  1. 修复地铁颜色从 `icon-config.json` 读取：`loadIconConfig()` 中添加 `Object.assign(SUBWAY_COLORS, iconConfig.subwayColors)`
  2. 重写地铁详情为时间轴式展示：线路名 + 方向 + 上车站→下车站 + 途经站数
  3. 新增 `drawTransitPolylines()` 函数，为每段地铁线路绘制彩色 polyline
- **影响范围**：地铁路线颜色、地铁详情展示、地图线路绘制

### 2026-08-19 15:30 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：修复主页项目列表加载 403 错误，将项目加载方式从 GitHub Contents API 改为直接读取 `project-config.json`
- **影响范围**：主页项目列表加载

### 2026-08-19 15:00 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修改
- **变更描述**：将所有按钮改为"文字 +icon"格式，确保即使 emoji 不显示也能正常使用
- **影响范围**：所有按钮显示
