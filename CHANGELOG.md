# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-08-19 18:38 (UTC+8)
- **修改文件**：`Projects/travel-planner-v2.0.0.html`
- **变更类型**：修复
- **变更描述**：修复地铁路线在缺少可绘制分段坐标时地图空白的问题，改为回退高德原生路线；同时修复地点详情入口、分类图标统一与当前位置 100km 同城附近搜索。
- **影响范围**：城市漫游行程助手 v2.0.0 的路线规划、地点详情、分类展示和地图搜索
- **关联请求**："选中地图上的地点并且选择地铁后，地图上直接不显示路线了"、"部分按钮的icon依然缺失：博物馆、驾车"、"地点列表的详情按钮点击了没反应"、"地点分类文字和显示的icon不一致"、"搜索的时候依然没有以当前位置为圆心"

### 2026-08-19 18:35 (UTC+8)
- **修改文件**：`Projects/project-config.json`
- **变更类型**：修改
- **变更描述**：在主页项目配置中新增 `travel-planner-v2.0.0.html`，使 `index.html` 通过既有项目加载逻辑展示城市漫游 v2.0.0 的入口。
- **影响范围**：首页项目列表、旅行规划分类
- **关联请求**："新版本的travelplanner没有在index.html中显示"

### 2026-08-19 18:26 (UTC+8)
- **修改文件**：`Projects/travel-planner-v2.0.0.html`
- **变更类型**：新增
- **变更描述**：新增带版本标识的独立城市漫游页面，不覆盖现有 `travel-planner.html`。该版本以现有页面为基础注入地铁配置色、详情直查、彩色分段与换乘标注、100km 同城搜索、图标兜底和折叠地图交通栏可见性修复。
- **影响范围**：城市漫游行程助手 v2.0.0 独立访问页
- **关联请求**："地铁路线的颜色根据kevinli.github.io/Projects/icon-config.json里面的配置表读取"、"搜索的时候把当前位置作为圆心，搜索本城市内周边100km的结果"、"依然存在icon缺失的情况"、"将功能区收起来后，我看不到选中地点后切换交通方式的按钮了"、"那你生成个新html吧，标注上版本"

### 2026-08-19 17:57 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：
  1. **搜索自动推荐回退**：将 `AMap.PlaceSearch` 回退到 `AMap.AutoComplete`，因为 `PlaceSearch` 返回完整搜索结果数据量大、响应慢，用户体验差。`AutoComplete` 是专门用于输入建议的 API，响应更快
  2. **地铁详情显示修复**：`extractTransitDetail()` 函数正确从 `seg.bus.buslines[0]` 中提取 `departure_stop.name`（起点站）、`arrival_stop.name`（终点站）、`via_num`（途径站数）
  3. **添加调试日志**：在 `showPlaceRoute()` 中添加 `console.log('🚇 地铁详情:', detail)` 便于排查问题
- **影响范围**：地图搜索自动推荐、地铁路线详情展示
- **关联请求**：用户反馈"搜索自动推荐不工作了，建议回退到之前工作的版本"、"地铁路线详情也不显示了，还不如上一个版本"

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
