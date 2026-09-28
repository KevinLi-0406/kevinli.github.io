@echo off
cd /d "C:\Users\yixing.li\AppData\Roaming\CherryStudio\Data\Agents\11b9a2f4-c869-5a7c-9524-5d948337f5e4\repo\Integration\feishu-bot"
"C:\Program Files\nodejs\npx.cmd" pm2 resurrect >> "%~dp0pm2-startup.log" 2>&1
