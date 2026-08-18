# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-08-18 15:00 (UTC+8)
- **修改文件**：`Projects/共享相册.html`、`Resources/Media/manifest.json`
- **变更类型**：修复
- **变更描述**：修复上传文件后上传者显示"未知"的 bug。根因：`loadManifest()` 双向同步逻辑在上传后重新扫描目录时，由于 GitHub API 缓存/延迟，将已上传文件误判为"新文件"，通过 `scanMediaDirectory()` 以 `uploader: 'unknown'` 重新添加并写回 manifest，覆盖了 `uploadFiles()` 设置的正确上传者信息。修复方案：在 `loadManifest()` 同步逻辑中添加去重检查（`updated.some()` 判断），若文件已存在于 manifest 中则跳过目录扫描的重复添加；同时修复 manifest.json 中 4 个被错误标记为 "unknown" 的条目（一起走、戳戳、擦擦头、躺躺），恢复为 Kevin/Kevin Li
- **影响范围**：上传流程、manifest 同步逻辑、相册上传者显示
- **关联请求**：用户反馈"登陆了kevin账号并且上传了图片，但是相册展示依然显示上传人是未知"

### 2026-08-18 14:43 (UTC+8)
- **修改文件**：`Projects/共享相册.html`、`Resources/Media/manifest.json`
- **变更类型**：修复
- **变更描述**：修复上传用户相关的 3 个问题：1) 上传面板移除下拉选择器，改为显示当前登录用户的信息条（头像首字母 + 昵称），上传者始终为当前登录用户；2) 用户筛选器改用 `uploaderNickname` 作为 Map key，修复所有文件 `uploader` 为 "unknown" 导致只显示一个用户的问题；3) 修复 manifest.json 中现有条目的 `uploader` 字段从 "unknown" 改为实际用户名（Kira/Kevin），`uploaderNickname` 改为对应昵称（Kira/Kevin Li）
- **影响范围**：上传面板 UI、用户筛选器、统计卡片中的上传用户数、manifest 数据一致性
- **关联请求**：用户反馈"上传用户可选用户应和 admin 清单一致"、"上传用户应为当前登录用户"、"manifest 有两个上传者但页面只显示一个"

### 2026-08-18 14:13 (UTC+8)
- **修改文件**：`Projects/F1数据大全.html`
- **变更类型**：修改
- **变更描述**：全面重构 F1 数据大全页面，集成 `Resources/F1-images/` 下的本地图片资源：1) 车手档案卡片集成 22 位车手官方半身照（Drivers 文件夹）；2) 赛车与车队卡片集成 11 支车队赛车照片（Teams 文件夹）；3) 赛程日历集成 15 张真实赛道地图（Tracks 文件夹），无图片的赛道保留 SVG fallback；4) 更新车手数据为 2026 赛季 22 人阵容（新增 Audi、Cadillac、Racing Bulls 等车队）；5) 美化页面设计，增加 hover 动画、渐变背景、切角效果等视觉增强
- **影响范围**：F1 数据大全页面的所有模块（赛程、积分榜、车手档案、赛车展示）
- **关联请求**：用户要求"根据 F1-images 文件夹下的车手/车队/赛道/赛车图片，应用并美化 F1数据大全.html"

### 2026-08-18 13:51 (UTC+8)
- **修改文件**：`Resources/Media/manifest.json`
- **变更类型**：删除
- **变更描述**：从 manifest.json 中移除所有 27 个以 2026 开头的 png 文件条目（包括 alpine/astonmartin/audi/cadillac/ferrari/haas/mclaren/mercedes/racingbulls/redbull/williams 等车队的赛车图和车辆图），manifest 现仅保留 3 个 gif 文件
- **影响范围**：共享相册的图片索引，相册中将不再显示这些 2026 png 文件
- **关联请求**：用户要求"把 Resources/Media/ 路径下所有2026开头的png文件都删除"
- **备注**：由于 GitHub MCP 工具不支持文件删除操作，本次仅更新了 manifest.json 移除索引记录。实际的 png 二进制文件仍存在于仓库中，如需彻底删除请通过 GitHub 网页或 git 命令行操作

### 2026-08-17 21:03 (UTC+8)
- **修改文件**：`Projects/Shared Album.html`
- **变更类型**：修复
- **变更描述**：修复 8 个问题：1) 登录弹窗立即显示，不再等待 loadUsers() 完成；2) 重置按钮恢复 🔁 emoji；3) 填满格子选项添加 📐 emoji；4) manifest.json 双向同步（目录有manifest没有→添加，manifest有目录没有→移除），新增 writeManifest() 通用函数；5) 布局改回垂直排列（概览→筛选器→上传→网格）；6) 图片 URL 改用 jsdelivr CDN 加速加载；7) 新增格式筛选器（JPEG/PNG/GIF/WEBP等），动态提取文件扩展名；8) 灯箱切换动效 CSS 选择器从 .lightbox-media-content 修正为 .lightbox-content，滑动距离增大到 80px
- **影响范围**：登录流程、manifest 同步、页面布局、图片加载速度、筛选功能、灯箱动效
- **关联请求**：用户反馈 8 个问题（登录慢/emoji消失/manifest不一致/布局/加载慢/格式筛选/灯箱动效）

### 2024-01-15 14:30 (UTC+8)
- **修改文件**：`Projects/Shared Album.html`
- **变更类型**：修复
- **变更描述**：修复 5 个用户反馈问题：1) 删除文件后 manifest.json 未正确更新，现在删除时会自动同步 manifest；2) 添加灯箱滚轮缩放功能（上滚放大/下滚缩小）；3) 添加图片左右切换的幻灯片动效（slide-left/slide-right）；4) 添加显示模式切换（填满格子/原始大小）；5) 重构页面布局，统计 + 筛选器和上传面板并排显示，相册网格横向扩大
- **影响范围**：删除功能、灯箱交互、相册布局、显示模式
- **关联请求**：用户反馈"删除 gif 后重新登录依然能看到"、"滚轮缩放没实现"、"幻灯片动效没实现"、"显示模式切换没实现"、"布局空白太多"

### 2024-01-15 12:15 (UTC+8)
- **修改文件**：`Projects/Shared Album.html`
- **变更类型**：修复
- **变更描述**：修复登录弹窗用户下拉列表为空的问题，调整初始化顺序确保 loadUsers() 完成后再弹出登录框
- **影响范围**：登录流程
- **关联请求**：用户反馈"登录页面不能选择用户了"

### 2024-01-15 11:45 (UTC+8)
- **修改文件**：`Projects/Shared Album.html`
- **变更类型**：修复
- **变更描述**：修复刷新按钮权限检查逻辑，将 !state.isAdministrator && !state.loginPat 改为 !state.currentUser，使游客也能刷新
- **影响范围**：刷新功能
- **关联请求**：用户反馈"点刷新提示请登录"
