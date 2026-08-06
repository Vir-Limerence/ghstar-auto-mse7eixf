import json, urllib.parse, datetime

douyin = [
    "趁夏天赴一场八大古镇之约",
    "中方对6家美国实体采取反制措施",
    "凉资源激活夏日经济热流量",
    '人贩子"梅姨"真实姓名曝光',
    "无畏巡回成都站开赛",
    "2026年的夏天要结束了",
    "2026抖音创作者大会来了",
    "难忘童年经典场景",
    "夏日蓝色系妆一眼降温",
    "台风白海豚或吞并台风鲸鱼",
]

github_daily = [
    ("KKKKhazix/human-writing", 1074, "让 AI 写的中文读起来像一个具体的人在说话。通用创作与改稿 Skill，开箱即用。"),
    ("Binaryify/open-kimi-ppt-skill", 635, "非官方 Kimi Slides Skill：让 AI Agent 生成可编辑 PPTD + PPTX，并附带本地浏览器编"),
    ("mikiarlo3/awesome-growth-hacking-skills", 430, "Find agentic growth hacking skills for Claude, ChatGPT, Manu"),
    ("criptogus/HermesOffice", 347, "HermesOffice — AI-native office suite forked from GenOffice"),
    ("0xwilliamortiz/claude-red", 330, "claude-red is a curated library of offensive security skills"),
    ("fuxicodex/Fuxi", 305, "FuXi is a fast, self-contained AI developer terminal"),
    ("SandAI-org/MAGI-2-preview", 291, "MAGI-2-preview: Scaling Video Generation Models Efficiently"),
    ("AMAP-ML/LongHorizon-Harness", 278, "The long-horizon computer-use harness. Run AI agents across"),
    ("ZzzLc0405/photo-abstract-editorial", 247, ""),
    ("cristicretu/diri", 204, "Native macOS orchestrator for coding agents — run Claude Cod"),
]

github_weekly = [
    ("yc-software/qm", 11699, "Multiplayer agent harness for work"),
    ("trycompai/crm", 6279, "An open-source, agentic-first CRM."),
    ("firecrawl/anydoc", 5122, "Convert Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CS"),
    ("bashalarmistalt/decimen-optical-transfer", 4697, ""),
    ("xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer", 3391, "FDE（前沿部署工程师）从零入门指南（基于范冰《增长黑客》原书框架）"),
    ("FareedKhan-dev/kimi-k3-in-c", 2580, "A 2.78-trillion-parameter Kimi K3 running inference on a sin"),
    ("imsai-sh/zhuzhiliao", 2037, "竹知了 —— 一转就哇哇叫的传统玩具，Web 模拟版。零依赖单文件，真实录音采样，移动端优先。"),
    ("microsoft/skill-recorder", 1967, "Desktop app that records your on-screen work session and use"),
    ("genspark-ai/genoffice", 1781, "An AI-native office suite for macOS and Windows: word proces"),
    ("thebuggeddev/anatomy", 1614, "An interactive 3D human anatomy explorer built using threejs"),
]

github_monthly = [
    ("xai-org/grok-build", 24225, "SpaceXAI's coding agent harness and TUI. Fullscreen, mouse i"),
    ("Fei-Away/Codex-Dream-Skin", 13265, "Codex Dream Skin"),
    ("andrewyng/openworker", 13126, ""),
    ("yc-software/qm", 11699, "Multiplayer agent harness for work"),
    ("img2threejs/img2threejs", 9900, "Rebuild the object in a reference image as a code-only, proc"),
]

bilibili = [
    ("大家还想看我搬空什么店", "https://www.bilibili.com/video/BV1bz3Q6oEMP"),
    ("《最讨厌复联の一集》", "https://www.bilibili.com/video/BV1KduF6ME4b"),
    ("当我被外星人取代", "https://www.bilibili.com/video/BV1RoMf6mEra"),
    ("完蛋！我被男同学包围了", "https://www.bilibili.com/video/BV1uPMZ6NEBb"),
    ("几十块入手世界级顶尖好物——居家用品篇", "https://www.bilibili.com/video/BV1Vo3C6VE1B"),
    ("当黑客入侵我家摄像头将看到……", "https://www.bilibili.com/video/BV1Lg3R65EZn"),
    ("还来！！！！！！！！！！！", "https://www.bilibili.com/video/BV1xwMQ6GEix"),
    ("你说偷吃零食被发现会死是吗？", "https://www.bilibili.com/video/BV1fGuc6xEmp"),
    ("老大，你的意思是我们抽烟抽的慢也得死吗？", "https://www.bilibili.com/video/BV126GG62E9G"),
    ("【苏新皓｜4K直拍】POWER 直拍｜梦寐以求·演唱会", "https://www.bilibili.com/video/BV1D23262EaD"),
]

def fmt_stars(n):
    if n >= 10000:
        return f"{n/1000:.1f}K"
    return f"{n/1000:.1f}K"

def rank_class(i):
    return ["rank-1","rank-2","rank-3"][i] if i < 3 else ""

