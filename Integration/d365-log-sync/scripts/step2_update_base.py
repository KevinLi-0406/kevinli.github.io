# -*- coding: utf-8 -*-
"""步骤2: 批量更新飞书多维表格的 Service Store Name"""

import json
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
print('=== 步骤2: 批量更新飞书多维表格 ===\n', flush=True)

# 飞书配置
BASE_TOKEN = "MeCQbGQ5paCJBdsfRFwcfneznFb"
LOG_TABLE = "tblTWNXVEKv0IScf"

# 1. 读取 Service Store Name 映射
print('1. 读取 Service Store Name 映射...', flush=True)
with open('service_store_mapping.json', 'r', encoding='utf-8') as f:
    wo_to_service_store = json.load(f)
print(f'   ✓ 共 {len(wo_to_service_store)} 个映射\n', flush=True)

# 2. 读取日志文件
print('2. 读取日志文件...', flush=True)
with open('logs_for_service_store.ndjson', 'r', encoding='utf-8') as f:
    lines = f.readlines()[1:]

logs = []
for line in lines:
    if line.strip():
        rec = json.loads(line)
        record_id = rec.get('record_id', '')
        wo_name = rec.get('Work Order', '')
        service_store = rec.get('Service Store Name', '')
        if record_id and wo_name and not service_store:
            logs.append({
                'record_id': record_id,
                'wo_name': wo_name
            })

print(f'   ✓ 共 {len(logs)} 条需要更新的记录\n', flush=True)

# 3. 构建更新记录
print('3. 构建更新记录...', flush=True)
records_to_update = []
for log in logs:
    wo_name = log['wo_name']
    service_store = wo_to_service_store.get(wo_name, '')
    if service_store:
        records_to_update.append({
            'record_id': log['record_id'],
            'service_store': service_store
        })

print(f'   ✓ 共 {len(records_to_update)} 条记录有 Service Store Name\n', flush=True)

# 4. 批量更新飞书多维表格
print('4. 批量更新飞书多维表格...', flush=True)
if not records_to_update:
    print('   没有需要更新的记录', flush=True)
    exit(0)

# 分批更新，每批 200 条（飞书 API 限制）
batch_size = 200
total_batches = (len(records_to_update) + batch_size - 1) // batch_size

for batch_idx in range(total_batches):
    start = batch_idx * batch_size
    end = min((batch_idx + 1) * batch_size, len(records_to_update))
    batch = records_to_update[start:end]

    print(f'   更新批次 {batch_idx + 1}/{total_batches} ({len(batch)} 条)...', flush=True)

    # 创建 JSON 文件
    update_data = {
        "update_records": [
            {
                "record_id": rec['record_id'],
                "fields": {
                    "Service Store Name": rec['service_store']
                }
            }
            for rec in batch
        ]
    }

    json_file = f'batch_update_{batch_idx}.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(update_data, f, ensure_ascii=False)

    # 调用 lark-cli 批量更新
    cmd = ['lark-cli', 'base', '+record-batch-update',
           '--base-token', BASE_TOKEN,
           '--table-id', LOG_TABLE,
           '--json', f'@{json_file}',
           '--as', 'bot']

    r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
    if r.returncode != 0:
        print(f'      ✗ 批次 {batch_idx + 1} 更新失败: {r.stderr[:200]}', flush=True)
    else:
        print(f'      ✓ 批次 {batch_idx + 1} 更新成功', flush=True)

print(f'\n=== 更新完成 ===', flush=True)
print(f'总计: {len(records_to_update)} 条记录已更新', flush=True)
