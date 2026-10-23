# -*- coding: utf-8 -*-
"""D365 日志同步 - 主流程脚本
输入: D365 fetchxml 结果 JSON 文件
输出: 1) 新增记录的 Base 写入 payload JSON
      2) 待发送(迈创BOM/主数据)记录信息
      3) 异常场景判定实时读取「异常场景判定配置」表；待补充组合自动新增（含查重）
用法:
    python sync.py <d365_json> [--out <dir>] [--skip-existing-check]
      默认从 Base 在线拉取现有日志ID做去重；--skip-existing-check 跳过（全部视为新增）。
"""
import sys, os, io, json, argparse, subprocess
from datetime import datetime, timezone, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from rules import judge_abnormal, build_error_text, extract_keyword

BJ = timezone(timedelta(hours=8))


def load_d365(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def fetch_existing_ids_from_base():
    """从 Base「D365 接口日志」表实时拉取全部现有日志ID。
    返回: set of logid strings.
    拉取失败返回空集合（调用方视为全部新增）。
    """
    ids = set()
    offset = 0
    try:
        while True:
            cmd = ['lark-cli', 'base', '+record-list', '--base-token', BASE_TOKEN,
                   '--table-id', LOG_TABLE, '--field', FIELD_LOGID,
                   '--page-size', '200', '--offset', str(offset), '--format', 'json',
                   '--as', 'bot']
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
                if row and row[0]:
                    ids.add(row[0])
            if data.get('has_more', False):
                offset += len(rows)
            else:
                break
    except Exception:
        return set()
    return ids


def fetch_config_rules():
    """实时读取「迈创异常场景判定配置」和「非迈创异常场景判定配置」两张表的全部规则。
    返回: list of dict {'scenario','keyword','abnormal','owner'}（按配置表顺序）。
    拉取失败返回空列表（调用方回退到本地静态规则）。
    """
    rules = []
    # 读取两张配置表
    for table_id in [CONFIG_TABLE_MAITUO, CONFIG_TABLE_NON_MAITUO]:
        offset = 0
        try:
            while True:
                cmd = ['lark-cli', 'base', '+record-list', '--base-token', BASE_TOKEN,
                       '--table-id', table_id,
                       '--field', CFG_FIELD_SCENARIO, '--field', CFG_FIELD_KEYWORD, '--field', CFG_FIELD_ABNORMAL, '--field', '责任人',
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
                si = field_ids.index(CFG_FIELD_SCENARIO) if CFG_FIELD_SCENARIO in field_ids else 0
                ki = field_ids.index(CFG_FIELD_KEYWORD) if CFG_FIELD_KEYWORD in field_ids else 1
                ai = field_ids.index(CFG_FIELD_ABNORMAL) if CFG_FIELD_ABNORMAL in field_ids else 2
                oi = field_ids.index('责任人') if '责任人' in field_ids else -1
                for row in rows:
                    try:
                        scen = row[si][0] if row[si] else ''
                        kw = row[ki] or ''
                        ab = row[ai][0] if row[ai] else ''
                        owner = row[oi] if oi >= 0 and row[oi] else []
                    except Exception:
                        continue
                    if scen and kw and ab:
                        rules.append({'scenario': scen, 'keyword': kw, 'abnormal': ab, 'owner': owner})
                if data.get('has_more', False):
                    offset += len(rows)
                else:
                    break
        except Exception:
            pass
    return rules


def fetch_site_ops_mapping():
    """实时读取「迈创站点运营」表，建立 Service Store Name → 负责人 的映射。
    返回: dict {'store_name': [user_list]}。
    拉取失败返回空字典。
    """
    mapping = {}
    offset = 0
    try:
        while True:
            cmd = ['lark-cli', 'base', '+record-list', '--base-token', BASE_TOKEN,
                   '--table-id', SITE_OPS_TABLE,
                   '--field', 'Service Store Name', '--field', '负责人',
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
            si = field_ids.index('Service Store Name') if 'Service Store Name' in field_ids else 0
            oi = field_ids.index('负责人') if '负责人' in field_ids else 1
            for row in rows:
                try:
                    store_name = row[si] or ''
                    owner = row[oi] if row[oi] else []
                except Exception:
                    continue
                if store_name and owner:
                    mapping[store_name] = owner
            if data.get('has_more', False):
                offset += len(rows)
            else:
                break
    except Exception:
        pass
    return mapping


def fetch_config_existing():
    """拉取「异常场景判定配置」表现有全部 (场景, 关键词) 组合，用于自动新增查重。
    返回: set of (scenario, keyword)
    """
    combos = set()
    offset = 0
    try:
        while True:
            cmd = ['lark-cli', 'base', '+record-list', '--base-token', BASE_TOKEN,
                   '--table-id', CONFIG_TABLE_ID,
                   '--field', CFG_FIELD_SCENARIO, '--field', CFG_FIELD_KEYWORD,
                   '--page-size', '200', '--offset', str(offset), '--format', 'json']
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
            si = field_ids.index(CFG_FIELD_SCENARIO) if CFG_FIELD_SCENARIO in field_ids else 0
            ki = field_ids.index(CFG_FIELD_KEYWORD) if CFG_FIELD_KEYWORD in field_ids else 1
            for row in rows:
                try:
                    scen = row[si][0] if row[si] else ''
                    kw = row[ki] or ''
                except Exception:
                    continue
                combos.add((scen, kw))
            if data.get('has_more', False):
                offset += len(rows)
            else:
                break
    except Exception:
        pass
    return combos


def write_config_records(new_rows):
    """把全新待补充组合批量写入配置表。返回写入条数。"""
    if not new_rows:
        return 0
    payload = {'create_records': new_rows}
    tmp = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_config_pending.json')
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(payload, f, ensure_ascii=False)
    cmd = ['lark-cli', 'base', '+record-batch-create',
           '--base-token', BASE_TOKEN, '--table-id', CONFIG_TABLE_ID,
           '--json', '@' + tmp, '--format', 'json']
    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = r.stdout.strip()
    try:
        d = json.loads(out)
        ok = d.get('ok', False)
    except Exception:
        ok = False
    try:
        os.remove(tmp)
    except Exception:
        pass
    return len(new_rows) if ok else 0


def parse_record(r, config_rules, site_ops_mapping):
    """把一条 D365 record 解析为 Base 行（中文 key -> 值）。"""
    logid = r.get('new_integrationlogid') or ''
    scen_guid = r.get('_new_integrationscenarioid_value') or ''
    scen = SCENARIO_MAP.get(scen_guid, scen_guid)
    createdon = r.get('createdon') or ''
    created_bj = ''
    if createdon:
        try:
            dt = datetime.fromisoformat(createdon.replace('Z', '+00:00'))
            created_bj = dt.astimezone(BJ).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            created_bj = createdon
    wo_fmt = r.get('_new_workorder_value@OData.Community.Display.V1.FormattedValue') or ''
    wo_id = r.get('_new_workorder_value') or ''
    source = r.get('a_208b9d7ba4714804b1c519c506ffca4f.new_sourcesystem@OData.Community.Display.V1.FormattedValue') or ''
    target = r.get('a_208b9d7ba4714804b1c519c506ffca4f.new_targetsystem@OData.Community.Display.V1.FormattedValue') or ''
    wo_status = r.get('a_0bbd1e7b159447d880264778ef724bf5.statuscode@OData.Community.Display.V1.FormattedValue') or ''
    service_type = r.get('a_0bbd1e7b159447d880264778ef724bf5.new_servicetypecode@OData.Community.Display.V1.FormattedValue') or ''
    wo_source = r.get('a_0bbd1e7b159447d880264778ef724bf5.new_workordersourcecode@OData.Community.Display.V1.FormattedValue') or ''
    service_store_name = r.get('a_servicestore.new_name') or ''
    reqjson = r.get('new_requestjson') or ''
    respjson = r.get('new_responsejson') or ''

    # 异常场景判定：实时读配置表规则（config_rules）；为空时回退本地静态
    abnormal, matched, fallback = judge_abnormal(scen, respjson, config_rules)
    err_text = build_error_text(abnormal, respjson)

    station = ''
    status = ''
    goodsid = ''
    material_list = []
    maituo_code = ''
    if reqjson:
        try:
            req = json.loads(reqjson)
            if isinstance(req, dict):
                station = req.get('station') or ''
                so = req.get('service_order') or {}
                if isinstance(so, dict):
                    maituo_code = so.get('id') or ''
                    status = so.get('status') or ''
                    items = so.get('items') or {}
                    if isinstance(items, dict):
                        goodsid = items.get('goodsId') or ''
                        mlist = items.get('hasMaterialList') or []
                        for m in mlist:
                            if isinstance(m, dict):
                                material_list.append({
                                    'Index': m.get('Index') or '',
                                    'applyMacId': m.get('applyMacId') or m.get('applymacid') or '',
                                    'quantity': m.get('quantity') or '',
                                })
        except Exception:
            pass

    other_desc_set = []
    if respjson:
        try:
            resp = json.loads(respjson)
            data_obj = resp.get('data') if isinstance(resp, dict) else resp
            if isinstance(data_obj, dict):
                # 提取 otherDesc（BOM 场景用）
                if abnormal == 'Maitrox-数据问题-out of SBOM':
                    od = data_obj.get('otherDesc')
                    if od:
                        other_desc_set = [x.strip() for x in str(od).split(',') if x.strip()]
        except Exception:
            pass

    keyword = extract_keyword(respjson) if abnormal == '待补充' else ''

    row = {
        FIELD_WORKORDER: wo_fmt,
        FIELD_CREATED: created_bj,
        FIELD_SCENARIO: [scen],
        FIELD_TARGET: target,
        FIELD_SOURCE: source,
        FIELD_REQJSON: reqjson,
        FIELD_RESPJSON: respjson,
        FIELD_ERROR: err_text,
        FIELD_STATION: station,
        FIELD_STATUS: status,
        FIELD_STATUS_REASON: wo_status,
        FIELD_B2X: r.get('a_0bbd1e7b159447d880264778ef724bf5.new_b2xorderid') or '',
        FIELD_LOGID: logid,
        FIELD_WOID: wo_id,
        FIELD_LOGLINK: LOG_URL_TPL.format(logid=logid),
        FIELD_WOLINK: WO_URL_TPL.format(woid=wo_id) if wo_id else '',
        FIELD_ABNORMAL: [abnormal],
        FIELD_SENT: False,
        FIELD_WOSTATUS: wo_status,
        FIELD_EXT4: r.get('new_extensionfield4') or '',
        FIELD_SERVICE_TYPE: service_type,
        FIELD_WO_SOURCE: wo_source,
        FIELD_SERVICE_STORE_NAME: service_store_name,
    }
    if maituo_code:
        row[FIELD_MAITUO_CODE] = maituo_code

    # 责任人赋值逻辑
    owner = []
    if abnormal.startswith('Maitrox-'):
        # 迈创场景：根据 Service Store Name 从迈创站点运营表读取责任人
        if service_store_name and service_store_name in site_ops_mapping:
            owner = site_ops_mapping[service_store_name]
    else:
        # 非迈创场景：从配置表中读取责任人
        for rule in config_rules:
            if rule['abnormal'] == abnormal and rule.get('owner'):
                owner = rule['owner']
                break

    if owner:
        row[FIELD_OWNER] = owner

    meta = {
        'logid': logid,
        'scenario': scen,
        'abnormal': abnormal,
        'matched': matched,
        'fallback': fallback,
        'keyword': keyword,
        'created_bj': created_bj,
        'wo': wo_fmt,
        '_wo_id': wo_id,
        'b2x': r.get('a_0bbd1e7b159447d880264778ef724bf5.new_b2xorderid') or '',
        'goodsId': goodsid,
        'material_list': material_list,
        'other_desc_set': other_desc_set,
        'err_text': err_text,
        'status': status,
        'maituo_code': maituo_code,
        'service_type': service_type,
        'wo_source': wo_source,
    }
    return row, meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('d365_json')
    ap.add_argument('--out', default='.')
    ap.add_argument('--skip-existing-check', action='store_true',
                    help='跳过 Base 现有ID检查，全部视为新增')
    args = ap.parse_args()

    d365 = load_d365(args.d365_json)
    records = d365.get('records', [])
    print(f'D365 records: {len(records)} (returnedCount={d365.get("returnedCount")})')

    # 实时读取配置表规则
    config_rules = fetch_config_rules()
    print(f'Config rules loaded: {len(config_rules)} (实时读取多维表格配置表)')

    # 实时读取迈创站点运营表映射
    site_ops_mapping = fetch_site_ops_mapping()
    print(f'Site ops mapping loaded: {len(site_ops_mapping)} (实时读取迈创站点运营表)')

    # 从 Base 实时拉取现有 ID（除非 --skip-existing-check）
    existing = set()
    if not args.skip_existing_check:
        existing = fetch_existing_ids_from_base()
        print(f'Existing ids from Base: {len(existing)}')
    else:
        print('Skip existing check (--skip-existing-check)')

    rows = []
    metas = []
    new_count = 0
    for r in records:
        logid = r.get('new_integrationlogid') or ''
        if existing and logid in existing:
            continue
        new_count += 1
        row, meta = parse_record(r, config_rules, site_ops_mapping)
        rows.append(row)
        metas.append(meta)

    print(f'New records (not in existing): {new_count}')

    pending = [m for m in metas if m['abnormal'] in ('迈创-数据问题-BOM', '迈创-数据问题-主数据', '迈创-接口问题-其他')]
    print(f'Pending alert (迈创BOM/主数据/接口问题-其他): {len(pending)}')

    # ---- 自动补配置表：待补充组合，查重后新增 ----
    to_add = [m for m in metas if m['abnormal'] == '待补充']
    print(f'Abnormal=待补充 (需检查配置表): {len(to_add)}')
    if to_add:
        existing_combos = fetch_config_existing()
        seen = set()
        new_rows = []
        for m in to_add:
            scen = m['scenario']
            kw = (m.get('keyword') or '').strip()
            if not kw:
                continue
            combo = (scen, kw)
            if combo in existing_combos or combo in seen:
                continue
            seen.add(combo)
            new_rows.append({
                CFG_FIELD_SCENARIO: scen,
                CFG_FIELD_KEYWORD: kw,
                CFG_FIELD_ABNORMAL: '待补充',
                CFG_FIELD_NOTE: '自动新增：D365日志 未命中配置，待人工补充规则',
            })
        if new_rows:
            n_written = write_config_records(new_rows)
            print(f'Config new (场景+关键词): {len(new_rows)}，已写入配置表 {n_written} 条')
        else:
            print('Config new: 0（已存在或无可提取关键词）')

    base = os.path.splitext(os.path.basename(args.d365_json))[0]
    outdir = args.out
    os.makedirs(outdir, exist_ok=True)
    payload_path = os.path.join(outdir, f'{base}.payload.json')
    meta_path = os.path.join(outdir, f'{base}.meta.json')
    with open(payload_path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'create_records': rows}, f, ensure_ascii=False)
    with open(meta_path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(metas, f, ensure_ascii=False)
    print(f'Payload -> {payload_path}')
    print(f'Meta    -> {meta_path}')

    for m in metas:
        print(f"  {m['wo']} | {m['scenario']} | {m['created_bj']} | {m['abnormal']}")


if __name__ == '__main__':
    main()
