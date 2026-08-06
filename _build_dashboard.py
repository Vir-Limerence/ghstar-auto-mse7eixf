#!/usr/bin/env python3
"""Build dashboard index.html from fetched data in /tmp"""
import json, datetime, os

# Read data files
with open("/tmp/douyin.txt") as f: douyin_raw = f.read()
with open("/tmp/gh_daily.txt") as f: github_daily = f.read()
with open("/tmp/gh_weekly.txt") as f: github_weekly = f.read()
with open("/tmp/gh_monthly.txt") as f: github_monthly = f.read()
with open("/tmp/bilibili.txt") as f: bilibili_raw = f.read()
with open("/tmp/vicoman.txt") as f: vicoman_raw = f.read()

# Parse Douyin
douyin = []
for line in douyin_raw.strip().split("\n"):
    parts = line.split("|")
    if len(parts) >= 3:
        douyin.append({"title": parts[1], "url": parts[2]})

# Parse Bilibili
bilibili = json.loads(bilibili_raw)

# Parse and classify Vicoman
vicoman_raw_data = json.loads(vicoman_raw)

def classify_news(title):
    t = title
    if any(kw in t for kw in ["融资","IPO","上市","经济","GDP","镍价","油价","股价","对冲基金","收购","估值","信贷","证监会","股票","银行","央行","营收","新台币","欧元","美元","市场","投资者","存款","金融"]):
        return ("财经", "badge-biz")
    if any(kw in t for kw in ["军事","战争","制裁","外交","谴责","国防","军队","北约","联合国","海地","欧盟","英国","美国","德国","俄罗斯","乌克兰","哥伦比亚","墨西哥","尼日利亚","印度","韩国","日本","印尼","以色列","巴勒斯坦","冲突","驱逐","移民","难民"]):
        return ("国际", "badge-intl")
    if any(kw in t for kw in ["AI","人工智能","大模型","LLM","GPT","DeepSeek","千问","ChatGPT","智能体","agent","Agent","模型","深度学习","机器学习","NLP","CV","机器人"]):
        return ("AI", "badge-ai")
    if any(kw in t for kw in ["黑客","入侵","泄露","攻击","漏洞","诈骗","欺诈","勒索","病毒","木马","安全威胁","爆炸","袭击"]):
        return ("安全", "badge-sec")
    return ("科技", "badge-tech")

vicoman = []
for item in vicoman_raw_data:
    badge_text, badge_class = classify_news(item["title"])
    vicoman.append({"title": item["title"], "badge": badge_text, "badge_class": badge_class})

# Format helpers
def format_stars(n):
    if n >= 1000:
        return f"{n/1000:.1f}K"
    return str(n)

def format_rank_num(i):
    cls = "rank-1" if i == 0 else "rank-2" if i == 1 else "rank-3" if i == 2 else ""
    return f'<span class="rank-num {cls}">{i+1}</span>'

def parse_github(raw):
    repos = []
    for line in raw.strip().split("\n"):
        parts = line.split("|")
        if len(parts) >= 5:
            repos.append({"repo": parts[1], "stars": int(parts[2]), "desc": parts[3], "url": parts[4]})
    return repos

def make_github_item(i, r):
    meta = f'<span class="rank-meta">⭐{format_stars(r["stars"])}</span>'
    desc_html = ""
    if r["desc"]:
        desc_html = f'<p style="font-size:11px;color:var(--text-muted);margin-top:2px">{r["desc"]}</p>'
    return f'      <li>{format_rank_num(i)}<div><a class="rank-title" href="{r["url"]}" target="_blank">{r["repo"]}</a>{meta}{desc_html}</div></li>'

gh_daily = parse_github(github_daily)
gh_weekly = parse_github(github_weekly)
gh_monthly = parse_github(github_monthly)

now = datetime.datetime.now()
update_time = now.strftime("%Y-%m-%d %H:%M CST")

# Build sections
douyin_items = "\n".join(
    f'      <li>{format_rank_num(i)}<a class="rank-title" href="{item["url"]}" target="_blank">{item["title"]}</a></li>'
    for i, item in enumerate(douyin[:10])
)

bili_items = "\n".join(
    f'      <li>{format_rank_num(i)}<a class="rank-title" href="{item["href"]}" target="_blank">{item["title"]}</a></li>'
    for i, item in enumerate(bilibili[:10])
)

