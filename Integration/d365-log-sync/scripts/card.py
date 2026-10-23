# -*- coding: utf-8 -*-
"""D365 日志同步 - 告警卡片构造（Card 2.0 中文版，基于真实成功格式）"""
import sys, os, io, json, argparse, subprocess
from datetime import datetime, timedelta, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OWNER_GONG, BASE_URL, GROUP_CHAT, BASE_TOKEN, SITE_OPS_TABLE
from config_loader import load_card_configs, get_card_config

WO_URL_TPL = "https://eusegwayspp.crm4.dynamics.com/main.aspx?appid=296808a8-ebd5-f011-8543-000d3adcfa64&newWindow=true&pagetype=entityrecord&etn=new_workorder&id={woid}"


def _red(text):
    return "<font color=red>{}</font>".format(text)


def _load_site_ops_mapping():
    """从迈创站点运营表加载 Service Store Name -> 飞书用户 ID 的映射"""
    mapping = {}
    offset = 0
    try:
        while True:
            cmd = ['lark-cli', 'base', '+record-list', '--base-token', BASE_TOKEN,
                   '--table-id', SITE_OPS_TABLE,
                   '--page-size', '200', '--offset', str(offset), '--format', 'json', '--as', 'bot']
            r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            out = r.stdout.strip()
            if not out:
                break
            d = json.loads(out)
            data = d.get('data', {})
            rows = data.get('data', []) or []
            if not rows:
                break
            for row in rows:
                try:
                    # row 格式: [国家，负责人，ASP, 备注，Email, Service Store Name, 负责人 (user), 飞书用户 ID (user)]
                    store_name = row[5] if len(row) > 5 and row[5] else ''
                    # 使用"负责人"字段（索引 6）
                    user_ids = row[6] if len(row) > 6 and row[6] else []
                    if store_name and user_ids:
                        # user_ids 是数组，每个元素是 {"id": "ou_xxx", "name": "xxx"}
                        if isinstance(user_ids, list):
                            mapping[store_name] = [u.get('id', '') for u in user_ids if isinstance(u, dict)]
                except Exception:
                    continue
            if data.get('has_more', False):
                offset += len(rows)
            else:
                break
    except Exception:
        pass
    return mapping


def _material_table(meta):
    rows = meta.get('material_list', [])
    over = set(meta.get('other_desc_set', []))
    lines = ["| 序号 | 物料号 | 数量 |", "| --- | --- | --- |"]
    for m in rows:
        mac = m.get('applyMacId') or ''
        cell = _red(mac) if mac in over else mac
        lines.append("| {} | {} | {} |".format(m.get('Index', ''), cell, m.get('quantity', '')))
    return "\n".join(lines)


def build_panel(meta, card_config=None, site_ops_mapping=None):
    wo = meta.get('wo', '')
    wo_link = meta.get('_wo_link', '')
    abnormal = meta.get('abnormal', '')
    created = meta.get('created_bj', '')
    status = meta.get('status', '')
    goodsid = meta.get('goodsId', '')
    err = meta.get('err_text', '')
    b2x = meta.get('b2x', '')
    service_type = meta.get('service_type', '')
    wo_source = meta.get('wo_source', '')
    service_store_name = meta.get('service_store_name', '')

    wo_text = "[{}]({})".format(wo, wo_link) if wo_link else wo

    # 从配置读取艾特逻辑
    if card_config is None:
        card_config = get_card_config(abnormal)

    # 迈创场景：根据 Service Store Name 查找对应的负责人并艾特
    at_text = ""
    if card_config.get('at_user', False):
        if site_ops_mapping and service_store_name and service_store_name in site_ops_mapping:
            user_ids = site_ops_mapping[service_store_name]
            if user_ids:
                at_text = " " + " ".join(["<at id={}></at>".format(uid) for uid in user_ids])
        elif OWNER_GONG:
            # 兜底：艾特贡梦夏
            at_text = " <at id={}></at>".format(OWNER_GONG)

    # B2X单号 / 工单来源 条件显示
    if b2x:
        b2x_label, b2x_value = "B2X单号", b2x
    else:
        b2x_label, b2x_value = "工单来源", wo_source

    # 整车物料号 / Service Type 条件显示
    err_match = 'The spare part category and repair method do not match'
    if err_match in (err or ''):
        goods_label, goods_value = "Service Type", service_type
    else:
        goods_label, goods_value = "整车物料号", goodsid

    panel_elements = [
        {
            "tag": "div",
            "margin": "0px 0px 12px 0px",
            "fields": [
                {"is_short": True, "text": {"tag": "lark_md", "content": "**工单号**\n{}".format(wo_text)}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**{}**\n{}".format(b2x_label, b2x_value)}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**异常场景**\n{}".format(_red(abnormal))}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**创建时间**\n{} (UTC+0)".format(created)}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**类型**\n{}".format(status)}},
                {"is_short": True, "text": {"tag": "lark_md", "content": "**{}**\n{}".format(goods_label, goods_value)}},
            ]
        }
    ]

    if err:
        panel_elements.append({
            "tag": "markdown",
            "margin": "0px 0px 12px 0px",
            "content": "**报错信息**\n{}".format(err)
        })

    part_count = len(meta.get('material_list', []))
    panel_elements.append({
        "tag": "markdown",
        "content": "**备件申请列表**（{} 项）\n{}".format(part_count, _material_table(meta))
    })

    return {
        "tag": "collapsible_panel",
        "expanded": False,
        "padding": "0px",
        "margin": "0px 0px 12px 0px",
        "header": {
            "title": {
                "tag": "markdown",
                "content": "▸ **{}** · {}{} <font color=grey>点击展开</font>".format(wo, abnormal, at_text)
            }
        },
        "elements": panel_elements,
    }


