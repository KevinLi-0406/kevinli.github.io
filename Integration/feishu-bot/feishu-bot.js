#!/usr/bin/env node
/**
 * 飞书实时监听机器人 - WebSocket 长连接模式
 *
 * 功能：
 *   1. 实时监听指定群聊中 @机器人 的消息，基于本地文档知识库调用 AI 生成回复
 *   2. 邮件操作：当授权用户 @机器人 请求查邮件/发邮件时，通过 IMAP/SMTP 执行
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

// 邮件配置（IMAP/SMTP）
const EMAIL_IMAP_HOST = process.env.IMAP_HOST || '';
const EMAIL_IMAP_PORT = Number(process.env.IMAP_PORT) || 993;
const EMAIL_SMTP_HOST = process.env.SMTP_HOST || '';
const EMAIL_SMTP_PORT = Number(process.env.SMTP_PORT) || 994;
const EMAIL_USER = process.env.EMAIL_USER || '';
const EMAIL_PASS = process.env.EMAIL_PASS || '';
// 允许执行邮件操作的飞书用户 open_id（逗号分隔）
const EMAIL_AUTHORIZED_IDS = (process.env.EMAIL_AUTHORIZED_OPEN_IDS || '')
  .split(',')
  .map(s => s.trim())
  .filter(Boolean);

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

if (!EMAIL_USER || !EMAIL_PASS) {
  console.warn('⚠️  EMAIL_USER/EMAIL_PASS 未配置，邮件功能不可用');
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
// 邮件操作（IMAP/SMTP）
// ────────────────────────────────────────────────────────────────

function createImapClient() {
  const { ImapFlow } = require('imapflow');
  if (!EMAIL_IMAP_HOST || !EMAIL_USER || !EMAIL_PASS) {
    throw new Error('邮件未配置：请设置 IMAP_HOST, EMAIL_USER, EMAIL_PASS');
  }
  return new ImapFlow({
    host: EMAIL_IMAP_HOST,
    port: EMAIL_IMAP_PORT,
    secure: true,
    auth: { user: EMAIL_USER, pass: EMAIL_PASS },
    tls: { rejectUnauthorized: false },
    logger: false,
  });
}

function createSmtpTransport() {
  const nodemailer = require('nodemailer');
  if (!EMAIL_SMTP_HOST || !EMAIL_USER || !EMAIL_PASS) {
    throw new Error('邮件未配置：请设置 SMTP_HOST, EMAIL_USER, EMAIL_PASS');
  }
  return nodemailer.createTransport({
    host: EMAIL_SMTP_HOST,
    port: EMAIL_SMTP_PORT,
    secure: true,
    auth: { user: EMAIL_USER, pass: EMAIL_PASS },
    tls: { rejectUnauthorized: false },
  });
}

/** 提取邮件纯文本正文（简易 RFC822 解析） */
function extractEmailBody(source) {
  if (!source) return '（无法提取正文）';
  const raw = typeof source === 'string' ? source : source.toString('utf-8');
  const headerEnd = raw.indexOf('\r\n\r\n');
  if (headerEnd === -1) return raw.slice(0, 3000);
  return raw.slice(headerEnd + 4, headerEnd + 4 + 5000);
}

/** 列出最近 N 封邮件 */
async function emailListRecent(count = 10) {
  const client = createImapClient();
  try {
    await client.connect();
    const lock = await client.getMailboxLock('INBOX');
    try {
      const total = client.mailbox.exists || 0;
      const start = Math.max(1, total - count + 1);
      const emails = [];
      for await (const msg of client.fetch(`${start}:*`, { envelope: true, uid: true, flags: true })) {
        const e = msg.envelope || {};
        emails.push({
          uid: msg.uid,
          seq: msg.seq,
          subject: e.subject || '（无主题）',
          from: e.from?.[0] ? `${e.from[0].name || ''} <${e.from[0].address || ''}>` : '',
          date: e.date ? new Date(e.date).toLocaleString('zh-CN') : '',
          read: msg.flags.has('\\Seen'),
        });
      }
      return { total, emails: emails.reverse() };
    } finally { lock.release(); }
  } finally { await client.logout().catch(() => {}); }
}

/** 读取指定邮件全文 */
async function emailRead(uid) {
  const client = createImapClient();
  try {
    await client.connect();
    const lock = await client.getMailboxLock('INBOX');
    try {
      const msg = await client.fetchOne(String(uid), { envelope: true, source: true, flags: true });
      if (!msg) throw new Error(`未找到 UID ${uid} 的邮件`);
      const e = msg.envelope || {};
      return {
        uid: msg.uid,
        subject: e.subject || '（无主题）',
        from: e.from?.[0] ? `${e.from[0].name || ''} <${e.from[0].address || ''}>` : '',
        to: (e.to || []).map(a => `${a.name || ''} <${a.address || ''}>`).join(', '),
        cc: (e.cc || []).map(a => `${a.name || ''} <${a.address || ''}>`).join(', '),
        date: e.date ? new Date(e.date).toLocaleString('zh-CN') : '',
        body: extractEmailBody(msg.source),
        read: msg.flags.has('\\Seen'),
      };
    } finally { lock.release(); }
  } finally { await client.logout().catch(() => {}); }
}

