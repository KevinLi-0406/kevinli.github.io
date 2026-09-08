# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 2026-09-08 18:50 (UTC+8)
- **修改文件**：`Integration/integration-details.md`
- **变更类型**：功能增强 + Skill 重构
- **变更描述**：
  1. **SPP Skill 拆分**：原 `spp` skill 拆分为 `sppprd`（生产环境）和 `sppuat2`（测试环境）两个独立 skill
  2. **MCP 环境绑定修正**：明确 `mcp__1ef94522-4afe-4997-9c03-3145aa460b10__*` 对应 UAT2 环境，`mcp__2de134c2-404e-465f-8170-8f6abb4ef943__*` 对应 PRD 环境
  3. **Mysav 集成日志定时任务**：新增两个定时任务
     - 每天北京时间 10:00 从 UAT2 环境导出 Mysav 集成错误日志到桌面
     - 每天北京时间 12:00 通过 SMTP 发送带附件邮件给 Paul 和 Somsanouk
  4. **SMTP 邮件配置**：使用网易企业邮箱 SMTP (smtphz.qiye.163.com:994) 发送带附件邮件
- **影响范围**：SPP 运维助手 skill 结构、Mysav 集成日志自动化流程
- **关联请求**：用户反馈需要自动化导出并发送 Mysav 集成错误日志

### 2026-09-04 16:56 (UTC+8)
