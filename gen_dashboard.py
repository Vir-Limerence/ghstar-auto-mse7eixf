#!/usr/bin/env python3
"""Generate index.html from collected data files."""
import json, datetime, sys

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M CST")

# Read data from stdin (JSON)
data = json.load(sys.stdin)

douyin_items = data["douyin"]
gh_daily = data["gh_daily"]
gh_weekly = data["gh_weekly"]
gh_monthly = data["gh_monthly"]
bili_items = data["bili"]

def fmt_stars(s):
    try:
        n = int(s)
        if n >= 10000:
            return f"⭐{n/1000:.1f}K"
        return f"⭐{n}"
    except:
        return f"⭐{s}"

def douyin_html(items):
    h = ""
    for i, (title, url) in enumerate(items):
        rc = f"rank-{i+1}" if i < 3 else ""
        h += f'      <li><span class="rank-num {rc}">{i+1}</span><a class="rank-title" href="{url}" target="_blank">{title}</a></li>\n'
    return h

def bili_html(items):
    h = ""
    for i, item in enumerate(items):
        rc = f"rank-{i+1}" if i < 3 else ""
        h += f'      <li><span class="rank-num {rc}">{i+1}</span><a class="rank-title" href="{item["href"]}" target="_blank">{item["title"]}</a></li>\n'
    return h

def gh_list(items):
    h = ""
    for i, r in enumerate(items):
        rc = f"rank-{i+1}" if i < 3 else ""
        desc_html = f'<p style="font-size:11px;color:var(--text-muted);margin-top:2px">{r["desc"]}</p>' if r.get("desc") else ""
        h += f'      <li><span class="rank-num {rc}">{i+1}</span><div><a class="rank-title" href="{r["url"]}" target="_blank">{r["repo"]}</a><span class="rank-meta">{fmt_stars(r["stars"])}</span>{desc_html}</div></li>\n'
    return h

def intro_items(items):
    h = ""
    medals = ["🥇", "🥈", "🥉"]
    for i, r in enumerate(items):
        medal = medals[i] if i < 3 else ""
        desc = r.get("desc") or "热门开源项目"
        h += f'  <div class="analysis-item"><h3>{medal} <a href="{r["url"]}" target="_blank">{r["repo"]}</a></h3><div class="meta">{fmt_stars(r["stars"])} 本月</div><div class="desc">{desc}</div><div class="tags"><span class="tag">GitHub</span><span class="tag">热门项目</span></div></div>\n'
    return h

vicoman_html = """<ul class="news-list">
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">英国保守党辩护提名前新纳粹成员为候选人</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">美国服务业PMI微升至54.1显示稳步扩张</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">民主党候选人埃尔-赛义德险胜密歇根州参议院初选</a></li>
  <li><span class="news-badge badge-tech">AI</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">SpaceX首份财报：营收78亿美元，AI支出激增致亏损</a></li>
  <li><span class="news-badge badge-tech">AI</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">Anthropic组建AI芯片设计团队以优化模型效率</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">联合国人权高专对伊朗处决人数激增表示关切</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">阿卜杜勒·埃尔-赛义德赢得密歇根州民主党参议员初选</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">Ring发布Peephole Cam 2K智能猫眼摄像头</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">专家呼吁中国立法保护海底光缆免受破坏</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">SpaceX巨额限售股解禁在即引发市场担忧</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">投行交易激增推动华尔街奖金预期上涨</a></li>
  <li><span class="news-badge badge-biz">国际</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">美共和党内部对战争部长皮特·赫格塞斯信任度下降</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">迪士尼证实正探索推出含广告的免费流媒体层级</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">中国联通：智算规模达45EFLOPS，今年算力投资超175亿元</a></li>
  <li><span class="news-badge badge-tech">科技</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">迪士尼第三财季利润超预期，乐园与流媒体业务双增</a></li>
  <li><span class="news-badge badge-tech">AI</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">CrowdStrike携手AWS推出国际AI安全挑战赛，奖金10万美元</a></li>
</ul>"""

html = f"""<!DOCTYPE html>
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
  <!-- 抖音 -->
  <div class="card accent-douyin">
    <div class="card-head"><span class="icon">🎵</span> 抖音热点</div>
    <ol class="rank-list">
{douyin_html(douyin_items)}    </ol>
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
{bili_html(bili_items)}    </ol>
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
<p class="update-time">数据来源 GitHub Search API · 每小时更新</p>
<div class="grid">
  <div class="card accent-gh">
    <div class="card-head">📅 今日涨星 TOP10</div>
    <ol class="rank-list">
{gh_list(gh_daily)}    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📆 本周涨星 TOP10</div>
    <ol class="rank-list">
{gh_list(gh_weekly)}    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📊 本月涨星 TOP5</div>
    <ol class="rank-list">
{gh_list(gh_monthly)}    </ol>
  </div>
</div>
</div>

<!-- AI新闻 -->
<div id="tab-news" class="tab-content">
<p class="update-time">来源 vicoman.top · vicoman 当前404，保留历史快照</p>
{vicoman_html}
</div>

<!-- 解读 -->
<div id="tab-intro" class="tab-content">
<div class="analysis">
{intro_items(gh_monthly)}
</div>
</div>

<p class="footer">Powered by <a href="https://github.com/NousResearch/hermes-agent">Hermes Agent</a> · 每小时自动抓取 · 更新于 {now_str}</p>

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
</html>"""

with open("/Users/maqi/idiom-roguelike/index.html", "w") as f:
    f.write(html)

print(f"index.html written ({len(html)} bytes)")
print(f"DOUYIN:{len(douyin_items)} BILI:{len(bili_items)} GH_DAILY:{len(gh_daily)} GH_WEEKLY:{len(gh_weekly)} GH_MONTHLY:{len(gh_monthly)} VICOMAN:404")