/** 搜索邮件 */
async function emailSearch(query, queryType = 'all') {
  const client = createImapClient();
  try {
    await client.connect();
    const lock = await client.getMailboxLock('INBOX');
    try {
      let criteria;
      switch (queryType) {
        case 'subject': criteria = { header: { subject: query } }; break;
        case 'from':    criteria = { from: query }; break;
        case 'to':      criteria = { to: query }; break;
        case 'unread':  criteria = { seen: false }; break;
        case 'since':   criteria = { since: new Date(query) }; break;
        default:        criteria = {};
      }
      const range = await client.search(criteria, { uid: true });
      if (!range || !range.length) return { count: 0, emails: [] };

      const emails = [];
      for await (const msg of client.fetch(range.slice(-50).join(','), { envelope: true, uid: true, flags: true })) {
        const e = msg.envelope || {};
        emails.push({
          uid: msg.uid,
          subject: e.subject || '（无主题）',
          from: e.from?.[0]?.address || '',
          date: e.date ? new Date(e.date).toLocaleString('zh-CN') : '',
          read: msg.flags.has('\\Seen'),
        });
      }
      return { count: emails.length, emails: emails.reverse() };
    } finally { lock.release(); }
  } finally { await client.logout().catch(() => {}); }
}

/** 发送邮件 */
async function emailSend(to, subject, body) {
  const transport = createSmtpTransport();
  const result = await transport.sendMail({
    from: EMAIL_USER, to, subject, text: body,
  });
  return { success: true, message_id: result.messageId };
}

/** 列出文件夹 */
async function emailListFolders() {
  const client = createImapClient();
  try {
    await client.connect();
    const tree = await client.list();
    return tree.map(f => ({
      name: f.name,
      path: f.path,
      messages: f.status?.messages ?? null,
      unseen: f.status?.unseen ?? null,
    }));
  } finally { await client.logout().catch(() => {}); }
}

/** 检测消息是否为邮件操作请求 */
function detectEmailRequest(text) {
  const lower = text.toLowerCase();

  // 查邮件/最新邮件/收件箱
  if (/(?:查看|查一下|看看|帮我查|列出|最近|最新|收件箱).{0,4}(?:邮件|email|信)/.test(lower)
      || /(?:邮件|email).{0,4}(?:列表|清单|汇总|有哪些|有什么)/.test(lower)) {
    return { operation: 'list' };
  }

  // 搜索邮件
  if (/(?:搜索|查找|找一下|搜一下|有没有|帮我找).{0,8}(?:邮件|email|信)/.test(lower)) {
    return { operation: 'search' };
  }

  // 读邮件（序号或UID）
  const numMatch = text.match(/(?:第|看|读|打开)\s*(\d+)\s*(?:封|个|条|邮件)/);
  if (numMatch) {
    return { operation: 'read', param: parseInt(numMatch[1]) };
  }
  const uidMatch = text.match(/(?:UID|uid)\s*(\d+)/);
  if (uidMatch) {
    return { operation: 'read', param: parseInt(uidMatch[1]), isUid: true };
  }

  // 发邮件
  if (/(?:发送?|发一?封|写一?封|回复).{0,4}(?:邮件|email|信)/.test(lower)
      || /(?:发邮件|发信|写邮件)/.test(lower)) {
    return { operation: 'send' };
  }

  // 文件夹
  if (/(?:文件夹|目录|folder)/.test(lower)) {
    return { operation: 'folders' };
  }

  return null;
}

