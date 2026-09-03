# Integration 集成项目文档

本目录包含所有平台集成的技术文档和设计文档。

## 目录结构

```
Integration/
├── cherry-integration/   # Cherry Studio 统一平台集成
│   ├── README.md
│   ├── requirements.md
│   ├── tasks.md
│   ├── progress-log.md
│   ├── operation-log.md
│   └── wecom-integration.md
│
├── feishu-integration/   # 飞书集成（历史记录）
│   ├── README.md
│   ├── requirements.md
│   ├── tasks.md
│   ├── progress-log.md
│   └── operation-log.md
│
└── unified-platform.md   # 统一信息平台架构设计（核心文档）
```

## 集成状态

| 平台 | CLI 工具 | 消息读取 | 消息发送 | 日程/会议 | 待办 | 联系人 |
|------|---------|---------|---------|----------|------|--------|
| 飞书 | lark-cli v1.0.92 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 企业微信 | wecom-cli v1.2.0 | ❌ (需启用) | ✅ | ✅ | ✅ | ✅ |
| Teams | 待开发 | ⏳ | ⏳ |  | ⏳ | ⏳ |
| 邮箱 | 待开发 |  | ⏳ | - | - | - |