def _header(card_config=None):
    if card_config is None:
        card_config = {'title': 'D365 集成报错告警', 'subtitle_template': '{scenario}', 'color': 'red'}
    return {
        "title": {"tag": "plain_text", "content": card_config.get('title', 'D365 集成报错告警')},
        "subtitle": {"tag": "plain_text", "content": card_config.get('subtitle_template', '{scenario}')},
        "template": card_config.get('color', 'red'),
    }


def _meta_div(run_info):
    return {
        "tag": "div",
        "margin": "0px 0px 12px 0px",
        "fields": [
            {"is_short": True, "text": {"tag": "lark_md", "content": "**本次运行**\n{}".format(run_info.get('now', ''))}},
            {"is_short": True, "text": {"tag": "lark_md", "content": "**下次运行**\n{}".format(run_info.get('next', ''))}},
            {"is_short": False, "text": {"tag": "lark_md", "content": "**数据来源范围**\n{}".format(run_info.get('range', ''))}},
        ],
    }


def _footer():
    return {
        "tag": "markdown",
        "content": "完整字段请查看[多维表格「D365 接口日志」]({})。".format(BASE_URL),
        "text_size": "notation",
    }


def build_card(metas, run_info, total_count=None, card_config=None, site_ops_mapping=None):
    # 所有迈创场景合并为一张卡片，@mention 在各自 panel 内
    total = total_count if total_count is not None else len(metas)
    if total > len(metas):
        summary = "本次新增 **{}** 条告警记录，此处展示前 **{}** 条，<font color=red> 点击工单标题可展开</font>详情与备件。".format(total, len(metas))
    else:
        summary = "本次新增 **{}** 条告警记录，<font color=red>▸ 点击工单标题可展开</font>详情与备件。".format(total)

    # 获取第一个记录的异常场景配置（用于 header）
    first_abnormal = metas[0].get('abnormal', '') if metas else ''
    if card_config is None:
        header_config = get_card_config(first_abnormal)
    else:
        header_config = card_config

    elements = [
        _meta_div(run_info),
        {"tag": "markdown", "content": summary}
    ]
    for m in metas:
        abnormal = m.get('abnormal', '')
        panel_config = get_card_config(abnormal)
        elements.append(build_panel(m, panel_config, site_ops_mapping))
    elements.append(_footer())

    # 更新 header 副标题
    subtitle = header_config.get('subtitle_template', '{scenario} · 迈创').format(scenario=first_abnormal)
    header = _header(header_config)
    header['subtitle']['content'] = subtitle

    return {
        "schema": "2.0",
        "config": {"update_multi": True, "width_mode": "default"},
        "header": header,
        "body": {
            "direction": "vertical",
            "padding": "12px 12px 20px 12px",
            "vertical_spacing": "12px",
            "elements": elements,
        },
    }