gh_daily_items = "\n".join(make_github_item(i, r) for i, r in enumerate(gh_daily))
gh_weekly_items = "\n".join(make_github_item(i, r) for i, r in enumerate(gh_weekly))
gh_monthly_items = "\n".join(make_github_item(i, r) for i, r in enumerate(gh_monthly))

news_items = "\n".join(
    f'  <li><span class="news-badge {item["badge_class"]}">{item["badge"]}</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">{item["title"]}</a></li>'
    for item in vicoman[:16]
)

intro_items = "\n".join(
    f'  <div class="analysis-item"><h3>{"🥇" if i==0 else "🥈" if i==1 else "🥉" if i==2 else ""} <a href="{r["url"]}" target="_blank">{r["repo"]}</a></h3><div class="meta">⭐{format_stars(r["stars"])} 本月</div><div class="desc">{r["desc"] if r["desc"] else "热门开源项目"}</div><div class="tags"><span class="tag">GitHub</span><span class="tag">热门项目</span></div></div>'
    for i, r in enumerate(gh_monthly[:5])
)

html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>⚡ 热度仪表盘</title>
<style>
:root{{--bg:#f8f9fa;--surface:#fff;--border:#e5e7eb;--text:#111827;--text-muted:#6b7280;--accent:#2563eb;--accent-hover:#1d4ed8;--red:#ef4444;--amber:#f59e0b;--green:#10b981;--font-sans:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;--font-mono:'SF Mono',Menlo,monospace;--radius:10px;--shadow:0 1px 3px rgba(0,0,0,.06);--shadow-hover:0 4px 12px rgba(0,0,0,.08)}}
@media(prefers-color-scheme:dark){{:root{{--bg:#0d1117;--surface:#161b22;--border:#30363d;--text:#e6edf3;--text-muted:#8b949e;--shadow:0 1px 3px rgba(0,0,0,.3);--shadow-hover:0 4px 12px rgba(0,0,0,.4)}}}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{overflow-x:clip}}
body{{background:var(--bg);color:var(--text);font-family:var(--font-sans);line-height:1.6;padding:clamp(12px,3vw,32px);-webkit-font-smoothing:antialiased}}
h1{{font-size:clamp(20px,4vw,28px);font-weight:700;text-align:center;margin-bottom:4px;letter-spacing:-.02em}}
.subtitle{{text-align:center;color:var(--text-muted);font-size:13px;margin-bottom:20px}}
.tabs{{display:flex;justify-content:center;gap:2px;margin-bottom:24px;flex-wrap:wrap}}
.tab-btn{{padding:8px 20px;border:1px solid var(--border);background:var(--surface);color:var(--text-muted);cursor:pointer;font-size:13px;font-weight:500;transition:all .15s;font-family:var(--font-sans)}}
.tab-btn:first-child{{border-radius:8px 0 0 8px}}
.tab-btn:last-child{{border-radius:0 8px 8px 0}}
.tab-btn.active{{background:var(--accent);color:#fff;border-color:var(--accent)}}
.tab-btn:hover:not(.active){{color:var(--text);border-color:var(--text-muted)}}
.tab-content{{display:none;max-width:1200px;margin:0 auto;animation:fadeIn .25s ease}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
.tab-content.active{{display:block}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(340px,100%),1fr));gap:16px}}
.card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;box-shadow:var(--shadow);transition:box-shadow .2s}}
.card:hover{{box-shadow:var(--shadow-hover)}}
.card-head{{padding:14px 18px;font-size:14px;font-weight:600;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:8px}}
.card-head .icon{{font-size:18px}}
.rank-list{{list-style:none;padding:0}}
.rank-list li{{display:flex;align-items:flex-start;gap:10px;padding:10px 16px;border-bottom:1px solid var(--border);font-size:13px;transition:background .12s}}
.rank-list li:last-child{{border-bottom:none}}
.rank-list li:hover{{background:var(--bg)}}
.rank-num{{font-weight:700;min-width:22px;text-align:center;font-size:12px;padding-top:2px}}
.rank-1{{color:var(--red)}}.rank-2{{color:var(--amber)}}.rank-3{{color:var(--green)}}
.rank-title{{flex:1;min-width:0;color:var(--text);text-decoration:none;line-height:1.4;overflow-wrap:anywhere}}
.rank-title:hover{{color:var(--accent)}}
.rank-meta{{font-size:11px;color:var(--text-muted);white-space:nowrap;font-family:var(--font-mono)}}
.accent-douyin .card-head{{border-left:3px solid #111}}
.accent-bili .card-head{{border-left:3px solid #fb7299}}
.accent-xhs .card-head{{border-left:3px solid #ff2442}}
.accent-ks .card-head{{border-left:3px solid #ff4906}}
.accent-gh .card-head{{border-left:3px solid var(--accent)}}
.news-list{{list-style:none;max-width:800px;margin:0 auto}}
.news-list li{{display:flex;align-items:flex-start;gap:12px;padding:14px 18px;border-bottom:1px solid var(--border);font-size:13px}}
.news-badge{{font-size:11px;font-weight:600;padding:2px 8px;border-radius:6px;white-space:nowrap;min-width:44px;text-align:center}}
.badge-tech{{background:#dbeafe;color:#1e40af}}.badge-biz{{background:#fef3c7;color:#92400e}}
.badge-intl{{background:#fce7f3;color:#9d174d}}.badge-ai{{background:#d1fae5;color:#065f46}}.badge-sec{{background:#fee2e2;color:#991b1b}}
.news-link{{flex:1;color:var(--text);text-decoration:none;line-height:1.4}}
.news-link:hover{{color:var(--accent)}}
.xhs-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:12px}}
.analysis{{max-width:700px;margin:0 auto}}
.analysis-item{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;margin-bottom:12px;box-shadow:var(--shadow)}}
.analysis-item h3{{font-size:15px;margin-bottom:6px}}
.analysis-item h3 a{{color:var(--accent);text-decoration:none}}
.analysis-item h3 a:hover{{text-decoration:underline}}
.analysis-item .meta{{font-size:12px;color:var(--text-muted);margin-bottom:8px}}
.analysis-item .desc{{font-size:13px;line-height:1.6;color:var(--text)}}
.analysis-item .tags{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}}
.tag{{padding:2px 8px;border-radius:4px;font-size:11px;background:var(--bg);color:var(--text-muted);border:1px solid var(--border)}}
.footer{{text-align:center;margin-top:36px;color:var(--text-muted);font-size:12px}}
.footer a{{color:var(--accent);text-decoration:none}}
.update-time{{text-align:center;color:var(--text-muted);font-size:11px;margin:6px 0}}
</style>
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
  <div class="card accent-douyin">
    <div class="card-head"><span class="icon">🎵</span> 抖音热点</div>
    <ol class="rank-list">
{douyin_items}
    </ol>
  </div>
  <div class="card accent-ks">
    <div class="card-head"><span class="icon">⚡</span> 快手热搜</div>
    <div style="padding:24px;text-align:center;color:var(--text-muted);font-size:13px;line-height:1.8">⚡ 快手网页版不展示热搜<br><span style="font-size:11px">需移动端API，等待适配</span></div>
  </div>
  <div class="card accent-bili">
    <div class="card-head"><span class="icon">📺</span> B站全站排行</div>
    <ol class="rank-list">
{bili_items}
    </ol>
  </div>
  <div class="card accent-xhs">
    <div class="card-head"><span class="icon">📕</span> 小红书热门</div>
    <div class="xhs-grid">
      <div style="padding:20px;text-align:center;color:var(--text-muted);font-size:13px;line-height:1.8">📕 小红书需要登录<br><span style="font-size:11px">请在 Chrome 中扫码登录一次后即可自动抓取</span></div>
    </div>
  </div>
</div>
</div>

<div id="tab-github" class="tab-content">
<p class="update-time">数据来源 GitHub Search API · 每小时更新</p>
<div class="grid">
  <div class="card accent-gh">
    <div class="card-head">📅 今日涨星 TOP10</div>
    <ol class="rank-list">
{gh_daily_items}
    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📆 本周涨星 TOP10</div>
    <ol class="rank-list">
{gh_weekly_items}
    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📊 本月涨星 TOP5</div>
    <ol class="rank-list">
{gh_monthly_items}
    </ol>
  </div>
</div>
</div>

<div id="tab-news" class="tab-content">
<p class="update-time">来源 vicoman.top · 实时更新</p>
<ul class="news-list">
{news_items}
</ul>
</div>

<div id="tab-intro" class="tab-content">
<div class="analysis">
{intro_items}
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

out = "/Users/maqi/idiom-roguelike/index.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print(f"DASHBOARD_OK|{len(html)}bytes")
print(f"DY={len(douyin)}|BL={len(bilibili)}|GH_D={len(gh_daily)}|GH_W={len(gh_weekly)}|GH_M={len(gh_monthly)}|NEWS={len(vicoman)}")
