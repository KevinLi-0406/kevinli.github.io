# -*- coding: utf-8 -*-
"""D365 日志同步 - 统一配置加载器
从多维表格读取所有配置化参数，包含本地兜底值防止拉取失败。
"""
import sys, os, io, json, subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (BASE_TOKEN, CARD_CONFIG_TABLE, CARD_CONFIG_TABLE_NON_MAITUO,
                    ALERT_RULES_TABLE, OWNER_GONG, GROUP_CHAT)


# ---- 本地兜底配置（防止多维表格拉取失败）----
DEFAULT_CARD_CONFIGS = {
    'Maitrox-数据问题-out of SBOM': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'red',
        'at_user': True,
        'at_user_id': OWNER_GONG,
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_DATA',
        'agg_subtitle': 'Maitrox-数据问题',
    },
    'Maitrox-数据问题-主数据缺失': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'red',
        'at_user': True,
        'at_user_id': OWNER_GONG,
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_DATA',
        'agg_subtitle': 'Maitrox-数据问题',
    },
    'Maitrox-数据问题-扣账失败': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'orange',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_INTERFACE',
        'agg_subtitle': 'Maitrox-接口问题',
    },
    'Maitrox-接口问题-其他': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'red',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_INTERFACE',
        'agg_subtitle': 'Maitrox-接口问题',
    },
    'Maitrox-接口问题-处理异常': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'orange',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_INTERFACE',
        'agg_subtitle': 'Maitrox-接口问题',
    },
    'Maitrox-接口问题-备件工单不匹配': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'yellow',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_INTERFACE',
        'agg_subtitle': 'Maitrox-接口问题',
    },
    'Maitrox-接口问题-验证失败': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'yellow',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_INTERFACE',
        'agg_subtitle': 'Maitrox-接口问题',
    },
    'Maitrox-接口问题': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'grey',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_OTHER',
        'agg_subtitle': 'Maitrox-接口问题',
    },
    'B2X-接口问题-必填为空': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'yellow',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_B2X',
        'agg_subtitle': 'B2X-接口问题',
    },
    'B2X-接口问题-状态': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'orange',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_B2X',
        'agg_subtitle': 'B2X-接口问题',
    },
    'B2X-接口问题-数据': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'orange',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_B2X',
        'agg_subtitle': 'B2X-接口问题',
    },
    'B2X-接口问题-工单重复': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'yellow',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_B2X',
        'agg_subtitle': 'B2X-接口问题',
    },
    'MySav-接口问题-必填为空': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'yellow',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_MYSAV',
        'agg_subtitle': 'MySav-接口问题',
    },
    'MySav-接口问题-状态': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'orange',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_MYSAV',
        'agg_subtitle': 'MySav-接口问题',
    },
    'MySav-接口问题-工单重复': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'yellow',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_MYSAV',
        'agg_subtitle': 'MySav-接口问题',
    },
    'B2X-接口问题': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'grey',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_B2X',
        'agg_subtitle': 'B2X-接口问题',
    },
    'MySav-接口问题': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'grey',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_MYSAV',
        'agg_subtitle': 'MySav-接口问题',
    },
    '通用': {
        'title': 'D365 集成报错告警',
        'subtitle_template': '{scenario}',
        'color': 'blue',
        'at_user': False,
        'at_user_id': '',
        'send_user_id': '',
        'chat_id': GROUP_CHAT,
        'max_per_card': 5,
        'data_range_days': 7,
        'agg_group': 'GROUP_OTHER',
        'agg_subtitle': '{scenario}',
    },
}


