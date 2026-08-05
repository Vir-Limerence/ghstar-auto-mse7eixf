#!/usr/bin/env python3
"""Generate index.html from scraped data."""
import json, sys
from datetime import datetime

# All collected data (hardcoded from this run)
douyin = [
    ("趁夏天赴一场八大古镇之约", "https://www.douyin.com/search/%E8%B6%81%E5%A4%8F%E5%A4%A9%E8%B5%B4%E4%B8%80%E5%9C%BA%E5%85%AB%E5%A4%A7%E5%8F%A4%E9%95%87%E4%B9%8B%E7%BA%A6"),
    ("山西菜申请出战暑期美食展", "https://www.douyin.com/search/%E5%B1%B1%E8%A5%BF%E8%8F%9C%E7%94%B3%E8%AF%B7%E5%87%BA%E6%88%98%E6%9A%91%E6%9C%9F%E7%BE%8E%E9%A3%9F%E5%B1%95"),
    ("我国成功在海上发射一箭双星", "https://www.douyin.com/search/%E6%88%91%E5%9B%BD%E6%88%90%E5%8A%9F%E5%9C%A8%E6%B5%B7%E4%B8%8A%E5%8F%91%E5%B0%84%E4%B8%80%E7%AE%AD%E5%8F%8C%E6%98%9F"),
    ("无畏巡回成都站开赛", "https://www.douyin.com/search/%E6%97%A0%E7%95%8F%E5%B7%A1%E5%9B%9E%E6%88%90%E9%83%BD%E7%AB%99%E5%BC%80%E8%B5%9B"),
    ("中方对6家美国实体采取反制措施", "https://www.douyin.com/search/%E4%B8%AD%E6%96%B9%E5%AF%B96%E5%AE%B6%E7%BE%8E%E5%9B%BD%E5%AE%9E%E4%BD%93%E9%87%87%E5%8F%96%E5%8F%8D%E5%88%B6%E6%8E%AA%E6%96%BD"),
    ("WTT横滨冠军赛今日赛程", "https://www.douyin.com/search/WTT%E6%A8%AA%E6%BB%A8%E5%86%A0%E5%86%9B%E8%B5%9B%E4%BB%8A%E6%97%A5%E8%B5%9B%E7%A8%8B"),
    ("西安通报赛格商场坠亡事件", "https://www.douyin.com/search/%E8%A5%BF%E5%AE%89%E9%80%9A%E6%8A%A5%E8%B5%9B%E6%A0%BC%E5%95%86%E5%9C%BA%E5%9D%A0%E4%BA%A1%E4%BA%8B%E4%BB%B6"),
    ("2026抖音创作者大会来了", "https://www.douyin.com/search/2026%E6%8A%96%E9%9F%B3%E5%88%9B%E4%BD%9C%E8%80%85%E5%A4%A7%E4%BC%9A%E6%9D%A5%E4%BA%86"),
    ("首届早餐烘焙大师赛", "https://www.douyin.com/search/%E9%A6%96%E5%B1%8A%E6%97%A9%E9%A4%90%E7%83%98%E7%84%99%E5%A4%A7%E5%B8%88%E8%B5%9B"),
    ("昆明一化工厂装卸黄磷时起火", "https://www.douyin.com/search/%E6%98%86%E6%98%8E%E4%B8%80%E5%8C%96%E5%B7%A5%E5%8E%82%E8%A3%85%E5%8D%B8%E9%BB%84%E7%A3%B7%E6%97%B6%E8%B5%B7%E7%81%AB"),
]

bilibili = [
    ("大家还想看我搬空什么店", "https://www.bilibili.com/video/BV1bz3Q6oEMP"),
    ("《最讨厌复联の一集》", "https://www.bilibili.com/video/BV1KduF6ME4b"),
    ("【苏新皓｜4K直拍】POWER 直拍｜梦寐以求·演唱会", "https://www.bilibili.com/video/BV1D23262EaD"),
    ("老大，你的意思是我们抽烟抽的慢也得死吗？", "https://www.bilibili.com/video/BV126GG62E9G"),
    ("几十块入手世界级顶尖好物——居家用品篇", "https://www.bilibili.com/video/BV1Vo3C6VE1B"),
    ("当黑客入侵我家摄像头将看到……", "https://www.bilibili.com/video/BV1Lg3R65EZn"),
    ("完蛋！我被男同学包围了", "https://www.bilibili.com/video/BV1uPMZ6NEBb"),
    ("当我被外星人取代", "https://www.bilibili.com/video/BV1RoMf6mEra"),
    ("【最闪暖的一集】闪暖七周年CG首曝 | 8月5日更新", "https://www.bilibili.com/video/BV1xS396ZEUz"),
    ("还来！！！！！！！！！！！", "https://www.bilibili.com/video/BV1xwMQ6GEix"),
]

