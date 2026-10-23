# -*- coding: utf-8 -*-
"""步骤1: 查询所有 Work Order 的 Service Store Name 并保存到文件"""

import json
import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')
print('=== 步骤1: 查询 Service Store Name ===\n', flush=True)

# D365 认证信息
DATAVERSE_URL = "https://eusegwayspp.crm4.dynamics.com"
CLIENT_ID = "<YOUR_CLIENT_ID>"
CLIENT_SECRET = "<YOUR_CLIENT_SECRET>"
TENANT_ID = "<YOUR_TENANT_ID>"

# 1. 获取 access token
print('1. 获取 access token...', flush=True)
url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
data = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": f"{DATAVERSE_URL}/.default"
}
r = requests.post(url, data=data, timeout=10)
access_token = r.json()["access_token"]
print(f'   ✓ Token 获取成功\n', flush=True)

# 2. 读取唯一的 Work Order
print('2. 读取 Work Order 列表...', flush=True)
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

unique_wos = list(set([log['wo_name'] for log in logs]))
print(f'   ✓ 共 {len(unique_wos)} 个唯一 Work Order\n', flush=True)

# 3. 查询每个 Work Order 的 Service Store Name
print('3. 查询 Service Store Name...', flush=True)
wo_to_service_store = {}
for i, wo in enumerate(unique_wos, 1):
    if i % 10 == 0:
        print(f'   进度: {i}/{len(unique_wos)}', flush=True)

    url = f"{DATAVERSE_URL}/api/data/v9.2/new_workorders"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Accept": "application/json"
    }
    params = {
        "$filter": f"new_name eq '{wo}'",
        "$select": "new_workorderid,new_name",
        "$expand": "new_servicestoreid($select=new_name)"
    }

    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            records = data.get("value", [])
            if records:
                service_store = records[0].get("new_servicestoreid", {})
                wo_to_service_store[wo] = service_store.get("new_name", "") if service_store else ""
        else:
            print(f'   ✗ 查询 {wo} 失败: {r.status_code}', flush=True)
    except Exception as e:
        print(f'   ✗ 查询 {wo} 异常: {e}', flush=True)

print(f'   ✓ 查询完成，共 {len(wo_to_service_store)} 个结果\n', flush=True)

# 4. 保存结果
print('4. 保存结果...', flush=True)
with open('service_store_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(wo_to_service_store, f, ensure_ascii=False, indent=2)

print(f'   ✓ 已保存到 service_store_mapping.json\n', flush=True)

# 5. 统计
has_store = sum(1 for v in wo_to_service_store.values() if v)
print(f'=== 统计 ===', flush=True)
print(f'总 Work Order 数: {len(unique_wos)}', flush=True)
print(f'有 Service Store Name: {has_store}', flush=True)
print(f'无 Service Store Name: {len(unique_wos) - has_store}', flush=True)
