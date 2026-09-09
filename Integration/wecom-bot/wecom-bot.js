#!/usr/bin/env node
/**
 * 企微智能机器人 - WebSocket 长连接模式
 *
 * 功能：
 *   基于企微官方 SDK（@wecom/aibot-node-sdk）建立 WebSocket 长连接，
 *   监听 @机器人 或单聊消息，调用 Dify Chat API 生成回复（支持多轮对话 + 流式回复）。
 *
 * 优势（对比 Webhook 短连接）：
 *   - 无需公网 URL / 内网穿透
 *   - 无 5 秒响应超时限制
 *   - 架构与飞书 feishu-bot 完全对称
 *
 * 前置条件：
 *   1. 企微管理后台 → 应用管理 → 智能机器人 → 获取 botId 和 secret
 *   2. 编辑 .env 填入凭证
 *
 * 使用方式：
 *   npm install
 *   cp .env.example .env  (然后编辑填入真实值)
 *   node wecom-bot.js
 */

'use strict';

const { WSClient, generateReqId } = require('@wecom/aibot-node-sdk');
const fs = require('fs');
const path = require('path');

// ────────────────────────────────────────────────────────────────
// 配置（优先从 .env 读取）
// ────────────────────────────────────────────────────────────────

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
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    if (!process.env[key]) process.env[key] = val;
  }
}
loadEnv();

const BOT_ID = process.env.WECOM_BOT_ID || '';
const BOT_SECRET = process.env.WECOM_BOT_SECRET || '';
const DIFY_API_URL = process.env.DIFY_API_URL || 'http://10.232.5.5/v1';
const DIFY_API_KEY = process.env.DIFY_API_KEY || '';

// ────────────────────────────────────────────────────────────────
// 启动前校验
// ────────────────────────────────────────────────────────────────

if (!BOT_ID || !BOT_SECRET) {
  console.error('❌ 错误：WECOM_BOT_ID 或 WECOM_BOT_SECRET 未配置');
  console.error('   请在 .env 文件中设置（从企微管理后台获取）');
  process.exit(1);
}

if (!DIFY_API_KEY) {
  console.warn('⚠️  DIFY_API_KEY 未配置，将使用固定提示回复（无法生成智能回答）');
}

// ────────────────────────────────────────────────────────────────
// 消息去重（防止企微重复回调）
// ────────────────────────────────────────────────────────────────

const processedMessages = new Set();
const MAX_CACHE_SIZE = 1000;

// ────────────────────────────────────────────────────────────────
// 多轮对话管理（Dify conversation_id）
// ────────────────────────────────────────────────────────────────

const conversations = new Map(); // key: user_id, value: { conversation_id, last_active }
const CONVERSATION_TTL_MS = 30 * 60 * 1000; // 30 分钟无活动则重置会话

function getConversationId(userId) {
  if (!userId) return null;
  const entry = conversations.get(userId);
  if (!entry) return null;
  if (Date.now() - entry.last_active > CONVERSATION_TTL_MS) {
    conversations.delete(userId);
    return null;
  }
  return entry.conversation_id;
}

function setConversationId(userId, conversationId) {
  if (!userId || !conversationId) return;
  conversations.set(userId, {
    conversation_id: conversationId,
    last_active: Date.now(),
  });
}

// 每小时清理一次过期的会话记录，避免内存泄漏
setInterval(() => {
  const now = Date.now();
  let cleaned = 0;
  for (const [userId, entry] of conversations.entries()) {
    if (now - entry.last_active > CONVERSATION_TTL_MS) {
      conversations.delete(userId);
      cleaned++;
    }
  }
  if (cleaned > 0) {
    console.log(`🧹 已清理 ${cleaned} 条过期会话记录（剩余 ${conversations.size} 条）`);
  }
}, 60 * 60 * 1000);

// ────────────────────────────────────────────────────────────────
// Dify Chat API 调用（与飞书侧共用逻辑）
// ────────────────────────────────────────────────────────────────

async function callDify(question, userId) {
  if (!DIFY_API_KEY) {
    return `你好，Dify API 密钥未配置，暂时无法回答你的问题。请联系管理员配置 DIFY_API_KEY。`;
  }

  try {
    const conversation_id = getConversationId(userId);

    const requestBody = {
      inputs: {},
      query: question,
      response_mode: 'blocking',
      user: userId || 'default-user',
    };
    if (conversation_id) {
      requestBody.conversation_id = conversation_id;
    }

    console.log(`  🧠 调用 Dify API（${conversation_id ? '多轮' : '首轮'}，user=${userId}）...`);
    const startTime = Date.now();

    const response = await fetch(`${DIFY_API_URL}/chat-messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${DIFY_API_KEY}`,
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error(`❌ Dify API 错误 [${response.status}]：${errText}`);
      return `抱歉，AI 服务暂时不可用（错误码 ${response.status}），请稍后再试。`;
    }

    const data = await response.json();
    const cost = Date.now() - startTime;
    console.log(`  ✅ Dify 响应完成（${cost}ms）`);

    if (data.conversation_id) {
      setConversationId(userId, data.conversation_id);
    }

    return data.answer || '抱歉，我暂时无法回答这个问题。';
  } catch (e) {
    console.error(`❌ Dify 调用异常：${e.message}`);
    return `抱歉，处理你的问题时遇到了错误，请稍后再试。`;
  }
}

