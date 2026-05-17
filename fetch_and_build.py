import json, os, time, re
from datetime import datetime
import requests

A_STOCKS = [
    {"code":"300308","name":"中际旭创", "chain":"光模块",    "chain_type":"optical",
     "logic":"800G/1.6T光模块，直供NVDA/谷歌/Meta，全球市占率领先",
     "profile":{"intro":"光模块行业全球龙头，专注高速率数据通信光收发模块，是AI数据中心高速互联的核心器件供应商。","ai_role":"AI算力集群的'神经连接'——服务器间超高速光互联，800G/1.6T模块是AI集群的必需品。","market_share":"全球800G光模块市占约30%+，NVIDIA、谷歌、Meta等超大规模数据中心主要供应商。","gross_margin":"约22-25%"}},
    {"code":"300394","name":"天孚通信", "chain":"光模块",    "chain_type":"optical",
     "logic":"CPO封装器件/光引擎，400G-1.6T核心，AI集群超高速互联",
     "profile":{"intro":"光无源器件与CPO封装器件龙头，专注于光引擎、FA阵列等精密光学器件，是AI时代CPO技术的核心供应商。","ai_role":"CPO（共封装光学）是AI芯片与网络的下一代接口方案，天孚是国内CPO核心器件的龙头布局者。","market_share":"国内光无源器件细分龙头，CPO器件市场份额随技术渗透持续提升。","gross_margin":"约45-50%"}},
    {"code":"300502","name":"新易盛",   "chain":"光模块",    "chain_type":"optical",
     "logic":"400G/800G光收发器，北美云厂商直供",
     "profile":{"intro":"专业光收发模块厂商，深度绑定北美超大规模云计算厂商，产品覆盖100G到800G全系列。","ai_role":"直供北美云厂商（AWS、Azure等），是AI数据中心光互联基础设施的直接受益者。","market_share":"北美400G/800G数据中心光模块主要供应商之一，供应链地位稳固。","gross_margin":"约20-23%"}},
    {"code":"601138","name":"工业富联", "chain":"AI服务器",  "chain_type":"server",
     "logic":"全球最大AI服务器ODM，供货NVDA/微软/谷歌",
     "profile":{"intro":"富士康旗下工业互联网旗舰，全球最大服务器与存储设备代工商（ODM），AI服务器产能全球领先。","ai_role":"AI服务器制造的'最大车间'，NVIDIA H100/H200及GB200服务器全球最大代工厂，把GPU算力变成可交付的数据中心产品。","market_share":"全球AI服务器ODM市场份额约35-40%，国内服务器制造绝对龙头。","gross_margin":"约9-10%（ODM模式）"}},
    {"code":"688008","name":"澜起科技", "chain":"内存接口",  "chain_type":"chip",
     "logic":"DDR5内存缓冲芯片，AI服务器内存关键器件",
     "profile":{"intro":"专注内存接口与混合安全芯片的Fabless芯片设计公司，DDR5时代全球内存缓冲芯片的绝对龙头。","ai_role":"AI服务器内存带宽瓶颈推动DDR5快速渗透，澜起的RCD是每条DDR5内存条必装的关键芯片。","market_share":"全球DDR5 RCD（注册缓冲器）芯片市占约60%+，国内唯一可与国际巨头竞争的内存接口芯片厂商。","gross_margin":"约55-60%"}},
    {"code":"688256","name":"寒武纪",   "chain":"AI芯片",   "chain_type":"chip",
     "logic":"国产AI推理/训练芯片，国产替代叠加",
     "profile":{"intro":"中国AI专用芯片（NPU）设计先驱，产品覆盖云端训练、推理及边缘AI芯片，国内最具代表性的AI芯片设计公司之一。","ai_role":"国产AI芯片自主可控的核心标的，在出口管制背景下是中国算力自给自足的重要探索者。","market_share":"国内AI专用训练芯片细分市场具有先发优势，受益于华为体系外的国产AI芯片需求。","gross_margin":"约60-65%（样本量较小，波动性大）"}},
    {"code":"002463","name":"沪电股份", "chain":"PCB",      "chain_type":"pcb",
     "logic":"高速背板PCB，AI服务器主板，价值量是普通服务器3-5倍",
     "profile":{"intro":"国内高端PCB龙头，专注高速、高频背板及HDI板，是AI服务器、网络交换机等高端设备的PCB核心供应商。","ai_role":"AI服务器所需PCB复杂度和单价是普通服务器3-5倍，沪电是国内唯一能大规模供应AI服务器高速背板的PCB厂商之一。","market_share":"国内高速背板PCB市占约15%，AI服务器配套PCB供应链核心厂商。","gross_margin":"约21-24%"}},
    {"code":"002281","name":"光迅科技", "chain":"光模块",    "chain_type":"optical",
     "logic":"电信+数通光模块，烽火集团旗下，数通侧AI算力互联",
     "profile":{"intro":"烽火通信旗下光器件与光模块龙头，兼顾电信级和数通级光模块，是国内光模块综合实力最强的国有企业。","ai_role":"数通侧光模块直接服务AI数据中心互联，同时受益于AI带动网络扩容升级对电信侧光模块的间接拉动。","market_share":"国内光模块综合市占约12-15%，数通+电信双领域布局，国内综合实力前三。","gross_margin":"约25-28%"}},
    {"code":"300124","name":"汇川技术", "chain":"工业自动化", "chain_type":"auto",
     "logic":"国内工业自动化龙头，AI+机器人时代核心受益，国产替代叠加",
     "profile":{"intro":"中国最大的工业自动化与驱动控制企业，产品涵盖变频器、伺服系统、PLC、工业机器人等，被称为'中国的三菱电机'。","ai_role":"AI驱动的智能制造、工业机器人浪潮的核心受益者；AI服务器工厂自动化改造同步拉动其产品需求。","market_share":"国内变频器市占约15%+（仅次于ABB、西门子等外资），伺服系统市占约20%+，国产替代最受益的工业自动化龙头。","gross_margin":"约33-36%"}},
    {"code":"688981","name":"中芯国际", "chain":"半导体制造", "chain_type":"semi",
     "logic":"中国最大晶圆代工，国产AI芯片制造唯一大规模支撑，国产替代核心",
     "profile":{"intro":"中国最大的集成电路晶圆代工企业，可量产14nm及以上制程，是中国半导体制造能力的集中体现。","ai_role":"中国AI芯片（寒武纪、华为海思等）的本土制造唯一大规模支撑方，在出口管制背景下战略地位极其重要。","market_share":"全球晶圆代工市占约6-7%（排名第三），中国大陆市场占有率约75%，绝对国内龙头。","gross_margin":"约18-22%"}},
]

