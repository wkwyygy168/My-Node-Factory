name: Node Collector Bot

# 触发条件设置
on:
  schedule:
    # 核心修改：cron 表达式。
    # GitHub 使用 UTC 时间，17:00 对应北京时间次日凌晨 01:00
    - cron: '0 17 * * *'
  
  # 保留手动触发开关，方便你随时点击 Run workflow 更新
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: 检查仓库代码
      uses: actions/checkout@v3

    - name: 安装 Python 环境
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: 安装依赖插件
      run: |
        pip install requests

    - name: 执行收割脚本
      run: python main.py

    - name: 将新节点推送到仓库
      run: |
        git config --local user.email "actions@github.com"
        git config --local user.name "GitHub Action"
        git add nodes.txt
        # 即使没有新节点也不报错打叉
        git commit -m "Auto Update Nodes: $(date +'%Y-%m-%d %H:%M:%S')" || exit 0
        git push
