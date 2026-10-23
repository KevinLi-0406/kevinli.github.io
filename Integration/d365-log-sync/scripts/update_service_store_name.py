# -*- coding: utf-8 -*-
"""批量更新 Service Store Name 脚本（优化版）"""

import json
import sys
import subprocess
import requests
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')
print('脚本开始执行...', flush=True)

# D365 认证信息
DATAVERSE_URL = "https://eusegwayspp.crm4.dynamics.com"
CLIENT_ID = "<YOUR_CLIENT_ID>"
CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
TENANT_ID = "<YOUR_TENANT_ID>"

# 飞书配置
BASE_TOKEN = "MeCQbGQ5paCJBdsfRFwcfneznFb"
LOG_TABLE = "tblTWNXVEKv0IScf"

def get_access_token():
    """获取 Azure AD access token"""
    print('  获取 access token...', flush=True)
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": f"{DATAVERSE_URL}/.default"
    }
    r = requests.post(url, data=data, timeout=10)
    r.raise_for_status()
    token = r.json()["access_token"]
    print(f'  ✓ Token 获取成功（长度: {len(token)}）', flush=True)
    return token

def query_workorder_service_store(access_token, wo_name):
    """从 D365 workorder 实体获取 Service Store Name"""
    url = f"{DATAVERSE_URL}/api/data/v9.2/new_workorders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json"
    }
    params = {
        "$filter": f"new_name eq '{wo_name}'",
        "$select": "new_workorderid,new_name",
        "$expand": "new_servicestoreid($select=new_name)"
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        records = data.get("value", [])
        if records:
            service_store = records[0].get("new_servicestoreid", {})
            return service_store.get("new_name", "") if service_store else ""
    except Exception as e:
        print(f"    ✗ 查询 {wo_name} 失败: {e}", flush=True)
    return ""

def main():
    print('=== 批量更新 Service Store Name ===\n', flush=True)

    # 1. 读取日志文件
    print('1. 读取日志文件...', flush=True)
    try:
        with open('logs_for_service_store.ndjson', 'r', encoding='utf-8') as f:
            lines = f.readlines()[1:]  # 跳过 manifest
    except Exception as e:
        print(f'  ✗ 读取失败: {e}', flush=True)
        return

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

    print(f'  ✓ 读取到 {len(logs)} 条需要更新的记录\n', flush=True)

    if not logs:
        print('没有需要更新的记录，退出', flush=True)
        return

    # 2. 获取 access token
    print('2. 获取 D365 access token...', flush=True)
    try:
        access_token = get_access_token()
        print('', flush=True)
    except Exception as e:
        print(f'  ✗ Token 获取失败: {e}', flush=True)
        return

    # 3. 提取唯一的 Work Order
    unique_wos = list(set([log['wo_name'] for log in logs]))
    print(f'3. 唯一 Work Order 数: {len(unique_wos)}\n', flush=True)

    # 4. 查询每个 Work Order 的 Service Store Name
    print('4. 查询 Service Store Name...', flush=True)
    wo_to_service_store = {}
    for i, wo in enumerate(unique_wos, 1):
        if i % 50 == 0 or i == 1:
            print(f'  进度: {i}/{len(unique_wos)}', flush=True)
        service_store = query_workorder_service_store(access_token, wo)
        wo_to_service_store[wo] = service_store

    print(f'  ✓ 查询完成\n', flush=True)

    # 5. 构建更新记录
    print('5. 构建更新记录...', flush=True)
    records_to_update = []
    for log in logs:
        wo_name = log['wo_name']
        service_store = wo_to_service_store.get(wo_name, '')
        if service_store:
            records_to_update.append({
                'record_id': log['record_id'],
                'service_store': service_store
            })

    print(f'  ✓ 共 {len(records_to_update)} 条记录有 Service Store Name\n', flush=True)

    # 6. 批量更新飞书多维表格
    print('6. 批量更新飞书多维表格...', flush=True)
    if not records_to_update:
        print('  没有需要更新的记录', flush=True)
        return

    # 分批更新，每批 500 条
    batch_size = 500
    total_batches = (len(records_to_update) + batch_size - 1) // batch_size

    for batch_idx in range(total_batches):
        start = batch_idx * batch_size
        end = min((batch_idx + 1) * batch_size, len(records_to_update))
        batch = records_to_update[start:end]

        print(f'  更新批次 {batch_idx + 1}/{total_batches} ({len(batch)} 条)...', flush=True)

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
            print(f'    ✗ 批次 {batch_idx + 1} 更新失败: {r.stderr[:200]}', flush=True)
        else:
            print(f'    ✓ 批次 {batch_idx + 1} 更新成功', flush=True)

    print(f'\n=== 更新完成 ===', flush=True)
    print(f'总计: {len(records_to_update)} 条记录已更新', flush=True)

if __name__ == '__main__':
    main()