US_STOCKS = [
    {"ticker":"NVDA", "name":"英伟达", "role":"GPU卖铲人",  "capex":"主要供应商",   "capex_pct":95,
     "profile":{"intro":"全球AI计算的核心基础设施供应商，GPU从游戏芯片进化为AI训练的标准算力单元，数据中心业务是主要增长引擎。","ai_role":"AI基础设施的'算力卖铲人'——H100/H200/GB200 GPU是全球AI训练的行业标准，CUDA生态构建深厚护城河。","market_share":"AI训练GPU市占约80-90%，数据中心GPU市场绝对龙头，AMD和英特尔合计不足20%。","gross_margin":"约74-78%，AI产品溢价持续推高"}},
    {"ticker":"MSFT", "name":"微软",   "role":"Azure AI",   "capex":"~$500亿/年",  "capex_pct":80,
     "profile":{"intro":"全球最大企业软件公司，通过对OpenAI的独家投资成为企业AI浪潮的最大受益者之一，Azure云是企业AI部署首选平台。","ai_role":"OpenAI最大股东+独家云合作伙伴，Azure AI将ChatGPT/GPT-4能力直接变现；Copilot覆盖Office全线产品，AI商业化最成熟。","market_share":"全球云计算市场约22%（IaaS+PaaS），企业软件市场绝对龙头，AI Copilot企业订阅用户快速增长。","gross_margin":"约69-70%（集团整体）"}},
    {"ticker":"GOOGL","name":"谷歌",   "role":"GCP+TPU",    "capex":"~$750亿/年",  "capex_pct":87,
     "profile":{"intro":"全球搜索引擎霸主与AI研究先驱，自研TPU芯片+GCP云服务+Gemini大模型三位一体，AI技术储备最为深厚。","ai_role":"全球AI基础研究最重要机构之一（Transformer论文原作者多来自谷歌），TPU自研芯片+GCP云服务+Gemini模型完整闭环。","market_share":"GCP全球云计算约10%，搜索广告市场约90%，AI搜索是其最大防御战场。","gross_margin":"约56-58%（集团整体）"}},
    {"ticker":"META", "name":"Meta",   "role":"Llama训练",  "capex":"~$600亿/年",  "capex_pct":76,
     "profile":{"intro":"全球最大社交媒体公司（Facebook/Instagram/WhatsApp），以开源Llama大模型和重压AI基础设施建设著称，AI领域最激进的投入者之一。","ai_role":"开源AI生态最大推手——Llama系列模型降低全球AI开发门槛；自建AI推理基础设施规模全球前三，广告AI化显著提升变现效率。","market_share":"全球社交媒体DAU超35亿，广告市场份额约20%+，Instagram/WhatsApp/Facebook三平台垄断全球社交流量。","gross_margin":"约81-83%（广告为主，极高利润率）"}},
    {"ticker":"AMZN", "name":"亚马逊", "role":"AWS最大",    "capex":"~$1000亿/年", "capex_pct":93,
     "profile":{"intro":"全球最大电商+云计算巨头，AWS是全球云计算市场的开创者和最大玩家，Trainium/Inferentia自研AI芯片持续降低AI推理成本。","ai_role":"全球最大AI基础设施提供商——AWS承载全球最多AI工作负载，Bedrock平台集成主流大模型，自研Trainium芯片对抗NVIDIA垄断。","market_share":"全球云计算IaaS市场约32%（排名第一），领先Azure（22%）和GCP（10%）。","gross_margin":"约47-49%（集团整体，AWS毛利率约60%+）"}},
    {"ticker":"TSM",  "name":"台积电", "role":"晶圆代工王", "capex":"~$320亿/年",  "capex_pct":75,
     "profile":{"intro":"全球最大独立晶圆代工厂，成立于1987年，由张忠谋创办，是现代半导体产业分工体系的缔造者，生产全球几乎所有最先进的芯片。","ai_role":"AI芯片制造的'唯一大厂'——NVIDIA、AMD、Apple、高通等顶级AI芯片全部由台积电制造，3nm/5nm先进制程是AI算力的物理基础。","market_share":"全球晶圆代工市占约60%，先进制程（3nm/5nm）市占约90%+，NVIDIA H100/H200全部采用台积电4N制程。","gross_margin":"约53-56%，先进制程溢价持续推高整体毛利率"}},
]