// ────────────────────────────────────────────────────────────────
// 主流程
// ────────────────────────────────────────────────────────────────

async function main() {
  console.log('┌─────────────────────────────────────────────┐');
  console.log('│     企微智能机器人（WebSocket 长连接模式）       │');
  console.log('└─────────────────────────────────────────────┘');
  console.log(`🤖 Bot ID：${BOT_ID}`);
  console.log(`🧠 Dify 端点：${DIFY_API_URL}`);
  console.log(`📡 连接模式：WebSocket 长连接（wss://openws.work.weixin.qq.com）`);
  console.log('─────────────────────────────────────────────');

  // 初始化企微 WSClient（官方 SDK，自动处理认证/心跳/断线重连）
  const wsClient = new WSClient({
    botId: BOT_ID,
    secret: BOT_SECRET,
  });

  // 监听连接事件
  wsClient.on('connected', () => {
    console.log('🔌 WebSocket 已连接');
  });

  wsClient.on('authenticated', () => {
    console.log('✅ 认证成功，正在实时监听消息...\n');
  });

  wsClient.on('disconnected', (reason) => {
    console.log(`⚠️  连接断开：${reason}`);
  });

  wsClient.on('reconnecting', (attempt) => {
    console.log(`🔄 正在重连（第 ${attempt} 次）...`);
  });

  wsClient.on('error', (err) => {
    console.error('❌ WebSocket 错误：', err?.message || err);
  });

  // ──────────────────────────────────────────────────────────────
  // 文本消息处理（核心逻辑）
  // ──────────────────────────────────────────────────────────────
  wsClient.on('message.text', async (frame) => {
    const body = frame.body;
    const question = (body.text?.content || '').trim();
    const userId = body.from?.userid || 'unknown';
    const chatType = body.chattype || 'unknown';
    const chatId = body.chatid || '(单聊)';
    const msgId = body.msgid;

    if (!question) return;
    // 忽略指令类消息
    if (question.startsWith('/')) return;

    // 消息去重（企微可能重复回调）
    if (processedMessages.has(msgId)) {
      console.log(`  ⏭️  重复消息，跳过：${msgId}`);
      return;
    }
    processedMessages.add(msgId);
    if (processedMessages.size > MAX_CACHE_SIZE) {
      const arr = [...processedMessages];
      arr.slice(0, Math.floor(arr.length / 2)).forEach(id => processedMessages.delete(id));
    }

    const timestamp = new Date().toLocaleTimeString('zh-CN', { hour12: false });
    const preview = question.length > 60 ? question.slice(0, 60) + '...' : question;
    console.log(`[${timestamp}] 💬 收到 ${chatType} 消息 from ${userId} (${chatId})：${preview}`);

    // ① 先发流式"思考中"占位
    const streamId = generateReqId('stream');
    try {
      await wsClient.replyStream(frame, streamId, '🤔 思考中...', false);
    } catch (e) {
      console.log(`  ⚠️  "思考中"占位发送失败：${e.message}`);
    }

    // ② 调用 Dify 生成回复
    const replyText = await callDify(question, userId);

    // ③ 用流式回复发送最终答案（finish=true 结束流）
    try {
      await wsClient.replyStream(frame, streamId, replyText, true);
      console.log(`  ✅ 回复已发送（${replyText.length} 字符）`);
    } catch (e) {
      console.error(`  ❌ 回复发送失败：${e.message}`);
    }
  });

  // ──────────────────────────────────────────────────────────────
  // 其他消息类型（仅记录，暂不处理）
  // ──────────────────────────────────────────────────────────────
  const ignoredTypes = ['image', 'mixed', 'voice', 'file', 'video'];
  for (const type of ignoredTypes) {
    wsClient.on(`message.${type}`, (frame) => {
      const userId = frame.body?.from?.userid || 'unknown';
      console.log(`ℹ️  收到 ${type} 消息 from ${userId}（暂不支持，忽略）`);
    });
  }

  // ──────────────────────────────────────────────────────────────
  // 进入会话事件（发送欢迎语）
  // ──────────────────────────────────────────────────────────────
  wsClient.on('event.enter_chat', (frame) => {
    const userId = frame.body?.from?.userid || 'unknown';
    console.log(`👋 用户 ${userId} 进入会话，发送欢迎语`);
    try {
      wsClient.replyWelcome(frame, {
        msgtype: 'text',
        text: { content: '您好！我是智能助手，@我或私聊我提问即可，我会基于项目文档回答您的问题。' },
      });
    } catch (e) {
      console.error(`  ❌ 欢迎语发送失败：${e.message}`);
    }
  });

  // ──────────────────────────────────────────────────────────────
  // 启动连接
  // ──────────────────────────────────────────────────────────────
  wsClient.connect();
}

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n🛑 收到停止信号');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n🛑 收到终止信号');
  process.exit(0);
});

process.on('uncaughtException', (err) => {
  console.error('❌ 未捕获的异常：', err);
});

process.on('unhandledRejection', (reason) => {
  console.error('❌ 未处理的 Promise 拒绝：', reason);
});

main().catch(console.error);
