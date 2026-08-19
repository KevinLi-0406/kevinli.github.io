# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-08-19 19:30 (UTC+8)
- **修改文件**：`Projects/travel-planner-v2.0.3.html`、`Projects/project-config.json`
- **变更类型**：新增
- **变更描述**：新增不可覆盖的城市漫游行程助手 v2.0.3。地铁路线和详情改为直接读取高德换乘响应中 `segments[].bus.buslines[]` 的线路类型、上下车站、途经站数、途经站及真实 `polyline`，并按 `icon-config.json` 的线路颜色绘制。
- **影响范围**：城市漫游行程助手 v2.0.3 地铁地图路线、地点详情弹窗及首页旅行规划项目列表
- **关联请求**："这些数据接口里都有，为什么你做前端展示的时候不用呢？"

### 2026-08-19 19:10 (UTC+8)
- **修改文件**：`Projects/travel-planner-v2.0.2.html`、`Projects/project-config.json`
- **变更类型**：新增
- **变更描述**：新增不可覆盖的城市漫游行程助手 v2.0.2。修复地铁分段配置色绘制被清除、详情按钮跨 iframe 访问词法变量失效、驾车与导航图标兜底，以及将搜索与输入推荐改为以高德已转换的当前位置为 `location` 的 100km 周边检索。
- **影响范围**：城市漫游行程助手 v2.0.2 独立访问页、首页旅行规划项目列表
- **关联请求**："你的地图上的地铁线路没有按照我的要求"、"location设置为这一步获取到的location"、"驾车icon为空、导航icon为空"、"地点列表的详情按钮点击后没有任何反应"

### 2026-08-19 18:45 (UTC+8)
- **修改文件**：`Projects/travel-planner-v2.0.1.html`、`Projects/project-config.json`
- **变更类型**：新增
- **变更描述**：新增不可覆盖的城市漫游行程助手 v2.0.1 独立版本文件，并在项目配置中新增首页入口。v2.0.1 以当前已修复的 v2.0.0 功能为发布基线，保留历史版本文件不变。
- **影响范围**：城市漫游行程助手 v2.0.1 独立访问页、首页旅行规划项目列表
- **关联请求**："为什么不生成新的版本的html？那我让你做版本管理还有什么意义"、"生成"

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

### 2026-08-19 16:30 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：修复搜索框 location 参数传递、保存方案入口、方案页滚动和交通按钮层级。
- **影响范围**：搜索功能、方案保存、方案页滚动、交通方式切换

### 2026-08-19 16:00 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：修复地铁颜色读取、地铁详情展示和分段 polyline 绘制。
- **影响范围**：地铁路线颜色、地铁详情展示、地图线路绘制

### 2026-08-19 15:30 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修复
- **变更描述**：修复主页项目列表加载 403 错误，将项目加载方式从 GitHub Contents API 改为直接读取 `project-config.json`。
- **影响范围**：主页项目列表加载

### 2026-08-19 15:00 (UTC+8)
- **修改文件**：`Projects/travel-planner.html`
- **变更类型**：修改
- **变更描述**：将所有按钮改为"文字 +icon"格式，确保即使 emoji 不显示也能正常使用。
- **影响范围**：所有按钮显示
