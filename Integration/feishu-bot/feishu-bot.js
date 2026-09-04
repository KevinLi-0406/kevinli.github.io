#!/usr/bin/env node
/**
 * 飞书实时监听机器人 - WebSocket 长连接模式
 *
 * 功能：实时监听指定群聊中 @机器人 的消息，基于本地文档知识库调用 AI 生成回复
 *
 * 前置条件：
 *   1. 飞书开放平台后台 → 事件与回调 → 订阅方式 → 选择"使用长连接接收事件"
 *   2. 添加事件订阅：im.message.receive_v1
 *   3. 确保机器人有 im:message 和 im:message:send_as_bot 权限
 *
 * 使用方式：
 *   npm install
 *   cp .env.example .env  (然后编辑填入真实值)
 *   node feishu-bot.js
 */

'use strict';

const Lark = require('@larksuiteoapi/node-sdk');
const fs = require('fs');
const path = require('path');

// ────────────────────────────────────────────────────────────────
// 配置（优先从环境变量读取）
// ────────────────────────────────────────────────────────────────

// 尝试加载 .env 文件（简单实现，不引入 dotenv 依赖）
function loadEnv() {
  const envPath = path.join(__dirname, '.env');
  if (!fs.existsSync(envPath)) return;
  const lines = fs.readFileSync(envPath, 'utf-8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    let val = trimmed.slice(eqIdx + 1).trim();
    // 去除引号
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (!process.env[key]) process.env[key] = val;
  }
}
loadEnv();

const APP_ID = process.env.FEISHU_APP_ID || 'cli_aa1d00640cf9dcd4';
const APP_SECRET = process.env.FEISHU_APP_SECRET || '';
const REPO_PATH = process.env.REPO_PATH || path.resolve(__dirname, '../../');
const CONFIG_PATH = path.join(REPO_PATH, 'Integration', 'monitored-chats.json');

// AI API 配置（兼容 OpenAI API 格式）
const AI_API_URL = process.env.AI_API_URL || 'https://api.openai.com/v1/chat/completions';
const AI_API_KEY = process.env.AI_API_KEY || '';
const AI_MODEL = process.env.AI_MODEL || 'gpt-4o-mini';

// ────────────────────────────────────────────────────────────────
// 启动前校验
// ────────────────────────────────────────────────────────────────

if (!APP_SECRET) {
  console.error('❌ 错误：FEISHU_APP_SECRET 未配置');
  console.error('   请在 .env 文件中设置，或通过环境变量传入');
  process.exit(1);
}

if (!AI_API_KEY) {
  console.warn('⚠️  AI_API_KEY 未配置，将使用固定提示回复（无法生成智能回答）');
}

// ────────────────────────────────────────────────────────────────
// 知识库加载
// ────────────────────────────────────────────────────────────────

function loadKnowledgeBase() {
  const docs = [
    { name: '项目概览', file: 'README.md' },
    { name: '统一平台设计', file: 'Integration/unified-platform.md' },
    { name: '集成详情', file: 'Integration/integration-details.md' },
    { name: '需求文档', file: 'Integration/requirements.md' },
  ];

  let kb = '';
  for (const doc of docs) {
    const filePath = path.join(REPO_PATH, doc.file);
    if (fs.existsSync(filePath)) {
      kb += `\n\n===== ${doc.name} =====\n`;
      kb += fs.readFileSync(filePath, 'utf-8');
    }
  }

  console.log(`📚 知识库已加载（${(kb.length / 1024).toFixed(1)} KB）`);
  return kb;
}

let knowledgeBase = loadKnowledgeBase();

// ────────────────────────────────────────────────────────────────
// 监听配置加载
// ────────────────────────────────────────────────────────────────

function loadMonitoredChats() {
  try {
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf-8'));
    return config.monitored_chats.filter(c => c.enabled);
  } catch (e) {
    console.error(`❌ 读取监听配置失败：${e.message}`);
    return [];
  }
}

function getMonitoredChatIds() {
  return new Set(loadMonitoredChats().map(c => c.chat_id));
}

// ────────────────────────────────────────────────────────────────
// AI 回复生成
// ────────────────────────────────────────────────────────────────