def sina_code(code):
    return ("sh" if code.startswith("6") else "sz") + code

def fetch_a_stocks():
    print("正在拉取A股实时行情（新浪财经）...")
    codes = [sina_code(s["code"]) for s in A_STOCKS]
    url = "https://hq.sinajs.cn/list=" + ",".join(codes)
    headers = {
        "Referer": "https://finance.sina.com.cn",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.encoding = "gbk"
        lines = resp.text.strip().split("\n")
    except Exception as e:
        print(f"  新浪接口失败: {e}")
        lines = []

    results = []
    for i, stock in enumerate(A_STOCKS):
        entry = {**stock, "price":"N/A","change_pct":"N/A","close60":[]}
        if i < len(lines):
            try:
                data_str = lines[i].split('"')[1]
                f = data_str.split(",")
                if len(f) > 5:
                    price = float(f[3])
                    prev  = float(f[2])
                    chg   = round((price - prev) / prev * 100, 2)
                    entry["price"]      = price
                    entry["change_pct"] = chg
                    print(f"  OK {stock['name']}  {price}  {chg:+.2f}%")
            except Exception as e:
                print(f"  失败 {stock['name']}: {e}")
        results.append(entry)
        time.sleep(0.15)
    return results

def fetch_us_stocks():
    print("正在拉取美股行情（需开VPN）...")
    results = []
    for stock in US_STOCKS:
        entry = {**stock, "price":"N/A","change_pct":"N/A","close60":[]}
        try:
            import yfinance as yf
            hist = yf.Ticker(stock["ticker"]).history(period="3mo")
            if not hist.empty:
                price = round(hist["Close"].iloc[-1], 2)
                prev  = round(hist["Close"].iloc[-2], 2)
                chg   = round((price - prev) / prev * 100, 2)
                entry["price"]      = price
                entry["change_pct"] = chg
                entry["close60"]    = [round(v,2) for v in hist["Close"].tolist()]
                print(f"  OK {stock['ticker']}  ${price}  {chg:+.2f}%")
        except Exception as e:
            print(f"  失败 {stock['ticker']}: {e}")
        results.append(entry)
    return results

def build_html(a_data, us_data, update_time):
    a_json  = json.dumps(a_data,  ensure_ascii=False)
    us_json = json.dumps(us_data, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8">
<title>AI Capex A股看板</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--bg:#0a0a0f;--sf:#12121a;--br:#1e1e2e;--ac:#00e5ff;--ac2:#ff3d71;--ac3:#a8ff3e;--tx:#e0e0f0;--mu:#5a5a8a;--up:#a8ff3e;--dn:#ff3d71}}
body{{background:var(--bg);color:var(--tx);font-family:sans-serif;font-size:13px;padding:28px}}
.hdr{{display:flex;align-items:baseline;gap:14px;margin-bottom:30px;border-bottom:1px solid var(--br);padding-bottom:14px}}
.hdr h1{{font-size:18px;color:var(--ac);font-family:monospace}}
.tag{{font-size:10px;padding:3px 10px;border:1px solid var(--ac);color:var(--ac);border-radius:2px;margin-left:auto}}
.sec{{font-size:10px;color:var(--mu);letter-spacing:2px;text-transform:uppercase;margin-bottom:12px;display:flex;align-items:center;gap:10px}}
.sec::after{{content:'';flex:1;height:1px;background:var(--br)}}
.hint{{font-size:9px;color:#2a2a4a;letter-spacing:0;text-transform:none;margin-left:4px}}
.ugrid{{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:30px}}
.uc{{background:var(--sf);border:1px solid var(--br);border-top:2px solid var(--ac);padding:13px;cursor:pointer;transition:border-color .15s,background .15s}}
.uc:hover{{border-color:rgba(0,229,255,.5);background:#14141f}}
.uc .tk{{font-size:14px;font-weight:700;color:var(--ac);margin-bottom:3px;font-family:monospace}}
.uc .cn{{font-size:10px;color:var(--mu);margin-bottom:7px}}
.uc .pr{{font-size:13px;font-family:monospace}}
.uc .cg{{font-size:11px;margin-top:2px;font-family:monospace}}
.cb{{margin-top:9px;height:3px;background:var(--br);border-radius:2px;overflow:hidden}}
.cf{{height:100%;background:linear-gradient(90deg,var(--ac),var(--ac3));border-radius:2px}}
.cl{{font-size:9px;color:var(--mu);margin-top:4px}}
.tw{{background:var(--sf);border:1px solid var(--br);overflow-x:auto;margin-bottom:28px}}
table{{width:100%;border-collapse:collapse;min-width:760px}}
thead tr{{background:rgba(0,229,255,.04);border-bottom:1px solid var(--br)}}
th{{font-size:10px;color:var(--mu);padding:10px 14px;text-align:left;white-space:nowrap;font-family:monospace}}
td{{padding:10px 14px;border-bottom:1px solid rgba(30,30,46,.5);vertical-align:middle}}
tbody tr{{cursor:pointer}}
tbody tr:hover{{background:rgba(0,229,255,.05)}}
.sc{{font-size:11px;color:var(--mu);display:block;font-family:monospace}}
.ct{{display:inline-block;font-size:9px;padding:2px 7px;border-radius:2px}}
.optical{{background:rgba(0,229,255,.12);color:var(--ac);border:1px solid rgba(0,229,255,.2)}}
.server{{background:rgba(168,255,62,.1);color:var(--ac3);border:1px solid rgba(168,255,62,.2)}}
.chip{{background:rgba(255,61,113,.1);color:var(--ac2);border:1px solid rgba(255,61,113,.2)}}
.pcb{{background:rgba(255,200,0,.1);color:#ffc800;border:1px solid rgba(255,200,0,.2)}}
.auto{{background:rgba(180,100,255,.1);color:#b464ff;border:1px solid rgba(180,100,255,.2)}}
.semi{{background:rgba(255,165,0,.1);color:#ffa500;border:1px solid rgba(255,165,0,.2)}}
.pn{{font-size:13px;display:block;font-family:monospace}}
.up{{color:var(--up)}}.dn{{color:var(--dn)}}.fl{{color:var(--mu)}}
.ch{{background:rgba(168,255,62,.12);color:var(--ac3);font-size:11px;padding:3px 8px;border-radius:2px}}
.cm{{background:rgba(0,229,255,.1);color:var(--ac);font-size:11px;padding:3px 8px;border-radius:2px}}
.nt{{font-size:10px;color:var(--mu);padding:11px 14px;border:1px solid var(--br);border-left:3px solid var(--ac2);margin-top:14px}}
#modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.78);z-index:100;align-items:center;justify-content:center}}
.mbox{{background:var(--sf);border:1px solid var(--br);border-top:3px solid var(--ac);padding:28px 32px;max-width:500px;width:90%;position:relative;border-radius:2px}}
.mbox h2{{font-size:16px;color:var(--ac);font-family:monospace;margin-bottom:20px;padding-right:28px}}
.mclose{{position:absolute;top:12px;right:14px;background:none;border:none;color:var(--mu);font-size:18px;cursor:pointer;line-height:1;padding:4px 6px}}
.mclose:hover{{color:var(--tx)}}
.mrow{{margin-bottom:14px}}
.mlabel{{font-size:9px;color:var(--mu);letter-spacing:2px;text-transform:uppercase;margin-bottom:5px}}
.mval{{font-size:12px;line-height:1.65;color:var(--tx)}}
.mval.hi{{color:var(--ac3)}}
.mval.ac{{color:var(--ac);font-family:monospace;font-size:14px;font-weight:700}}
.mgrid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
</style></head><body>
<div class="hdr">
  <h1>AI CAPEX → A股映射看板</h1>
  <span class="tag">更新于 {update_time}</span>
</div>
<div class="sec">美股 AI CAPEX 核心驱动方<span class="hint">· 点击查看详情</span></div>
<div class="ugrid" id="ug"></div>
<div class="sec">A股关联标的（实时行情）<span class="hint">· 点击行查看详情</span></div>
<div class="tw"><table>
  <thead><tr><th>代码/公司</th><th>产业链</th><th>关联逻辑</th><th>现价(¥)</th><th>今日涨跌</th><th>相关性</th></tr></thead>
  <tbody id="at"></tbody>
</table></div>
<div class="nt">A股数据来自新浪财经（约15分钟延迟）。美股数据需开VPN。仅供参考，不构成投资建议。</div>
<div id="modal">
  <div class="mbox">
    <button class="mclose" onclick="closeModal()">✕</button>
    <h2 id="m-name"></h2>
    <div class="mrow"><div class="mlabel">公司简介</div><div class="mval" id="m-intro"></div></div>
    <div class="mrow"><div class="mlabel">AI基础设施定位</div><div class="mval hi" id="m-role"></div></div>
    <div class="mgrid">
      <div class="mrow"><div class="mlabel">市场份额</div><div class="mval" id="m-share"></div></div>
      <div class="mrow"><div class="mlabel">毛利率</div><div class="mval ac" id="m-margin"></div></div>
    </div>
  </div>
</div>
<script>
const AD={a_json},UD={us_json};
const CR={{"300308":{{l:"极高★★★",c:"ch"}},"300394":{{l:"极高★★★",c:"ch"}},"300502":{{l:"极高★★★",c:"ch"}},"601138":{{l:"极高★★★",c:"ch"}},"688008":{{l:"中高★★",c:"cm"}},"688256":{{l:"国产替代★★",c:"cm"}},"002463":{{l:"中高★★",c:"cm"}},"002281":{{l:"中高★★",c:"cm"}},"300124":{{l:"中高★★",c:"cm"}},"688981":{{l:"国产替代★★",c:"cm"}}}};
const PROF={{}};
AD.forEach(s=>{{if(s.profile)PROF[s.code]={{name:s.name,...s.profile}}}});
UD.forEach(s=>{{if(s.profile)PROF[s.ticker]={{name:s.name,...s.profile}}}});
function pc(v){{return v==="N/A"?"fl":parseFloat(v)>=0?"up":"dn"}}
function ps(v){{if(v==="N/A")return"N/A";const f=parseFloat(v);return(f>=0?"+":"")+f.toFixed(2)+"%"}}
function showModal(k){{
  const p=PROF[k];if(!p)return;
  document.getElementById('m-name').textContent=p.name;
  document.getElementById('m-intro').textContent=p.intro;
  document.getElementById('m-role').textContent=p.ai_role;
  document.getElementById('m-share').textContent=p.market_share;
  document.getElementById('m-margin').textContent=p.gross_margin;
  document.getElementById('modal').style.display='flex';
}}
function closeModal(){{document.getElementById('modal').style.display='none'}}
document.getElementById('modal').addEventListener('click',function(e){{if(e.target===this)closeModal()}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeModal()}});
UD.forEach(s=>{{
  const cc=pc(s.change_pct),pr=s.price!=="N/A"?"$"+s.price.toFixed(2):"需开VPN";
  document.getElementById("ug").innerHTML+=`<div class="uc" onclick="showModal('${{s.ticker}}')"><div class="tk">${{s.ticker}}</div><div class="cn">${{s.name}} · ${{s.role}}</div><div class="pr ${{cc}}">${{pr}}</div><div class="cg ${{cc}}">${{ps(s.change_pct)}}</div><div class="cb"><div class="cf" style="width:${{s.capex_pct}}%"></div></div><div class="cl">Capex ${{s.capex}}</div></div>`;
}});
AD.forEach(s=>{{
  const cc=pc(s.change_pct),cfg=CR[s.code]||{{l:"—",c:"cm"}};
  const pr=s.price!=="N/A"?"¥"+s.price:"获取中...";
  document.getElementById("at").innerHTML+=`<tr onclick="showModal('${{s.code}}')"><td><span class="sc">${{s.code}}</span>${{s.name}}</td><td><span class="ct ${{s.chain_type}}">${{s.chain}}</span></td><td style="font-size:11px;color:#8080b0;max-width:180px">${{s.logic}}</td><td><span class="pn">${{pr}}</span></td><td><span class="${{cc}}">${{ps(s.change_pct)}}</span></td><td><span class="${{cfg.c}}">${{cfg.l}}</span></td></tr>`;
}});
</script></body></html>"""

if __name__ == "__main__":
    print("="*40)
    print("AI Capex A股映射看板 - 启动")
    print("="*40)
    a_data  = fetch_a_stocks()
    us_data = fetch_us_stocks()
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    html = build_html(a_data, us_data, update_time)
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ("index.html", "output.html"):
        out = os.path.join(base, name)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
    print(f"\n完成！已生成: index.html / output.html")
    print("用浏览器打开 index.html 查看\n")
