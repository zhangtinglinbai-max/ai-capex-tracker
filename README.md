# AI Capex → A股映射看板

## 一句话说明
运行这个脚本，会自动拉取实时行情，生成一个本地 HTML 看板。

---

## 第一次使用：安装环境（只需做一次）

打开终端（Mac 用 Terminal，Windows 用 PowerShell），进入这个文件夹：

```bash
cd 你的文件夹路径
pip install -r requirements.txt
```

---

## 每次使用：运行脚本

```bash
python fetch_and_build.py
```

运行完成后，用浏览器打开同目录下的 `output.html` 即可。

---

## 用 Claude Code 跑（推荐方式）

如果你已经安装了 Claude Code（`npm install -g @anthropic-ai/claude-code`），
在这个文件夹下直接输入：

```bash
claude
```

然后告诉 Claude：
- "帮我运行 fetch_and_build.py 并打开结果"
- "帮我加一个新股票：300124 汇川技术"
- "帮我加一个每天早上9点自动运行的定时任务"

---

## 数据来源
- A股：AKShare（东方财富数据源，约15分钟延迟）
- 美股：Yahoo Finance（实时行情）

## 注意
- 美股数据需要能访问 Yahoo Finance（需开VPN）
- A股数据国内网络直接访问即可
- 本脚本数据仅供参考，不构成投资建议
