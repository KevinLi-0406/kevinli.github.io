# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

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