gh_daily = [
    ("KKKKhazix/human-writing", 746, "让 AI 写的中文读起来像一个具体的人在说话", "https://github.com/KKKKhazix/human-writing"),
    ("Packets/Vanta", 344, "A two-faction battle royale. Own what you earn.", "https://github.com/Packets/Vanta"),
    ("AMAP-ML/LongHorizon-Harness", 246, "The long-horizon computer-use harness.", "https://github.com/AMAP-ML/LongHorizon-Harness"),
    ("SandAI-org/MAGI-2-preview", 222, "MAGI-2-preview: Scaling Video Generation Models", "https://github.com/SandAI-org/MAGI-2-preview"),
    ("mikiarlo3/awesome-growth-hacking-skills", 210, "Find agentic growth hacking skills for Claude, ChatGPT", "https://github.com/mikiarlo3/awesome-growth-hacking-skills"),
    ("criptogus/HermesOffice", 199, "HermesOffice — AI-native office suite", "https://github.com/criptogus/HermesOffice"),
    ("fuxicodex/Fuxi", 191, "FuXi is a fast, self-contained AI developer terminal", "https://github.com/fuxicodex/Fuxi"),
    ("cristicretu/diri", 168, "Native macOS orchestrator for coding agents", "https://github.com/cristicretu/diri"),
    ("ZzzLc0405/photo-abstract-editorial", 143, "", "https://github.com/ZzzLc0405/photo-abstract-editorial"),
    ("jd-opensource/JoyAI-Video-Edit", 129, "", "https://github.com/jd-opensource/JoyAI-Video-Edit"),
]

gh_weekly = [
    ("yc-software/qm", 11438, "Multiplayer agent harness for work", "https://github.com/yc-software/qm"),
    ("trycompai/crm", 5447, "An open-source, agentic-first CRM.", "https://github.com/trycompai/crm"),
    ("bashalarmistalt/decimen-optical-transfer", 4617, "", "https://github.com/bashalarmistalt/decimen-optical-transfer"),
    ("xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer", 3244, "FDE（前沿部署工程师）从零入门指南", "https://github.com/xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer"),
    ("firecrawl/anydoc", 2822, "Convert Word, PowerPoint, Excel, OpenDocument, RTF", "https://github.com/firecrawl/anydoc"),
    ("FareedKhan-dev/kimi-k3-in-c", 2294, "Kimi K3 inference in C on a single machine", "https://github.com/FareedKhan-dev/kimi-k3-in-c"),
    ("microsoft/skill-recorder", 1896, "Desktop app that records your on-screen work session", "https://github.com/microsoft/skill-recorder"),
    ("imsai-sh/zhuzhiliao", 1884, "竹知了 —— 传统玩具 Web 模拟版", "https://github.com/imsai-sh/zhuzhiliao"),
    ("genspark-ai/genoffice", 1576, "An AI-native office suite for macOS and Windows", "https://github.com/genspark-ai/genoffice"),
    ("DannyMac180/sol-advisor", 1377, "Codex-native architect orchestration", "https://github.com/DannyMac180/sol-advisor"),
]

gh_monthly = [
    ("xai-org/grok-build", 24178, "SpaceXAI's coding agent harness and TUI.", "https://github.com/xai-org/grok-build"),
    ("Fei-Away/Codex-Dream-Skin", 13237, "Codex Dream Skin", "https://github.com/Fei-Away/Codex-Dream-Skin"),
    ("andrewyng/openworker", 12991, "", "https://github.com/andrewyng/openworker"),
    ("yc-software/qm", 11438, "Multiplayer agent harness for work", "https://github.com/yc-software/qm"),
    ("img2threejs/img2threejs", 9805, "Rebuild images as code-only procedural 3D", "https://github.com/img2threejs/img2threejs"),
]

