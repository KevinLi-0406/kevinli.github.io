# 飞书实时监听机器人

基于 **WebSocket 长连接** 的飞书群聊实时监听方案。当有人在群里 @机器人 提问时，自动读取项目文档、调用 AI 生成回复并发送到群里。

**对比轮询方案的优势：**

| 维度 | 轮询（2分钟/次） | 长连接（本方案） |
|------|------------------|------------------|
| 响应延迟 | 0-2 分钟 | 1-3 秒 |
| API 调用量 | 每天 ~720 次/群 | 仅按需调用 |
| 公网地址 | 不需要 | 不需要 |
| 部署复杂度 | 低（定时任务） | 低（常驻进程） |

---

## 快速开始

### 1. 飞书开放平台配置（必须先完成）

登录 [飞书开放平台](https://open.feishu.cn/app/) → 找到应用 `cli_aa1d00640cf9dcd4`：

1. **事件与回调** → **订阅方式** → 选择 **"使用长连接接收事件/回调"**
2. **事件与回调** → **事件配置** → 添加事件：
   - `im.message.receive_v1`（接收消息）
3. **权限管理** → 确保以下权限已开通：
   - `im:message` — 获取与发送单聊、群组消息
   - `im:message:send_as_bot` — 以应用身份发送消息
4. **版本管理与发布** → 创建新版本并发布

### 2. 本地安装

```bash
cd Integration/feishu-bot
npm install
cp .env.example .env
```

### 3. 编辑 .env 配置

填入飞书 App Secret 和 AI API 密钥，详见 `.env.example` 中的注释说明。

### 4. 启动

```bash
npm start       # 正常启动
npm run dev     # 开发模式（文件修改后自动重启，需要 Node.js 22+）
```

---

## 工作原理

```
用户在群里 @机器人 提问
        ↓ (~1秒)
飞书通过 WebSocket 推送 im.message.receive_v1 事件
        ↓
脚本接收事件 → 校验群聊 → 排除非@消息
        ↓
贴表情（LOVE ❤️）表示已收到
        ↓
从本地仓库读取文档作为知识库
        ↓
调用 AI API（OpenAI 兼容格式）生成回复
        ↓
在群里回复消息（@提问人）
        ↓
总延迟：2-5 秒
```

---

## 文件结构

```
Integration/feishu-bot/
├── feishu-bot.js      # 主脚本
├── package.json       # 依赖管理
├── .env.example       # 配置模板
├── .env               # 你的实际配置（不提交到 Git）
├── .gitignore         # Git 忽略规则
└── README.md          # 本文档
```

---

## 常见问题

**Q: 连接失败怎么办？**
A: 检查 App Secret 是否正确，确保在飞书后台选择了"长连接"模式（非 Webhook）。

**Q: 收不到消息？**
A: 确保已在飞书后台添加 `im.message.receive_v1` 事件订阅，并发布新版本。

**Q: 如何后台常驻运行？**
A: 推荐使用 `pm2`：
```bash
npm install -g pm2
pm2 start feishu-bot.js --name feishu-bot
pm2 save
pm2 startup
```

**Q: 如何更换 AI 模型？**
A: 修改 `.env` 中的 `AI_API_URL` 和 `AI_MODEL`。支持任何 OpenAI 兼容 API。

**Q: 文档更新后需要重启吗？**
A: 不需要。脚本会监听文档文件变化，自动重新加载知识库。
