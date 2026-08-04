#!/usr/bin/env python3
"""从 CDP Chrome 提取完整 cookie，调 GitHub API 创建仓库"""
import subprocess, json, urllib.request

CDP = "http://127.0.0.1:3456"

def cdp_eval(expression, target="C34A8F21C23BDA35C10E4C7EA84D03A7"):
    """通过 CDP proxy 执行 JS"""
    r = subprocess.run(['curl', '-s', '--max-time', '10', '-X', 'POST',
        f'{CDP}/eval?target={target}', '-d', expression],
        capture_output=True, text=True)
    return json.loads(r.stdout).get('value', '')

def cdp_cookies():
    """通过 CDP eval 获取完整 cookie（发 fetch 到自己）"""
    # 从浏览器内部发一个请求到 localhost 来获取完整 cookie header
    js = '''
    (async () => {
        var r = await fetch("https://github.com", {credentials: "include"});
        return "ok";
    })();
    '''
    # 直接用 document.cookie + 尝试从 request header 获取
    return cdp_eval('document.cookie')

# 1. 拿 cookie
cookie = cdp_cookies()
print(f"Cookie 长度: {len(cookie)}")
# 显示关键字段
for c in cookie.split('; '):
    if any(k in c.lower() for k in ['user_session', 'logged_in', 'dotcom']):
        print(f"  {c[:80]}")

# 2. 用 cookie 调 API
headers = {
    'Cookie': cookie,
    'Accept': 'application/vnd.github+json',
    'Content-Type': 'application/json',
}
data = json.dumps({'name': 'ghstar-2026', 'private': False, 
                    'description': 'GitHub 涨星排行榜'}).encode()

req = urllib.request.Request('https://api.github.com/user/repos', data=data, headers=headers)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    result = json.loads(resp.read())
    print(f"\n✅ 仓库创建成功: {result.get('html_url', result)}")
except Exception as e:
    print(f"\n❌ 失败: {e}")
