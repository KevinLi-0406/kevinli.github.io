# Integration - 统一信息平台

本目录包含**统一信息平台**项目的所有技术文档。

> 核心理念：**一个大脑，四个触角** —— Cherry Studio AI 整合企微、飞书、Teams、邮箱

## 目录结构

```
Integration/
├── README.md              # 本文件
├── unified-platform.md    # 统一平台架构设计（需求 + 方案 + 路线图）
├── requirements.md        # 功能需求文档
├── tasks.md               # 任务清单
├── progress-log.md        # 进度日志
├── operation-log.md       # 操作日志
└── wecom-integration.md   # 企业微信集成详情
```

## 集成状态

| 平台 | CLI 工具 | 消息读取 | 消息发送 | 日程/会议 | 待办 | 联系人 |
|------|---------|---------|---------|----------|------|--------|
| 飞书 | lark-cli v1.0.92 | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| 企业微信 | wecom-cli v1.2.0 | ❌ (需启用) | ✅ (aibot) | ✅ | ✅ | ✅ |
| Teams | 待开发 |  | ⏳ | ⏳ |  | ⏳ |
| 邮箱 | 待开发 | ⏳ | ⏳ | - | - | - |

## 快速链接

- [统一平台架构设计](unified-platform.md)
- [企业微信集成详情](wecom-integration.md)
- [项目任务清单](tasks.md)
- [进度日志](progress-log.md)
- [操作日志](operation-log.md)