vicoman = [
    ("WindBorne获3700万美元融资优化AI气象预测", "财经"),
    ("沙特阿美投资印度Mitti Labs助力农业节水", "科技"),
    ("韩国股东起诉三星与SK海力士CEO涉嫌违规发放奖金", "科技"),
    ("AMD向Linux内核提交eSPI标准框架补丁以统一硬件支持", "科技"),
    ("俄无人机袭击赫尔松致多人伤亡", "科技"),
    ("硅谷人形机器人热潮引发自动化就业担忧", "科技"),
    ("台湾启动年度军事演习，模拟应对潜在外部军事入侵场景", "国际"),
    ("世卫组织总干事赴刚果支援埃博拉疫情，确诊病例近四千例", "科技"),
    ("东北亚遭遇创纪录高温，日韩朝多地民众与动物受严重影响", "科技"),
    ("礼来季度业绩超预期，上调2026年营收指引至850-870亿美元", "科技"),
    ("俄导弹袭击基辅致17死乌防空系统失效", "科技"),
    ("SpaceX火箭残骸疑似撞击月球表面", "科技"),
    ("华为乾崑智驾ADS Pro V5.0升级，支持园区领航辅助泊车功能", "科技"),
    ("秘鲁主教促成1.5亿美元铅中毒和解案", "科技"),
    ("迪士尼2026财年第三财季净利润同比减半", "科技"),
    ("高盛上调中国AI模型市场营收预测至130亿美元", "AI"),
]


def num_fmt(n):
    if n >= 1000:
        return f"{n//1000},{n%1000:03d}"
    return str(n)


def rank_class(i):
    if i == 0: return "rank-1"
    if i == 1: return "rank-2"
    if i == 2: return "rank-3"
    return ""


def badge_class(badge):
    if badge in ("财经", "国际", "AI"): return "badge-biz"
    return "badge-tech"


now = datetime.now()
update_time = now.strftime("%Y-%m-%d %H:%M CST")