def make_douyin(i, w):
    u = f"https://www.douyin.com/search/{urllib.parse.quote(w)}"
    return f'      <li><span class="rank-num {rank_class(i)}">{i+1}</span><a class="rank-title" href="{u}" target="_blank">{w}</a></li>'

def make_gh(i, repo, stars, desc):
    u = f"https://github.com/{repo}"
    d = f'<p style="font-size:11px;color:var(--text-muted);margin-top:2px">{desc}</p>' if desc else ""
    return f'      <li><span class="rank-num {rank_class(i)}">{i+1}</span><div><a class="rank-title" href="{u}" target="_blank">{repo}</a><span class="rank-meta">⭐{fmt_stars(stars)}</span>{d}</div></li>'

def make_bili(i, t, h):
    return f'      <li><span class="rank-num {rank_class(i)}">{i+1}</span><a class="rank-title" href="{h}" target="_blank">{t}</a></li>'

douyin_html = '\n'.join(make_douyin(i, w) for i, w in enumerate(douyin))
daily_html = '\n'.join(make_gh(i, *item) for i, item in enumerate(github_daily))
weekly_html = '\n'.join(make_gh(i, *item) for i, item in enumerate(github_weekly))
monthly_html = '\n'.join(make_gh(i, *item) for i, item in enumerate(github_monthly))
bili_html = '\n'.join(make_bili(i, *item) for i, item in enumerate(bilibili))

medals = ["🥇 ", "🥈 ", "🥉 "]
analysis_html = '\n'.join(
    f'  <div class="analysis-item"><h3>{medals[i] if i<3 else ""}<a href="https://github.com/{r}" target="_blank">{r}</a></h3><div class="meta">⭐{fmt_stars(s)} 本月</div><div class="desc">{d or "热门开源项目"}</div><div class="tags"><span class="tag">GitHub</span><span class="tag">热门项目</span></div></div>'
    for i, (r, s, d) in enumerate(github_monthly)
)

news_items = [
    ("科技", "英国保守党辩护提名前新纳粹成员为候选人"),
    ("科技", "美国服务业PMI微升至54.1显示稳步扩张"),
    ("科技", "民主党候选人埃尔-赛义德险胜密歇根州参议院初选"),
    ("AI", "SpaceX首份财报：营收78亿美元，AI支出激增致亏损"),
    ("AI", "Anthropic组建AI芯片设计团队以优化模型效率"),
    ("科技", "联合国人权高专对伊朗处决人数激增表示关切"),
    ("科技", "阿卜杜勒·埃尔-赛义德赢得密歇根州民主党参议员初选"),
    ("科技", "Ring发布Peephole Cam 2K智能猫眼摄像头"),
    ("科技", "专家呼吁中国立法保护海底光缆免受破坏"),
    ("科技", "SpaceX巨额限售股解禁在即引发市场担忧"),
    ("科技", "投行交易激增推动华尔街奖金预期上涨"),
    ("国际", "美共和党内部对战争部长皮特·赫格塞斯信任度下降"),
    ("科技", "迪士尼证实正探索推出含广告的免费流媒体层级"),
    ("科技", "中国联通：智算规模达45EFLOPS，今年算力投资超175亿元"),
    ("科技", "迪士尼第三财季利润超预期，乐园与流媒体业务双增"),
    ("AI", "CrowdStrike携手AWS推出国际AI安全挑战赛，奖金10万美元"),
]
bm = {"科技":"badge-tech","财经":"badge-biz","国际":"badge-intl","AI":"badge-ai","安全":"badge-sec"}
news_html = '\n'.join(
    f'  <li><span class="news-badge {bm.get(b,"badge-tech")}">{b}</span><a class="news-link" href="https://vicoman.top/tools/ai-news/" target="_blank">{t}</a></li>'
    for b, t in news_items
)

update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M CST")

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
{douyin_html}
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
{bili_html}
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
<p class="update-time">数据来源 GitHub Search API · 每小时更新</p>
<div class="grid">
  <div class="card accent-gh">
    <div class="card-head">📅 今日涨星 TOP10</div>
    <ol class="rank-list">
{daily_html}
    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📆 本周涨星 TOP10</div>
    <ol class="rank-list">
{weekly_html}
    </ol>
  </div>
  <div class="card accent-gh">
    <div class="card-head">📊 本月涨星 TOP5</div>
    <ol class="rank-list">
{monthly_html}
    </ol>
  </div>
</div>
</div>

<!-- AI新闻 -->
<div id="tab-news" class="tab-content">
<p class="update-time">来源 vicoman.top · vicoman 当前404，保留历史快照</p>
<ul class="news-list">
{news_html}
</ul>
</div>

<!-- 解读 -->
<div id="tab-intro" class="tab-content">
<div class="analysis">
{analysis_html}
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
</html>"""

with open("/Users/maqi/idiom-roguelike/index.html", "w") as f:
    f.write(html)

counts = f"DOUYIN:{len(douyin)} BILI:{len(bilibili)} GH_DAILY:{len(github_daily)} GH_WEEKLY:{len(github_weekly)} GH_MONTHLY:{len(github_monthly)} NEWS:{len(news_items)}(404snapshot)"
print(f"OK|{counts}|{len(html)}chars")
