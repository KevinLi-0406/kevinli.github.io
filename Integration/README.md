# Integration - 多平台集成项目

本目录包含所有平台集成的技术文档和设计文档。

## 目录结构

```
Integration/
├── cherry-integration/   # Cherry Studio 统一平台集成
│   ├── README.md         # 项目概述
│   ├── requirements.md   # 需求文档
│   ├── tasks.md          # 任务清单
│   ├── progress-log.md   # 进度日志
│   ├── operation-log.md  # 操作日志
│   ├── unified-platform-design.md  # 统一平台架构设计
│   └── wecom-integration.md        # 企业微信集成详情
│
└── feishu-integration/   # 飞书集成（历史记录）
    └── (已清空，内容合并到 cherry-integration/)
```

## 集成状态

| 平台 | CLI 工具 | 消息读取 | 消息发送 | 日程/会议 | 待办 | 联系人 |
|------|---------|---------|---------|----------|------|--------|
| 飞书 | lark-cli v1.0.92 | ✅ | ✅ | ✅ | ⚠️ | ✅ |
| 企业微信 | wecom-cli v1.2.0 | ❌ (需启用) | ✅ (aibot) | ✅ | ✅ | ✅ |
| Teams | 待开发 |  | ⏳ | ⏳ |  | ⏳ |
| 邮箱 | 待开发 | ⏳ | ⏳ | - | - | - |

## 快速链接

- [统一平台架构设计](cherry-integration/unified-platform-design.md)
- [企业微信集成详情](cherry-integration/wecom-integration.md)
- [项目任务清单](cherry-integration/tasks.md)
- [进度日志](cherry-integration/progress-log.md)
- [操作日志](cherry-integration/operation-log.md)