# Build CSS (same as before)
css = '''<style>
:root {--bg:#f8f9fa;--surface:#fff;--border:#e5e7eb;--text:#111827;--text-muted:#6b7280;--accent:#2563eb;--accent-hover:#1d4ed8;--red:#ef4444;--amber:#f59e0b;--green:#10b981;--font-sans:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;--font-mono:'SF Mono',Menlo,monospace;--radius:10px;--shadow:0 1px 3px rgba(0,0,0,.06);--shadow-hover:0 4px 12px rgba(0,0,0,.08)}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--surface:#161b22;--border:#30363d;--text:#e6edf3;--text-muted:#8b949e;--shadow:0 1px 3px rgba(0,0,0,.3);--shadow-hover:0 4px 12px rgba(0,0,0,.4)}}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{overflow-x:clip}
body{background:var(--bg);color:var(--text);font-family:var(--font-sans);line-height:1.6;padding:clamp(12px,3vw,32px);-webkit-font-smoothing:antialiased}
h1{font-size:clamp(20px,4vw,28px);font-weight:700;text-align:center;margin-bottom:4px;letter-spacing:-.02em}
.subtitle{text-align:center;color:var(--text-muted);font-size:13px;margin-bottom:20px}
.tabs{display:flex;justify-content:center;gap:2px;margin-bottom:24px;flex-wrap:wrap}
.tab-btn{padding:8px 20px;border:1px solid var(--border);background:var(--surface);color:var(--text-muted);cursor:pointer;font-size:13px;font-weight:500;transition:all .15s;font-family:var(--font-sans)}
.tab-btn:first-child{border-radius:8px 0 0 8px}
.tab-btn:last-child{border-radius:0 8px 8px 0}
.tab-btn.active{background:var(--accent);color:#fff;border-color:var(--accent)}
.tab-btn:hover:not(.active){color:var(--text);border-color:var(--text-muted)}
.tab-content{display:none;max-width:1200px;margin:0 auto;animation:fadeIn .25s ease}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.tab-content.active{display:block}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:16px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);transition:box-shadow .2s}
.card:hover{box-shadow:var(--shadow-hover)}
.card-head{padding:14px 18px;font-size:14px;font-weight:600;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px}
.card-head .icon{font-size:18px}
.rank-list{list-style:none;padding:0}
.rank-list li{display:flex;align-items:flex-start;gap:10px;padding:10px 16px;border-bottom:1px solid var(--border);font-size:13px;transition:background .12s}
.rank-list li:last-child{border-bottom:none}
.rank-list li:hover{background:var(--bg)}
.rank-num{font-weight:700;min-width:22px;text-align:center;font-size:12px;padding-top:2px}
.rank-1{color:var(--red)}.rank-2{color:var(--amber)}.rank-3{color:var(--green)}
.rank-title{flex:1;min-width:0;color:var(--text);text-decoration:none;line-height:1.4;overflow-wrap:anywhere}
.rank-title:hover{color:var(--accent)}
.rank-meta{font-size:11px;color:var(--text-muted);white-space:nowrap;font-family:var(--font-mono)}
.accent-douyin .card-head{border-left:3px solid #111}
.accent-bili .card-head{border-left:3px solid #fb7299}
.accent-xhs .card-head{border-left:3px solid #ff2442}
.accent-ks .card-head{border-left:3px solid #ff4906}
.accent-gh .card-head{border-left:3px solid var(--accent)}
.news-list{list-style:none;max-width:800px;margin:0 auto}
.news-list li{display:flex;align-items:flex-start;gap:12px;padding:14px 18px;border-bottom:1px solid var(--border);font-size:13px}
.news-badge{font-size:11px;font-weight:600;padding:2px 8px;border-radius:6px;white-space:nowrap;min-width:44px;text-align:center}
.badge-tech{background:#dbeafe;color:#1e40af}.badge-biz{background:#fef3c7;color:#92400e}
.news-link{flex:1;color:var(--text);text-decoration:none;line-height:1.4}
.news-link:hover{color:var(--accent)}
.xhs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:12px}
.analysis{max-width:700px;margin:0 auto}
.analysis-item{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;margin-bottom:12px;box-shadow:var(--shadow)}
.analysis-item h3{font-size:15px;margin-bottom:6px}
.analysis-item h3 a{color:var(--accent);text-decoration:none}
.analysis-item h3 a:hover{text-decoration:underline}
.analysis-item .meta{font-size:12px;color:var(--text-muted);margin-bottom:8px}
.analysis-item .desc{font-size:13px;line-height:1.6;color:var(--text)}
.analysis-item .tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}
.tag{padding:2px 8px;border-radius:4px;font-size:11px;background:var(--bg);color:var(--text-muted);border:1px solid var(--border)}
.footer{text-align:center;margin-top:36px;color:var(--text-muted);font-size:12px}
.footer a{color:var(--accent);text-decoration:none}
.update-time{text-align:center;color:var(--text-muted);font-size:11px;margin:6px 0}
</style>'''

# Build list items
def douyin_items():
    items = []
    for i, (title, url) in enumerate(douyin):
        rc = rank_class(i)
        items.append(f'      <li><span class="rank-num {rc}">{i+1}</span><a class="rank-title" href="{url}" target="_blank">{title}</a></li>')
    return "\n".join(items)

def bilibili_items():
    items = []
    for i, (title, url) in enumerate(bilibili):
        rc = rank_class(i)
        items.append(f'      <li><span class="rank-num {rc}">{i+1}</span><a class="rank-title" href="{url}" target="_blank">{title}</a></li>')
    return "\n".join(items)

def gh_items(data):
    items = []
    for i, (name, stars, desc, url) in enumerate(data):
        rc = rank_class(i)
        desc_html = f'<p style="font-size:11px;color:var(--text-muted);margin-top:2px">{desc}</p>' if desc else ''
        items.append(f'      <li><span class="rank-num {rc}">{i+1}</span><div><a class="rank-title" href="{url}" target="_blank">{name}</a><span class="rank-meta">⭐{num_fmt(stars)}</span>{desc_html}</div></li>')
    return "\n".join(items)

def news_items():
    items = []
    for title, badge in vicoman:
        bc = badge_class(badge)
        items.append(f'  <li><span class="news-badge {bc}">{badge}</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">{title}</a></li>')
    return "\n".join(items)