def split_metas(metas, max_display=5):
    """只返回前 max_display 条作为单组，其余截断。"""
    return [metas[:max_display]] if metas else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('meta_json')
    ap.add_argument('--out', default='.')
    ap.add_argument('--now', default='', help='本次运行时间，默认自动取当前时间')
    ap.add_argument('--next', default='', help='下次运行时间，默认自动取当前+1h整点')
    ap.add_argument('--range', default='', help='数据来源范围，默认近7天')
    args = ap.parse_args()

    # 从配置表读取所有场景配置
    configs = load_card_configs()

    metas = json.load(open(args.meta_json, encoding='utf-8'))

    # 按异常场景分组，只处理启用的场景
    grouped_by_abnormal = {}
    for m in metas:
        abnormal = m.get('abnormal', '')
        if abnormal in configs and configs[abnormal].get('enabled', True):
            if abnormal not in grouped_by_abnormal:
                grouped_by_abnormal[abnormal] = []
            grouped_by_abnormal[abnormal].append(m)

    if not grouped_by_abnormal:
        print('NO_ALERT')
        return

    # 按聚合组代码重新分组
    grouped_by_agg = {}
    agg_config_map = {}  # 记录每个聚合组的配置（以第一个场景的配置为准）

    for abnormal, scene_metas in grouped_by_abnormal.items():
        card_config = get_card_config(abnormal)
        agg_group = card_config.get('agg_group', 'GROUP_OTHER')

        if agg_group not in grouped_by_agg:
            grouped_by_agg[agg_group] = []
            agg_config_map[agg_group] = card_config

        grouped_by_agg[agg_group].extend(scene_metas)

    # 为每个聚合组生成卡片
    all_cards = []
    for agg_group, agg_metas in grouped_by_agg.items():
        card_config = agg_config_map[agg_group]
        agg_subtitle = card_config.get('agg_subtitle', '{scenario}')

        # 设置工单链接
        for m in agg_metas:
            wo_id = m.get('_wo_id', '')
            m['_wo_link'] = WO_URL_TPL.format(woid=wo_id) if wo_id else ''

        # 自动计算时间
        tz_bj = timezone(timedelta(hours=8))
        now_dt = datetime.now(tz_bj)
        now_str = args.now if args.now else now_dt.strftime('%Y-%m-%d %H:%M:%S (UTC+8)')
        next_dt = (now_dt + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        next_str = args.next if args.next else next_dt.strftime('%Y-%m-%d %H:%M:%S (UTC+8)')
        data_range_days = card_config.get('data_range_days', 7)
        range_start = (now_dt - timedelta(days=data_range_days)).strftime('%Y-%m-%d')
        range_end = now_dt.strftime('%Y-%m-%d')
        range_str = args.range if args.range else '{} ~ {} (近{}天)'.format(range_start, range_end, data_range_days)

        run_info = {'now': now_str, 'next': next_str, 'range': range_str}
        max_per_card = card_config.get('max_per_card', 5)
        total_count = len(agg_metas)
        groups = split_metas(agg_metas, max_display=max_per_card)

        for g in groups:
            # 使用聚合后的副标题
            agg_card_config = card_config.copy()
            agg_card_config['subtitle_template'] = agg_subtitle
            # 加载迈创站点运营表映射（用于艾特负责人）
            site_ops_mapping = _load_site_ops_mapping()
            card = build_card(g, run_info, total_count=total_count, card_config=agg_card_config, site_ops_mapping=site_ops_mapping)
            all_cards.append({
                'card': card,
                'config': card_config
            })

    # 输出卡片
    outdir = args.out
    os.makedirs(outdir, exist_ok=True)
    for i, item in enumerate(all_cards):
        card = item['card']
        config = item['config']
        p = os.path.join(outdir, 'card_{}.json'.format(i))
        with open(p, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(card, f, ensure_ascii=False)
        card_size = len(json.dumps(card, ensure_ascii=False).encode('utf-8'))
        panel_count = len(card['body']['elements']) - 3

        # 确定发送目标
        send_target = ''
        if config.get('send_user_id'):
            send_target = '私聊:{}'.format(config.get('send_user_id', ''))
        elif config.get('chat_id') and config.get('chat_id') != GROUP_CHAT:
            send_target = '群聊:{}'.format(config.get('chat_id', ''))
        else:
            send_target = '群聊:{}'.format(GROUP_CHAT)

        print('card_{}: {} bytes, panels={}, send_to={}'.format(
            i, card_size, panel_count, send_target))
    print('Total cards: {}'.format(len(all_cards)))


if __name__ == '__main__':
    main()