def load_card_configs():
    """从「告警卡片配置 - 迈创」和「告警卡片配置 - 非迈创」表加载所有场景的卡片配置。
    返回: dict of abnormal_scenario -> config_dict
    拉取失败返回本地兜底值。
    """
    configs = DEFAULT_CARD_CONFIGS.copy()

    # 读取两个配置表
    for table_id in [CARD_CONFIG_TABLE, CARD_CONFIG_TABLE_NON_MAITUO]:
        offset = 0
        try:
            while True:
                cmd = ['lark-cli', 'base', '+record-list', '--base-token', BASE_TOKEN,
                       '--table-id', table_id,
                       '--field', '异常场景',
                       '--field', '是否启用',
                       '--field', '卡片标题',
                       '--field', '卡片副标题模板',
                       '--field', '卡片颜色',
                       '--field', '是否艾特',
                       '--field', '艾特用户',
                       '--field', '发送用户',
                       '--field', '发送群组',
                       '--field', '最大展示条数',
                       '--field', '数据来源范围天数',
                       '--field', '聚合组代码',
                       '--field', '聚合后副标题',
                       '--page-size', '200', '--offset', str(offset), '--format', 'json', '--as', 'bot']
                r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                out = r.stdout.strip()
                if not out:
                    break
                d = json.loads(out)
                data = d.get('data', {})
                rows = data.get('data', []) or []
                field_ids = data.get('field_id_list', []) or []
                if not rows:
                    break

                # 建立字段名到索引的映射
                field_name_to_idx = {}
                field_names = ['异常场景', '是否启用', '卡片标题', '卡片副标题模板', '卡片颜色',
                               '是否艾特', '艾特用户', '发送用户', '发送群组', '最大展示条数',
                               '数据来源范围天数', '聚合组代码', '聚合后副标题']
                for i, fname in enumerate(field_names):
                    if i < len(field_ids):
                        field_name_to_idx[fname] = i

                for row in rows:
                    try:
                        # 使用字段名获取值
                        abnormal_list = row[field_name_to_idx.get('异常场景', 0)] if '异常场景' in field_name_to_idx else []
                        abnormal = abnormal_list[0] if abnormal_list else '通用'

                        enabled = row[field_name_to_idx.get('是否启用', 1)] if '是否启用' in field_name_to_idx else True
                        title = row[field_name_to_idx.get('卡片标题', 2)] if '卡片标题' in field_name_to_idx else 'D365 集成报错告警'
                        subtitle = row[field_name_to_idx.get('卡片副标题模板', 3)] if '卡片副标题模板' in field_name_to_idx else '{scenario}'
                        color_list = row[field_name_to_idx.get('卡片颜色', 4)] if '卡片颜色' in field_name_to_idx else ['blue']
                        color = color_list[0] if color_list else 'blue'
                        at_user = row[field_name_to_idx.get('是否艾特', 5)] if '是否艾特' in field_name_to_idx else False

                        at_user_id = ''
                        at_user_idx = field_name_to_idx.get('艾特用户', 6)
                        if at_user_idx < len(row) and row[at_user_idx]:
                            users = row[at_user_idx]
                            if isinstance(users, list) and users:
                                at_user_id = users[0].get('id', '') if isinstance(users[0], dict) else ''

                        send_user_id = ''
                        send_user_idx = field_name_to_idx.get('发送用户', 7)
                        if send_user_idx < len(row) and row[send_user_idx]:
                            users = row[send_user_idx]
                            if isinstance(users, list) and users:
                                send_user_id = users[0].get('id', '') if isinstance(users[0], dict) else ''

                        chat_id = ''
                        chat_idx = field_name_to_idx.get('发送群组', 8)
                        if chat_idx < len(row) and row[chat_idx]:
                            groups = row[chat_idx]
                            if isinstance(groups, list) and groups:
                                chat_id = groups[0].get('id', '') if isinstance(groups[0], dict) else ''

                        max_per_card = int(row[field_name_to_idx.get('最大展示条数', 9)]) if '最大展示条数' in field_name_to_idx and row[field_name_to_idx.get('最大展示条数', 9)] else 5
                        data_range_days = int(row[field_name_to_idx.get('数据来源范围天数', 10)]) if '数据来源范围天数' in field_name_to_idx and row[field_name_to_idx.get('数据来源范围天数', 10)] else 7

                        agg_group = row[field_name_to_idx.get('聚合组代码', 11)] if '聚合组代码' in field_name_to_idx and row[field_name_to_idx.get('聚合组代码', 11)] else 'GROUP_OTHER'
                        agg_subtitle = row[field_name_to_idx.get('聚合后副标题', 12)] if '聚合后副标题' in field_name_to_idx and row[field_name_to_idx.get('聚合后副标题', 12)] else '{scenario}'

                        configs[abnormal] = {
                            'enabled': enabled,
                            'title': title,
                            'subtitle_template': subtitle,
                            'color': color,
                            'at_user': at_user,
                            'at_user_id': at_user_id,
                            'send_user_id': send_user_id,
                            'chat_id': chat_id if chat_id else GROUP_CHAT,
                            'max_per_card': max_per_card,
                            'data_range_days': data_range_days,
                            'agg_group': agg_group,
                            'agg_subtitle': agg_subtitle,
                        }
                    except Exception:
                        continue
                if data.get('has_more', False):
                    offset += len(rows)
                else:
                    break
        except Exception:
            pass

    return configs


def get_card_config(abnormal_scenario):
    """获取指定异常场景的卡片配置。
    优先使用场景专属配置，否则使用"通用"配置，最后使用兜底配置。
    """
    configs = load_card_configs()
    if abnormal_scenario in configs:
        return configs[abnormal_scenario]
    elif '通用' in configs:
        return configs['通用']
    else:
        return {
            'enabled': True,
            'title': 'D365 集成报错告警',
            'subtitle_template': '{scenario}',
            'color': 'red',
            'at_user': False,
            'at_user_id': '',
            'send_user_id': '',
            'chat_id': GROUP_CHAT,
            'max_per_card': 5,
            'data_range_days': 7,
            'agg_group': 'GROUP_OTHER',
            'agg_subtitle': '{scenario}',
        }


def load_alert_rules():
    """从「告警规则配置」表加载规则。
    返回: list of rule dicts
    拉取失败返回空列表。
    """
    rules = []
    offset = 0
    try:
        while True:
            cmd = ['lark-cli', 'base', '+record-list', '--base-token', BASE_TOKEN,
                   '--table-id', ALERT_RULES_TABLE,
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
                    rule = {
                        'rule_type': row[0] if len(row) > 0 else '',
                        'condition_scenario': row[1] if len(row) > 1 else '',
                        'condition_keyword': row[2] if len(row) > 2 else '',
                        'result_abnormal': row[3] if len(row) > 3 else '',
                        'field_display': row[4] if len(row) > 4 else '',
                        'highlight_condition': row[5] if len(row) > 5 else '',
                        'priority': int(row[6]) if len(row) > 6 and row[6] else 0,
                        'description': row[7] if len(row) > 7 else '',
                    }
                    rules.append(rule)
                except Exception:
                    continue
            if data.get('has_more', False):
                offset += len(rows)
            else:
                break
    except Exception:
        pass
    return rules


if __name__ == '__main__':
    print("=== 告警卡片配置（多行结构）===")
    configs = load_card_configs()
    for abnormal, config in configs.items():
        print(f"\n{abnormal}:")
        for k, v in config.items():
            print(f"  {k}: {v}")

    print("\n=== 告警规则配置 ===")
    alert_rules = load_alert_rules()
    for rule in alert_rules:
        print(f"{rule['rule_type']}: {rule['condition_scenario']} + {rule['condition_keyword']} -> {rule['result_abnormal']}")