def intro_items():
    medals = ["🥇", "🥈", "🥉", "", ""]
    items = []
    for i, (name, stars, desc, url) in enumerate(gh_monthly):
        m = medals[i]
        d = desc or "热门开源项目"
        items.append(f'  <div class="analysis-item"><h3>{m} <a href="{url}" target="_blank">{name}</a></h3><div class="meta">⭐{num_fmt(stars)} 本月</div><div class="desc">{d}</div><div class="tags"><span class="tag">GitHub</span><span class="tag">热门项目</span></div></div>')
    return "\n".join(items)

html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>⚡ 热度仪表盘</title>
{css}
</head>
<body>
<h1>⚡ 热度仪表盘</h1>
<p class="subtitle">多平台实时热榜 · 自动每小时更新</p>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('app')">🔥 APP热榜</button>
  <button class="tab-btn" onclick="switchTab('github')">📊 GitHub</button>
  <button class="tab-btn" onclick="switchTab('news')">📰 新闻</button>
  <button class="tab-btn" onclick="switchTab('intro')">💡 解读</button>
</div>

<!-- APP热榜 -->
<div id="tab-app" class="tab-content active">
<div class="grid">
  <!-- 抖音 -->
  <div class="card accent-douyin">
    <div class="card-head"><span class="icon">🎵</span> 抖音热点</div>
    <ol class="rank-list">
{douyin_items()}
    </ol>
  </div>
  <!-- 快手 -->
  <div class="card accent-ks">
    <div class="card-head"><span class="icon">⚡</span> 快手热搜</div>
    <div style="padding:24px;text-align:center;color:var(--text-muted);font-size:13px;line-height:1.8">⚡ 快手网页版不展示热搜<br><span style="font-size:11px">需移动端API，等待适配</span></div>
  </div>
  <!-- B站 -->
  <div class="card accent-bili">
    <div class="card-head"><span class="icon">📺</span> B站全站排行</div>
    <ol class="rank-list">
{bilibili_items()}
    </ol>
  </div>
  <!-- 小红书 -->
  <div class="card accent-xhs">
    <div class="card-head"><span class="icon">📕</span> 小红书热门</div>
    <div class="xhs-grid">
      <div style="padding:20px;text-align:center;color:var(--text-muted);font-size:13px;line-height:1.8">📕 小红书需要登录<br><span style="font-size:11px">请在 Chrome 中扫码登录一次后即可自动抓取</span></div>
    </div>
  </div>
</div>
</div>

<!-- GitHub 排行榜 -->
<div id="tab-github" class="tab-content">
<p class="update-time">数据来源 GitHub Trending · 每小时更新</p>
<div class="grid">
  <div class="card accent-gh">
    <div class="card-head">📅 今日涨星 TOP10</div>
    <ol class="rank-list">
{gh_items(gh_daily)}
    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📆 本周涨星 TOP10</div>
    <ol class="rank-list">
{gh_items(gh_weekly)}
    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📊 本月涨星 TOP10</div>
    <ol class="rank-list">
{gh_items(gh_monthly)}
    </ol>
  </div>
</div>
</div>

<!-- AI新闻 -->
<div id="tab-news" class="tab-content">
<p class="update-time">来源 vicoman.top · 实时更新</p>
<ul class="news-list">
{news_items()}
</ul>
</div>

<!-- 解读 -->
<div id="tab-intro" class="tab-content">
<div class="analysis">
{intro_items()}
</div>
</div>

<p class="footer">Powered by <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a> · 每小时自动抓取 · 更新于 {update_time}</p>

<script>
function switchTab(tab){{
  document.querySelectorAll('.tab-content').forEach(function(t){{t.classList.remove('active')}});
  document.querySelectorAll('.tab-btn').forEach(function(b){{b.classList.remove('active')}});
  document.getElementById('tab-'+tab).classList.add('active');
  var btns=document.querySelectorAll('.tab-btn');
  var idx={{app:0,github:1,news:2,intro:3}};
  btns[idx[tab]].classList.add('active');
}}
</script>
</body>
</html>'''

with open("/Users/maqi/idiom-roguelike/index.html", "w") as f:
    f.write(html)

print(f"HTML written: {len(html)} chars")
counts = {
    "抖音": len(douyin),
    "B站": len(bilibili),
    "GitHub日榜": len(gh_daily),
    "GitHub周榜": len(gh_weekly),
    "GitHub月榜": len(gh_monthly),
    "vicoman新闻": len(vicoman),
}
print(json.dumps(counts, ensure_ascii=False))
print(f"更新于 {update_time}")