async function generateReply(question, senderName) {
  if (!AI_API_KEY) {
    return `你好 ${senderName}，AI API 密钥未配置，暂时无法回答你的问题。请联系管理员配置 AI_API_KEY。`;
  }

  try {
    const response = await fetch(AI_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${AI_API_KEY}`,
      },
      body: JSON.stringify({
        model: AI_MODEL,
        messages: [
          {
            role: 'system',
            content: [
              '你是"李奕兴的智能助手"，一个在飞书群聊中工作的项目助理机器人。',
              '你的职责是基于以下项目文档回答团队成员的问题。',
              '',
              '回答规则：',
              '1. 只基于文档中的事实信息回答，不推测',
              '2. 如果问题超出文档范围，回复"这个问题我还需要确认，稍后回复你"',
              '3. 回答简洁明了，控制在 200 字以内',
              '4. 使用中文回复，保持友好专业的语气',
              '5. 不要使用 markdown 格式（飞书消息不支持）',
              '',
              '--- 项目文档 ---',
              knowledgeBase,
            ].join('\n'),
          },
          {
            role: 'user',
            content: `${senderName} 提问：${question}`,
          },
        ],
        temperature: 0.3,
        max_tokens: 500,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error(`❌ AI API 错误 [${response.status}]：${errText}`);
      return `抱歉，AI 服务暂时不可用，请稍后再试。`;
    }

    const data = await response.json();
    return data.choices?.[0]?.message?.content || '抱歉，我暂时无法回答这个问题。';
  } catch (e) {
    console.error(`❌ AI 调用异常：${e.message}`);
    return `抱歉，处理你的问题时遇到了错误，请稍后再试。`;
  }
}

// ────────────────────────────────────────────────────────────────
// 消息工具函数
// ────────────────────────────────────────────────────────────────

/**
 * 检查消息是否 @了机器人
 * 飞书事件 mentions 结构：{ id: { open_id, union_id }, mentioned_type: "bot"|"user", name: "机器人名" }
 */
function isAtBot(data, botAppId) {
  const mentions = data.message?.mentions || [];
  for (const m of mentions) {
    // 最可靠：mentioned_type 为 "bot" 且 name 匹配
    if (m.mentioned_type === 'bot') return true;
    // 兼容：name 包含机器人名称
    if (m.name && m.name.includes('智能助手')) return true;
    // 兼容：id 为字符串时直接比较 app_id
    if (typeof m.id === 'string' && m.id === botAppId) return true;
  }
  return false;
}

/**
 * 从消息中提取纯文本内容
 */
function extractText(data) {
  const msgType = data.message?.message_type;
  const content = data.message?.content;
  if (!content) return '';

  try {
    const parsed = JSON.parse(content);

    if (msgType === 'text') {
      // text 类型：{"text":"@_user_1 你好"}
      return (parsed.text || '').replace(/@_user_\d+/g, '').trim();
    }

    if (msgType === 'post') {
      // post 类型：嵌套的 content 数组
      const postContent = parsed.content || parsed.zh_cn?.content || [];
      const texts = [];
      for (const line of postContent) {
        for (const segment of line) {
          if (segment.tag === 'text' && segment.text) {
            texts.push(segment.text);
          }
        }
      }
      return texts.join(' ').trim();
    }
  } catch (e) {
    // JSON 解析失败，返回空
  }
  return '';
}

/**
 * 从事件数据中提取发送者信息
 */
function getSenderInfo(data) {
  return {
    openId: data.sender?.sender_id?.open_id || '',
    senderType: data.sender?.sender_type || '',
  };
}

/**
 * 发送回复消息（基于原消息回复，形成消息串）
 * 使用 im.v1.message.reply API，回复会挂在原消息下方
 */
async function sendReply(client, messageId, senderOpenId, replyText) {
  const content = {
    zh_cn: {
      title: '',
      content: [
        [
          { tag: 'at', user_id: senderOpenId, user_name: '' },
          { tag: 'text', text: ` ${replyText}` },
        ],
      ],
    },
  };

  try {
    await client.im.v1.message.reply({
      path: { message_id: messageId },
      data: {
        content: JSON.stringify(content),
        msg_type: 'post',
      },
    });
    console.log(`  ✅ 回复已发送（引用原消息）`);
  } catch (e) {
    console.error(`  ❌ 回复发送失败：${e.message}`);
  }
}

/**
 * 发送简单文本消息
 */
async function sendText(client, chatId, text) {
  try {
    await client.im.v1.message.create({
      params: { receive_id_type: 'chat_id' },
      data: {
        receive_id: chatId,
        content: JSON.stringify({ text }),
        msg_type: 'text',
      },
    });
  } catch (e) {
    console.error(`  ❌ 消息发送失败：${e.message}`);
  }
}

// ────────────────────────────────────────────────────────────────
// 主流程
// ────────────────────────────────────────────────────────────────

async function main() {
  const monitoredChatIds = getMonitoredChatIds();

  if (monitoredChatIds.size === 0) {
    console.error('❌ 没有启用的监听群聊，请检查配置：' + CONFIG_PATH);
    process.exit(1);
  }

  console.log('┌─────────────────────────────────────────────┐');
  console.log('│       飞书实时监听机器人（WebSocket 模式）       │');
  console.log('└─────────────────────────────────────────────┘');
  console.log(`🤖 App ID：${APP_ID}`);
  console.log(`📋 监听群聊数：${monitoredChatIds.size}`);
  for (const chat of loadMonitoredChats()) {
    console.log(`   • ${chat.chat_name} (${chat.chat_id})`);
  }
  console.log(`🧠 AI 模型：${AI_MODEL}`);
  console.log(`📡 连接模式：WebSocket 长连接`);
  console.log('─────────────────────────────────────────────');

  // 初始化飞书 Client（用于发送消息）
  const client = new Lark.Client({
    appId: APP_ID,
    appSecret: APP_SECRET,
    appType: Lark.AppType.SelfBuild,
    domain: Lark.Domain.Feishu,
  });

  // 初始化 WebSocket Client（用于接收事件）
  const wsClient = new Lark.WSClient({
    appId: APP_ID,
    appSecret: APP_SECRET,
    loggerLevel: Lark.LoggerLevel.warn,
    autoReconnect: true,
    onReady: () => {
      console.log('✅ WebSocket 已连接，正在实时监听消息...\n');
    },
    onError: (err) => {
      console.error('❌ WebSocket 致命错误：', err.message);
    },
    onReconnecting: () => {
      console.log('⚠️  连接断开，正在重连...');
    },
    onReconnected: () => {
      console.log('✅ 重连成功');
    },
  });

  // 消息去重（防止重复处理）
  const processedMessages = new Set();
  const MAX_CACHE_SIZE = 1000;

  // 启动 WebSocket 监听
  wsClient.start({
    eventDispatcher: new Lark.EventDispatcher({}).register({
      'im.message.receive_v1': async (data) => {
        const messageId = data.message?.message_id;
        const chatId = data.message?.chat_id;

        // 去重
        if (messageId && processedMessages.has(messageId)) return;
        if (messageId) {
          processedMessages.add(messageId);
          if (processedMessages.size > MAX_CACHE_SIZE) {
            const arr = [...processedMessages];
            arr.slice(0, Math.floor(arr.length / 2)).forEach(id => processedMessages.delete(id));
          }
        }

        const { openId: senderOpenId, senderType } = getSenderInfo(data);

        // ① 只处理启用的群聊
        if (!monitoredChatIds.has(chatId)) return;

        // ② 排除机器人自己发的消息
        if (senderType === 'app') return;

        // ③ 只处理 @机器人 的消息
        if (!isAtBot(data, APP_ID)) return;

        const questionText = extractText(data);
        if (!questionText) return;

        // ④ 忽略指令类消息
        if (questionText.startsWith('/')) return;

        const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false });
        console.log(`[${timestamp}] 💬 收到 @消息：${questionText.slice(0, 60)}${questionText.length > 60 ? '...' : ''}`);

        // ⑤ 给消息贴表情，表示已收到
        try {
          const reactionRes = await client.request({
            method: 'POST',
            url: `https://open.feishu.cn/open-apis/im/v1/messages/${messageId}/reactions`,
            data: {
              reaction_type: {
                emoji_type: 'LOVE',
              },
            },
          });
          if (reactionRes.code === 0) {
            console.log(`  ✅ 已贴表情`);
          } else {
            console.log(`  ⚠️ 贴表情失败：code=${reactionRes.code}, msg=${reactionRes.msg}`);
          }
        } catch (e) {
          console.log(`  ⚠️ 贴表情异常：${e.message}`);
        }

        // ⑥ 调用 AI 生成回复
        const replyText = await generateReply(questionText, senderOpenId);

        // ⑦ 发送回复（基于原消息回复，@提问人）
        await sendReply(client, messageId, senderOpenId, replyText);
      },
    }),
  });

  // 支持热重载知识库：监听文件变化
  const watchFiles = ['README.md', 'Integration/unified-platform.md', 'Integration/integration-details.md'];
  for (const file of watchFiles) {
    const filePath = path.join(REPO_PATH, file);
    if (fs.existsSync(filePath)) {
      fs.watchFile(filePath, { interval: 5000 }, () => {
        console.log(`📄 检测到文档变更：${file}，重新加载知识库...`);
        knowledgeBase = loadKnowledgeBase();
      });
    }
  }

  // 定期刷新监听配置（每 60 秒检查一次配置变更）
  setInterval(() => {
    const newChatIds = getMonitoredChatIds();
    if (newChatIds.size !== monitoredChatIds.size) {
      console.log(`📋 监听配置已变更，重新加载（${newChatIds.size} 个群聊）`);
      monitoredChatIds.clear();
      for (const id of newChatIds) monitoredChatIds.add(id);
    }
  }, 60000);
}

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n🛑 收到停止信号，正在断开连接...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n🛑 收到终止信号，正在断开连接...');
  process.exit(0);
});

process.on('uncaughtException', (err) => {
  console.error('❌ 未捕获的异常：', err);
});

process.on('unhandledRejection', (reason) => {
  console.error('❌ 未处理的 Promise 拒绝：', reason);
});

main().catch(console.error);
