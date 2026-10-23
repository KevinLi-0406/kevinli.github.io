#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
重新判定"待补充"记录的异常场景并更新责任人
"""

import json
import sys
import subprocess
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE_TOKEN = "MeCQbGQ5paCJBdsfRFwcfneznFb"
LOG_TABLE = "tblTWNXVEKv0IScf"
CONFIG_TABLE_NON_MAITUO = "tblbscUEUlXSUQE4"

def fetch_config_rules():
    """从配置表读取判定规则"""
    cmd = [
        'lark-cli', 'base', '+record-list',
        '--base-token', BASE_TOKEN,
        '--table-id', CONFIG_TABLE_NON_MAITUO,
        '--limit', '200',
        '--output', 'config_rules.ndjson',
        '--as', 'bot',
        '--overwrite'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"读取配置表失败: {result.stderr}")
        return []

    # 读取 ndjson 文件
    rules = []
    with open('config_rules.ndjson', 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # 跳过 manifest
        for line in lines:
            if line.strip():
                rec = json.loads(line)
                scenario = rec.get('Integration Scenario', [])
                keyword = rec.get('Response JSON 关键词', '')
                abnormal = rec.get('异常场景', [])
                owner = rec.get('责任人', [])

                if scenario and keyword and abnormal:
                    rules.append({
                        'scenario': scenario[0] if isinstance(scenario, list) else scenario,
                        'keyword': keyword,
                        'abnormal': abnormal[0] if isinstance(abnormal, list) else abnormal,
                        'owner': owner
                    })

    return rules

def judge_abnormal(scenario, response, rules):
    """判定异常场景"""
    for rule in rules:
        if rule['scenario'] == scenario and rule['keyword'] in response:
            return rule['abnormal'], rule['owner']
    return None, None

def main():
    print("=== 重新判定'待补充'记录的异常场景 ===\n")

    # 1. 读取配置表规则
    print("1. 读取配置表规则...")
    rules = fetch_config_rules()
    print(f"   读取到 {len(rules)} 条规则\n")

    # 2. 读取 D365接口日志表中的'待补充'记录
    print("2. 读取'待补充'记录...")
    cmd = [
        'lark-cli', 'base', '+record-list',
        '--base-token', BASE_TOKEN,
        '--table-id', LOG_TABLE,
        '--limit', '2000',
        '--output', 'pending_records.ndjson',
        '--as', 'bot',
        '--overwrite'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"读取日志表失败: {result.stderr}")
        return

    # 3. 筛选'待补充'记录
    pending_records = []
    ndjson_path = Path('pending_records.ndjson')
    with open(ndjson_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # 跳过 manifest
        for line in lines:
            if line.strip():
                rec = json.loads(line)
                abnormal = rec.get('异常场景', [])
                if abnormal and abnormal[0] == '待补充':
                    pending_records.append(rec)

    print(f"   找到 {len(pending_records)} 条'待补充'记录\n")

    # 4. 重新判定异常场景
    print("3. 重新判定异常场景...")
    update_records = []
    matched_count = 0

    for rec in pending_records:
        record_id = rec.get('record_id')
        scenario = rec.get('Integration Scenario', [])
        response = rec.get('Response JSON', '')

        scenario_name = scenario[0] if isinstance(scenario, list) and scenario else ''

        abnormal, owner = judge_abnormal(scenario_name, response, rules)

        if abnormal:
            matched_count += 1
            update_rec = {
                'record_id': record_id,
                'fields': {
                    '异常场景': [abnormal]
                }
            }
            if owner:
                update_rec['fields']['责任人'] = owner
            update_records.append(update_rec)

    print(f"   匹配到 {matched_count} 条记录\n")

    # 5. 批量更新
    if update_records:
        print("4. 批量更新...")

        # 分批更新（每批 200 条）
        batch_size = 200
        for i in range(0, len(update_records), batch_size):
            batch = update_records[i:i+batch_size]
            batch_file = f'update_pending_batch_{i//batch_size}.json'

            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump({'update_records': batch}, f, ensure_ascii=False, indent=2)

            cmd = [
                'lark-cli', 'base', '+record-batch-update',
                '--base-token', BASE_TOKEN,
                '--table-id', LOG_TABLE,
                '--json', f'@{batch_file}',
                '--as', 'bot'
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                print(f"   批次 {i//batch_size + 1}: 更新 {len(batch)} 条记录")
            else:
                print(f"   批次 {i//batch_size + 1}: 更新失败 - {result.stderr}")

        print(f"\n✓ 完成！更新了 {matched_count} 条记录")
    else:
        print("没有找到可以匹配的记录")

if __name__ == '__main__':
    main()
