# -*- coding: utf-8 -*-
"""拉取 Base「D365 接口日志」表全部现有日志ID（fldjUqQtB5），输出到文件（可选）。
注意: sync.py 现在直接从 Base 实时拉取，不再需要此脚本。
      此脚本仅用于调试/手动检查。
用法: python fetch_existing_ids.py [out.txt]
"""
import sys, os, io, json, subprocess, argparse

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import BASE_TOKEN, LOG_TABLE, FIELD_LOGID


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out', nargs='?', default='existing_ids.txt')
    args = ap.parse_args()

    offset = 0
    ids = []
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
        rows = d.get('data', {}).get('data', []) or []
        if not rows:
            break
        for row in rows:
            if row and row[0]:
                ids.append(row[0])
        if d.get('data', {}).get('has_more', False):
            offset += len(rows)
        else:
            break

    with open(args.out, 'w', encoding='utf-8', newline='\n') as f:
        for i in ids:
            f.write(i + '\n')
    print('Existing log ids: {} -> {}'.format(len(ids), args.out))


if __name__ == '__main__':
    main()