/** 处理邮件操作请求 */
async function handleEmailRequest(client, messageId, senderOpenId, text) {
  // 权限检查
  if (EMAIL_AUTHORIZED_IDS.length > 0 && !EMAIL_AUTHORIZED_IDS.includes(senderOpenId)) {
    await sendText(client, null, '⚠️ 你没有权限使用邮件功能。', messageId);
    return;
  }

  const detected = detectEmailRequest(text);
  const operation = detected?.operation || 'list';

  try {
    let replyText = '';

    switch (operation) {
      case 'list': {
        const count = (text.match(/(\d+)/) || [, '10'])[1];
        const result = await emailListRecent(Math.min(parseInt(count) || 10, 30));
        const lines = [`📬 收件箱（共 ${result.total} 封，显示最近 ${result.emails.length} 封）：\n`];
        result.emails.forEach((e, i) => {
          const icon = e.read ? '📭' : '📩';
          lines.push(`${icon} ${i + 1}. [${e.read ? '已读' : '未读'}] ${e.subject}`);
          lines.push(`   From: ${e.from}  ${e.date}`);
        });
        lines.push('\n💡 输入「帮我读第N封邮件」查看内容');
        replyText = lines.join('\n');
        break;
      }

      case 'search': {
        const query = text.replace(/(?:搜索|查找|找一下|搜一下|帮我找|邮件|email|信)/g, '').trim();
        if (!query) {
          replyText = '请提供搜索关键词，例如「搜索来自 xxx 的邮件」';
          break;
        }
        let queryType = 'subject';
        if (/\d{4}-\d{2}-\d{2}/.test(query)) queryType = 'since';
        else if (/@/.test(query)) queryType = 'from';
        const result = await emailSearch(query, queryType);
        if (result.count === 0) {
          replyText = `🔍 未找到匹配「${query}」的邮件`;
        } else {
          const lines = [`🔍 找到 ${result.count} 封匹配「${query}」的邮件：\n`];
          result.emails.slice(0, 15).forEach((e, i) => {
            lines.push(`${i + 1}. [${e.read ? '已读' : '未读'}] ${e.subject}`);
            lines.push(`   From: ${e.from}  ${e.date}`);
          });
          replyText = lines.join('\n');
        }
        break;
      }

      case 'read': {
        const num = detected.param;
        let targetUid;
        if (detected.isUid) {
          targetUid = num;
        } else {
          const recent = await emailListRecent(Math.max(num, 10));
          const target = recent.emails[num - 1];
          if (!target) {
            replyText = `第 ${num} 封邮件不在最近列表中（共 ${recent.emails.length} 封）`;
            break;
          }
          targetUid = target.uid;
        }
        const email = await emailRead(targetUid);
        const bodyPreview = email.body.slice(0, 2000);
        replyText = [
          `📧 ${email.subject}`,
          `From: ${email.from}`,
          `To: ${email.to}`,
          email.cc ? `Cc: ${email.cc}` : '',
          `Date: ${email.date}`,
          `\n--- 正文 ---\n${bodyPreview}${email.body.length > 2000 ? '\n...(正文已截断)' : ''}`,
        ].filter(Boolean).join('\n');
        break;
      }

      case 'send': {
        const toMatch = text.match(/[\w.+-]+@[\w-]+\.[\w.-]+/);
        const subjectMatch = text.match(/(?:主题|标题)[：:]\s*(.+?)(?:\n|$)/);
        const bodyMatch = text.match(/(?:正文|内容)[：:]\s*([\s\S]+)$/);
        if (!toMatch) {
          replyText = '请提供收件人邮箱地址，例如「发邮件给 xxx@xxx.com 主题：测试 正文：你好」';
        } else {
          const to = toMatch[0];
          const subject = subjectMatch?.[1]?.trim() || '来自飞书助手';
          const body = bodyMatch?.[1]?.trim() || '';
          if (!body) {
            replyText = `请提供邮件正文，例如「发邮件给 ${to} 主题：${subject} 正文：你的内容」`;
          } else {
            await emailSend(to, subject, body);
            replyText = `✅ 邮件已发送\n收件人：${to}\n主题：${subject}`;
          }
        }
        break;
      }

      case 'folders': {
        const folders = await emailListFolders();
        const lines = [`📁 邮箱文件夹（共 ${folders.length} 个）：\n`];
        folders.forEach(f => {
          const icon = f.path === 'INBOX' ? '📥' : f.unseen > 0 ? '🔔' : '📁';
          const counts = f.messages !== null ? `（${f.messages} 封，未读 ${f.unseen || 0}）` : '';
          lines.push(`${icon} ${f.name}${counts}`);
        });
        replyText = lines.join('\n');
        break;
      }
    }

    await sendReply(client, messageId, senderOpenId, replyText);
  } catch (err) {
    console.error(`  ❌ 邮件操作异常：${err.message}`);
    await sendReply(client, messageId, senderOpenId, `❌ 邮件操作失败：${err.message}`);
  }
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
async function sendText(client, chatId, text, replyMessageId) {
  try {
    if (replyMessageId) {
      // 如果有原消息ID，使用回复方式
      await client.im.v1.message.reply({
        path: { message_id: replyMessageId },
        data: {
          content: JSON.stringify({ text }),
          msg_type: 'text',
        },
      });
    } else {
      await client.im.v1.message.create({
        params: { receive_id_type: 'chat_id' },
        data: {
          receive_id: chatId,
          content: JSON.stringify({ text }),
          msg_type: 'text',
        },
      });
    }
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
  console.log(`📧 邮件功能：${EMAIL_USER ? '已配置 (' + EMAIL_USER + ')' : '未配置'}`);
  console.log(`🔐 邮件授权用户：${EMAIL_AUTHORIZED_IDS.length ? EMAIL_AUTHORIZED_IDS.join(', ') : '（未限制）'}`);
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

        // ⑥ 检测是否为邮件操作请求
        const emailRequest = detectEmailRequest(questionText);
        if (emailRequest) {
          console.log(`  📧 识别为邮件操作：${emailRequest.operation}`);
          await handleEmailRequest(client, messageId, senderOpenId, questionText);
          return;
        }

        // ⑦ 调用 AI 生成回复
        const replyText = await generateReply(questionText, senderOpenId);

        // ⑧ 发送回复（基于原消息回复，@提问人）
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
